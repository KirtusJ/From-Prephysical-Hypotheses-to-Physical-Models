//! Exact certificate for the nearest separable terminal-position law.
//! All interval endpoints below are integers with a common positive denominator.
use num_bigint::BigInt;
use std::array::from_fn;

const B: [[i64; 4]; 4] = [[2, 2, 2, 1], [2, 2, 1, 0], [2, 1, 2, 0], [1, 0, 0, 2]];
const EFFECT4: [[[i64; 2]; 2]; 4] = [
    [[0, 0], [0, 1]],
    [[1, -1], [-1, 2]],
    [[2, 1], [1, 1]],
    [[1, 0], [0, 0]],
];
const L: [[i64; 2]; 2] = [[2, -1], [-1, -2]];
const NULL: [i64; 4] = [3, -1, -1, 3];
const X: [i64; 4] = [2, -2, 2, -2];
const Z: [i64; 4] = [-4, 0, 0, 4];
const CELLS64: [[i64; 4]; 4] = [[1, 3, 3, 1], [3, 7, 5, 1], [3, 5, 19, 5], [1, 1, 5, 1]];
// Coefficients in ascending powers, including explicit zero terms when needed.
const CUBIC: [i64; 4] = [-448, 784, 140, -125];
const COFACTORS: [[i64; 4]; 4] = [
    [384, -384, -200, 100],
    [-256, 288, 80, -50],
    [-256, 288, 80, -50],
    [-192, 368, -180, 25],
];
const SCALE: i64 = 1_000_000_000;

#[derive(Clone, Debug)]
struct Bounds {
    lo: BigInt,
    hi: BigInt,
}

impl Bounds {
    fn point(value: impl Into<BigInt>) -> Self {
        let value = value.into();
        Self {
            lo: value.clone(),
            hi: value,
        }
    }

    fn plus(&self, other: &Self) -> Self {
        Self {
            lo: &self.lo + &other.lo,
            hi: &self.hi + &other.hi,
        }
    }

    fn times(&self, other: &Self) -> Self {
        let products = [
            &self.lo * &other.lo,
            &self.lo * &other.hi,
            &self.hi * &other.lo,
            &self.hi * &other.hi,
        ];
        Self {
            lo: products.iter().min().unwrap().clone(),
            hi: products.iter().max().unwrap().clone(),
        }
    }

    fn scaled(&self, factor: i64) -> Self {
        self.times(&Self::point(factor))
    }
}

// Return an enclosure for scale^degree * polynomial(x / scale).
fn polynomial(coeff: &[i64], x: &Bounds, scale: i64) -> Bounds {
    let (last, rest) = coeff.split_last().unwrap();
    let mut value = Bounds::point(*last);
    let mut denominator = BigInt::from(1);
    for &c in rest.iter().rev() {
        denominator *= scale;
        value = value.times(x).plus(&Bounds::point(&denominator * c));
    }
    value
}

fn determinant(rows: &[Vec<i64>]) -> i64 {
    if rows.is_empty() {
        return 1;
    }
    rows[0]
        .iter()
        .enumerate()
        .map(|(j, a)| {
            let minor: Vec<_> = rows[1..]
                .iter()
                .map(|r| {
                    r.iter()
                        .enumerate()
                        .filter(|(k, _)| *k != j)
                        .map(|(_, &v)| v)
                        .collect()
                })
                .collect();
            let sign = if j % 2 == 0 { 1 } else { -1 };
            sign * a * determinant(&minor)
        })
        .sum()
}

fn det_submatrix(m: &[[i64; 4]; 4], rows: &[usize], cols: &[usize]) -> i64 {
    determinant(
        &rows
            .iter()
            .map(|&i| cols.iter().map(|&j| m[i][j]).collect())
            .collect::<Vec<_>>(),
    )
}

fn verify_primal(parameter: &Bounds) {
    let zero = BigInt::from(0);
    assert!(polynomial(&CUBIC, &Bounds::point(parameter.lo.clone()), SCALE).hi < zero);
    assert!(polynomial(&CUBIC, &Bounds::point(parameter.hi.clone()), SCALE).lo > zero);
    assert!(polynomial(&[784, 280, -375], parameter, SCALE).lo > zero);

    // Five distinct points certify the polynomial identities of degrees at most four.
    for t in 0..5 {
        let m: [[i64; 4]; 4] =
            from_fn(|i| from_fn(|j| 4 * B[i][j] + t * L[i / 2][j / 2] * L[i % 2][j % 2]));
        let indices = [0, 1, 2, 3];
        let trace: i64 = (0..4).map(|i| m[i][i]).sum();
        assert_eq!(trace, 32);
        for i in 0..4 {
            for j in 0..4 {
                assert_eq!(m[i][j], m[2 * (i / 2) + j % 2][2 * (j / 2) + i % 2]);
            }
        }
        let eval = |coeff: &[i64]| coeff.iter().rev().fold(0, |v, c| v * t + c);
        assert_eq!(
            det_submatrix(&m, &indices, &indices),
            (4 - 5 * t) * eval(&CUBIC)
        );
        for (j, coeff) in COFACTORS.iter().enumerate() {
            let cols: Vec<_> = (0..4).filter(|&k| k != j).collect();
            let sign = if j % 2 == 0 { 1 } else { -1 };
            assert_eq!(sign * det_submatrix(&m, &[1, 2, 3], &cols), eval(coeff));
        }
        assert_eq!(m[1][1], 8 - 4 * t);
        assert_eq!(det_submatrix(&m, &[1, 2], &[1, 2]), eval(&[48, -72, 15]));
    }
    // The lower 3x3 principal block is positive definite; the Schur complement
    // is zero at the root of CUBIC, yielding a positive semidefinite state.
    for coeff in [&[8, -4][..], &[48, -72, 15], &COFACTORS[0]] {
        assert!(polynomial(coeff, parameter, SCALE).lo > zero);
    }
}

fn verify_detector() {
    for a in 0..2 {
        for b in 0..2 {
            let sum =
                |weights: &[i64; 4]| (0..4).map(|i| weights[i] * EFFECT4[i][a][b]).sum::<i64>();
            assert_eq!(sum(&[1; 4]), if a == b { 4 } else { 0 });
            assert_eq!(sum(&X), if a != b { 4 } else { 0 });
            assert_eq!(sum(&Z), [[4, 0], [0, -4]][a][b]);
            assert_eq!(sum(&NULL), 0);
        }
    }
    for i in 0..4 {
        let mut local_trace = 0;
        for a in 0..2 {
            for b in 0..2 {
                local_trace += EFFECT4[i][a][b] * L[b][a];
            }
        }
        assert_eq!(local_trace, [-2, 0, 0, 2][i]);
        for j in 0..4 {
            let mut trace = 0;
            for a in 0..4 {
                for b in 0..4 {
                    trace += B[a][b] * EFFECT4[i][b / 2][a / 2] * EFFECT4[j][b % 2][a % 2];
                }
            }
            assert_eq!(trace, 2 * CELLS64[i][j]);
        }
    }
}

fn verify_dual(parameter: &Bounds) {
    let cofactor = COFACTORS.map(|coeff| polynomial(&coeff, parameter, SCALE));
    let twice_d: [[[i64; 2]; 2]; 4] = from_fn(|i| [[1 + Z[i], X[i]], [X[i], 1 - Z[i]]]);
    // Each entry encloses 4 * c0^2 * s_ij, with c0 scaled by SCALE^3.
    let s: [[Bounds; 4]; 4] = from_fn(|i| {
        from_fn(|j| {
            let mut sum = Bounds::point(0);
            for a in 0..4 {
                for b in 0..4 {
                    let factor = twice_d[i][a / 2][b / 2] * twice_d[j][a % 2][b % 2];
                    sum = sum.plus(&cofactor[a].times(&cofactor[b]).scaled(factor));
                }
            }
            sum
        })
    });
    // Use one positive multiplier, 24 * c0^2, for every adjusted score.
    let h = [
        Bounds::point(0),
        cofactor[0].times(&cofactor[0]).scaled(-24),
        Bounds::point(0),
        s[0][0].plus(&s[3][3].scaled(-1)),
    ];
    let score: [[Bounds; 4]; 4] = from_fn(|i| {
        from_fn(|j| {
            s[i][j]
                .scaled(6)
                .plus(&h[j].scaled(NULL[i]))
                .plus(&h[i].scaled(NULL[j]))
        })
    });
    // The two high corners are equal by the construction of h[3]. The low
    // corners are equal by exchange symmetry (the middle cofactors coincide).
    assert_eq!(COFACTORS[1], COFACTORS[2]);
    for i in 0..4 {
        for j in 0..4 {
            if matches!(i, 1 | 2) || matches!(j, 1 | 2) {
                assert!(score[i][j].hi < score[0][0].lo);
                assert!(score[i][j].lo > score[0][3].hi);
            }
        }
    }
}

fn main() {
    let bracket = Bounds {
        lo: 544_238_217.into(),
        hi: 544_238_219.into(),
    };
    verify_detector();
    verify_primal(&bracket);
    verify_dual(&bracket);
    println!("Certified TV = t/64 in (544238217/64000000000, 544238219/64000000000).");
}
