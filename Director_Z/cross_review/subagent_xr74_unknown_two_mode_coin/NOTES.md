# NOTES xr74
CONTROL: U=[[1,i],[i,1]]/sqrt2 = exp(i pi/4 X); U^n = cos(n pi/4) I + i sin(n pi/4) X; return prob cos^2(n pi/4): n=1: 1/2, n=2: 0, n=3: 1/2, n=4: 1.
Step 1 read note+checker+result. Own derivation agrees: L_t = int q U_{t-1}(s/2)^2 + c/2; F=int q^2 + c/4; W=int q(r-a)^2 + c(1+(a-1)^2)/2; D=int (q-1/2)^2 exactly for all c. Bounds (Chebyshev, split q=1/4) follow. Alias pair feasible iff a<=2. Note names NO Lean file.
My additions: full all-clock alias family (Fourier uniqueness): c=0, nu = nu_0(q=0, any r) + nu_a(r=a), int q dnu_a = 1/2; F ranges (1/4, (1-a/4)/2]; cubic max 5/16 -> false-pass eta in [4/5,1).
Single pure coin (q,r=a) with eta=(4q-1)/(4q^2) gives W=D_obs=0 (4-setting test, no mixture needed).
Reduced score under loss: balanced coin + count c=(1-eta)/2 gives T_obs=0 (count hidden), since D_obs<0.
Step 2 checker rerun: python3 rc0, -O rc0, both outputs sha ca10ea36... == stored; rerun into same dir refuses (FileExistsError rc1). No Lean file named by note; grep of Director_G/lean finds none for it.
Step 3 own program xr74_coin.py run1 rc0; run2 rc0 (bytes compared below); overwrite refused. P1-P8,P9,P11 all pass; P9b fail 239/239, P9c fail 16/16, P10 fail 1/1 (attack predicates, kept).
Step 4 final: run2 rc0, result bytes identical to run1 (sha 10831e09...), program sha 6ceed369.... Lean: note names none; nothing formalized. Verdict: no defect in range; GAPs: loss robustness (single pure coin false pass, reduced score hides count), closing assumption list omits tick-stationarity, abstract omits complex conjugation, endpoint exact-only. No repo file needs changing.
