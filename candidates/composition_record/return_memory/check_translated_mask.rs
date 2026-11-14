//! Exact signed paths and a whole-mask versus fine-port detector on nine wells.
type Field = [[i32; 2]; 9];

fn propagate(source: usize, ticks: usize) -> Field {
    let mut state = [[0; 2]; 9];
    state[source][0] = 1;
    for _ in 0..ticks {
        let mut next = [[0; 2]; 9];
        for (site, [right, left]) in state.iter().copied().enumerate() {
            next[(site + 1) % 9][0] = right + left;
            next[(site + 8) % 9][1] = right - left;
        }
        state = next;
    }
    state
}

fn enumerate(source: usize, ticks: usize) -> Field {
    let mut result = [[0; 2]; 9];
    for word in 0..(1 << ticks) {
        let (mut site, mut previous, mut sign) = (source, 0, 1);
        for tick in 0..ticks {
            let rail = (word >> tick) & 1;
            if previous == 1 && rail == 1 {
                sign = -sign;
            }
            site = (site + if rail == 0 { 1 } else { 8 }) % 9;
            previous = rail;
        }
        result[site][previous] += sign;
    }
    result
}

fn main() {
    let mut mask_norms = [0; 9];
    for (source, mask_norm) in mask_norms.iter_mut().enumerate() {
        let state = propagate(source, 3);
        assert_eq!(state, enumerate(source, 3));
        let norm: i32 = state.iter().flatten().map(|v| v * v).sum();
        assert_eq!(norm, 8);
        for (site, rails) in state.into_iter().enumerate() {
            for value in rails {
                let square = value * value;
                // Common denominator 840. With q=1/2 the scores have total 6,
                // and with q=2 total 20. Mixture weights are 9/14 and 5/14.
                let mixed_numerator = 90 * value.abs() + 15 * square * square;
                assert_eq!(mixed_numerator, 105 * square);
                if site == 0 || site == 2 {
                    *mask_norm += square;
                }
            }
        }
    }
    let panel = [0, 5, 3, 1].map(|source| mask_norms[source]);
    assert_eq!(panel, [0, 1, 2, 6]);
    println!("Squared norm in wells 0 and 2 by launch site, denominator 8: {mask_norms:?}");
    println!("Four selected launches: {panel:?}. Fine-port mixture matches every port.");

    // At tick five each nonzero squared tally is 1, 4, or 16.
    let mut contrasts = [0; 3];
    for (source, coefficient, expected) in [
        (0, -11, [0, 0, 0]),
        (1, -4, [0, 2, 0]),
        (4, 14, [1, 0, 0]),
        (6, 1, [2, 0, 1]),
    ] {
        let state = propagate(source, 5);
        assert_eq!(state, enumerate(source, 5));
        let mut spectrum = [0; 3];
        let mut target = [0; 3];
        for (site, rails) in state.into_iter().enumerate() {
            for value in rails {
                let class = match value.abs() {
                    0 => continue,
                    1 => 0,
                    2 => 1,
                    4 => 2,
                    _ => panic!("unexpected magnitude"),
                };
                spectrum[class] += 1;
                if site == 0 || site == 2 {
                    target[class] += 1;
                }
            }
        }
        assert_eq!(spectrum, [4, 3, 1]);
        assert_eq!(target, expected);
        for (total, count) in contrasts.iter_mut().zip(target) {
            *total += coefficient * count;
        }
    }
    assert_eq!(contrasts, [16, -8, 1]);
    println!("Five-tick fine-port numerator: 16 - 8u + u^2, u = 4^q.");
}
