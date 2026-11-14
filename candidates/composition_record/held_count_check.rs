//! Reproduce the held-cohort bounds for the five-eighths walk cell.
//! Build with `rustc --edition=2021 -O held_count_check.rs -o held_count_check`.
use std::cmp::Ordering;
use std::fmt;
use std::ops::{Add, Div, Mul, Sub};

// Small signed fractions for the explicitly limited (N <= 8) pooling calculation.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct Fraction(i128, i128);

impl Fraction {
    fn new(mut n: i128, mut d: i128) -> Self {
        assert_ne!(d, 0);
        if d < 0 {
            n = -n;
            d = -d;
        }
        let (mut a, mut b) = (n.abs(), d);
        while b != 0 {
            (a, b) = (b, a % b);
        }
        Self(n / a, d / a)
    }
    fn square(self) -> Self {
        self * self
    }
}
impl PartialOrd for Fraction {
    fn partial_cmp(&self, rhs: &Self) -> Option<Ordering> {
        Some((self.0 * rhs.1).cmp(&(rhs.0 * self.1)))
    }
}
impl Add for Fraction {
    type Output = Self;
    fn add(self, rhs: Self) -> Self {
        Self::new(self.0 * rhs.1 + rhs.0 * self.1, self.1 * rhs.1)
    }
}
impl Sub for Fraction {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self {
        Self::new(self.0 * rhs.1 - rhs.0 * self.1, self.1 * rhs.1)
    }
}
impl Mul for Fraction {
    type Output = Self;
    fn mul(self, rhs: Self) -> Self {
        Self::new(self.0 * rhs.0, self.1 * rhs.1)
    }
}
impl Div for Fraction {
    type Output = Self;
    fn div(self, rhs: Self) -> Self {
        Self::new(self.0 * rhs.1, self.1 * rhs.0)
    }
}
impl fmt::Display for Fraction {
    fn fmt(&self, out: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(out, "{}/{}", self.0, self.1)
    }
}

fn pooled_variance(n: u32) -> (Fraction, Fraction) {
    assert!((1..=8).contains(&n));
    let m = Fraction::new(5, 8);
    let floor = Fraction::new(4, 7);
    let zero = Fraction::new(0, 1);
    let mut deficit = zero;
    let mut mass_at_floor = zero;
    let mut variance = zero;
    let mut split_at = zero;
    let mut weights = vec![1_i128];
    for _ in 0..n {
        let mut next = vec![0; weights.len() + 1];
        for (k, v) in weights.into_iter().enumerate() {
            next[k] += 3 * v;
            next[k + 1] += 5 * v;
        }
        weights = next;
    }
    for (k, w) in weights.into_iter().enumerate() {
        let h = Fraction::new(k as i128, n.into());
        let prob = Fraction::new(w, 8_i128.pow(n));
        let pooled = if h <= floor {
            prob
        } else if deficit > zero {
            let required = deficit / (h - floor);
            if required < prob {
                required
            } else {
                prob
            }
        } else {
            zero
        };
        if pooled > zero {
            split_at = h;
        }
        deficit = deficit + (floor - h) * pooled;
        mass_at_floor = mass_at_floor + pooled;
        variance = variance + (prob - pooled) * (h - m).square();
    }
    assert_eq!(deficit, zero);
    (split_at, variance + mass_at_floor * (floor - m).square())
}

// Nonnegative base-10^9 digits, least significant first, canonical zero is [].
// Measurement-count numerators have about 440 decimal digits at N=483.
const BASE: u64 = 1_000_000_000;
#[derive(Clone, Debug, Eq, PartialEq)]
struct Natural(Vec<u32>);

impl Natural {
    fn zero() -> Self {
        Self(vec![])
    }
    fn one() -> Self {
        Self(vec![1])
    }
    fn add_in_place(&mut self, rhs: &Self) {
        let n = self.0.len().max(rhs.0.len());
        self.0.resize(n, 0);
        let mut carry = 0_u64;
        for (i, x) in self.0.iter_mut().enumerate() {
            let sum = u64::from(*x) + u64::from(rhs.0.get(i).copied().unwrap_or(0)) + carry;
            *x = (sum % BASE) as u32;
            carry = sum / BASE;
        }
        if carry != 0 {
            self.0.push(carry as u32);
        }
    }
    fn times(&self, factor: u64) -> Self {
        if factor == 0 {
            return Self::zero();
        }
        let mut out = Vec::<u32>::with_capacity(self.0.len() + 2);
        let mut carry = 0_u128;
        for &d in &self.0 {
            let value = u128::from(d) * u128::from(factor) + carry;
            out.push((value % u128::from(BASE)) as u32);
            carry = value / u128::from(BASE);
        }
        while carry > 0 {
            out.push((carry % u128::from(BASE)) as u32);
            carry /= u128::from(BASE);
        }
        Self(out)
    }
    fn divide_exact(&mut self, d: u32) {
        assert_ne!(d, 0);
        let mut remainder = 0_u64;
        for cell in self.0.iter_mut().rev() {
            let current = remainder * BASE + u64::from(*cell);
            *cell = (current / u64::from(d)) as u32;
            remainder = current % u64::from(d);
        }
        assert_eq!(remainder, 0);
        while self.0.last() == Some(&0) {
            self.0.pop();
        }
    }
    fn pow_small(base: u64, exponent: u32) -> Self {
        (0..exponent).fold(Self::one(), |p, _| p.times(base))
    }
    fn minus(&self, rhs: &Self) -> Self {
        assert_ne!(self.cmp(rhs), Ordering::Less);
        let mut digits = self.0.clone();
        let mut borrow = 0_i64;
        for (i, d) in digits.iter_mut().enumerate() {
            let difference = i64::from(*d) - i64::from(rhs.0.get(i).copied().unwrap_or(0)) - borrow;
            borrow = i64::from(difference < 0);
            *d = (difference + borrow * BASE as i64) as u32;
        }
        assert_eq!(borrow, 0);
        while digits.last() == Some(&0) {
            digits.pop();
        }
        Self(digits)
    }
    fn cmp(&self, rhs: &Self) -> Ordering {
        self.0
            .len()
            .cmp(&rhs.0.len())
            .then_with(|| self.0.iter().rev().cmp(rhs.0.iter().rev()))
    }
}

fn binomial_weights(n: u32) -> (Vec<Natural>, Natural) {
    assert!((1..=483).contains(&n));
    let total = Natural::pow_small(8, n);
    let mut weight = Natural::pow_small(3, n); // C(n,k) 5^k 3^(n-k) at k=0
    let mut weights = Vec::with_capacity(n as usize + 1);
    for k in 0..=n {
        weights.push(weight.clone());
        if k < n {
            weight = weight.times(u64::from(5 * (n - k)));
            weight.divide_exact(3 * (k + 1));
        }
    }
    let mut sum = Natural::zero();
    for w in &weights {
        sum.add_in_place(w);
    }
    assert_eq!(sum, total);
    (weights, total)
}

// Return a median of K, then numerator and denominator of min_t E|K/N - t|.
fn median_deviation(n: u32) -> (u32, Natural, Natural) {
    let (weights, total) = binomial_weights(n);
    let mut cumulative = Natural::zero();
    let k_median = weights
        .iter()
        .position(|w| {
            cumulative.add_in_place(w);
            cumulative.times(2).cmp(&total) != Ordering::Less
        })
        .unwrap() as u32;
    let mut numerator = Natural::zero();
    for (k, w) in weights.iter().enumerate() {
        numerator.add_in_place(&w.times(u64::from((k as u32).abs_diff(k_median))));
    }
    (k_median, numerator, total.times(n.into()))
}

fn check_crossing(
    n: u32,
    d_num: u64,
    d_den: u64,
    median: u32,
    lower_trillionths: u64,
    before: bool,
) {
    let (k, num, den) = median_deviation(n);
    assert_eq!(k, median);
    let comparison = num.times(d_den).cmp(&den.times(d_num));
    assert_eq!(
        comparison,
        if before {
            Ordering::Greater
        } else {
            Ordering::Less
        }
    );
    const SCALE: u64 = 1_000_000_000_000;
    assert_eq!(
        num.times(SCALE).cmp(&den.times(lower_trillionths)),
        Ordering::Greater
    );
    assert_eq!(
        num.times(SCALE).cmp(&den.times(lower_trillionths + 1)),
        Ordering::Less
    );
    println!("N={n} median={k} fair-shift threshold in (0.{lower_trillionths:012}, 0.{:012}), {} {d_num}/{d_den}", lower_trillionths+1,if before { "above" } else {"below"});
}

fn run_checks() {
    for (n, z, v) in [
        (2, Fraction::new(1, 1), Fraction::new(9, 448)),
        (5, Fraction::new(4, 5), Fraction::new(20127, 1146880)),
        (8, Fraction::new(3, 4), Fraction::new(12619581, 939524096)),
    ] {
        assert_eq!(pooled_variance(n), (z, v));
        println!("N={n} floor=4/7 pooled through H={z}, sharp variance supremum {v}");
    }
    check_crossing(482, 9, 512, 301, 17_590_866_691, true);
    check_crossing(483, 9, 512, 302, 17_566_584_448, false);
    check_crossing(4, 3, 16, 3, 201_293_945_312, true);
    check_crossing(5, 3, 16, 3, 165_734_863_281, false);
    check_sharp_tv();
}

// Relocate mass eta at t=k/N to the endpoints in proportions 1-t and t.
// Let T=8^N and M=sum_j w_j |j-k|, so D=M/(N T).
// Then eta = N G/(T B), G=9NT-512M and B=1024 k(N-k).
fn check_sharp_tv() {
    const N: u32 = 483;
    let (k, m, nt) = median_deviation(N);
    assert_eq!(k, 302);
    let (weights, total) = binomial_weights(N);
    let (n, k) = (u64::from(N), u64::from(k));
    let b = 1024 * k * (n - k);
    let gap = nt.times(9).minus(&m.times(512));
    let numerator = gap.times(n);
    let denominator = total.times(b);
    // w_k/T >= eta leaves a nonnegative atom at the median.
    assert_eq!(
        weights[k as usize].times(b).cmp(&numerator),
        Ordering::Greater
    );
    let mut below = Natural::zero();
    let mut above = Natural::zero();
    for (j, w) in weights.iter().enumerate() {
        match (j as u64).cmp(&k) {
            Ordering::Less => below.add_in_place(w),
            Ordering::Greater => above.add_in_place(w),
            Ordering::Equal => {}
        }
    }
    let mut new_below = below.times(b);
    let mut new_above = above.times(b);
    new_below.add_in_place(&gap.times(n - k));
    new_above.add_in_place(&gap.times(k));
    for tail in [&new_below, &new_above] {
        assert_eq!(tail.times(2).cmp(&denominator), Ordering::Less);
    }
    const SCALE: u64 = 1_000_000_000_000_000;
    let lo = 24_626_647_717;
    let scaled = numerator.times(SCALE);
    assert_eq!(scaled.cmp(&denominator.times(lo)), Ordering::Greater);
    assert_eq!(scaled.cmp(&denominator.times(lo + 1)), Ordering::Less);
    println!("N=483 sharp TV in (0.{lo:015}, 0.{:015}); median atom supplies transfer and both resulting tails are < 1/2", lo+1);
}
fn main() {
    run_checks();
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn arithmetic_agrees_with_small_binomial_counts() {
        for n in 1..=32 {
            let total = 8_i128.pow(n);
            let mut cumulative = 0_i128;
            let mut weight = 3_i128.pow(n);
            let mut median = None;
            let mut weights = Vec::new();
            for k in 0..=n {
                cumulative += weight;
                if median.is_none() && 2 * cumulative >= total {
                    median = Some(k);
                }
                weights.push(weight);
                if k < n {
                    weight = weight * i128::from(5 * (n - k)) / i128::from(3 * (k + 1));
                }
            }
            let (k, num, den) = median_deviation(n);
            assert_eq!(Some(k), median);
            let expected: i128 = weights
                .iter()
                .enumerate()
                .map(|(i, w)| w * i128::from((i as u32).abs_diff(k)))
                .sum();
            let digits = |mut x: i128| {
                let mut ds = vec![];
                while x > 0 {
                    ds.push((x % i128::from(BASE)) as u32);
                    x /= i128::from(BASE);
                }
                Natural(ds)
            };
            assert_eq!(num, digits(expected));
            assert_eq!(den, digits(i128::from(n) * total));
        }
    }
    #[test]
    fn reproduce_witnesses_and_thresholds() {
        run_checks();
    }
}
