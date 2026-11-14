//! Exact polynomial and trial-score checks for the real-probe calibration note.
//! Run with rustc --edition=2021 check_real_probe.rs and execute the result.
const E4: [[[i64; 2]; 2]; 4] = [
    [[0, 0], [0, 1]],
    [[1, -1], [-1, 2]],
    [[2, 1], [1, 1]],
    [[1, 0], [0, 0]],
];
const COUNTS: [[i64; 4]; 4] = [[1, 3, 3, 1], [3, 7, 5, 1], [3, 5, 19, 5], [1, 1, 5, 1]];
const SCORE: [[i64; 4]; 4] = [
    [37, -19, 13, -43],
    [-43, 13, 13, 69],
    [21, -3, -3, -27],
    [-59, 29, -3, 85],
];

fn det(matrix: &[Vec<i64>]) -> i64 {
    if matrix.is_empty() {
        return 1;
    }
    matrix[0]
        .iter()
        .enumerate()
        .map(|(j, &a)| {
            let minor: Vec<_> = matrix[1..]
                .iter()
                .map(|row| {
                    row.iter()
                        .enumerate()
                        .filter(|(col, _)| *col != j)
                        .map(|(_, &v)| v)
                        .collect()
                })
                .collect();
            let sign = if j % 2 == 0 { 1 } else { -1 };
            sign * a * det(&minor)
        })
        .sum()
}

fn verify_rival() {
    // Both expressions have degree at most four in each independent variable.
    // Five-by-five integer interpolation certifies the polynomial identity.
    for a in 0..5 {
        for b in 0..5 {
            let m = [
                vec![2, 2 * b, 2 * a, a * b],
                vec![2 * b, 2, a * b, 0],
                vec![2 * a, a * b, 2, 0],
                vec![a * b, 0, 0, 2],
            ];
            let (x, y) = (a * a, b * b);
            assert_eq!(det(&m), (4 - x * y).pow(2) - 16 * (x + y - x * y));
            // Effective detector in the rotated frame: amplify the off-diagonal
            // by 1/a (or 1/b); the corresponding factor in M cancels exactly.
            if a != 0 && b != 0 {
                for i in 0..4 {
                    for j in 0..4 {
                        let mut count = 0;
                        for k in 0..4 {
                            for l in 0..4 {
                                let divisor = (if k / 2 != l / 2 { a } else { 1 })
                                    * (if k % 2 != l % 2 { b } else { 1 });
                                assert_eq!(m[k][l] % divisor, 0);
                                count +=
                                    (m[k][l] / divisor) * E4[i][k / 2][l / 2] * E4[j][k % 2][l % 2];
                            }
                        }
                        assert_eq!(count, 2 * COUNTS[i][j]);
                    }
                }
            }
        }
    }
    // At maximal tilts x=y=1/2, sixteen times the determinant is positive.
    assert_eq!(15_i64.pow(2) - 16 * 12, 33);
}

fn verify_score() {
    let v = [3, -1, -3, -1];
    let x = [2, -2, 2, -2];
    let z = [-4, 0, 0, 4];
    let mut sum = 0;
    for i in 0..4 {
        let a = [[1 + z[i], x[i]], [x[i], 1 - z[i]]]; // twice D_i(1)
        for j in 0..4 {
            let b = [[3 * (1 + z[j]), 2 * x[j]], [2 * x[j], 3 * (1 - z[j])]]; // six times D_j(2/3)
            let mut total = 0;
            for k in 0..4 {
                for l in 0..4 {
                    total += v[k] * v[l] * a[k / 2][l / 2] * b[k % 2][l % 2];
                }
            }
            assert_eq!(total, 12 * SCORE[i][j]);
            sum += COUNTS[i][j] * SCORE[i][j];
        }
    }
    assert_eq!(COUNTS.iter().flatten().sum::<i64>(), 64);
    assert_eq!(sum, -32);
    assert_eq!(
        SCORE.iter().flatten().max().unwrap() - SCORE.iter().flatten().min().unwrap(),
        144
    );
}

fn main() {
    verify_rival();
    verify_score();
    println!("16 counts, asymmetric determinant, and one-station score checked. Mean -1/2; TV radius 1/288.");
}
