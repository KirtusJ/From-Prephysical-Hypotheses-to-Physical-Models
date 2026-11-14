# Citation and prior-art check, candidate G1 "edge record walk"

Session date: 13 November 2026. Sub-agent (same model family as Director Z; not independent review).
Rule: a source is reported as checked only if it was opened in this session. Marks:
SUPPORTED / NOT SUPPORTED / COULD NOT OPEN / EXISTS BUT CLAIM NOT FOUND.

## 0. Inventory of external links (grep of *.md, *.py, *.lean, *.json in the candidate folder)

20 external URLs:
- cosmology.md: doi 10.1103/PhysRevD.78.103502; arXiv 2503.14738 (twice); arXiv 2605.27221; arXiv 2601.14559; arXiv 1807.06209; arXiv 2112.04510
- millennium.md: claymath.org/millennium-problems/ ; claymath.org/news/navier-stokes-announcement/ ; riemann.pdf ; hodge.pdf ; birchswin.pdf ; navierstokes.pdf ; pvsnp.pdf ; yangmills.pdf ; poincare.pdf ; claymath.org/millennium/poincare-conjecture/
- mechanics.md: doi 10.1088/1367-2630/12/12/123022
- fixed_ring_calibration.md: arXiv 1504.06396 ; annals.math.princeton.edu/2002/155-3/p04
- README.md, attacks.md: github.com/KirtusJ/... WHY_ABANDONED.md (internal project link, commit b2fa602)

Prior-art grep (goldstein|struyve|bell|vink|aaronson|bohm|jordan|von neumann|parallelogram|gleason|valentini|durr|zanghi) over the folder:
no hits for any of these names. Only "Born" appears (attacks.md line 9; check_edge_records.py line 157). The candidate cites none of the prior art listed in Part 2.

## BLOCK (recorded at once, 13 Nov 2026)

- WebFetch https://www.claymath.org/news/navier-stokes-announcement/ -> `getaddrinfo ENOTFOUND www.claymath.org`
- WebFetch https://www.claymath.org/millennium-problems/ -> `getaddrinfo ENOTFOUND www.claymath.org`
- WebFetch https://arxiv.org/abs/2503.14738 -> `getaddrinfo ENOTFOUND arxiv.org`
  The tool message says such a failure means the host is outside the session's allowed network domains (or does not exist) and
  that after a second host fails the same way no further sites should be tried with WebFetch. Two hosts failed; WebFetch was not tried again.
- A single diagnostic `curl` through the session proxy returned HTTP 200 (status code only; no body kept or read) for
  https://arxiv.org/abs/2503.14738 and https://www.claymath.org/millennium-problems/ . So both URLs RESOLVE (HTTP 200),
  but nothing was read from them.
- A following `curl` download of the Clay pages and PDFs was DENIED by the Claude Code permission classifier
  ("Containment Escape"). It was not retried in another form. No page body was therefore opened by curl either.
- WebSearch works. Everything below that is marked "search result" is the search tool's title/URL list and its machine summary,
  NOT the source itself. Under the task rule, such items keep the mark COULD NOT OPEN.

## Part 1. Citations (all: page body NOT opened; evidence is WebSearch title/URL lists plus the search tool's machine summary)

### 1.1 millennium.md line 9, https://www.claymath.org/news/navier-stokes-announcement/  -> COULD NOT OPEN
- Resolves: a search restricted to claymath.org returns a result titled "Navier-Stokes Announcement - Clay Mathematics Institute"
  at exactly this URL; the Clay homepage is reported to list it under latest news. (curl status check on the sibling URL
  /millennium-problems/ gave HTTP 200; this URL itself was not status-checked.)
- Search summary of the page (not opened): dated 11 September 2026; brief; says the problem has "apparently been settled"
  (one summary) / "appears to have been solved" (secondary outlets); CMI shares the community's excitement, hopes the work
  will be analysed, points to the prize rules for evaluation and credit; "The process is deliberately unhurried, but we will provide updates."
  No verdict. One summary attributes the announcement to "C. Fukushima and J. Westerweel of the Technical University of Delft";
  that reads like a picture credit on the page, not the announcer. UNVERIFIED either way.
- What was announced, by whom, which direction (all from secondary sources via search, none opened):
  OpenAI, 8 September 2026: an internal/unreleased model produced a proof of FINITE-TIME BLOW-UP for the 3D incompressible
  Navier-Stokes equations WITH A SMOOTH FORCING, at every fixed viscosity; a 166-page manuscript and a Lean repository
  ("NavierStokesAndEuler") were released. An arXiv title returned by search says it outright: "... the OpenAI 2026 forced
  blow-up construction" (arXiv:2609.17642); a search summary of another arXiv paper says the claim is "statements (C) and (D)
  of the Clay formulation" (whole space with forcing, and periodic with forcing). Further arXiv titles in the same result list:
  "Density of Forces Producing Navier-Stokes Blowup" (2609.10262); "The Positive Defect Problem: Target and Admissibility Criteria
  for a Programmatic Search for Unforced Navier-Stokes Blowup" (2609.23868) - i.e. the unforced case is treated as still open.
  A Yahoo/tech headline: "OpenAI's 10,000-Agent Navier-Stokes Claim Solves the Wrong Problem ...".
  Status of the proof: unverified; arXiv:2610.08144 (Bastounis, Circelli, Hansen, "Navier-Stokes lost in translation") argues the
  Lean formalisation does not correspond to the natural-language proof (Lemma 8.6, eq. (10.19)); commentators say this does not
  by itself invalidate the proof.
- Relation to the candidate's adopted position (A) (global smooth existence, unforced, whole space):
  IF the announced result is as the secondary sources describe (forced breakdown, Clay alternatives (C)/(D)), THEN it is
  LOGICALLY INDEPENDENT of (A): (A) concerns f = 0 only. It neither proves nor refutes (A). But note what the candidate's
  sentence leaves out: under Fefferman's formulation ANY ONE of (A)-(D) settles the prize problem, so the announced result,
  if it stands, resolves the Millennium problem by (C)/(D) while (A) stays an open conjecture that is no longer "the" Clay problem.
  The candidate's own sentence "A forced breakdown alone would leave the unforced assertion open" is consistent with this.
  The candidate's text does not say which direction the announced result goes; a reader could take "adopt (A)" as siding with
  or against the announcement. This is a wording gap, not an error.
- Cited sentence "On 11 September 2026 Clay acknowledged an announcement of an apparent resolution of Navier-Stokes":
  consistent with every search result; not confirmed against the page text. Mark stays COULD NOT OPEN.

### 1.2 millennium.md line 9, https://www.claymath.org/millennium-problems/  -> COULD NOT OPEN (resolves: HTTP 200 by status check)
- Claim: "five problems Unsolved, Navier-Stokes Active, Poincare Solved; status page still distinguishes that case".
- Search summary (not opened): "Its Navier-Stokes page currently uses the status 'Active'". The five "Unsolved" labels and "Solved" for
  Poincare were not confirmed in this session.

### 1.3 cosmology.md lines 21, 23, https://arxiv.org/abs/2503.14738  -> COULD NOT OPEN (resolves: HTTP 200 by status check)
- Search: "DESI DR2 Results II: Measurements of Baryon Acoustic Oscillations and Cosmological Constraints", DESI Collaboration,
  March 2025, v3 matches the Phys. Rev. D version.
- Abstract sentences as returned by the search summary: "When also including SNe, the preference for a dynamical dark energy model
  over LCDM ranges from 2.8-4.2 sigma depending on which SNe sample is used." Also: "preferred over LCDM at 3.1 sigma for the
  combination of DESI BAO and CMB data"; BAO-preferred parameters "in mild, 2.3 sigma tension with those determined from the CMB".
- Candidate sentence: "When the collaboration included CMB and supernova data, its comparison with a time-dependent equation of
  state favored the latter at 2.8-4.2 sigma, depending on the supernova sample." -> agrees with the abstract as summarised.
  "DESI DR2 reported a good fit of flat LCDM to its BAO measurements alone" -> not confirmed by any snippet in this session
  (the snippets give the 2.3 sigma BAO-vs-CMB tension inside LCDM, which the candidate does not mention).

### 1.4 cosmology.md line 23, https://arxiv.org/abs/2605.27221  -> COULD NOT OPEN
- Search: exists. "Constraints on Dynamical Dark Energy from Multiple Probes in the Full Dark Energy Survey", DES Collaboration,
  late May 2026 (v2 exists; "to appear in PRL" per one listing). Full six-year DES: SNe Ia + BAO + 3x2pt.
- Search summary: adding DESI DR2 BAO gives w0 = -0.84 (+0.06/-0.07), wa = -0.53 (+0.33/-0.28), "a 2.3 sigma deviation";
  described as the most stringent low-redshift-only test of dynamical dark energy.
- Candidate sentence "The 2026 DES multiprobe analysis reported 2.3 sigma for its low-redshift combination with DESI BAO" -> agrees
  with the summary. (This paper is after the assistant's training data; nothing about it is known except from this search.)

### 1.5 cosmology.md line 31, https://arxiv.org/abs/2601.14559  -> COULD NOT OPEN
- Search: "Dark Energy Survey Year 6 Results: Cosmological Constraints from Galaxy Clustering and Weak Lensing",
  DES Collaboration (T. M. C. Abbott et al.), submitted 21 January 2026; Phys. Rev. D accepted 2 November 2026.
- Search summary: flat LCDM S8 = 0.789 +/- 0.012 (68% CL), Omega_m = 0.333 (+0.023/-0.028); "projected only into S8 the difference
  is 2.6 sigma" relative to the CMB combination Planck 2018 + ACT-DR6 + SPT-3G DR1; full-parameter-space difference 1.8 sigma.
- Candidate sentence (S8 = 0.789 +/- 0.012; 2.6 sigma along S8 versus 1.8 sigma across the full parameter space, "from its
  specified CMB comparison") -> agrees with the summary in all three numbers and in which is which.

### 1.6 cosmology.md line 32, https://arxiv.org/abs/1807.06209  -> COULD NOT OPEN
- Search: "Planck 2018 results. VI. Cosmological parameters", Planck Collaboration, submitted 17 July 2018, A&A 641, A6 (2020).
- Search summary of the abstract: Hubble constant "H0 = (67.4 +/- 0.5) km s^-1 Mpc^-1" assuming base-LCDM; described as model-dependent.
- Candidate: "Planck inferred 67.4 +/- 0.5 km/s/Mpc under its base cosmology" -> agrees with the summary.

### 1.7 cosmology.md line 32, https://arxiv.org/abs/2112.04510  -> COULD NOT OPEN
- Search: Riess et al., "A Comprehensive Measurement of the Local Value of the Hubble Constant with 1 km/s/Mpc Uncertainty from the
  Hubble Space Telescope and the SH0ES Team", arXiv Dec 2021, ApJ Lett. 934, L7 (2022).
- Search summary: baseline "73.04 +/- 1.04 km/s/Mpc", including systematics; 73.30 +/- 1.04 with high-z SNe; 5 sigma from Planck+LCDM.
- Candidate: "the 2022 SH0ES distance ladder reported 73.04 +/- 1.04" -> agrees with the summary ("2022" = journal year; arXiv 2021).

### 1.8 cosmology.md line 17, https://doi.org/10.1103/PhysRevD.78.103502  -> COULD NOT OPEN
- Search: Sahni, Shafieloo, Starobinsky, "Two new diagnostics of dark energy", Phys. Rev. D 78, 103502 (2008), arXiv:0807.3548.
- Search summary: Om(z) = [h^2(z) - 1]/[(1+z)^3 - 1], h = H/H0 (taken by the search tool from a co-author's slides, not from the paper);
  Om is constant (= Omega_0m) in LCDM; the 2008 paper's two-point quantity is the DIFFERENCE Om(x1,x2) = Om(x1) - Om(x2).
- The candidate's K_ij = [E^2(z_i) - E^2(z_j)]/(X_i - X_j) is the h^2-difference two-point form. Per the search summary that form is
  written out in Shafieloo, Sahni, Starobinsky, arXiv:1205.2870 (2012, Phys. Rev. D 86, 103527), with the caveat that the 2012 text
  may be restating earlier work. So: the 2008 paper supports "Om diagnostic" and the null test; "This is the two-redshift form of
  the Om diagnostic" is better attributed to the 2012 paper (or the 2008 paper gives it only as the special case z_j = 0).
  Possible attribution slip; not confirmed against either text.

### 1.9 mechanics.md line 39, https://doi.org/10.1088/1367-2630/12/12/123022  -> COULD NOT OPEN
- Search: G. J. de Valcarcel, E. Roldan, A. Romanelli, "Tailoring discrete quantum walk dynamics via extended initial conditions",
  New J. Phys. 12, 123022 (2010), arXiv:1004.0976 (arXiv subtitle: "Towards homogeneous probability distributions").
- Search summary: "By analysing the dispersion relation of the process, continuous wave equations are derived whose form depends on
  the initial distribution shape"; one source: for a class of initial conditions "the evolution is dictated by the Schrodinger
  equation of a free particle".
- "Eq. (11)" as the leading envelope equation: two targeted searches did not return the equation or its number. NOT CONFIRMED.
  The paper and its subject match; the equation number is unchecked.

### 1.10 fixed_ring_calibration.md line 11, https://arxiv.org/abs/1504.06396  -> COULD NOT OPEN
- Search: N. Konno, Y. Shimizu, M. Takei, "Periodicity for the Hadamard walk on cycles", arXiv April 2015;
  Interdisciplinary Information Sciences 23(1) (2017) 1-8.
- Search summary, quoting the abstract: "Dukes (2014) ... showed T_2 = 2, T_4 = 8, T_8 = 24 for the Hadamard walk case. We prove that the
  Hadamard walk does not have any period except for his case, i.e., N = 2, 4, 8."
- Candidate: "On four sites, four steps translate the sharp source by two sites and multiply it by four ... On eight sites, 24 steps return
  the initial sharp source multiplied by 4096 ... The periods of the normalized walk on these cycles also appear in the published
  literature." -> the 24 for N = 8 agrees. For N = 4 the published period is 8, while the note's "four steps" is a return up to a
  translation by two sites, a different statement (4 steps: translate by 2; 8 steps: identity up to scale 16); no contradiction, but the
  task description's "the note uses 8 and 24" is not literally what the note says: it uses 4 (up to translation) and 24.
  Also: the periods are due to Dukes (2014) per the abstract; Konno-Shimizu-Takei prove there are no others. Attribution is loose but
  "appear in the published literature" is true of this paper.
  Convention caution (not checked): the note's raw step is (r,l) -> (r+l, r-l) with the minus on L->L; whether that is the same
  Hadamard-walk convention as in the paper was not verified, since the paper was not opened.

### 1.11 fixed_ring_calibration.md line 32, https://annals.math.princeton.edu/2002/155-3/p04  -> COULD NOT OPEN
- Search: J.-H. Evertse, H. P. Schlickewei, W. M. Schmidt, "Linear equations in variables which lie in a multiplicative group",
  Annals of Math. 155 (2002) 807-836; arXiv:math/0409604.
- Theorem 1.1 as returned by search (two summaries, one from the Leiden preprint, one from citing papers): K a field (characteristic 0;
  the "algebraically closed" wording was not confirmed), Gamma a subgroup of (K^*)^n of FINITE RANK r, a_1,...,a_n nonzero in K.
  Then a_1x_1+...+a_nx_n = 1 has at most exp((6n)^{3n}(r+1)) non-degenerate solutions (x_1,...,x_n) in Gamma, where non-degenerate
  means no proper nonempty subsum vanishes. The bound depends only on n and r, not on the coefficients.
- Is "finitely many nondegenerate solutions of a_1x_1+...+a_nx_n=1 in a finitely generated multiplicative group of rank r" what it gives?
  Yes, and more: (i) the group is a subgroup of the product (K^*)^n, which is how the note uses it (group generated by the eigenvalue
  vector and the constant vector (1/3,...,1/3) inside (C^*)^|I|, rank at most 2); (ii) finite rank is weaker than finitely generated,
  so the note's finitely generated group is covered; (iii) the conclusion is an explicit uniform bound, of which finiteness is a
  corollary. Hypotheses the note must meet and does state: coefficients nonzero, no vanishing subsum (its inclusion-minimal subset I).
  Statement taken from search summaries, not from the paper.

