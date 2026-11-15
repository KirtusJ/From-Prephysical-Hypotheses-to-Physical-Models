# A source audit of 33 Z33 theorem-register entries

Kirtus Justus, research direction. OpenAI Codex, source audit and computational checks. 15 November 2026. Z33 contains 456 inventory entries. This audit covers every entry carrying either `PROOF_NOT_ADJACENT` (24) or `CONDITIONAL_ON_NAMED_INPUTS` (9), across 14 papers. Two entries point to bibliographic references. The other 31 correspond to statements in the manuscripts. Each judgment records the argument located, its scope, and any outstanding analytic dependency. [Issued register](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PROGRAM/registers/THEOREM_REGISTRY.csv) · [All 33 judgments](judgments.md)

| Entry | What the cited page establishes |
|---|---|
| D6-05-11 | The printed line refers to Theorem 1.3 of Deift, Its and Krasovsky in bibliography item [5]. [D6, p. 38](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D6_Concentration_Spectrum_of_the_Half_Filled_Sine_Kernel_Periods_Tails_an/D6_Concentration_Spectrum_of_the_Half_Filled_Sine_Kernel_Periods_Tails_an.pdf#page=38) · [Original theorem, p. 5](https://arxiv.org/pdf/1110.4089v2#page=5) |
| F2-01-06 | The printed line points to the companion paper’s Proposition 6. That paper contains the statement and proof under F1-01-06. [F2, p. 8](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/F2_Stochastic_Recovery_from_Information_Loss_and_Equality_of_Channel_Capa/F2_Stochastic_Recovery_from_Information_Loss_and_Equality_of_Channel_Capa.pdf#page=8) · [F1, p. 7](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/F1_Abstract_Channels_and_Gaussian_Capacity/F1_Abstract_Channels_and_Gaussian_Capacity.pdf#page=7) |
| D8-03-04 | Corollary 4 proves the fixed-positive-mass two-bond expansion. The extractor matches the substring “conditional” in its title “unconditional”. The claim concerns one term of the entropy decomposition. [D8, pp. 19–20](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates/D8_Wilson_Dirac_Covariance_Majorant_and_Boundary_Estimates.pdf#page=19) |
| D3-01-01 | Theorem 1 appears on p. 2. Section 7 gives the proof by name on p. 8, beyond the next statement matched by the extractor. Its four-branch assembly still depends on the cited analytic estimates. [D3, p. 8](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/PAPERS/D3_Finite_Part_of_Wilson_Dirac_Relative_Entropy/D3_Finite_Part_of_Wilson_Dirac_Relative_Entropy.pdf#page=8) |

The classifications describe document structure. In particular, the original extractor looks for a proof marker only before the next matched heading. The audit distinguishes a verified implication under named hypotheses from an independent reconstruction of every upstream proof. [Issued extraction code](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/tools/assemble.py#L71-L94)

## Reproduce the register checks

From a Git checkout containing the Z33 commit, run the following, adjusting the script path to this directory. The default command requires Python 3.8 or later and checks all 33 IDs, issued headings, status labels and assembled-paper page links against the pinned theorem register and paper index. With PyMuPDF available, the second command also replays the issued extraction function on the original five components. The F1 entry is a positive control outside the 33. The PDF replay was verified with PyMuPDF 1.26.6.

```sh
python3 path/to/check_register.py
python3 path/to/check_register.py --replay
```

The script also accepts `--repo /path/to/checkout` or `--source-tree /path/to/Z33` for an extracted archive. It checks each input against its published Git blob ID. It reads Git objects without changing branches or modifying the issued edition. Source commit `0ca75f60c76af1be7f3c25c2ed8914e82243ff5d`. [Assembled edition](https://github.com/KirtusJ/From-Prephysical-Hypotheses-to-Physical-Models/blob/0ca75f60c76af1be7f3c25c2ed8914e82243ff5d/edition/README.md)
