//! std-only exact checks for detector_marks.md; signed amplitudes omit sqrt(8).
type Flight = [[i32; 2]; 8];

#[derive(Clone, Copy)]
enum Coin { H, I, X }

fn tick(input: Flight, coin: impl Fn(usize) -> Coin) -> Flight {
    let mut output = [[0; 2]; 8];
    for (x, [r, l]) in input.into_iter().enumerate() {
        let (right, left) = match coin(x) {
            Coin::H => (r + l, r - l),
            Coin::I => (r, l),
            Coin::X => (l, r),
        };
        output[(x + 1) % 8][0] = right;
        output[(x + 7) % 8][1] = left;
    }
    output
}

fn walk_cells() {
    let mut state = [[0; 2]; 8];
    state[0][0] = 1;
    for _ in 0..3 { state = tick(state, |_| Coin::H); }
    assert_eq!([state[5], state[7], state[1], state[3]], [[0,1],[-1,0],[2,1],[1,0]]);
    let mut heavy = [[0; 2]; 8];
    heavy[1] = state[1];
    let mut minor = state;
    minor[1] = [0, 0];
    for split in [false, true] {
        let terminal = [heavy, minor].map(|tag| {
            let after_four = tick(tag, |_| Coin::I);
            tick(after_four, |x| if split && x == 2 { Coin::I } else { Coin::X })
                .map(|[r,l]| r*r + l*l)
        });
        let mut expected_heavy = [0; 8];
        expected_heavy[1] = if split { 1 } else { 5 };
        expected_heavy[3] = if split { 4 } else { 0 };
        assert_eq!(terminal, [expected_heavy,[0,0,0,1,0,1,0,1]]);
    }
}

fn choose(n: usize, k: usize) -> i128 {
    (1..=k).fold(1, |c, i| c * (n - i + 1) as i128 / i as i128)
}

// Denominator base^n is common to every mode and count.
fn likelihood(n: usize, k: usize, j: i128, base: i128) -> i128 {
    choose(n,k) * j.pow(k as u32) * (base - j).pow((n-k) as u32)
}

fn finite_difference() {
    for n in 0..=12 {
        let d = n + 1;
        let signed: Vec<_> = (0..=d).map(|j| {
            let c = choose(d, j);
            if j % 2 == 0 { c } else { -c }
        }).collect();
        for length in 0..=n {
            for k in 0..=length {
                let sum: i128 = signed.iter().enumerate()
                    .map(|(j,g)| g * likelihood(length,k,j as i128,d as i128)).sum();
                assert_eq!(sum, 0);
            }
        }
        let extra: i128 = signed.iter().enumerate().map(|(j,g)| g * (j as i128).pow(d as u32)).sum();
        let factorial: i128 = (1..=d as i128).product();
        assert_eq!(extra, if d % 2 == 0 { factorial } else { -factorial });
    }
}

fn example_marks() {
    let nodes = [0,1,3]; // denominator 3
    let g = [2,-3,1];
    for n in 0..=2 {
        let mut counts = Vec::new();
        let mut signed = Vec::new();
        for k in 0..=n {
            let row = nodes.map(|j| likelihood(n,k,j,3));
            counts.push(row.iter().sum::<i128>());
            signed.push(row.iter().zip(g).map(|(l,z)| l*z).sum::<i128>());
        }
        assert_eq!(counts.iter().sum::<i128>(), 3 * 3i128.pow(n as u32));
        match n {
            0 => { assert_eq!(counts,[3]); assert_eq!(signed,[0]); }
            1 => { assert_eq!(counts,[5,4]); assert_eq!(signed,[0,0]); }
            2 => { assert_eq!(counts,[13,4,10]); assert_eq!(signed,[6,-12,6]); }
            _ => unreachable!(),
        }
    }
    // Inverse for unconditional gap-by-count and equal mode probabilities.
    let joint_numerators = [[9,4,0], [0,4,0], [0,1,9]];
    let recovery = [[12,-12,0], [0,27,0], [0,-3,12]];
    for i in 0..3 {
        for j in 0..3 {
            let value: i32 = (0..3).map(|k| recovery[i][k]*joint_numerators[k][j]).sum();
            assert_eq!(value, if i == j {108} else {0});
        }
    }
}

fn main() {
    walk_cells();
    example_marks();
    finite_difference();
    println!("Verified both eight-well settings, every count stratum for the example, the exact inverse, and sharp annihilators for 0 through 12 marks.");
}
