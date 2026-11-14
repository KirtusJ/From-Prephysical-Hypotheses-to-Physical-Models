//! Replay the finite calibration examples using only exact integer arithmetic.
fn choose(n: u32, k: u32) -> i128 {
    if k > n {
        return 0;
    }
    (0..k.min(n - k)).fold(1, |c, i| c * i128::from(n - i) / i128::from(i + 1))
}

// Probabilities p_j=j/4 and mode weights w_j/8. All counts share 8*4^r.
fn count_histogram(r: u32, weights: [i128; 5]) -> Vec<i128> {
    assert_eq!(weights.iter().sum::<i128>(), 8);
    (0..=r)
        .map(|k| {
            choose(r, k)
                * weights
                    .iter()
                    .enumerate()
                    .map(|(j, w)| {
                        let j = j as i128;
                        w * j.pow(k) * (4 - j).pow(r - k)
                    })
                    .sum::<i128>()
        })
        .collect()
}

fn determinant(a: [[i128; 3]; 3]) -> i128 {
    let [[x, y, z], [u, v, w], [b, c, d]] = a;
    x * (v * d - w * c) - y * (u * d - w * b) + z * (u * c - v * b)
}

fn replay() {
    let four_mark_rows = [
        ([0, 4, 0, 4, 0], [41, 60, 54, 60, 41], 0),
        ([1, 0, 6, 0, 1], [44, 48, 72, 48, 44], 3),
    ];
    for (pop, row, mean_square) in four_mark_rows {
        let three = count_histogram(3, pop);
        assert_eq!(three, [7, 9, 9, 7].map(|x| x * 16));
        let four = count_histogram(4, pop);
        assert_eq!(four, row.map(|x| x * 8));
        // Recover s_j from the observed counts with common denominator 8*4^4*12.
        // 12 is divisible by each binomial coefficient (4 choose j).
        let moments: [i128; 5] = std::array::from_fn(|j| {
            let j = j as u32;
            let sum: i128 = four
                .iter()
                .enumerate()
                .map(|(k, weight)| weight * choose(k as u32, j))
                .sum();
            sum * (12 / choose(4, j))
        });
        let coeff = [3, -16, 16];
        let h = std::array::from_fn(|i| std::array::from_fn(|j| moments[i + j]));
        let q_squared: i128 = (0..3)
            .map(|i| (0..3).map(|j| coeff[i] * h[i][j] * coeff[j]).sum::<i128>())
            .sum();
        assert_eq!(q_squared, moments[0] * mean_square);
        assert_eq!(determinant(h) == 0, mean_square == 0);
        println!("marks=4 counts/256={row:?}, E[(16p^2-16p+3)^2]={mean_square}");
    }
    // The parity populations have equal raw mark histograms through the cutoff.
    // Compare r=order-1 directly in the Bernstein basis. Thinning gives all shorter records.
    for order in 1_u32..=12 {
        let r = order - 1;
        for k in 0..=r {
            let delta: i128 = (0..=order)
                .map(|j| {
                    let sign = if j % 2 == 0 { 1 } else { -1 };
                    sign * choose(order, j)
                        * choose(r, k)
                        * i128::from(j).pow(k)
                        * i128::from(order - j).pow(r - k)
                })
                .sum();
            assert_eq!(delta, 0);
        }
    }
    println!("finite-difference control: orders 1 through 12");
}
fn main() {
    replay();
}
#[cfg(test)]
mod tests {
    #[test]
    fn calibrate_using_only_observed_histograms() {
        super::replay();
    }
}
