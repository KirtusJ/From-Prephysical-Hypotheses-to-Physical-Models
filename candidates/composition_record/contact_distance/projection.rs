//! Build with rustc --edition=2021 projection.rs and run the binary.
//! An optional output filename defaults to position_difference.svg.
use std::fmt::Write as _;
use std::{env, fs, io};

const SITES: [i32; 4] = [-3, -1, 1, 3];
// The exact determinant root t satisfies this cubic; isolating endpoints
// are the certificate's rational numbers with a common denominator.
const DEN: i128 = 1_000_000_000;
const LOWER: i128 = 544_238_217;
const UPPER: i128 = 544_238_219;

fn cubic_numerator(n: i128) -> i128 {
    -448 * DEN.pow(3) + 784 * n * DEN.pow(2) + 140 * n.pow(2) * DEN - 125 * n.pow(3)
}

fn display_distance(divisor: i128) -> String {
    // The entire certified interval rounds to one value at eight places.
    let round = |n| (n * 100_000_000 + DEN * divisor / 2) / (DEN * divisor);
    let lower = round(LOWER);
    assert_eq!(lower, round(UPPER));
    format!("{}.{:08}", lower / 100_000_000, lower % 100_000_000)
}

fn cell_coefficients() -> [[i32; 4]; 4] {
    // These matrices are 4E_i in ascending terminal-site order. The primal
    // changes the state by (t/32) L⊗L, L=2Z−X. Thus each law difference is
    // (t/128) times the product of 2 tr(E_i L) and 2 tr(E_j L).
    let effects = [[0, 0, 1], [1, -1, 2], [2, 1, 1], [1, 0, 0]];
    let traces = effects.map(|[a, b, d]| a - b - d);
    traces.map(|left| traces.map(|right| left * right))
}

fn render() -> String {
    assert!(cubic_numerator(LOWER) < 0 && cubic_numerator(UPPER) > 0);
    let distance = display_distance(64);
    let cell_change = display_distance(128);
    let mut svg = format!(
        r#"<svg xmlns="http://www.w3.org/2000/svg" width="640" height="590" viewBox="0 0 640 590" role="img" aria-labelledby="title desc">
  <title id="title">Closest separable law minus blank-register law</title>
  <desc id="desc">A four-by-four position grid. Equal endpoint corners gain t/128; opposite endpoint corners lose t/128. Twelve other cells are zero. Each marginal is unchanged. Total variation is t/64.</desc>
  <rect width="640" height="590" fill="white"/>
  <g font-family="sans-serif" text-anchor="middle" fill="black">
    <text x="320" y="38" font-size="23">Closest separable law minus blank-register law</text>
    <text x="320" y="67" font-size="16">TV = t/64 ≈ {distance}  ·  Nonzero cell change = ±{cell_change}</text>
"#
    );
    for (row, values) in cell_coefficients().iter().enumerate() {
        let y = 93 + 98 * (3 - row);
        writeln!(
            svg,
            r#"    <text x="100" y="{}" font-size="18">{}</text>"#,
            y + 56,
            SITES[row]
        )
        .unwrap();
        for (column, &value) in values.iter().enumerate() {
            let x = 124 + 98 * column;
            let (color, text_color, label) = match value {
                -1 => ("#7e1640", "white", "−t/128"),
                0 => ("#f5f6f6", "#414c54", "0"),
                1 => ("#16547f", "white", "+t/128"),
                _ => unreachable!("unexpected cell coefficient"),
            };
            writeln!(svg, r##"    <rect x="{x}" y="{y}" width="98" height="98" fill="{color}" stroke="#adb6bb"/>"##).unwrap();
            writeln!(
                svg,
                r#"    <text x="{}" y="{}" font-size="20" fill="{text_color}">{label}</text>"#,
                x + 49,
                y + 56
            )
            .unwrap();
        }
    }
    for (column, site) in SITES.iter().enumerate() {
        writeln!(
            svg,
            r#"    <text x="{}" y="513" font-size="18">{site}</text>"#,
            173 + 98 * column
        )
        .unwrap();
    }
    svg.push_str(
        r#"    <text x="320" y="551" font-size="19">Walker B terminal site</text>
    <text transform="translate(58 289) rotate(-90)" font-size="19">Walker A terminal site</text>
  </g>
</svg>
"#,
    );
    svg
}

fn main() -> io::Result<()> {
    let destination = env::args_os()
        .nth(1)
        .unwrap_or_else(|| "position_difference.svg".into());
    fs::write(destination, render())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn switches_only_the_four_corners() {
        let cells = cell_coefficients();
        let expected = [[1, 0, 0, -1], [0; 4], [0; 4], [-1, 0, 0, 1]];
        assert_eq!(cells, expected);
        for i in 0..4 {
            assert_eq!(cells[i].iter().sum::<i32>(), 0);
            assert_eq!(cells.iter().map(|r| r[i]).sum::<i32>(), 0);
        }
        // Half the absolute sum in units of t/128 is exactly t/64.
        assert_eq!(cells.iter().flatten().map(|x| x.abs()).sum::<i32>(), 4);
    }

    #[test]
    fn labels_match_the_bracket_and_positive_site_is_above_origin() {
        assert_eq!(display_distance(64), "0.00850372");
        assert_eq!(display_distance(128), "0.00425186");
        let svg = render();
        assert!(svg.contains(r#"x="100" y="149" font-size="18">3</text>"#));
        assert!(svg.contains(r#"x="100" y="443" font-size="18">-3</text>"#));
        assert_eq!(svg.matches(">+t/128</text>").count(), 2);
        assert_eq!(svg.matches(">−t/128</text>").count(), 2);
        assert_eq!(svg.matches(">0</text>").count(), 12);
    }
}
