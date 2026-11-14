//! Orthographic views of binary joint distributions. Run tests with rustc --test.
mod camera;
mod frame_export;
mod series;
use frame_export::export_sequence;
use std::collections::{BTreeMap, BTreeSet};
use std::fmt::{self, Write};
use std::{env, fs, process};

type Counts = [i128; 4];
type Coordinates = [Fraction; 3];

#[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd)]
struct Fraction(i128, i128);

impl Fraction {
    fn new(n: i128, d: i128) -> Self {
        assert!(d > 0);
        let (mut a, mut b) = (n.abs(), d);
        while b != 0 {
            (a, b) = (b, a % b);
        }
        Self(n / a, d / a)
    }
    fn value(self) -> f64 {
        self.0 as f64 / self.1 as f64
    }
}

impl fmt::Display for Fraction {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if self.1 == 1 {
            write!(f, "{}", self.0)
        } else {
            write!(f, "{}/{}", self.0, self.1)
        }
    }
}

struct Row {
    label: String,
    counts: Counts,
}

fn parse(input: &str) -> Result<Vec<Row>, String> {
    let mut lines = input.lines();
    if lines.next() != Some("setting\t++\t+-\t-+\t--") {
        return Err("expected header: setting, ++, +-, -+, -- (tab-delimited)".into());
    }
    let mut rows = Vec::new();
    let mut labels = BTreeSet::new();
    for (i, line) in lines.enumerate() {
        let fields: Vec<_> = line.split('\t').collect();
        if fields.len() != 5 {
            return Err(format!("row {} needs five fields", i + 2));
        }
        let label = fields[0];
        if label.is_empty()
            || label.len() > 12
            || !label
                .bytes()
                .all(|c| c.is_ascii_alphanumeric() || b"-_.".contains(&c))
        {
            return Err(format!("invalid setting label on row {}", i + 2));
        }
        if !labels.insert(label) {
            return Err(format!("duplicate setting {label}"));
        }
        let mut counts = [0; 4];
        for (n, field) in counts.iter_mut().zip(&fields[1..]) {
            if field.is_empty() || !field.bytes().all(|c| c.is_ascii_digit()) {
                return Err(format!("invalid count for {label}"));
            }
            *n = field
                .parse::<i128>()
                .map_err(|_| format!("invalid count for {label}"))?;
            if *n > 1_000_000_000 {
                return Err(format!("count over 1000000000 for {label}"));
            }
        }
        if counts == [0; 4] {
            return Err(format!("zero total for {label}"));
        }
        rows.push(Row {
            label: label.into(),
            counts,
        });
        if rows.len() > 16 {
            return Err("at most 16 settings per figure".into());
        }
    }
    if rows.is_empty() {
        return Err("at least one setting is required".into());
    }
    Ok(rows)
}

fn numerators([pp, pm, mp, mm]: Counts) -> (i128, [i128; 3]) {
    (
        pp + pm + mp + mm,
        [pp + pm - mp - mm, pp - pm + mp - mm, pp - pm - mp + mm],
    )
}

fn coordinates(counts: Counts) -> Coordinates {
    let (n, values) = numerators(counts);
    values.map(|v| Fraction::new(v, n))
}

#[derive(Clone, Copy)]
enum View {
    Marginal,
    Correlation,
    Oblique,
}

impl View {
    fn projection(self, counts: Counts) -> [Fraction; 2] {
        let (n, [a, b, c]) = numerators(counts);
        let pair = match self {
            Self::Marginal => [a, b],
            Self::Correlation => [a, c],
            Self::Oblique => [b - a, 2 * c - a - b],
        };
        pair.map(|v| Fraction::new(v, n))
    }
    fn screen(self, x: f64, y: f64, q: [Fraction; 2]) -> (f64, f64) {
        let [u, v] = q.map(Fraction::value);
        match self {
            Self::Oblique => (x + 49. * u / 2.0f64.sqrt(), y - 49. * v / 6.0f64.sqrt()),
            _ => (x + 72. * u, y - 72. * v),
        }
    }
}

fn text(out: &mut String, x: f64, y: f64, class: &str, value: &str) {
    // All user-visible variable strings are decimal numbers or allow-listed labels.
    let (size, weight, color) = match class {
        "title" => (27, "bold", "#172b3c"),
        "mode" => (18, "bold", "#172b3c"),
        "ptitle" => (15, "bold", "#172b3c"),
        "fraction" => (7, "normal", "#344a57"),
        "smallmean" => (8, "normal", "#344a57"),
        "vertex" => (11, "normal", "#465968"),
        _ => (13, "normal", "#344a57"),
    };
    writeln!(
        out,
        r##"<text x="{x:.2}" y="{y:.2}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{value}</text>"##
    )
    .unwrap();
}

fn line(out: &mut String, from: (f64, f64), to: (f64, f64), class: &str) {
    let (color, width) = match class {
        "grid" => ("#cfdae1", 1.0),
        "wire" => ("#91a5b1", 1.2),
        _ => ("#a7b4bc", 0.8),
    };
    writeln!(
        out,
        r##"<line x1="{:.2}" y1="{:.2}" x2="{:.2}" y2="{:.2}" stroke="{color}" stroke-width="{width}"/>"##,
        from.0, from.1, to.0, to.1
    )
    .unwrap();
}

fn panel(out: &mut String, x: f64, y: f64, view: View, rows: &[Row], powered: bool) {
    let center = (x + 95., y + 119.);
    let (title, subtitle) = match view {
        View::Marginal => ("Marginals", "Horizontal A  /  vertical B"),
        View::Correlation => ("Marginal and correlation", "Horizontal A  /  vertical AB"),
        View::Oblique => ("Joint-law tetrahedron", "Camera direction (1, 1, 1)"),
    };
    text(out, x, y, "ptitle", title);
    text(out, x, y + 20., "caption", subtitle);
    if matches!(view, View::Oblique) {
        let v: Vec<_> = (0..4)
            .map(|i| {
                let mut c = [0; 4];
                c[i] = 1;
                view.screen(center.0, center.1, view.projection(c))
            })
            .collect();
        for i in 0..4 {
            for j in 0..i {
                line(out, v[i], v[j], "wire");
            }
            let dx = if i == 1 { -22. } else { 4. };
            text(
                out,
                v[i].0 + dx,
                v[i].1 - 4.,
                "vertex",
                ["++", "+-", "-+", "--"][i],
            );
        }
    } else {
        for t in [-72., 0., 72.] {
            line(
                out,
                (center.0 + t, center.1 - 72.),
                (center.0 + t, center.1 + 72.),
                "grid",
            );
            line(
                out,
                (center.0 - 72., center.1 + t),
                (center.0 + 72., center.1 + t),
                "grid",
            );
        }
        text(out, center.0 - 78., center.1 + 88., "vertex", "−1");
        text(out, center.0 - 3., center.1 + 88., "vertex", "0");
        text(out, center.0 + 65., center.1 + 88., "vertex", "+1");
        text(out, center.0 - 95., center.1 - 67., "vertex", "+1");
        text(out, center.0 - 95., center.1 + 75., "vertex", "−1");
    }
    let mut groups = BTreeMap::<[Fraction; 2], Vec<&str>>::new();
    for row in rows {
        let counts = if powered {
            row.counts.map(|n| n * n)
        } else {
            row.counts
        };
        groups
            .entry(view.projection(counts))
            .or_default()
            .push(&row.label);
    }
    let mut points: Vec<_> = groups
        .into_iter()
        .map(|(q, labels)| (view.screen(center.0, center.1, q), labels))
        .collect();
    points.sort_by(|a, b| a.0 .1.total_cmp(&b.0 .1).then(a.0 .0.total_cmp(&b.0 .0)));
    let mut label_y = y + 52.;
    // Keep true projected centers, including near-coincident points. Only label baselines move.
    let mut marks = String::new();
    for (point, labels) in points {
        let anchor = (x + 201., label_y - 4.);
        line(out, point, anchor, "leader");
        let c = if powered { "#ab521f" } else { "#006b68" };
        writeln!(
            marks,
            r##"<circle cx="{:.2}" cy="{:.2}" r="3" fill="{c}" stroke="white" stroke-width="0.7"/>"##,
            point.0, point.1
        )
        .unwrap();
        // Wrapping preserves every input label even when all 16 projections coincide.
        let mut active = String::new();
        for label in labels {
            if !active.is_empty() && active.len() + label.len() + 2 > 17 {
                text(out, x + 206., label_y, "marklabel", &active);
                active.clear();
                label_y += 16.;
            }
            if !active.is_empty() {
                active.push_str(", ");
            }
            active.push_str(label);
        }
        text(out, x + 206., label_y, "marklabel", &active);
        label_y += 21.;
    }
    out.push_str(&marks);
}

fn figure(rows: &[Row]) -> String {
    let mode_height = (rows.len() as i32 * 21 + 106).max(265);
    let table_y = 130 + 2 * mode_height;
    let height = table_y + 110 + 42 * rows.len() as i32;
    let mut out = format!(
        r#"<svg xmlns="http://www.w3.org/2000/svg" width="1060" height="{height}" viewBox="0 0 1060 {height}" role="img" aria-labelledby="title desc">
<title id="title">Orthographic views of binary joint distributions</title>
<desc id="desc">Each law is represented by its two signed marginal means and its correlation. The first row uses the input counts. The second squares each cell and renormalizes within each setting. The table gives the underlying counts and exact coordinates.</desc>
<rect width="100%" height="100%" fill="white"/>"#
    );
    text(
        &mut out,
        32.,
        42.,
        "title",
        "Binary joint laws in three coordinates",
    );
    text(&mut out,32.,67.,"sub","A and B are signed outcomes. AB is their product. Leader lines identify settings at their exact projected centers.");
    for mode in 0..2 {
        let y = (107 + mode * mode_height) as f64;
        text(
            &mut out,
            32.,
            y,
            "mode",
            if mode == 0 {
                "Count-normalized laws"
            } else {
                "Hypothetical squaring of the binned counts"
            },
        );
        for (i, view) in [View::Marginal, View::Correlation, View::Oblique]
            .into_iter()
            .enumerate()
        {
            panel(
                &mut out,
                32. + 344. * i as f64,
                y + 35.,
                view,
                rows,
                mode == 1,
            );
        }
    }
    let top = table_y as f64;
    text(
        &mut out,
        32.,
        top,
        "mode",
        "Input counts and exact signed means",
    );
    text(&mut out,32.,top+24.,"caption","Each row has its own denominator. In the control each squared count is divided by the sum of the four squares.");
    let xs = [
        32., 135., 220., 305., 390., 475., 566., 657., 748., 850., 952.,
    ];
    for (x, title) in xs.into_iter().zip([
        "Setting",
        "++",
        "+-",
        "-+",
        "--",
        "A",
        "B",
        "AB",
        "Squared A",
        "Squared B",
        "Squared AB",
    ]) {
        text(&mut out, x, top + 53., "ptitle", title);
    }
    for (idx, row) in rows.iter().enumerate() {
        let y = top + 78. + 42. * idx as f64;
        line(&mut out, (32., y - 17.), (1028., y - 17.), "grid");
        text(&mut out, xs[0], y, "num", &row.label);
        for (j, count) in row.counts.iter().enumerate() {
            text(&mut out, xs[j + 1], y, "num", &count.to_string());
        }
        for (j, v) in coordinates(row.counts)
            .into_iter()
            .chain(coordinates(row.counts.map(|n| n * n)))
            .enumerate()
        {
            let frac = v.to_string();
            if frac.len() > 10 && v.1 != 1 {
                text(&mut out, xs[5 + j], y, "fraction", &v.0.to_string());
                text(
                    &mut out,
                    xs[5 + j],
                    y + 15.,
                    "fraction",
                    &format!("/{}", v.1),
                );
            } else {
                text(&mut out, xs[5 + j], y, "num", &frac);
            }
        }
    }
    out.push_str("</svg>\n");
    out
}

fn angles(values: &[std::ffi::OsString]) -> Result<(f64, f64), String> {
    let [az, el] = values else {
        return Err("supply both azimuth and elevation in degrees".into());
    };
    let read = |v: &std::ffi::OsString| {
        v.to_str()
            .and_then(|s| s.parse::<f64>().ok())
            .filter(|d| d.is_finite())
            .ok_or("angles must be finite decimal degrees")
    };
    let (az, el) = (read(az)?, read(el)?);
    if !(-90. ..=90.).contains(&el) {
        return Err("elevation must lie between -90 and 90 degrees".into());
    }
    Ok((az, el))
}

fn run() -> Result<(), String> {
    let args: Vec<_> = env::args_os().skip(1).collect();
    let usage = "usage: project INPUT.tsv OUTPUT.svg | INPUT.tsv --view OUTPUT.svg AZ EL | INPUT.tsv --frames NEW_DIR N | INPUT.tsv --series NEW_DIR [AZ EL]";
    let [input, mode, rest @ ..] = args.as_slice() else {
        return Err(usage.into());
    };
    let raw = fs::read_to_string(input).map_err(|e| e.to_string())?;
    match (mode.to_str(), rest) {
        (Some("--series"), [directory, degrees @ ..]) => {
            let (az, el) = if degrees.is_empty() {
                (45., 25.)
            } else {
                angles(degrees)?
            };
            series::export(&raw, directory.as_ref(), az, el)
        }
        (Some("--frames"), [directory, count]) => {
            let rows = parse(&raw)?;
            let count = count
                .to_str()
                .and_then(|s| s.parse::<usize>().ok())
                .filter(|n| (4..=360).contains(n))
                .ok_or("rotation needs 4 through 360 frames")?;
            export_sequence(directory.as_ref(), count, |i| {
                camera::render_frame(
                    &rows,
                    360. * i as f64 / count as f64,
                    25.,
                    &format!("Camera frame {i} of {count}  ·  input counts held fixed"),
                )
            })
        }
        (Some("--view"), [output, degrees @ ..]) => {
            let (az, el) = angles(degrees)?;
            let svg = camera::render_frame(&parse(&raw)?, az, el, "Single camera view");
            fs::write(output, svg).map_err(|e| e.to_string())
        }
        (Some("--series" | "--frames" | "--view"), _) => Err(usage.into()),
        (_, []) => fs::write(mode, figure(&parse(&raw)?)).map_err(|e| e.to_string()),
        _ => Err(usage.into()),
    }
}

fn main() {
    if let Err(reason) = run() {
        eprintln!("{reason}");
        process::exit(2);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn inverse_exactly_recovers_every_small_count_table() {
        for code in 1..5i32.pow(4) {
            let counts = std::array::from_fn(|i| i128::from(code / 5i32.pow(i as u32) % 5));
            let (n, [a, b, c]) = numerators(counts);
            assert_eq!(
                [n + a + b + c, n + a - b - c, n - a + b - c, n - a - b + c],
                counts.map(|k| 4 * k)
            );
        }
    }
    #[test]
    fn loss_and_control_are_visible_on_fixture() {
        let rows = parse(include_str!("bell.tsv")).unwrap();
        let counts: Vec<_> = rows.iter().map(|r| r.counts).collect();
        assert_eq!(
            View::Marginal.projection(counts[0]),
            View::Marginal.projection(counts[3])
        );
        assert_ne!(
            View::Correlation.projection(counts[0]),
            View::Correlation.projection(counts[3])
        );
        assert_eq!(coordinates(counts[1]), coordinates(counts[2]));
        let p: Vec<_> = counts.iter().map(|row| row.map(|n| n * n)).collect();
        assert_ne!(coordinates(p[0]), coordinates(p[1]));
        assert_eq!(
            View::Oblique.projection(p[0]),
            View::Oblique.projection(p[1])
        );
        let marginal = |s: Counts| Fraction::new(s[0] + s[1], s.iter().sum());
        assert_eq!(marginal(p[0]), Fraction(1, 5));
        assert_eq!(marginal(p[1]), Fraction(1, 6));
        assert_eq!(coordinates(p[0])[0], Fraction(-3, 5));
        assert_eq!(coordinates(p[1])[0], Fraction(-2, 3));
        for row in [0, 1, 2, 3] {
            assert_eq!(coordinates(p[row])[0], coordinates(p[row])[1]);
        }
    }
    #[test]
    fn validates_input_and_handles_large_coincidences() {
        let h = "setting\t++\t+-\t-+\t--\n";
        for bad in [
            "x\t0\t0\t0\t0",
            "x\t1\t2\t3",
            "x\t-1\t0\t0\t1",
            "x\t1000000001\t0\t0\t1",
            "<x>\t1\t1\t1\t1",
            "a\t1\t0\t0\t0\na\t1\t0\t0\t0",
        ] {
            assert!(parse(&format!("{h}{bad}")).is_err());
        }
        let raw = (0..16).fold(h.to_string(), |mut s, i| {
            writeln!(s, "point_{i:06}\t1000000000\t0\t0\t0").unwrap();
            s
        });
        let plot = figure(&parse(&raw).unwrap());
        assert_eq!(plot.matches("<circle ").count(), 6);
        assert_eq!(plot.matches("point_000015").count(), 7);
        let full = figure(&parse(include_str!("bell.tsv")).unwrap());
        assert!(full.contains("00, 01, 10, 11"));
        assert_eq!(full, figure(&parse(include_str!("bell.tsv")).unwrap()));
    }
}
