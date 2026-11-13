# P1b (follow-up to failed P1 sub-predicate, which used sympy simplify on exp roots): two-input and three-input instances for Phi=Re(c a^3), d=q=3 Fourier, on Eisenstein integers, numeric with tolerance 1e-6 on integers-of-size<=6 (values < 1e4, float error ~1e-10).
import cmath, itertools
w=cmath.exp(2j*cmath.pi/3)
E=[x+y*w for x in range(-3,4) for y in range(-3,4)]
for c in (1,1j,0.3+0.7j):
    F=lambda a:(c*a**3).real
    two=True;three_fail=0;tot=0
    for a in E:
        for b in E:
            for (y,y2) in ((0,1),(0,2),(1,2)):
                be=[0,0,0];be[y]=a;be[y2]=b
                if abs(sum(F(sum(w**(z*t)*be[t] for t in range(3))) for z in range(3))-3*sum(F(x) for x in be))>1e-6:two=False
    for a,b,g in itertools.product(E[::5],repeat=3):
        tot+=1
        be=[a,b,g]
        if abs(sum(F(sum(w**(z*t)*be[t] for t in range(3))) for z in range(3))-3*sum(F(x) for x in be))>1e-6:three_fail+=1
    inv=all(abs(F(w*a)-F(a))<1e-6 for a in E)
    print(c,'two-input all hold:',two,'three-input failures:',three_fail,'of',tot,'invariant:',inv)
# d=4 Fourier block q=4: does Re(a^4) satisfy all two-input instances? (tests scope of "false for d>=3")
F=lambda a:(a**4).real
G=[complex(x,y) for x in range(-3,4) for y in range(-3,4)]
bad=0
for a in G:
    for b in G:
        for y,y2 in itertools.combinations(range(4),2):
            be=[0]*4;be[y]=a;be[y2]=b
            if abs(sum(F(sum((1j)**(z*t)*be[t] for t in range(4))) for z in range(4))-4*sum(F(x) for x in be))>1e-6:bad+=1
print('d=q=4 Fourier, Re(a^4), two-input violations:',bad)
