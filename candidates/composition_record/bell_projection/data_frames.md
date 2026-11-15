# Watching a change of preparation at a fixed camera angle

The [five-frame input](coherence.tsv) varies the real overlap $r$ between two states of an additional marker of the accepted routes. Tracing out this marker multiplies the filtered pair’s off-diagonal entry by $r$, changing it from $-1/3$ to $-r/3$ while preserving both diagonal entries. Frame $i$ uses $r=i/4$. These are separate model preparations. Frame number counts the parameter settings and carries no physical time unit. Each row supplies integer weights with total 96. Each frame contains all four measurement-setting pairs.

```sh
rustc --edition=2021 -O project.rs -o project
./project coherence.tsv --series coherence-frames 45 25
```

The last arguments are azimuth and elevation in degrees. The command writes five standalone SVGs, from `frame_000.svg` through `frame_004.svg`, to a new directory. The camera, coordinate frame, limits and physical scale are fixed across these data frames. By comparison, the [camera rotation](README.md) holds every row fixed while its viewing angle changes.

Only setting 11 moves in the ordinary data. Its two local means stay at $-1/3$ and its correlation is $(11-4r)/24$. The Bell score through the five frames is $15/8$, $23/12$, $47/24$, $2$, and $49/24$. The transition from equality to violation is visible in the full joint records even though the local marginal view remains stationary. The [terminal-position calculation](../terminal_bell_read.md) gives the physical assumptions of this comparison.

For a new sequence use the tab-separated header `frame, setting, ++, +-, -+, --` with tabs in place of commas. Frame indices start at zero without gaps. Each frame supplies the same set of setting labels, in any order. Up to 360 frames and 16 settings per frame are supported. The four nonnegative integer weights may have a different total for each row. Every total must be positive. A previous run's output directory is preserved.
