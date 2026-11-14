//! Bundle a contiguous series of complete SVG camera frames into one offline SVG.
//! Compile with rustc --edition=2021 -O animate.rs -o animate.
//! Usage: animate FRAMES_DIR OUTPUT.svg [milliseconds-per-frame]
use std::env;
use std::fmt::Write as _;
use std::fs;
use std::path::{Path, PathBuf};

fn frame_id(name: &str) -> Option<usize> {
    let digits = name.strip_prefix("frame_")?.strip_suffix(".svg")?;
    if digits.len() != 3 || !digits.bytes().all(|b| b.is_ascii_digit()) {
        return None;
    }
    digits.parse().ok()
}

fn frame_paths(dir: &Path) -> Result<Vec<PathBuf>, String> {
    let mut frames = Vec::new();
    for entry in fs::read_dir(dir).map_err(|e| format!("{}: {e}", dir.display()))? {
        let path = entry.map_err(|e| e.to_string())?.path();
        let name = path.file_name().and_then(|s| s.to_str()).unwrap_or("");
        if name.starts_with("frame_") && name.ends_with(".svg") {
            let id = frame_id(name).ok_or_else(|| format!("invalid frame filename {name}"))?;
            frames.push((id, path));
        }
    }
    frames.sort_by_key(|(id, _)| *id);
    if frames.is_empty() {
        return Err("expected frame_000.svg in the input directory".into());
    }
    for (expected, (id, _)) in frames.iter().enumerate() {
        if *id != expected {
            return Err(format!("missing frame_{expected:03}.svg"));
        }
    }
    Ok(frames.into_iter().map(|(_, p)| p).collect())
}

// The renderer writes an integer width and height and the matching origin-zero
// viewBox. Only the numeric viewport is imported into the outer document.
fn viewport(frame: &str) -> Result<(u32, u32), String> {
    let root = frame
        .trim_start()
        .strip_prefix("<svg ")
        .and_then(|s| s.split_once('>'))
        .map(|(s, _)| s)
        .ok_or("expected the camera renderer's SVG root element")?;
    let attr = |name: &str| {
        let key = format!(" {name}=\"");
        root.split_once(&key)
            .and_then(|(_, tail)| tail.split_once('"'))
            .map(|(v, _)| v)
    };
    let dimension = |name: &str| {
        attr(name)
            .and_then(|s| s.parse::<u32>().ok())
            .filter(|v| *v > 0)
            .ok_or_else(|| format!("expected a positive integer {name}"))
    };
    let (w, h) = (dimension("width")?, dimension("height")?);
    let expected = format!("0 0 {w} {h}");
    if attr("viewBox") != Some(&expected) {
        return Err(format!("expected viewBox=\"{expected}\""));
    }
    Ok((w, h))
}

fn base64(input: &[u8], out: &mut String) {
    const ALPHABET: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    for triple in input.chunks(3) {
        let a = triple[0] as usize;
        let b = triple.get(1).copied().unwrap_or(0) as usize;
        let c = triple.get(2).copied().unwrap_or(0) as usize;
        out.push(ALPHABET[a >> 2] as char);
        out.push(ALPHABET[((a & 3) << 4) | (b >> 4)] as char);
        out.push(if triple.len() > 1 {
            ALPHABET[((b & 15) << 2) | (c >> 6)] as char
        } else {
            '='
        });
        out.push(if triple.len() > 2 {
            ALPHABET[c & 63] as char
        } else {
            '='
        });
    }
}

fn preview(paths: &[PathBuf], ms: u32) -> Result<String, String> {
    let total = paths.len();
    if total == 0 || ms == 0 {
        return Err("at least one frame and a positive milliseconds-per-frame are required".into());
    }
    let duration = total as u64 * u64::from(ms);
    let mut out = String::new();
    let mut size = None;
    for (i, path) in paths.iter().enumerate() {
        let frame = fs::read_to_string(path).map_err(|e| format!("{}: {e}", path.display()))?;
        let (w, h) = viewport(&frame).map_err(|e| format!("{}: {e}", path.display()))?;
        if i == 0 {
            size = Some((w, h));
            writeln!(out, r#"<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc" data-count="{total}" data-ms="{ms}">"#).unwrap();
            out.push_str("<title id=\"title\">Joint-law projection sequence</title>\n");
            writeln!(out, "<desc id=\"desc\">{total} ordered projection frames, {ms} milliseconds each. The numbered frame files can be viewed separately.</desc>").unwrap();
        } else if size != Some((w, h)) {
            return Err(format!("{} has a different viewport", path.display()));
        }
        let initial = if i == 0 { "visible" } else { "hidden" };
        writeln!(out, r#"<g id="frame-{i}" visibility="{initial}">"#).unwrap();
        if total > 1 {
            let start = i as f64 / total as f64;
            let end = (i + 1) as f64 / total as f64;
            let (times, states) = if i == 0 {
                (format!("0;{end:.12};1"), "visible;hidden;hidden")
            } else if i + 1 == total {
                (format!("0;{start:.12};1"), "hidden;visible;visible")
            } else {
                (
                    format!("0;{start:.12};{end:.12};1"),
                    "hidden;visible;hidden;hidden",
                )
            };
            writeln!(out, r#"<animate attributeName="visibility" calcMode="discrete" keyTimes="{times}" values="{states}" dur="{duration}ms" repeatCount="indefinite"/>"#).unwrap();
        }
        write!(
            out,
            r#"<image width="{w}" height="{h}" href="data:image/svg+xml;base64,"#
        )
        .unwrap();
        base64(frame.as_bytes(), &mut out);
        out.push_str("\"/>\n</g>\n");
    }
    out.push_str("</svg>\n");
    Ok(out)
}

fn run(args: &[String]) -> Result<(), String> {
    if !(args.len() == 3 || args.len() == 4) {
        return Err("usage: animate FRAMES_DIR OUTPUT.svg [milliseconds-per-frame]".into());
    }
    let ms = args
        .get(3)
        .map(|s| s.parse::<u32>())
        .transpose()
        .map_err(|_| "milliseconds-per-frame must be a positive integer")?
        .unwrap_or(180);
    let dir = Path::new(&args[1]);
    let output = Path::new(&args[2]);
    if output
        .file_name()
        .and_then(|s| s.to_str())
        .and_then(frame_id)
        .is_some()
    {
        return Err("the output name must be distinct from the numbered source frames".into());
    }
    let data = preview(&frame_paths(dir)?, ms)?;
    fs::write(output, data).map_err(|e| format!("{}: {e}", output.display()))
}

fn main() {
    if let Err(e) = run(&env::args().collect::<Vec<_>>()) {
        eprintln!("{e}");
        std::process::exit(1);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static COUNTER: AtomicUsize = AtomicUsize::new(0);
    struct Temp(PathBuf);
    impl Temp {
        fn new() -> Self {
            let dir = env::temp_dir().join(format!(
                "pcp-svg-test-{}-{}",
                std::process::id(),
                COUNTER.fetch_add(1, Ordering::Relaxed)
            ));
            fs::create_dir(&dir).unwrap();
            Self(dir)
        }
        fn write(&self, i: usize, w: u32, text: &str) {
            fs::write(self.0.join(format!("frame_{i:03}.svg")),
                format!(r#"<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="20" viewBox="0 0 {w} 20">{text}</svg>"#)).unwrap();
        }
    }
    impl Drop for Temp {
        fn drop(&mut self) {
            let _ = fs::remove_dir_all(&self.0);
        }
    }
    #[test]
    fn base64_pads_all_remainders() {
        for (source, expected) in [
            ("", ""),
            ("f", "Zg=="),
            ("fo", "Zm8="),
            ("foo", "Zm9v"),
            ("foob", "Zm9vYg=="),
        ] {
            let mut actual = String::new();
            base64(source.as_bytes(), &mut actual);
            assert_eq!(actual, expected);
        }
    }
    #[test]
    fn sequences_are_ordered_gap_free_and_viewport_checked() {
        let t = Temp::new();
        t.write(2, 40, "");
        t.write(0, 40, "");
        assert!(frame_paths(&t.0).unwrap_err().contains("001"));
        t.write(1, 50, "");
        let paths = frame_paths(&t.0).unwrap();
        assert_eq!(paths[0].file_name().unwrap(), "frame_000.svg");
        assert!(preview(&paths, 100)
            .unwrap_err()
            .contains("different viewport"));
        fs::write(t.0.join("frame_4.svg"), "").unwrap();
        assert!(frame_paths(&t.0).is_err());
    }
    #[test]
    fn frames_stay_in_image_documents_and_last_interval_is_visible() {
        let t = Temp::new();
        for i in 0..4 {
            t.write(i, 40, "<script>source_side_effect()</script>");
        }
        let paths = frame_paths(&t.0).unwrap();
        let svg = preview(&paths, 500).unwrap();
        assert!(!svg.contains("source_side_effect"));
        assert_eq!(svg.matches("data:image/svg+xml;base64,").count(), 4);
        assert_eq!(svg.matches("dur=\"2000ms\"").count(), 4);
        assert!(svg.contains("0;0.750000000000;1\" values=\"hidden;visible;visible\""));
        assert!(!preview(&paths[..1], 20).unwrap().contains("<animate "));
        assert!(preview(&paths, 0).is_err());
    }
}
