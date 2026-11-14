//! Reconstruct joint well counts by adding signed routes at fixed outgoing
//! rails and memory. Run with rustc --edition=2021 -D warnings <this-file>.
use std::collections::BTreeMap;
type Routes = BTreeMap<(i32, i32), [i64; 2]>;
type Cells = BTreeMap<(i32, i32), i64>;

fn routes(clock: usize) -> Routes {
    let mut state = Routes::from([((1, 1), [1, 0]), ((-1, -1), [0, 1])]);
    for _ in 0..clock {
        let mut next = Routes::new();
        for ((site, rail), pair) in state {
            for direction in [-1, 1] {
                let sign = if (rail, direction) == (-1, -1) { -1 } else { 1 };
                let dest = next.entry((site + direction, direction)).or_default();
                for i in 0..2 {
                    dest[i] += sign * pair[i];
                }
            }
        }
        state = next;
    }
    state
}

fn joint(left: usize, right: usize) -> Cells {
    let mut cells = Cells::new();
    let right_paths = routes(right);
    for ((x, _), [a, b]) in routes(left) {
        for (&(y, _), &[c, d]) in &right_paths {
            // Surviving memory vectors on 00,11 can be represented as (1,0)
            // and (-1,1). Trace that memory and sum over both terminal rails.
            *cells.entry((x, y)).or_default() += (a * c - b * d).pow(2) + (b * d).pow(2);
        }
    }
    assert_eq!(cells.values().sum::<i64>(), 3_i64 << (left + right));
    cells
}

fn signs(cells: &Cells) -> [i64; 4] {
    let mut counts = [0; 4];
    for (&(x, y), &n) in cells {
        counts[2 * usize::from(x <= 0) + usize::from(y <= 0)] += n;
    }
    counts
}

fn row(cells: &Cells, x: i32) -> Vec<i64> {
    cells
        .iter()
        .filter(|((site, _), _)| *site == x)
        .map(|(_, n)| *n)
        .collect()
}

fn clock_bins(clock: usize) -> Vec<Vec<i64>> {
    let n = clock + 2;
    (0..1_usize << n)
        .map(|mask| {
            (0..n)
                .map(|i| if mask & (1 << i) == 0 { -1 } else { 1 })
                .collect()
        })
        .collect()
}

fn verify_clock_pairs() {
    // The other setting at each site is the immediate, right-positive read.
    for a in 0..=5 {
        let bins_a = clock_bins(a);
        for b in 0..=5 {
            let bins_b = clock_bins(b);
            let ab = joint(a, b);
            let a0 = joint(a, 0);
            let b0 = joint(0, b);
            let den = 3_i64 << (a + b);
            let index = |x: i32, t: usize| ((x + t as i32 + 1) / 2) as usize;
            let signed = |x: i32| if x > 0 { 1 } else { -1 };
            let mut maximum = 0;
            for mask in &bins_a {
                let ez = a0
                    .iter()
                    .map(|(&(x, y), &n)| mask[index(x, a)] * signed(y) * n)
                    .sum::<i64>()
                    << b;
                // Accumulate Bob's coefficients once for each Alice bin.
                let mut coefficients = vec![0; b + 2];
                for (&(x, y), &n) in &b0 {
                    coefficients[index(y, b)] += (signed(x) * n) << a;
                }
                for (&(x, y), &n) in &ab {
                    coefficients[index(y, b)] -= mask[index(x, a)] * n;
                }
                for other in &bins_b {
                    let s = den
                        + ez
                        + coefficients
                            .iter()
                            .zip(other)
                            .map(|(x, y)| x * y)
                            .sum::<i64>();
                    maximum = maximum.max(s.abs());
                }
            }
            let (p, q) = match (a, b) {
                (3, 3) => (49, 24),
                (3, 4) | (4, 3) => (65, 32),
                (4, 4) => (129, 64),
                _ => (2, 1),
            };
            assert_eq!(maximum * q, den * p, "clock pair ({a},{b})");
        }
    }
    println!("All 36 fixed-clock pairs through five ticks checked with every sign partition.");
}

fn main() {
    verify_clock_pairs();
    let early = joint(0, 0);
    let mixed = joint(3, 0);
    let late = joint(3, 3);
    for (cells, expected) in [
        (&early, [1, 0, 0, 2]),
        (&mixed, [6, 2, 2, 14]),
        (&late, [30, 34, 34, 94]),
    ] {
        assert_eq!(signs(cells), expected);
    }
    assert_eq!(signs(&joint(0, 3)), signs(&mixed));
    let sites = [-4, -2, 0, 2, 4];
    let mixed_rows = [[2, 0], [10, 1], [2, 1], [2, 5], [0, 1]];
    let late_rows = [
        [2, 10, 2, 2, 0],
        [10, 43, 11, 23, 1],
        [2, 11, 3, 7, 1],
        [2, 23, 7, 19, 5],
        [0, 1, 1, 5, 1],
    ];
    for (i, x) in sites.into_iter().enumerate() {
        assert_eq!(row(&mixed, x), mixed_rows[i]);
        assert_eq!(row(&late, x), late_rows[i]);
        assert_eq!(
            8 * mixed_rows[i].iter().sum::<i64>(),
            late_rows[i].iter().sum::<i64>()
        );
    }
    let v = row(&late, 4);
    let w: Vec<_> = v.iter().rev().copied().collect();
    assert_eq!(
        row(&late, 0),
        v.iter().zip(&w).map(|(a, b)| a + 2 * b).collect::<Vec<_>>()
    );
    let sum_pow = |numbers: &[i64], q: u32| numbers.iter().map(|n| n.pow(q)).sum::<i64>();
    let late_odds = (sum_pow(&late_rows[2], 2), sum_pow(&late_rows[4], 2));
    assert_eq!(late_odds, (184, 28));
    let mixed_odds = (sum_pow(&mixed_rows[2], 2), sum_pow(&mixed_rows[4], 2));
    assert_eq!(mixed_odds, (5, 1));
    println!("Raw site rows and all sign cells reproduced; squared site odds 5 and 46/7.");
}
