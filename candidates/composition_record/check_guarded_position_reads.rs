//! Exact amplitude replay. Each global Hadamard layer contributes a common
//! denominator sqrt(2), omitted from the integer amplitudes below.
use std::ops::{Add, Neg, Sub};

#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
struct Gaussian(i64, i64);

impl Add for Gaussian {
    type Output = Self;
    fn add(self, other: Self) -> Self { Self(self.0 + other.0, self.1 + other.1) }
}
impl Neg for Gaussian {
    type Output = Self;
    fn neg(self) -> Self { Self(-self.0, -self.1) }
}
impl Sub for Gaussian {
    type Output = Self;
    fn sub(self, other: Self) -> Self { self + -other }
}
impl Gaussian {
    fn norm(self) -> i64 { self.0 * self.0 + self.1 * self.1 }
}

type Spinor = [Gaussian; 2];
const ZERO: Gaussian = Gaussian(0, 0);
const ONE: Gaussian = Gaussian(1, 0);

#[derive(Clone, Copy)]
enum Coin { Identity, Hadamard, Swap }

impl Coin {
    fn apply(self, [right, left]: Spinor) -> Spinor {
        match self {
            Self::Identity => [right, left],
            Self::Hadamard => [right + left, right - left],
            Self::Swap => [left, right],
        }
    }
}

fn tick(input: &[Spinor], coin: impl Fn(usize) -> Coin) -> Vec<Spinor> {
    let n = input.len();
    let mut output = vec![[ZERO; 2]; n];
    for (x, spinor) in input.iter().enumerate() {
        let [right, left] = coin(x).apply(*spinor);
        output[(x + 1) % n][0] = right;
        output[(x + n - 1) % n][1] = left;
    }
    output
}

#[derive(Clone, Copy)]
enum Layout { Triples, Pairs }

impl Layout {
    fn center(self, x: usize) -> bool {
        match self { Self::Triples => x % 3 == 0, Self::Pairs => x % 4 < 2 }
    }
}

fn verify(input: &[Spinor], layout: Layout, first: Coin) {
    let n = input.len();
    let centers: Vec<_> = (0..n).filter(|&x| layout.center(x)).collect();
    assert!(input.iter().enumerate().all(|(x, s)| layout.center(x) || *s == [ZERO; 2]));
    let after_two = tick(&tick(input, |_| first), |_| Coin::Hadamard);
    let output = match layout {
        Layout::Triples => after_two,
        Layout::Pairs => tick(&after_two, |x| if layout.center(x) { Coin::Identity } else { Coin::Swap }),
    };
    let mut occupied = vec![false; n];
    let mut expected = vec![[ZERO; 2]; n];
    for x in centers {
        let [a, b] = first.apply(input[x]);
        let half = a.norm() + b.norm(); // common output denominator restored by division
        match layout {
            Layout::Triples => {
                let left = (x + n - 2) % n;
                let right = (x + 2) % n;
                for site in [left, x, right] { assert!(!std::mem::replace(&mut occupied[site], true)); }
                expected[left] = [ZERO, -b];
                expected[x] = [b, a];
                expected[right] = [a, ZERO];
                let mass = |j: usize| output[j][0].norm() + output[j][1].norm();
                assert_eq!(mass(x), half);
                assert_eq!(mass(left) + mass(right), half);
            }
            Layout::Pairs => {
                let left = (x + n - 1) % n;
                let right = (x + 1) % n;
                for site in [left, right] {
                    assert!(!std::mem::replace(&mut occupied[site], true));
                    assert_eq!(output[site][0].norm() + output[site][1].norm(), half);
                }
                expected[left] = [-b, a];
                expected[right] = [b, a];
            }
        }
    }
    assert!(occupied.iter().all(|&used| used));
    assert_eq!(output, expected);
}

fn main() {
    let mut trials = 0;
    for (layout, period) in [(Layout::Triples, 3), (Layout::Pairs, 4)] {
        for blocks in 1..=8 {
            let n = period * blocks;
            for first in [Coin::Identity, Coin::Hadamard] {
                let mut dense = vec![[ZERO; 2]; n];
                for x in (0..n).filter(|&x| layout.center(x)) {
                    for rail in 0..2 {
                        let mut basis = vec![[ZERO; 2]; n];
                        basis[x][rail] = ONE;
                        verify(&basis, layout, first);
                        trials += 1;
                    }
                    let k = x as i64;
                    dense[x] = [Gaussian(1 - k, 2 + k), Gaussian(3 + k, -2 * k - 1)];
                }
                verify(&dense, layout, first);
                trials += 1;
            }
        }
    }
    println!("Verified {trials} exact basis and coherent-input replays, including rings of length 3, 4 and 6.");
}
