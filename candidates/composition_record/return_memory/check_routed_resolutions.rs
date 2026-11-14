//! Five real Hadamard ticks followed by permutations of 18 output modes.
//! Cells are ordered (site 0 R, site 0 L, site 1 R, ...).
const CELLS: usize = 18;
const TARGET: usize = 8;
type Counts = [usize; CELLS];

const LIGHT: [usize; 4] = [7, 9, 10, 12];
const MEDIUM: [usize; 3] = [3, 13, 17];
const HEAVY: usize = 6;

fn source() -> Counts {
    let mut state = [[0i32; 2]; 9];
    state[0][0] = 1;
    for _ in 0..5 {
        let mut next = [[0; 2]; 9];
        for (x, &[r, l]) in state.iter().enumerate() {
            next[(x + 1) % 9][0] = r + l;
            next[(x + 8) % 9][1] = r - l;
        }
        state = next;
    }
    let weights = std::array::from_fn(|i| state[i / 2][i % 2].pow(2) as usize);
    assert_eq!(
        weights,
        [0, 0, 0, 4, 0, 0, 16, 1, 0, 1, 1, 0, 1, 4, 0, 0, 0, 4]
    );
    weights
}

// base labels and destinations, one entry per occupied input. Map the ten
// dark labels, in order, to the ten remaining output modes.
fn permute(input: &Counts, occupied_routes: &[(usize, usize)]) -> Counts {
    let mut perm = [None; CELLS];
    let mut used = [false; CELLS];
    for &(i, o) in occupied_routes {
        assert!(input[i] > 0 && perm[i].is_none() && !used[o]);
        perm[i] = Some(o);
        used[o] = true;
    }
    let mut free = (0..CELLS).filter(|&o| !used[o]);
    let mut board = [0; CELLS];
    for i in 0..CELLS {
        let o = perm[i].unwrap_or_else(|| {
            assert_eq!(input[i], 0);
            free.next().unwrap()
        });
        board[o] = input[i];
    }
    assert!(free.next().is_none());
    assert_eq!(board.iter().sum::<usize>(), 32);
    board
}

fn spectator(input: &Counts, joined: usize) -> Counts {
    let mut routes = vec![(HEAVY, 0), (MEDIUM[0], 2), (MEDIUM[1], 4), (MEDIUM[2], 6)];
    for pair in 0..2 {
        let first = TARGET + pair * 4;
        routes.push((LIGHT[2 * pair], first));
        routes.push((
            LIGHT[2 * pair + 1],
            first + if pair < joined { 1 } else { 2 },
        ));
    }
    permute(input, &routes)
}

fn subset(input: &Counts, selected: &[usize]) -> Counts {
    let mut inside = 0;
    let mut outside = TARGET;
    let mut routes = Vec::new();
    for (i, &w) in input.iter().enumerate() {
        if w == 0 {
            continue;
        }
        if selected.contains(&i) {
            assert!(inside < TARGET);
            routes.push((i, inside));
            inside += 1;
        } else {
            assert!(outside < CELLS);
            routes.push((i, outside));
            outside += 1;
        }
    }
    assert_eq!(inside, selected.len());
    permute(input, &routes)
}

fn occupied(values: impl Iterator<Item = usize>) -> Vec<usize> {
    let mut v: Vec<_> = values.filter(|&w| w > 0).collect();
    v.sort_unstable();
    v
}

fn input_classes(input: &Counts, name: &str, selected: &[usize], target: &[usize]) {
    let output = subset(input, selected);
    let rails = occupied(output[..TARGET].iter().copied());
    assert_eq!(rails, target);
    assert_eq!(occupied(output.into_iter()), [1, 1, 1, 1, 4, 4, 4, 16]);
    let sites_in = occupied(output[..TARGET].chunks_exact(2).map(|v| v[0] + v[1]));
    let sites_out = occupied(output[TARGET..].chunks_exact(2).map(|v| v[0] + v[1]));
    let (expect_in, expect_out): (&[usize], &[usize]) = match name {
        "A" => (&[2, 2], &[8, 20]),
        "B" => (&[4], &[2, 4, 5, 17]),
        "C" => (&[16], &[2, 4, 5, 5]),
        "D" => (&[2, 4, 5, 5], &[16]),
        "E" => (&[8], &[2, 5, 17]),
        "F" => (&[4, 20], &[2, 2, 4]),
        "O" => (&[], &[2, 2, 8, 20]),
        _ => unreachable!(),
    };
    assert_eq!(sites_in, expect_in);
    assert_eq!(sites_out, expect_out);
    println!("{name}: target rails {rails:?}, site weights in/out {sites_in:?} / {sites_out:?}");
}

fn main() {
    let w = source();
    for (j, expected) in [vec![1, 1, 1, 1], vec![1, 1, 2], vec![2, 2]]
        .into_iter()
        .enumerate()
    {
        let out = spectator(&w, j);
        assert_eq!(occupied(out[..TARGET].iter().copied()), [4, 4, 4, 16]);
        assert_eq!(
            occupied(out[..TARGET].chunks_exact(2).map(|c| c[0] + c[1])),
            [4, 4, 4, 16]
        );
        assert_eq!(
            occupied(out[TARGET..].chunks_exact(2).map(|c| c[0] + c[1])),
            expected
        );
        assert_eq!(occupied(out[TARGET..].iter().copied()), [1, 1, 1, 1]);
        println!("{j} joined: target sites [4,4,4,16], outside sites {expected:?}");
    }
    input_classes(&w, "A", &LIGHT, &[1, 1, 1, 1]);
    input_classes(&w, "B", &[MEDIUM[0]], &[4]);
    input_classes(&w, "C", &[HEAVY], &[16]);
    input_classes(
        &w,
        "D",
        &[
            LIGHT[0], LIGHT[1], LIGHT[2], LIGHT[3], MEDIUM[0], MEDIUM[1], MEDIUM[2],
        ],
        &[1, 1, 1, 1, 4, 4, 4],
    );
    input_classes(&w, "E", &[MEDIUM[0], MEDIUM[1]], &[4, 4]);
    input_classes(&w, "F", &[HEAVY, MEDIUM[0], MEDIUM[1]], &[4, 4, 16]);
    input_classes(&w, "O", &[], &[]);

    // Denominator-cleared polynomial identity for the site gap. Both
    // sides have degree <=2 in z and <=3 in k. The finite grid contains
    // more distinct integer points than either degree.
    for z in 1..=4i64 {
        for k in 1..=5i64 {
            let den0 = k + 4;
            let den1 = k + 2 + z;
            let den2 = k + 2 * z;
            let gap_num = k * (den1 * den2 - 2 * den0 * den2 + den0 * den1);
            assert_eq!(gap_num, 2 * k * (z - 2).pow(2));
        }
    }
    for u in 1..=4i64 {
        // Both rail numerators are quadratic in u.
        assert_eq!(5 * (4 - u) + u * u - (4 + 3 * u), (u - 4).pow(2));
    }
}
