//! Exact replay of the event-ready, position-only CHSH test.
//! Build with rustc --edition=2021 -D warnings check_heralded_bell.rs
//! and run the executable. No external libraries or input data are needed.
use std::collections::{BTreeMap, BTreeSet};

// A real symmetric 2-by-2 matrix is stored as [M00, M01, M11].
type Sym = [i64; 3];
type Paths = BTreeMap<i32, [[i64; 2]; 2]>;
const I8: Sym = [8, 0, 8];
const Z8: Sym = [8, 0, -8];

fn physical_input() -> Paths {
    // At each site the rows are outgoing rails R,L and the columns are
    // the two input alternatives |+1,R>, |-1,L>, in that order.
    BTreeMap::from([(1, [[1, 0], [0, 0]]), (-1, [[0, 0], [0, 1]])])
}

fn step(paths: &Paths) -> Paths {
    let mut next = Paths::new();
    for (&site, rows) in paths {
        for col in 0..2 {
            next.entry(site + 1).or_default()[0][col] += rows[0][col] + rows[1][col];
            next.entry(site - 1).or_default()[1][col] += rows[0][col] - rows[1][col];
        }
    }
    next
}

fn gram(rows: &[[i64; 2]; 2]) -> Sym {
    let [[a, b], [c, d]] = *rows;
    [a * a + c * c, a * b + c * d, b * b + d * d]
}

fn binned_effects(clock: u32, paths: &Paths) -> Vec<(i32, Sym)> {
    // Amplitude denominator 2^(clock/2). Put every position effect over 8.
    assert!(clock <= 3);
    paths
        .iter()
        .map(|(&x, rows)| (x, gram(rows).map(|v| v * (8 >> clock))))
        .collect()
}

fn sum_observable(sites: &[(i32, Sym)], sign: impl Fn(i32, usize) -> i64) -> Sym {
    let mut observable = [0; 3];
    for (i, &(x, effect)) in sites.iter().enumerate() {
        for k in 0..3 {
            observable[k] += sign(x, i) * effect[k];
        }
    }
    observable
}

fn product_numerator(a: Sym, b: Sym, diag0: i64, off: i64, diag1: i64) -> i64 {
    // Contraction with the 00,11 block; its trace and operator scales are
    // accounted for by the caller. The off-diagonal term occurs twice.
    diag0 * a[0] * b[0] + 2 * off * a[1] * b[1] + diag1 * a[2] * b[2]
}

fn corr192(a: Sym, b: Sym) -> i64 {
    product_numerator(a, b, 1, -1, 2)
}

fn conditional_outcomes768(a: Sym, b: Sym) -> [i64; 4] {
    // For observable A/8 the effect for a sign is (8I + sign*A)/16.
    let mut counts = [0; 4];
    for (i, sign_a) in [1, -1].into_iter().enumerate() {
        for (j, sign_b) in [1, -1].into_iter().enumerate() {
            let ea = std::array::from_fn(|k| I8[k] + sign_a * a[k]);
            let eb = std::array::from_fn(|k| I8[k] + sign_b * b[k]);
            counts[2 * i + j] = product_numerator(ea, eb, 1, -1, 2);
        }
    }
    assert!(counts.iter().all(|&x| x >= 0));
    assert_eq!(counts.iter().sum::<i64>(), 768);
    counts
}

fn max_chsh192(settings: &BTreeSet<Sym>) -> i64 {
    let settings: Vec<_> = settings.iter().collect();
    let row: Vec<Vec<i64>> = settings
        .iter()
        .map(|&&a| settings.iter().map(|&&b| corr192(a, b)).collect())
        .collect();
    let mut best = i64::MIN;
    // For a fixed pair on Bob's side, Alice's two maximizations are independent.
    // The setting pool contains each observable and its negative.
    for b0 in 0..settings.len() {
        for b1 in 0..settings.len() {
            let plus = row.iter().map(|r| r[b0] + r[b1]).max().unwrap();
            let minus = row.iter().map(|r| r[b0] - r[b1]).max().unwrap();
            best = best.max(plus + minus);
        }
    }
    best
}

fn check_filter() {
    // The traced blank gives 4*rho = u*u^T + f*f^T with u=(1,1,1,0),
    // f=|11>. Compute both branches of the same product filter K tensor K.
    // Each local matrix given below equals 2K, so the outer products over
    // the two propagated columns have the common denominator 4*4^2=64.
    let k = [[1, 0], [-1, 1]];
    let transform = |input: [i64; 4]| -> [i64; 4] {
        std::array::from_fn(|i| {
            (0..4)
                .map(|j| k[i / 2][j / 2] * k[i % 2][j % 2] * input[j])
                .sum()
        })
    };
    let u = transform([1, 1, 1, 0]);
    let f = transform([0, 0, 0, 1]);
    assert_eq!(u, [1, 0, 0, -1]);
    assert_eq!(f, [0, 0, 0, 1]);
    let state: [[i64; 4]; 4] =
        std::array::from_fn(|i| std::array::from_fn(|j| u[i] * u[j] + f[i] * f[j]));
    assert_eq!(state, [[1, 0, 0, -1], [0; 4], [0; 4], [-1, 0, 0, 2]]);
    assert_eq!((0..4).map(|i| state[i][i]).sum::<i64>(), 3);
    // 4*(I-K^T K) has positive leading minor and positive determinant.
    let a = 4 - k[0][0] * k[0][0] - k[1][0] * k[1][0];
    let b = -k[0][0] * k[0][1] - k[1][0] * k[1][1];
    let d = 4 - k[0][1] * k[0][1] - k[1][1] * k[1][1];
    assert!(a > 0 && a * d - b * b > 0);
}

fn check_bell_bounds(z: Sym, o: Sym) {
    for a0 in [-1, 1] {
        for a1 in [-1, 1] {
            for b0 in [-1, 1] {
                for b1 in [-1, 1] {
                    let s: i64 = a0 * (b0 + b1) + a1 * (b0 - b1);
                    assert_eq!(s.abs(), 2);
                }
            }
        }
    }
    let settings = [(z, z), (z, o), (o, z), (o, o)];
    let masses = settings.map(|(a, b)| conditional_outcomes768(a, b));
    assert_eq!(
        masses,
        [
            [256, 0, 0, 512],
            [192, 64, 64, 448],
            [192, 64, 64, 448],
            [120, 136, 136, 376]
        ]
    );
    let corr = settings.map(|(a, b)| corr192(a, b));
    assert_eq!(corr, [192, 128, 128, 56]);
    let s = corr[0] + corr[1] + corr[2] - corr[3];
    assert_eq!(s * 24, 49 * 192);
    // Signed coefficient of eta^2 for the double positives, and coefficient
    // of eta for the singles, when every missing local result is assigned -1.
    let joint = masses[0][0] + masses[1][0] + masses[2][0] - masses[3][0];
    let singles = 2 * masses[0][0] + masses[0][1] + masses[0][2];
    assert_eq!((joint, singles), (520, 512));
    assert_eq!(64 * joint, 65 * singles);
    // Fully dephasing the filtered code removes the off-diagonal entries.
    let classical = settings.map(|(a, b)| product_numerator(a, b, 1, 0, 2));
    assert_eq!(
        classical[0] + classical[1] + classical[2] - classical[3],
        360
    ); // 15/8
       // Preannounced preparation failures return (+,+) on every setting.
    let all_launch = 3 * s + (64 - 3) * 2 * 192;
    assert_eq!(all_launch * 512, 1025 * 64 * 192);
}

fn main() {
    check_filter();
    let mut paths = physical_input();
    let mut pool = BTreeSet::new();
    for clock in 0..=3 {
        let sites = binned_effects(clock, &paths);
        assert_eq!(sum_observable(&sites, |_, _| 1), I8);
        for mask in 0..(1 << sites.len()) {
            pool.insert(sum_observable(&sites, |_, i| {
                if mask & (1 << i) == 0 {
                    1
                } else {
                    -1
                }
            }));
        }
        if clock >= 2 {
            let best = max_chsh192(&pool);
            let expected = if clock == 2 { (23, 384) } else { (45, 392) };
            assert_eq!((pool.len(), best), expected);
            println!(
                "Clocks 0..={clock}: {} distinct observables, maximum S={best}/192",
                pool.len()
            );
        }
        if clock == 3 {
            assert_eq!(
                sites,
                [
                    (-4, [0, 0, 1]),
                    (-2, [1, -2, 5]),
                    (0, [1, 0, 1]),
                    (2, [5, 2, 1]),
                    (4, [1, 0, 0])
                ]
            );
            let o = sum_observable(&sites, |x, _| if x > 0 { 1 } else { -1 });
            assert_eq!(o, [4, 4, -6]);
            check_bell_bounds(Z8, o);
            // Optional rail-resolving read adds (0,R) to the positive bin.
            let r = paths[&0][0];
            let delta = [2 * r[0] * r[0], 2 * r[0] * r[1], 2 * r[1] * r[1]];
            let rail = std::array::from_fn(|k| o[k] + delta[k]);
            assert_eq!(rail, [6, 4, -6]);
            assert_eq!(
                corr192(Z8, Z8) + 2 * corr192(Z8, rail) - corr192(rail, rail),
                404
            );
        }
        paths = step(&paths);
    }
    println!("Herald 3/64; all four complete conditional tables passed; position S=49/24.");
    println!("Rail-resolving S=101/48; position erasure threshold 64/65; all-launch S=1025/512.");
}
