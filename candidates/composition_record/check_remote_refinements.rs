//! Exact replay of the remote refinements. Build with rustc --edition=2021.
use std::collections::BTreeMap;

type Flight = BTreeMap<i32, [i64; 2]>;

fn flight(x: i32, side: usize, coins: &str) -> Flight {
    let mut seed = [0, 0];
    seed[side] = 1;
    let mut state = Flight::from([(x, seed)]);
    for coin in coins.bytes() {
        let mut next = Flight::new();
        for (&pos, &[r, l]) in &state {
            let (right, left) = match coin {
                b'H' => (r + l, r - l),
                b'I' => (r, l),
                _ => panic!("unknown coin"),
            };
            next.entry(pos + 1).or_default()[0] += right;
            next.entry(pos - 1).or_default()[1] += left;
        }
        state = next;
    }
    state
}

fn masses(x: i32, side: usize, coins: &str) -> BTreeMap<i32, i64> {
    let cells: BTreeMap<_, _> = flight(x, side, coins)
        .into_iter()
        .map(|(p, [r, l])| (p, r * r + l * l))
        .collect();
    assert_eq!(
        cells.values().sum::<i64>(),
        1 << coins.bytes().filter(|&b| b == b'H').count()
    );
    cells
}

fn populated(coins: &str) -> Vec<i64> {
    let mut v: Vec<_> = masses(0, 0, coins)
        .into_values()
        .filter(|&x| x > 0)
        .collect();
    v.sort();
    v
}

// The left port is split only on the active arm. Scale both arms' raw tables
// to the same units. In both, the structural zero stays dark at q=0.
fn near_score(left: &[i64], right: &[i64], q: u32, split: bool) -> (i64, i64) {
    let mut den = 0;
    let mut score = 0;
    let pow = |v: i64| if v == 0 { 0 } else { v.pow(q) };
    for (i, (&b, &a)) in left.iter().zip(right).enumerate() {
        let left_weight = if split { 2 * pow(b) } else { pow(2 * b) };
        let count = left_weight + pow(2 * a);
        den += count;
        score += match i {
            0 => 4 * count,
            1 => -count,
            _ => 0,
        };
    }
    (score, den)
}

fn walk_checks() {
    let wells = [-4, -2, 0, 2, 4];
    let right = masses(1, 0, "HHH");
    let left = masses(-1, 1, "HHH");
    let a = wells.map(|x| right.get(&x).copied().unwrap_or(0));
    let b = wells.map(|x| left.get(&x).copied().unwrap_or(0));
    assert_eq!(a, [0, 1, 1, 5, 1]);
    assert_eq!(b, [1, 5, 1, 1, 0]);
    for q in 0..=4 {
        let (sn, sd) = near_score(&b.map(|v| 2 * v), &a, q, true);
        let (bn, bd) = near_score(&b.map(|v| 2 * v), &a, q, false);
        let t = 2i64.pow(q);
        let u = 5i64.pow(q);
        assert_eq!(
            i128::from(sn * bd - bn * sd) * i128::from(3 * (1 + t) * (3 + u)),
            i128::from((2 - t) * (5 - u)) * i128::from(sd * bd)
        );
    }
    assert_eq!(populated("HHIII"), [1, 1, 1, 1]);
    assert_eq!(populated("HHHII"), [1, 1, 1, 1, 4]);
    for len in 0..=4 {
        for mask in 0..(1 << len) {
            let word: String = (0..len)
                .map(|i| if mask & (1 << i) == 0 { 'H' } else { 'I' })
                .collect();
            // Normalize to denominator 16 so an equivalent table at another scale counts.
            let mut weights = populated(&word);
            let total = weights.iter().sum::<i64>();
            for v in &mut weights {
                *v *= 16 / total;
            }
            assert_ne!(weights, [2, 2, 2, 2, 8]);
        }
    }
}

fn spectator_checks() {
    for a in 0..=24i64 {
        for b in 0..=24 {
            for c in 1..=12 {
                let (pp, pq, qq) = (2 * a + c, a + b + c, 2 * b + c);
                let numerator = c * (pq * qq + pp * pq - 2 * pp * qq);
                assert_eq!(numerator, 2 * c * (a - b).pow(2));
                assert_eq!(numerator == 0, a == b);
            }
        }
    }
    // N=8 fixture. Use unit masses as weights for q=0,1,2; spectator unsplit.
    for (q, (n, d)) in [(0, (1, 30)), (1, (0, 1)), (2, (2, 165))] {
        let (a, b, c) = (2i64.pow(q), 2, 4i64.pow(q));
        assert_eq!(
            2 * c * (a - b).pow(2) * d,
            n * (2 * a + c) * (a + b + c) * (2 * b + c)
        );
    }
}

// Raw weights on the 32-unit grid, scaled by 32*(256-t). The normalized
// large-cell rate on the perturbed row will be t/256 instead of 24/32.
fn raw_weight(cell: i64, t: i64) -> i64 {
    if cell == 24 {
        8 * t
    } else {
        cell * (256 - t)
    }
}

fn invisible_types() {
    for t in [191, 193] {
        for k in 1..=32 {
            assert!(raw_weight(k - 1, t) < raw_weight(k, t));
        }
    }
    // A common persistent sign shifts P(both hit) by (1/256)^2.
    assert_eq!(191i64.pow(2) + 193i64.pow(2) - 2 * 192i64.pow(2), 2);
    let mut hist = Vec::new();
    let mut checked = 0;
    fn visit(hist: &mut Vec<i64>, remaining: i64, cap: i64, checked: &mut u32) {
        if remaining == 0 {
            let denominators =
                [191, 193].map(|t| hist.iter().map(|&cell| raw_weight(cell, t)).sum::<i64>());
            let [lo, hi] = denominators;
            for &cell in hist.iter() {
                let sum_num = raw_weight(cell, 191) * hi + raw_weight(cell, 193) * lo;
                assert_eq!(32 * sum_num, 2 * cell * lo * hi);
            }
            *checked += 1;
            return;
        }
        for n in 1..=remaining.min(cap) {
            hist.push(n);
            visit(hist, remaining - n, n, checked);
            hist.pop();
        }
    }
    visit(&mut hist, 32, 32, &mut checked);
    assert_eq!(checked, 8349);
    println!("All {checked} integer partitions of 32 match the two-type one-shot law.");
}

// Site labels run from 0 through 7 modulo eight; -3 and -1 are sites 5 and 7.
// Rail amplitudes have a common denominator sqrt(8) after the three H pulses.
type Ring = [[i64; 2]; 8];

fn ring_tick(input: Ring, coin_at: impl Fn(usize) -> u8) -> Ring {
    let mut output = [[0; 2]; 8];
    for (site, [r, l]) in input.into_iter().enumerate() {
        let (right, left) = match coin_at(site) {
            b'H' => (r + l, r - l),
            b'I' => (r, l),
            b'X' => (l, r),
            _ => panic!("unknown coin"),
        };
        output[(site + 1) % 8][0] += right;
        output[(site + 7) % 8][1] += left;
    }
    output
}

fn held_split_ring() {
    let mut prepared = [[0; 2]; 8];
    prepared[0][0] = 1;
    for _ in 0..3 {
        prepared = ring_tick(prepared, |_| b'H');
    }
    assert_eq!(
        prepared,
        [
            [0, 0],
            [2, 1],
            [0, 0],
            [1, 0],
            [0, 0],
            [0, 1],
            [0, 0],
            [-1, 0]
        ]
    );
    let minor = [0, 0, 0, 1, 0, 1, 0, 1];
    let mut tagged = [[[0; 2]; 8]; 2];
    for (site, rails) in prepared.into_iter().enumerate() {
        tagged[usize::from(site != 1)][site] = rails;
    }
    for split in [false, true] {
        let cells = tagged.map(|rails| {
            let coast = ring_tick(rails, |_| b'I');
            let end = ring_tick(coast, |site| if split && site == 2 { b'I' } else { b'X' });
            end.map(|[r, l]| r * r + l * l)
        });
        let heavy = if split {
            [0, 1, 0, 4, 0, 0, 0, 0]
        } else {
            [0, 5, 0, 0, 0, 0, 0, 0]
        };
        assert_eq!(cells, [heavy, minor]);
        assert_eq!(cells.iter().flatten().sum::<i64>(), 8);
        let bob: [i64; 8] = std::array::from_fn(|site| cells[0][site] + cells[1][site]);
        assert_eq!(bob[3], if split { 5 } else { 1 });
        for q in 0..=4 {
            // Raw-power controls illustrate the order of pooling, including
            // support counting. They are separate from the lower-half calibration.
            let weight = |m: i64| if m == 0 { 0 } else { m.pow(q) };
            let minor_weight = cells[1].iter().copied().map(weight).sum::<i64>();
            let total: i64 = cells.iter().flatten().copied().map(weight).sum();
            assert_eq!(minor_weight, 3);
            assert_eq!(
                total,
                if split {
                    4_i64.pow(q) + 4
                } else {
                    5_i64.pow(q) + 3
                }
            );
            assert_eq!(bob.into_iter().map(weight).sum::<i64>(), 5_i64.pow(q) + 3);
        }
        println!("Eight-site split={split}: heavy={heavy:?}, minor={minor:?}, Bob(+3)={}. All entries /8.", bob[3]);
    }
}

fn main() {
    walk_checks();
    held_split_ring();
    spectator_checks();
    invisible_types();
    println!("Walk spectra, signed marginal tests, spectator identities and equalities passed.");
}
