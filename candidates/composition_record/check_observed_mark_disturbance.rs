//! Replay the unedited Zenodo 5146074 QILGST count file named in the note.
//! Std-only. Prints one CSV row per delay, without filtering or fitting.
use std::collections::{BTreeMap, BTreeSet};
use std::{env, fs};

const POINTS: usize = 39;
const SHOTS: u16 = 1024;
const LABELS: [&str; 6] = ["0", "1", "p0:0", "p0:1", "p1:0", "p1:1"];

// First two entries are terminal-only; last four are (mark, terminal).
// The parser verifies which entries were applicable before replacing -- by 0.
type Counts = [u16; 6];

fn parse(text: &str) -> BTreeMap<&str, Vec<Counts>> {
    let mut lines = text.lines();
    let header = lines.next().unwrap().strip_prefix("## Columns = ").unwrap();
    let expected: Vec<String> = (0..POINTS)
        .flat_map(|d| LABELS.map(|label| format!("delay_{:04} {label} count", 500 + 40*d)))
        .collect();
    assert!(header.split(", ").eq(expected.iter().map(String::as_str)), "incorrect header");
    let mut table = BTreeMap::new();
    for line in lines {
        let mut fields = line.split_whitespace();
        let circuit = fields.next().expect("blank circuit");
        let marked = circuit.contains("(Iz)");
        let mut curve = Vec::new();
        for _ in 0..POINTS {
            let mut counts = [0u16; 6];
            for (column, count) in counts.iter_mut().enumerate() {
                let field = fields.next().expect("missing count");
                if (column >= 2) == marked {
                    *count = field.parse().expect("inapplicable or nonintegral count");
                    assert!(*count <= SHOTS);
                } else {
                    assert_eq!(field, "--", "unexpected count in an inapplicable column");
                }
            }
            assert_eq!(counts.iter().sum::<u16>(), SHOTS, "{circuit}: incomplete denominator");
            curve.push(counts);
        }
        assert!(fields.next().is_none(), "extra column");
        assert!(table.insert(circuit, curve).is_none(), "duplicate circuit");
    }
    assert_eq!(table.len(), 128);
    assert_eq!(table.keys().filter(|s| s.contains("(Iz)")).count(), 36);
    table
}

// All comparison-success allocations compatible with the recorded two groups.
// Returns (would-be mark-zero / comparison hits, weighted effect in group zero,
// weighted effect in group one), each expressed as an integer numerator interval.
fn compatible(marked: Counts, control_hits: u16) -> [(i32, i32); 3] {
    let [_, _, n00, n01, n10, n11] = marked.map(i32::from);
    let (w0, w1, u) = (n00 + n01, n10 + n11, i32::from(control_hits));
    let (lo, hi) = ((u - w1).max(0), w0.min(u));
    assert!(lo <= hi);
    [(lo, hi), (n01 - hi, n01 - lo), (n11 - u + lo, n11 - u + hi)]
}

fn main() {
    let path = env::args_os().nth(1).expect("pass the original ...-final.txt path");
    let text = fs::read_to_string(path).expect("read input");
    let table = parse(&text);
    let control = &table["GxGx"];
    let marked = &table["(Iz)GxGx"];
    let controls_by_delay: BTreeSet<Vec<Counts>> = (0..POINTS)
        .map(|i| table.iter().filter(|(name, _)| !name.contains("(Iz)"))
             .map(|(_, curve)| curve[i]).collect())
        .collect();
    assert_eq!(controls_by_delay.len(), POINTS);
    assert_eq!(control.iter().collect::<BTreeSet<_>>().len(), 23);
    assert_eq!(marked[0], [0,0,795,200,18,11]);
    assert_eq!(marked[38], [0,0,35,961,8,20]);
    assert_eq!(control[0], [36,988,0,0,0,0]);
    assert_eq!(control[38], [29,995,0,0,0,0]);
    let no_gates = &table["{}"];
    let marked_no_gates = &table["(Iz)"];
    assert_eq!(marked_no_gates[0], [0,0,966,38,13,7]);
    assert_eq!(marked_no_gates[38], [0,0,969,35,11,9]);
    assert_eq!(no_gates[0], [994,30,0,0,0,0]);
    assert_eq!(no_gates[38], [1002,22,0,0,0,0]);

    println!("delay_ns,mark0_final0,mark0_final1,mark1_final0,mark1_final1,control_final0,control_final1,marked_final1,gated_delta_num,no_gates_marked_final1,no_gates_control_final1,no_gates_delta_num,group0_shots,group0_low_num,group0_high_num,group1_shots,group1_low_num,group1_high_num");
    let mut nonnegative = Vec::new();
    let mut delta = Vec::new();
    for (i, (&m, &c)) in marked.iter().zip(control).enumerate() {
        let delay = 500 + 40*i;
        let hits = m[3] + m[5];
        let difference = i32::from(hits) - i32::from(c[1]);
        delta.push(difference);
        if difference >= 0 { nonnegative.push((delay, difference)); }
        let bare_hits = marked_no_gates[i][3] + marked_no_gates[i][5];
        let bare_control = no_gates[i][1];
        let bare_difference = i32::from(bare_hits) - i32::from(bare_control);
        let [_, (lo0, hi0), (lo1, hi1)] = compatible(m, c[1]);
        println!("{delay},{},{},{},{},{},{},{hits},{difference},{bare_hits},{bare_control},{bare_difference},{},{lo0},{hi0},{},{lo1},{hi1}",m[2],m[3],m[4],m[5],c[0],c[1],m[2]+m[3],m[4]+m[5]);
    }
    assert_eq!(compatible(marked[0], control[0][1]), [(959,988),(-788,-759),(-18,11)]);
    assert_eq!(compatible(marked[38], control[38][1]), [(967,995),(-34,-6),(-8,20)]);
    assert_eq!(compatible(marked_no_gates[0], no_gates[0][1])[1], (8,28));
    assert_eq!(compatible(marked_no_gates[38], no_gates[38][1])[1], (13,33));
    assert_eq!(delta[0] - delta[38], -763);
    assert_eq!(nonnegative, [(1180,0), (1260,1), (1500,7), (1900,3), (1980,8)]);
    eprintln!("Checked all 128 circuits × 39 run columns, 1,024 outcomes per circuit and column. All 39 control vectors are distinct.");
}
