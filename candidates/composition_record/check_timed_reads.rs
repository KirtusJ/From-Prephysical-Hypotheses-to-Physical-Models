//! Exact first-click records for two opportunities. All chances per opportunity
//! use a common denominator D. Each entry of a record then has denominator D².
const D: i64 = 80;
const MINOR_NUM: i64 = 3;
const MINOR_DEN: i64 = 8;

#[derive(Clone, Copy, Debug)]
struct Slot {
    any: i64,
    minor: i64,
}

fn slot(any: i64, minor: i64) -> Slot {
    assert!((0..=D).contains(&any) && (0..=any).contains(&minor));
    Slot { any, minor }
}

// Order: first minor, first heavy, second minor, second heavy, timeout.
fn records(first: Slot, second_if_alive: Slot) -> [i64; 5] {
    let remaining = D - first.any;
    let row = [
        D * first.minor,
        D * (first.any - first.minor),
        remaining * second_if_alive.minor,
        remaining * (second_if_alive.any - second_if_alive.minor),
        remaining * (D - second_if_alive.any),
    ];
    assert_eq!(row.iter().sum::<i64>(), D * D);
    row
}

fn score(direct: &[i64; 5], split: &[i64; 5]) -> i64 {
    // Measured numerator multiplied by 3 to clear 1/r.
    MINOR_NUM * (split[4] - direct[4] - 2 * (direct[2] + direct[3])) + 2 * MINOR_DEN * direct[2]
}

fn sum_into(total: &mut [i64; 5], row: [i64; 5]) {
    for (a, b) in total.iter_mut().zip(row) {
        *a += b;
    }
}

fn main() {
    let mut checked = 0;
    for b in (0..=D).step_by(8) {
        let minor = MINOR_NUM * b / MINOR_DEN;
        for a in minor..=D {
            let u = slot(a, minor);
            let s = slot(b, minor);
            assert_eq!(
                score(&records(u, u), &records(s, s)),
                MINOR_NUM * (a - b).pow(2)
            );
            checked += 1;
        }
    }
    let s = slot(40, 15);
    let ordinary = records(s, s);
    let mut fair_direct = [0; 5];
    for a in [45, 36] {
        let u = slot(a, 15);
        sum_into(&mut fair_direct, records(u, u));
    }
    let doubled_split = ordinary.map(|v| 2 * v);
    assert_eq!(score(&fair_direct, &doubled_split), 3 * 41);
    println!("{checked} linked hazard pairs; fair held-type contrast 41/12800");

    // Physical subports. These are ordinary projective masses multiplied by
    // filter transmission probabilities. Scale branch-specific hazards by 80.
    let mut ports_u = [0; 5];
    let mut ports_s = [0; 5];
    for (mass, u, s) in [
        (4, slot(40, 0), slot(30, 0)),
        (1, slot(40, 0), slot(80, 0)),
        (3, slot(40, 40), slot(40, 40)),
    ] {
        sum_into(&mut ports_u, records(u, u).map(|v| v * mass));
        sum_into(&mut ports_s, records(s, s).map(|v| v * mass));
    }
    assert_eq!(ports_u[..2], ports_s[..2]);
    assert_eq!(128 * score(&ports_u, &ports_s), 5 * 3 * 8 * D * D);
    println!("matched first-bin absorbing ports: contrast 5/128");

    // Here signs are redrawn after a miss. Each phase has two possible
    // raw gains, giving the same pooled binary kernel as the ordinary model.
    // Twice 80 permits the pooled minor hazard (3/8)*(9/20)=27/160.
    let target_events = [27, 45, 88]; // minor, heavy, blank in units of 1/160
    let mut held_u = [0; 5];
    let mut held_s = [0; 5];
    for (b, minor) in [(32, 12), (40, 15)] {
        let u = slot(36, minor);
        let s = slot(b, minor);
        sum_into(&mut held_u, records(u, u));
        sum_into(&mut held_s, records(s, s));
    }
    assert_eq!(held_u[..2], held_s[..2]);
    assert_eq!(400 * score(&held_u, &held_s), 3 * 2 * D * D);
    println!("matched single-opportunity cells; held two-mode contrast 1/400");
    for first_split in [false, true] {
        for second_split in [false, true] {
            let settings = |split| {
                if split {
                    [slot(32, 12), slot(40, 15)]
                } else {
                    [slot(36, 12), slot(36, 15)]
                }
            };
            let mut total = [0; 5];
            for first in settings(first_split) {
                for second in settings(second_split) {
                    sum_into(&mut total, records(first, second));
                }
            }
            let [m, h, q] = target_events;
            assert_eq!(total, [160 * m, 160 * h, q * m, q * h, q * q]);
        }
    }
    println!(
        "all four setting words and all five first-click outcomes match under per-slot redraw"
    );
}
