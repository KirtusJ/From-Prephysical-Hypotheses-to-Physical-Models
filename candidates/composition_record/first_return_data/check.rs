//! Reconstruct first returns from the pinned three-spin Sampler job histograms.
use std::env;
use std::fs::{File, OpenOptions};
use std::io::{self, BufRead, BufReader, BufWriter, Write};

const TICKS: usize = 20;
const SHOTS: u32 = 40_000;
type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

struct Job {
    id: String,
    radians: String,
    qasm_angle: String,
    // Index 0 represents no return by the end of the window.
    bins: [u32; TICKS + 1],
}

impl Job {
    fn add(&mut self, word: &str, count: &str) -> Result<()> {
        if word.len() != TICKS || !word.bytes().all(|c| c == b'0' || c == b'1') {
            return Err("expected one 20-bit word".into());
        }
        let value = u32::from_str_radix(word, 2)?;
        let tick = if value == 0 {
            0
        } else {
            value.trailing_zeros() as usize + 1
        };
        let suffix_tick = word.rfind('1').map_or(0, |last| TICKS - last);
        let frequency: u32 = count.parse()?;
        if suffix_tick != tick || frequency == 0 || frequency > SHOTS {
            return Err("invalid word frequency or inconsistent bit order".into());
        }
        self.bins[tick] = self.bins[tick]
            .checked_add(frequency)
            .ok_or("count overflow")?;
        Ok(())
    }

    fn row(&self) -> Result<String> {
        let total = self.bins.iter().map(|&n| u64::from(n)).sum::<u64>();
        if total != u64::from(SHOTS) {
            return Err(format!("{}: observed {total} shots", self.id).into());
        }
        let mut cells = vec![
            self.id.clone(),
            self.radians.clone(),
            self.qasm_angle.clone(),
            total.to_string(),
        ];
        cells.extend(self.bins[1..].iter().map(ToString::to_string));
        cells.push(self.bins[0].to_string());
        for pair in self.bins[1..].windows(2) {
            cells.push((i64::from(pair[1]) - i64::from(pair[0])).to_string());
        }
        Ok(cells.join(","))
    }
}

fn audit(input: impl BufRead) -> Result<Vec<String>> {
    let mut columns = vec![
        "job_id".into(),
        "J_radians".into(),
        "QASM_angle".into(),
        "shots".into(),
    ];
    columns.extend((1..=TICKS).map(|t| format!("hit_{t:02}")));
    columns.push("no_hit_by_20".into());
    columns.extend((1..TICKS).map(|t| format!("hit_{:02}_minus_{t:02}", t + 1)));
    let mut rows = vec![columns.join(",")];
    let mut current: Option<Job> = None;
    for line in input.lines() {
        let line = line?;
        let mut fields = line.split('\t');
        let key = fields.next().ok_or("empty input line")?;
        if key == "job" {
            if let Some(prior) = current.take() {
                rows.push(prior.row()?);
            }
            let id = fields.next().ok_or("missing job ID")?;
            let radians = fields.next().ok_or("missing J")?;
            let angle = fields.next().ok_or("missing QASM angle")?;
            current = Some(Job {
                id: id.into(),
                radians: radians.into(),
                qasm_angle: angle.into(),
                bins: [0; TICKS + 1],
            });
        } else {
            let frequency = fields.next().ok_or("missing frequency")?;
            current
                .as_mut()
                .ok_or("missing job header")?
                .add(key, frequency)?;
        }
        if fields.next().is_some() {
            return Err("extra input field".into());
        }
    }
    rows.push(current.ok_or("no jobs found")?.row()?);
    if rows.len() != 100 {
        return Err("expected 99 job rows".into());
    }
    Ok(rows)
}

fn main() -> Result<()> {
    let args: Vec<_> = env::args_os().collect();
    if args.len() != 3 {
        return Err("usage: check word_counts.tsv new_first_returns.csv".into());
    }
    let rows = audit(BufReader::new(File::open(&args[1])?))?;
    let mut out = BufWriter::new(
        OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(&args[2])?,
    );
    for row in rows {
        writeln!(out, "{row}")?;
    }
    out.flush().map_err(io::Error::into)
}
