# p9/b1 builder: G10 Thm posprodq(i) on rings N=5,8,10 (M=4,5)
Run: cd this dir; timeout 300 python3 explore.py res_T8_W6_B2.txt 8 6 2  (exit 124: killed by timeout during N=10 q=3; file partial, 8 of 15 carriers done)
P1 (one-site reach, |U|+|V|<=2, T<=8, <=6 walks): PASS N=5 q=2, N=8 q=2; FAIL (not found in bound) N=5 q=3,4; N=8 q=3,4; N=10 q=2.
P2 (PPE consistency forces projection on |m|<=2 to expected span): PASS on all 7 qualifying carriers run.
No proof written. Outcome PARTIAL (COMPUTED only). Controls M>=6 not reached (timeout).
