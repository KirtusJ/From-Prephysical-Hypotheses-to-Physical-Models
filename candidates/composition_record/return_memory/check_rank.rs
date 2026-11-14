//! Check a four-state lower bound directly from the seven earliest arrival bins.
//! All classification decisions use integer determinants and cofactors.
use std::{
    env,
    error::Error,
    fs,
    io::{self, Write},
};

const N: i128 = 40_000;
const WIDTH: usize = 4;
const EPS_NUM: i128 = 1_131;
const EPS_DEN: i128 = 100_000;

fn minor(matrix: &[Vec<i128>], row: usize, col: usize) -> Vec<Vec<i128>> {
    matrix
        .iter()
        .enumerate()
        .filter(|(i, _)| *i != row)
        .map(|(_, values)| {
            values
                .iter()
                .enumerate()
                .filter(|(j, _)| *j != col)
                .map(|(_, &v)| v)
                .collect()
        })
        .collect()
}

fn det(matrix: &[Vec<i128>]) -> i128 {
    if matrix.len() == 1 {
        return matrix[0][0];
    }
    matrix[0]
        .iter()
        .enumerate()
        .map(|(j, &v)| {
            let term = v * det(&minor(matrix, 0, j));
            if j % 2 == 0 {
                term
            } else {
                -term
            }
        })
        .sum()
}

fn main() -> Result<(), Box<dyn Error>> {
    let path = env::args_os()
        .nth(1)
        .ok_or("provide the published first_returns.csv")?;
    let data = fs::read_to_string(path)?;
    let mut lines = data.lines();
    let header: Vec<_> = lines.next().ok_or("missing header")?.split(',').collect();
    let columns: Vec<_> = (1..=7)
        .map(|i| {
            let name = format!("hit_{i:02}");
            header
                .iter()
                .position(|c| *c == name)
                .ok_or("missing arrival column")
        })
        .collect::<Result<_, _>>()?;
    let index = |name| {
        header
            .iter()
            .position(|v| *v == name)
            .ok_or("missing job metadata")
    };
    let (job, shots) = (index("job_id")?, index("shots")?);
    let mut out = io::BufWriter::new(io::stdout().lock());
    writeln!(
        out,
        "grid_index,job_id,abs_det_counts,max_adjugate_row_sum,rank4_certified"
    )?;
    let mut jobs = 0;
    for line in lines {
        let row: Vec<_> = line.split(',').collect();
        if row.len() != header.len() || row[shots].parse::<i128>()? != N {
            return Err("invalid job row".into());
        }
        let hits: Vec<_> = columns
            .iter()
            .map(|&k| row[k].parse::<i128>())
            .collect::<Result<_, _>>()?;
        if hits.iter().any(|&v| v < 0) || hits.iter().sum::<i128>() > N {
            return Err("invalid first arrivals".into());
        }
        let matrix: Vec<Vec<_>> = (0..WIDTH)
            .map(|i| (0..WIDTH).map(|j| hits[i + j]).collect())
            .collect();
        let determinant = det(&matrix).abs();
        let max_cofactor_sum = (0..WIDTH)
            .map(|j| {
                (0..WIDTH)
                    .map(|i| det(&minor(&matrix, i, j)).abs())
                    .sum::<i128>()
            })
            .max()
            .unwrap();
        let certified = determinant * EPS_DEN > (WIDTH as i128) * EPS_NUM * N * max_cofactor_sum;
        jobs += 1;
        writeln!(
            out,
            "{jobs},{},{determinant},{max_cofactor_sum},{certified}",
            row[job]
        )?;
    }
    if jobs != 99 {
        return Err("expected 99 gate settings".into());
    }
    out.flush()?;
    Ok(())
}
