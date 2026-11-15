//! Exact signed walk, coherent label controls and finite pointer comparisons.
//! rustc --edition=2021 check_light_probes.rs -o check_light_probes
use std::collections::BTreeMap;

type Rails = [i64; 2];
type Flight = BTreeMap<i32, Rails>;
type Source = [[i64; 2]; 4];
type DensitySum = [[i64; 8]; 8];

fn flight(input: Rails, ticks: usize) -> Flight {
    let mut state = BTreeMap::from([(0, input)]);
    for _ in 0..ticks {
        let mut next = Flight::new();
        for (site, [r, l]) in state {
            next.entry(site + 1).or_default()[0] += r + l;
            next.entry(site - 1).or_default()[1] += r - l;
        }
        state = next;
    }
    state
}

fn well_weights(input: &Source) -> [i64; 4] {
    let mut result = [0; 4];
    for &rails in input {
        for (index, [r, l]) in flight(rails, 3).into_values().enumerate() {
            result[index] += r * r + l * l;
        }
    }
    result
}

fn controls(input: Source) -> (DensitySum, [i64; 4]) {
    let original = well_weights(&input);
    let mut sum = [[0; 8]; 8];
    for shift in 0..4 {
        for phase in 0..4usize {
            let mut output = [[0; 2]; 4];
            for (label, rails) in input.iter().enumerate() {
                let sign = if (label & phase).count_ones() % 2 == 0 {
                    1
                } else {
                    -1
                };
                output[label ^ shift] = [sign * rails[0], sign * rails[1]];
            }
            assert_eq!(well_weights(&output), original);
            for i in 0..8 {
                for j in 0..8 {
                    sum[i][j] += output[i / 2][i % 2] * output[j / 2][j % 2];
                }
            }
        }
    }
    (sum, original)
}

fn main() {
    let r = [1, 0];
    let l = [0, 1];
    let (plus, plus_weights) = controls([r, r, r, l]);
    let (minus, minus_weights) = controls([r, l, l, l]);
    let (sharp, sharp_weights) = controls([r; 4]);
    assert_eq!(plus_weights, [4, 8, 16, 4]);
    assert_eq!(minus_weights, [4, 16, 8, 4]);
    assert_eq!(sharp_weights, [4, 4, 20, 4]);
    for i in 0..8 {
        for j in 0..8 {
            assert_eq!(2 * sharp[i][j], 3 * plus[i][j] - minus[i][j]);
        }
    }
    let left = flight(r, 8);
    let right = flight(l, 8);
    assert_eq!(left[&-4], [3, -1]);
    assert_eq!(right[&4], [1, 3]);
    let pure = [[3, -1], [1, 1], [1, 3]];
    for (state, expected) in pure
        .into_iter()
        .zip([[16, 20, 40, 4], [0, 4, 8, 4], [4, 40, 20, 16]])
    {
        assert_eq!(well_weights(&[state, [0, 0], [0, 0], [0, 0]]), expected);
    }
    // All source matrices above are exact. Only the sensitivity scale below
    // uses floating-point evaluation of its closed-form radicals.
    let reference: f64 = 5.0 / 8.0;
    let min_dark =
        |p: f64| (1.0 - (p * reference).sqrt() - ((1.0 - p) * (1.0 - reference)).sqrt()) / 2.0;
    let dark = (min_dark(2.0 / 3.0) + min_dark(7.0 / 12.0)) / 2.0;
    assert!((1.0 - dark).powi(6450) > 0.05 && (1.0 - dark).powi(6451) < 0.05);
    println!(
        "four-well numerators over 32: {plus_weights:?}, {minus_weights:?}, {sharp_weights:?}"
    );
    println!("all 64 entries of 2*sharp = 3*plus - minus verified after 16 label controls");
    println!(
        "eight-tick preparations: {:?}, {:?}, each over 16",
        left[&-4], right[&4]
    );
    println!("fair rival minimum mean dark mass {dark:.12}, zero-hit boundary 6451 trials");
}
