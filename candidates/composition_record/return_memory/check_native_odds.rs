//! A ten-tick signed walk on a 23-site ring. Integer rails include both
//! coefficients of (a + b sqrt(2)) / 32. No floating point or dependencies.
use std::ops::{Add, Neg};

const SITES: usize = 23;
const SCALE: i32 = 32;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Amplitude(i32, i32);

const ZERO: Amplitude = Amplitude(0, 0);

impl Add for Amplitude {
    type Output = Self;
    fn add(self, rhs: Self) -> Self {
        Self(self.0 + rhs.0, self.1 + rhs.1)
    }
}

impl Neg for Amplitude {
    type Output = Self;
    fn neg(self) -> Self {
        Self(-self.0, -self.1)
    }
}

impl Amplitude {
    fn divided_by_sqrt_two(self) -> Self {
        assert_eq!(self.0 % 2, 0, "inadequate dyadic scale for H");
        Self(self.1, self.0 / 2)
    }
    // Return the norm numerator in the same basis, denominator SCALE^2.
    fn norm(self) -> Self {
        Self(self.0 * self.0 + 2 * self.1 * self.1, 2 * self.0 * self.1)
    }
}

fn site(x: i32) -> usize {
    x.rem_euclid(SITES as i32) as usize
}

fn run(j: i32, d: i32) {
    let mut state = [[ZERO; 2]; SITES];
    state[site(0)][0] = Amplitude(SCALE, 0); // rails [R,L]
    for t in 0..2 * d {
        let mut next = [[ZERO; 2]; SITES];
        for (x, &[r, l]) in state.iter().enumerate() {
            let is_split = (t == 0 && x == site(0)) || (1 <= t && t <= j && x == site(-t));
            let is_mirror = t == d && (x == site(d) || x == site(-d));
            let (out_r, out_l) = if is_split {
                (
                    (r + l).divided_by_sqrt_two(),
                    (r + -l).divided_by_sqrt_two(),
                )
            } else if is_mirror {
                (l, r)
            } else {
                (r, l)
            };
            next[(x + 1) % SITES][0] = out_r;
            next[(x + SITES - 1) % SITES][1] = out_l;
        }
        state = next;
        let total = state.iter().flatten().fold(ZERO, |a, z| a + z.norm());
        assert_eq!(total, Amplitude(SCALE * SCALE, 0), "norm at tick {}", t + 1);
    }
    let [weak, reference] = state[site(0)];
    let expected = if d == 4 && j == 4 {
        Amplitude(0, -4) // H at the left turn sends its R daughter home
    } else {
        [
            Amplitude(-16, 0),
            Amplitude(0, 8),
            Amplitude(-8, 0),
            Amplitude(0, 4),
        ][(j - 1) as usize]
    };
    assert_eq!(weak, expected);
    assert_eq!(reference, Amplitude(0, 16));
    let odds = 1 << j;
    assert_eq!(odds * weak.norm().0, reference.norm().0);

    // Check every discarded rail independently, including the outward
    // final daughter if the last splitter also serves as the mirror.
    let mut discarded = [[ZERO; 2]; SITES];
    for t in 1..=j {
        let prior = [
            Amplitude(16, 0),
            Amplitude(0, -8),
            Amplitude(8, 0),
            Amplitude(0, -4),
        ][(t - 1) as usize];
        if t == d {
            discarded[site(-2 * d)][1] = -prior;
        } else {
            discarded[site(2 * d - 2 * t)][0] = prior;
        }
    }
    assert_eq!(discarded[site(0)], [ZERO, ZERO]);
    state[site(0)] = [ZERO, ZERO];
    assert_eq!(state, discarded);
    println!(
        "tick={} j={} small:large=1:{} port={}/{} discarded={}/{}",
        2 * d,
        j,
        odds,
        odds + 1,
        2 * odds,
        odds - 1,
        2 * odds
    );
}

fn main() {
    for j in 1..=4 {
        run(j, 5);
    }
    for j in 1..=4 {
        run(j, 4);
    }
}
