//! Write a new frame sequence without replacing any previous run.
use std::fs::{self, OpenOptions};
use std::io::Write;
use std::path::Path;

pub(super) fn export_sequence(
    directory: &Path,
    count: usize,
    mut render: impl FnMut(usize) -> String,
) -> Result<(), String> {
    if !(1..=360).contains(&count) {
        return Err("expected 1 to 360 frames".into());
    }
    fs::create_dir(directory)
        .map_err(|e| format!("create new directory {}: {e}", directory.display()))?;
    let mut created = Vec::new();
    for i in 0..count {
        let path = directory.join(format!("frame_{i:03}.svg"));
        let output = render(i);
        let result = OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&path)
            .and_then(|mut file| {
                created.push(path.clone());
                file.write_all(output.as_bytes())
            });
        if let Err(e) = result {
            // Remove only paths this run created. Other files prevent remove_dir.
            for file in created {
                let _ = fs::remove_file(file);
            }
            let _ = fs::remove_dir(directory);
            return Err(format!("write {}: {e}", path.display()));
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn a_second_run_preserves_existing_frames() {
        let suffix = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        let d = std::env::temp_dir().join(format!("bell-frames-{}-{suffix}", std::process::id()));
        export_sequence(&d, 2, |i| format!("first-{i}")).unwrap();
        assert!(export_sequence(&d, 2, |i| format!("second-{i}")).is_err());
        assert_eq!(
            fs::read_to_string(d.join("frame_001.svg")).unwrap(),
            "first-1"
        );
        for name in ["frame_000.svg", "frame_001.svg"] {
            fs::remove_file(d.join(name)).unwrap();
        }
        fs::remove_dir(d).unwrap();
    }
}
