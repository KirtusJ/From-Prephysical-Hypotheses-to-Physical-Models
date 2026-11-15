# PREP for four gains on rings when B^M = 1 (Director Z, 15 November 2026)

**Status.** Proof by the director, written before any check. This closes the gap that the challenger of `PREP_REDUCTION.md` found for odd N.

## Setting and notation

The setting is that of G10's subsection "Four arc gains", on the ring ℤ_N.

- Put M = N/gcd(N,2) and B = bc/a².
- Assume B^M = 1. Then Δ_N = ⟨δ⟩.

## Lemma R_N (ring recoding)

**Statement.** Let w be a walk of length T from (0,R) on ℤ_N, ending at the vertex (x̄, rail), with ρ right steps and λ left steps. Then:

- if w ends on R, g(w) = κ(w) · g_δ(w), where κ(w) = a^(ρ−λ) (bc)^λ;
- if w ends on L, g(w) = κ(w) · bδd⁻¹ · g_δ(w).

Moreover κ(w) depends only on T and x̄.

**Proof.**
1. The factor formula is the computation of G10 Lemma 5.49. That computation uses only Lemma 5.46, which holds for each walk on the ring as on the line.
2. **κ depends only on T and x̄.** Two walks of length T to the same x̄ satisfy ρ − λ ≡ ρ' − λ' (mod N) and ρ + λ = ρ' + λ'. Hence ρ' = ρ + k and λ' = λ − k with 2k ≡ 0 (mod N), that is, M divides k.
3. Then κ(w')/κ(w) = a^(2k) (bc)^(−k) = B^(−k) = 1. ∎

Write κ_{T,x̄} for this common value.

## Proposition P_N (PREP on rings)

**Statement.** Let N/gcd(N,2) ≥ 6 and B^M = 1. Assume the ring case of G10 Lemma 5.34 for D_δ. Then, for every κ ∈ H, U ∈ M(κ⟨δ⟩) and V ∈ M(κ b d⁻¹⟨δ⟩), there are a site x̄ and a position product event S with m_S(x̄,R) = U and m_S(x̄,L) = V.

**Proof.**
1. **Empty target.** If U = V = ∅, take A_1 = ∅.
2. **Choose the coset representative.** H = ⟨a, bc, δ⟩ is finite, so there are x₀, μ₀ ≥ 0 with κ₀ = a^(x₀) (bc)^(μ₀) ∈ κ⟨δ⟩. Put x̄ = x₀ mod N.
3. **Fix the D_δ targets.** Put U' = T_{κ₀}⁻¹ U and V' = T_{κ₀bδd⁻¹}⁻¹ V. Lemma 5.34 gives an event S' in D_δ, of some length T₀, with m^δ_{S'}(x̄,R) = U' and m^δ_{S'}(x̄,L) = V'.
4. **Read off κ₁.** Since U' or V' is non-empty, some walk of S' ends at x̄. Its ρ₁ − λ₁ = x₀ + N s for some integer s, so κ_{T₀,x̄} = κ₁ = a^(x₀ + N s) (bc)^(λ₁).
5. **Two prefixes.** Each is a single walk from (0,R) back to (0,R), so in D_δ it has gain 1 and leaves the multisets of D_δ unchanged.
   - The prefix "left, then right" (A_1 = {−1}, A_2 = {0}) multiplies the four-gain ratio by bc, since λ grows by 1.
   - The prefix "N steps right" (A_s = {s mod N} for s = 1, …, N) multiplies it by a^N, since ρ grows by N. On ℤ_N with N ≥ 3 these are distinct sites, so the walk is unique.
6. **Adjust the ratio.** Use i prefixes of the second kind and j of the first, with i ≡ −s modulo the order of a^N and j ≡ μ₀ − λ₁ modulo the order of bc. Then the ratio becomes a^(x₀) (bc)^(μ₀) = κ₀.
7. **Conclude.** By Lemma R_N, m_S(x̄,R) = T_{κ₀} U' = U and m_S(x̄,L) = V. ∎

## Consequence

On rings with M ≥ 6 and B^M = 1, the conclusion of G10 Theorem 5.51(i) holds, given the ring case of Lemma 5.34: the count, and for r even one square.

When B^M ≠ 1 the question is open. A builder is attacking it.

## What would break this

- The well-definedness step in Lemma R_N: it needs 2k ≡ 0 (mod N) ⇒ M | k. For N odd, k ≡ 0 (mod N). For N even, k ≡ 0 (mod N/2) = M. ✓
- The prefix of N right steps being not unique or not closed. It returns to site N ≡ 0 on rail R. The masks {1}, …, {N−1}, {0} admit only right steps, because a left step from s lands at s − 2 ≠ s + 1 (mod N) when N ≥ 3. ✓
- Lemma 5.34 on rings, which is Director G's (M ≥ 6).
