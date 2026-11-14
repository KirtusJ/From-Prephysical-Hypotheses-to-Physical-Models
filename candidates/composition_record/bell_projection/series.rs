//! Data frames share a physical coordinate system and a fixed camera.
//! All frame labels refer to indices in the input, with identical setting names.
use super::{camera, parse, Row};
use std::collections::BTreeMap;
use std::path::Path;

fn timeline(input: &str) -> Result<Vec<Vec<Row>>, String> {
    let mut lines = input.lines();
    if lines.next() != Some("frame\tsetting\t++\t+-\t-+\t--") {
        return Err("expected tab-separated header: frame, setting, ++, +-, -+, --".into());
    }
    let mut groups = BTreeMap::<usize, String>::new();
    for (i, line) in lines.enumerate() {
        let (key, rest) = line
            .split_once('\t')
            .ok_or_else(|| format!("missing frame or setting at line {}", i + 2))?;
        let id: usize = key
            .parse()
            .map_err(|_| format!("invalid frame index at line {}", i + 2))?;
        if id >= 360 || key != id.to_string() {
            return Err("frame must be a decimal integer from 0 to 359".into());
        }
        let table = groups
            .entry(id)
            .or_insert_with(|| "setting\t++\t+-\t-+\t--\n".into());
        table.push_str(rest);
        table.push('\n');
    }
    if groups.is_empty() {
        return Err("at least one data frame is required".into());
    }
    let mut names: Option<Vec<String>> = None;
    let mut result = Vec::new();
    for (expected, (id, data)) in groups.into_iter().enumerate() {
        if expected != id {
            return Err(format!("missing data frame {expected}"));
        }
        let mut rows = parse(&data).map_err(|err| format!("frame {id}: {err}"))?;
        rows.sort_by(|a, b| a.label.cmp(&b.label));
        let labels: Vec<_> = rows.iter().map(|r| r.label.clone()).collect();
        if let Some(first) = &names {
            if *first != labels {
                return Err(format!("frame {id} changes the set of plotted settings"));
            }
        } else {
            names = Some(labels);
        }
        result.push(rows);
    }
    Ok(result)
}

pub(super) fn export(
    input: &str,
    directory: &Path,
    azimuth: f64,
    elevation: f64,
) -> Result<(), String> {
    if !(azimuth.is_finite() && (-90.0..=90.0).contains(&elevation)) {
        return Err("azimuth must be finite and elevation between -90 and 90 degrees".into());
    }
    let frames = timeline(input)?;
    let azimuth = azimuth.rem_euclid(360.);
    super::export_sequence(directory, frames.len(), |i| {
        camera::render_frame(&frames[i], azimuth, elevation, &format!("Data frame {i}"))
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    const RECORDS: &str = include_str!("coherence.tsv");
    #[test]
    fn hidden_which_route_copy_changes_only_the_late_correlation() {
        let frames = timeline(RECORDS).unwrap();
        assert_eq!(frames.len(), 5);
        for (i, rows) in frames.iter().enumerate() {
            for (j, r) in rows.iter().enumerate() {
                let (n, [a, b, c]) = super::super::numerators(r.counts);
                assert_eq!(n, 96);
                assert_eq!((a, b), (-32, -32));
                assert_eq!(c, [96, 64, 64, 44 - 4 * i as i128][j]);
            }
        }
    }
    #[test]
    fn timeline_checks_alignment_before_writing_any_frame() {
        let head = "frame\tsetting\t++\t+-\t-+\t--\n";
        for body in [
            "",
            "1\ta\t1\t0\t0\t0",
            "0\ta\t1\t0\t0\t0\n1\tb\t1\t0\t0\t0",
            "0\ta\t0\t0\t0\t0",
        ] {
            assert!(timeline(&format!("{head}{body}")).is_err());
        }
        let unordered = format!(
            "{head}1\tb\t1\t0\t0\t0\n0\ta\t0\t1\t0\t0\n0\tb\t0\t0\t1\t0\n1\ta\t0\t0\t0\t1\n"
        );
        let t = timeline(&unordered).unwrap();
        assert_eq!(t[0][0].label, "a");
        assert_eq!(t[1][0].counts, [0, 0, 0, 1]);
    }
}
