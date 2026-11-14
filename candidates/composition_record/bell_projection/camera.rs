//! Fixed-scale orthographic camera on the cube of signed binary coordinates.
use super::{coordinates, line, text, Row};
use std::collections::BTreeSet;
use std::fmt::Write;

type Vec3 = [f64; 3];
const CENTER: (f64, f64) = (304., 369.);
const SCALE: f64 = 124.;

struct Camera {
    right: Vec3,
    up: Vec3,
}

fn dot(a: Vec3, b: Vec3) -> f64 {
    a.into_iter().zip(b).map(|(x, y)| x * y).sum()
}

impl Camera {
    fn new(azimuth: f64, elevation: f64) -> Self {
        let (sa, ca) = azimuth.rem_euclid(360.).to_radians().sin_cos();
        let (se, ce) = elevation.to_radians().sin_cos();
        Self {
            right: [-sa, ca, 0.],
            up: [-se * ca, -se * sa, ce],
        }
    }

    fn screen(&self, p: Vec3) -> (f64, f64) {
        (
            CENTER.0 + SCALE * dot(self.right, p),
            CENTER.1 - SCALE * dot(self.up, p),
        )
    }
}

fn xml(value: &str) -> String {
    let mut escaped = String::with_capacity(value.len());
    for ch in value.chars() {
        match ch {
            '<' => escaped.push_str("&lt;"),
            '>' => escaped.push_str("&gt;"),
            '&' => escaped.push_str("&amp;"),
            '"' => escaped.push_str("&quot;"),
            '\'' => escaped.push_str("&apos;"),
            '\t' | '\n' | '\r' => escaped.push(ch),
            '\u{fffe}' | '\u{ffff}' => escaped.push('�'),
            c if c < ' ' => escaped.push('�'),
            c => escaped.push(c),
        }
    }
    escaped
}

fn cube_corner(mask: usize) -> Vec3 {
    std::array::from_fn(|axis| if mask & (1 << axis) == 0 { -1. } else { 1. })
}

fn stroke(out: &mut String, a: (f64, f64), b: (f64, f64), color: &str, width: f64) {
    writeln!(out, r#"<line x1="{:.2}" y1="{:.2}" x2="{:.2}" y2="{:.2}" stroke="{color}" stroke-width="{width}"/>"#, a.0,a.1,b.0,b.1).unwrap();
}

fn wireframe(out: &mut String, camera: &Camera) {
    for mask in 0..8 {
        for axis in 0..3 {
            if mask & (1 << axis) == 0 {
                stroke(
                    out,
                    camera.screen(cube_corner(mask)),
                    camera.screen(cube_corner(mask | (1 << axis))),
                    "#d8e1e6",
                    1.,
                );
            }
        }
    }
    let corners = [[1., 1., 1.], [1., -1., -1.], [-1., 1., -1.], [-1., -1., 1.]];
    for (i, &a) in corners.iter().enumerate() {
        for &b in &corners[..i] {
            stroke(out, camera.screen(a), camera.screen(b), "#829aa6", 1.6);
        }
    }
    let mut label_positions: Vec<(f64, f64)> = Vec::new();
    for (axis, (name, color)) in [("+A", "#8f4724"), ("+B", "#1b6878"), ("+AB", "#704a83")]
        .into_iter()
        .enumerate()
    {
        let mut positive = [0.; 3];
        positive[axis] = 1.;
        let end = camera.screen(positive);
        stroke(out, camera.screen(positive.map(|v| -v)), end, color, 1.25);
        // A white halo keeps labels legible over the wires at cardinal views.
        let x = end.0 + 5.;
        let mut y = end.1 - 5.;
        while label_positions
            .iter()
            .any(|&(px, py)| (x - px).abs() < 26. && (y - py).abs() < 13.)
        {
            y += 14.;
        }
        label_positions.push((x, y));
        let width = if name == "+AB" { 26. } else { 19. };
        writeln!(
            out,
            r#"<rect x="{:.2}" y="{:.2}" width="{width}" height="14" fill="white"/>"#,
            x - 1.,
            y - 11.
        )
        .unwrap();
        writeln!(out, r#"<text x="{x:.2}" y="{y:.2}" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="{color}">{name}</text>"#).unwrap();
    }
}

/// Azimuth turns from +A toward +B. Elevation rises toward +AB.
/// The caller supplies finite degrees and an elevation between -90 and 90.
pub(super) fn render_frame(
    rows: &[Row],
    azimuth_degrees: f64,
    elevation_degrees: f64,
    frame_label: &str,
) -> String {
    let camera = Camera::new(azimuth_degrees, elevation_degrees);
    let mut out = String::from(
        r#"<svg xmlns="http://www.w3.org/2000/svg" width="1060" height="820" viewBox="0 0 1060 820" role="img">
<title>Orthographic projection of binary joint laws</title>
<desc>Count-normalized rows shown in a fixed-size probability tetrahedron. Each setting is retained in the exact table. Several settings can project to one marker.</desc>
<rect width="1060" height="820" fill="white"/>"#,
    );
    text(&mut out, 30., 45., "title", "Binary joint laws");
    text(&mut out, 30., 75., "sub", &xml(frame_label));
    text(&mut out, 30., 111., "ptitle", "Orthographic projection");
    text(
        &mut out,
        30.,
        134.,
        "caption",
        &format!(
            "Azimuth {:.2}°     Elevation {:.2}°",
            azimuth_degrees.rem_euclid(360.),
            elevation_degrees
        ),
    );
    out.push_str(r##"<rect x="30" y="150" width="525" height="460" rx="2" fill="#fbfcfd" stroke="#c7d4db"/>"##);
    wireframe(&mut out, &camera);
    let mut markers = BTreeSet::new();
    for (i, row) in rows.iter().enumerate() {
        let uv = camera.screen(coordinates(row.counts).map(|v| v.value()));
        let y = 181. + 26. * i as f64;
        let label_width = 6.7 * row.label.len() as f64;
        line(&mut out, uv, (44. + label_width, y - 3.), "leader");
        writeln!(out,r##"<text x="41" y="{y:.2}" textLength="{label_width:.2}" lengthAdjust="spacingAndGlyphs" font-family="monospace" font-size="11" fill="#465968">{}</text>"##, row.label).unwrap();
        // Group only at the actual SVG output precision. Exact table rows always survive.
        markers.insert((format!("{:.2}", uv.0), format!("{:.2}", uv.1)));
    }
    for (x, y) in markers {
        writeln!(
            out,
            r##"<circle cx="{x}" cy="{y}" r="4" fill="#006b68" stroke="white" stroke-width="1"/>"##
        )
        .unwrap();
    }
    text(&mut out, 30., 644., "ptitle", "Reading the frame");
    text(
        &mut out,
        30.,
        671.,
        "caption",
        "The pale cube covers −1 to +1 on each axis. The darker tetrahedron",
    );
    text(
        &mut out,
        30.,
        691.,
        "caption",
        "connects the four deterministic outcomes. Its interior and faces",
    );
    text(
        &mut out,
        30.,
        711.,
        "caption",
        "contain every binary joint law for a single pair of settings.",
    );
    text(
        &mut out,
        30.,
        744.,
        "caption",
        "A and B are signed marginal means. AB is their correlation.",
    );
    text(
        &mut out,
        30.,
        765.,
        "caption",
        "A leader reaches the true marker for each setting.",
    );
    text(
        &mut out,
        583.,
        111.,
        "ptitle",
        "Original counts and exact signed means",
    );
    text(
        &mut out,
        583.,
        134.,
        "caption",
        "Outcome order  ++, +−, −+, −−",
    );
    for (i, row) in rows.iter().enumerate() {
        let y = 179. + 39. * i as f64;
        line(&mut out, (583., y - 17.), (1028., y - 17.), "grid");
        text(&mut out, 583., y, "vertex", &row.label);
        let [pp, pm, mp, mm] = row.counts;
        text(&mut out, 687., y, "num", &format!("{pp}, {pm}, {mp}, {mm}"));
        let [a, b, c] = coordinates(row.counts);
        for (j, (axis, value)) in [("A", a), ("B", b), ("AB", c)].into_iter().enumerate() {
            let label = format!("{axis}  {value}");
            let class = if label.len() > 19 {
                "smallmean"
            } else {
                "vertex"
            };
            text(&mut out, 637. + 135. * j as f64, y + 15., class, &label);
        }
    }
    out.push_str("</svg>\n");
    out
}

#[cfg(test)]
mod tests {
    use super::*;
    fn near(a: (f64, f64), b: (f64, f64)) {
        assert!(
            (a.0 - b.0).abs() < 1e-9 && (a.1 - b.1).abs() < 1e-9,
            "{a:?} != {b:?}"
        );
    }
    #[test]
    fn cardinal_views_expose_orientation_and_preserve_magnification() {
        let p = [1., -1., -1.];
        near(
            Camera::new(0., 0.).screen(p),
            (CENTER.0 - SCALE, CENTER.1 + SCALE),
        );
        near(
            Camera::new(90., 0.).screen(p),
            (CENTER.0 - SCALE, CENTER.1 + SCALE),
        );
        near(
            Camera::new(180., 0.).screen(p),
            (CENTER.0 + SCALE, CENTER.1 + SCALE),
        );
        near(
            Camera::new(270., 0.).screen(p),
            (CENTER.0 + SCALE, CENTER.1 + SCALE),
        );
        near(
            Camera::new(0., 90.).screen(p),
            (CENTER.0 - SCALE, CENTER.1 + SCALE),
        );
        // Every cube vertex has norm sqrt(3), hence any camera axis has projection
        // at most sqrt(3). This checks the continuous range, including oblique extrema.
        let extent = SCALE * 3.0_f64.sqrt();
        assert!(CENTER.0 - extent >= 30. && CENTER.0 + extent <= 555.);
        assert!(CENTER.1 - extent >= 150. && CENTER.1 + extent <= 610.);
        for az in [0., 24., 90., 180., 359.] {
            for el in [-90., -20., 0., 25., 90.] {
                let cam = Camera::new(az, el);
                assert!((dot(cam.right, cam.up)).abs() < 1e-12);
                assert!((dot(cam.right, cam.right) - 1.).abs() < 1e-12);
                assert!((dot(cam.up, cam.up) - 1.).abs() < 1e-12);
                for i in 0..8 {
                    let (x, y) = cam.screen(cube_corner(i));
                    assert!((30. ..555.).contains(&x) && (150. ..610.).contains(&y));
                }
            }
        }
    }
    #[test]
    fn saved_frame_keeps_exact_inputs_escapes_labels_and_replays() {
        let rows = super::super::parse(include_str!("bell.tsv")).unwrap();
        let a = render_frame(&rows, 45., 25., "Example <&> \"test\"");
        assert!(a.contains("Example &lt;&amp;&gt; &quot;test&quot;"));
        assert!(a.contains("32, 0, 0, 64"));
        for cell in ["A  -1/3", "B  -1/3", "AB  7/24"] {
            assert!(a.contains(cell));
        }
        assert_eq!(a.matches("<circle ").count(), 3);
        let top = render_frame(&rows, 45., 90., "top view");
        assert_eq!(top.matches("<circle ").count(), 1);
        assert_ne!(a, top);
        assert_eq!(a, render_frame(&rows, 45., 25., "Example <&> \"test\""));
    }
}
