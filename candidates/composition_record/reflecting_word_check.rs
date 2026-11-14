//! Exact finite reflecting-walk terminal word masses. Run `rustc --edition=2021
//! reflecting_word_check.rs -o reflecting_word_check` and then the executable.
//! Tables are kinematic squared norms with a single denominator 2^(2L).
use std::collections::BTreeMap;

type State = Vec<[i128; 2]>;

fn advance(state: &[[i128; 2]]) -> State {
    let last = state.len() - 1;
    let mut out = vec![[0; 2]; state.len()];
    for (x, &[r, l]) in state.iter().enumerate() {
        // R,L coin numerators (r+l,r-l); the 1/sqrt(2) is in the denominator.
        // An outward proposal stays at the boundary and reverses rail with phase +1.
        if x == last {
            out[x][1] += r + l;
        } else {
            out[x + 1][0] += r + l;
        }
        if x == 0 {
            out[x][0] += r - l;
        } else {
            out[x - 1][1] += r - l;
        }
    }
    out
}

fn cut(mut state: State, high: bool) -> State {
    let n = state.len();
    for (x, a) in state.iter_mut().enumerate() {
        // The physical coordinate is (x+1/2)/L. The boundary belongs to high.
        if (2 * x + 1 >= n) != high {
            *a = [0, 0];
        }
    }
    state
}

fn norm(state: &[[i128; 2]]) -> i128 {
    state.iter().flatten().map(|n| n * n).sum()
}

fn histories(length: usize) -> [i128; 8] {
    assert!((4..=32).contains(&length) && length % 4 == 0);
    let clocks = [length / 2, length, 2 * length];
    let mut seed = vec![[0; 2]; length];
    seed[length / 4][0] = 1;
    let mut branches = vec![seed];
    for tick in 1..=2 * length {
        branches = branches.into_iter().map(|state| advance(&state)).collect();
        if clocks.contains(&tick) {
            branches = branches
                .into_iter()
                .flat_map(|state| [cut(state.clone(), false), cut(state, true)])
                .collect();
            assert_eq!(
                branches.iter().map(|state| norm(state)).sum::<i128>(),
                1_i128 << tick
            );
        }
    }
    std::array::from_fn(|i| norm(&branches[i]))
}

// Check the shortest two rows by independently summing microscopic path signs.
// Only amplitudes at the same full word, well and final rail interfere.
fn enumerate_paths(length: usize) -> [i128; 8] {
    assert!(length == 4 || length == 8);
    let ticks = 2 * length;
    let mut amplitudes = BTreeMap::<(usize, usize, usize), i128>::new();
    for path in 0..(1_usize << ticks) {
        let (mut x, mut rail, mut word, mut sign) = (length / 4, 0, 0, 1_i128);
        for t in 1..=ticks {
            let proposal = (path >> (t - 1)) & 1;
            if rail == 1 && proposal == 1 {
                sign = -sign;
            }
            // Compare a signed displacement with the walls independently of advance().
            let target = x as isize + (1 - 2 * proposal as isize);
            if (0..length as isize).contains(&target) {
                x = target as usize;
                rail = proposal;
            } else {
                rail = 1 - proposal;
            }
            if [length / 2, length, ticks].contains(&t) {
                word = 2 * word + usize::from(x >= length / 2);
            }
        }
        *amplitudes.entry((word, x, rail)).or_default() += sign;
    }
    let mut counts = [0_i128; 8];
    for ((word, _, _), amplitude) in amplitudes {
        counts[word] += amplitude * amplitude;
    }
    counts
}

fn check() {
    println!("word columns: 000 001 010 011 100 101 110 111");
    // Independent reference maxima from Director_G/check_reflected_histories.py.
    for (length, expected_max) in [
        (4, 100_i128),
        (8, 30_936),
        (12, 4_764_931),
        (16, 2_118_536_008),
        (20, 382_551_073_356),
        (24, 132_626_386_599_624),
        (28, 30_368_865_819_833_436),
        (32, 7_607_857_330_084_015_784),
    ] {
        let counts = histories(length);
        if length <= 8 {
            assert_eq!(counts, enumerate_paths(length));
        }
        let denominator = 1_i128 << (2 * length);
        assert_eq!(counts.iter().sum::<i128>(), denominator);
        let maximum = *counts.iter().max().unwrap();
        assert_eq!(maximum, expected_max);
        assert!(2 * maximum < denominator, "a resolved word reaches half at L={length}");
        println!("L={length} denominator={denominator} all_words_below_half={} max={maximum} counts={counts:?}",2*maximum<denominator);
    }
}

fn main() {
    check();
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn finite_cohorts_and_path_oracle() {
        check();
    }
}
