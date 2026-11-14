# Micro-review brute force for G10_subsection_what_masks_read.tex. Float arithmetic; tolerance 1e-9
# (sums of <= 512 unit-modulus terms in doubles; rounding ~1e-13). Seed fixed. Nothing overwritten: prints only.
import itertools, cmath, random, math
random.seed(20261114)
def rnd(): return cmath.exp(1j*random.uniform(0,2*math.pi))
def carrier(eta=-1):
    a,b,c=rnd(),rnd(),rnd(); d=eta*b*c/a; return a,b,c,d
def run(N,word,rail,g):
    a,b,c,d=g; x=0; amp=1; sites=[]
    for s in word:
        if s=='R': amp*= a if rail=='R' else c; rail='R'; x+=1
        else: amp*= b if rail=='R' else d; rail='L'; x-=1
        sites.append(x if N is None else x%N)
    return amp,sites,rail
def red(x,N): return x if N is None else x%N
def P(N,t,masks,port,g,al,be,ret_words=False):
    x,rho=port; tot=0; ws=[]
    for w in itertools.product('RL',repeat=t):
        ok=None
        for r0,coef in (('R',al),('L',be)):
            amp,sites,rail=run(N,w,r0,g)
            if all(m is None or sites[j] in m for j,m in enumerate(masks)) and sites[-1]==red(x,N) and rail==rho:
                tot+=coef*amp; ok=True
        if ok: ws.append(''.join(w))
    p=abs(tot)**2/2**t
    return (p,ws) if ret_words else p
def M_of(N): return N//math.gcd(N,2)
def chk(name,ok,info=''): print(('PASS ' if ok else 'FAIL ')+name+' '+str(info))
tol=1e-9
# Q2/Q3: fork words and formula, N=1..9 (N=1,2 included to see if (iii) extends)
for N in range(1,10):
    M=M_of(N); s=(-1)**(M-1)
    masks=[{j%N,(-j)%N} for j in range(1,M)]+[{M%N},None]
    g=carrier(); a,b,c,d=g; u=b*c/a**2; om=u**M; gam=c/a
    al,be=rnd()*0.6,rnd()*0.8; kap=al.conjugate()*be*gam
    p,ws=P(N,M+1,masks,(M+1,'R'),g,al,be,True)
    f=(abs(al)**2*(2+2*s*om.real)+abs(be)**2*(2-2*s*om.real)+4*s*om.imag*kap.imag)/2**(M+1)
    chk(f'fork N={N} M={M} words={ws}', ws==sorted(['R'*(M+1),'L'*M+'R']) or sorted(ws)==sorted(['R'*(M+1),'L'*M+'R']), f'|P-formula|={abs(p-f):.1e}')
    chk(f'fork formula N={N}',abs(p-f)<tol)
    # (iv) and mirror
    m4=[{1%N}]+[{(1+j)%N,(1-j)%N} for j in range(1,M)]+[{(1+M)%N},None]
    p4=P(N,M+2,m4,(M+2,'R'),g,al,be); f4=(0.5+kap.real)*(2+2*s*om.real)/2**(M+1)
    m5=[{(-1)%N}]+[{(-1-j)%N,(-1+j)%N} for j in range(1,M)]+[{(-1-M)%N},None]
    p5=P(N,M+2,m5,(-M-2,'L'),g,al,be); f5=(0.5-kap.real)*(2+2*s*om.real)/2**(M+1)
    chk(f'(iv) N={N}',abs(p4-f4)<tol,f'{abs(p4-f4):.1e}'); chk(f'(iv) mirror x->-x N={N}',abs(p5-f5)<tol,f'{abs(p5-f5):.1e}')
    # (i),(ii)
    pi1=P(N,3,[None]*3,(1,'R'),g,al,be); pi2=P(N,3,[None]*3,(-1,'L'),g,al,be)
    chk(f'(i) N={N}',abs(pi1-abs(al)**2/2)<tol and abs(pi2-abs(be)**2/2)<tol,f'{pi1-abs(al)**2/2:.3f} {pi2-abs(be)**2/2:.3f}')
    q1=P(N,1,[None],(1,'R'),g,al,be); q2=P(N,1,[None],(-1,'L'),g,al,be)
    chk(f'(ii) N={N}',abs(q1-0.5-kap.real)<tol and abs(q2-0.5+kap.real)<tol)
    # short ports: all words at a port of length t<=M have the same l mod... same k
    bad=[]
    for t in range(1,M+1):
        for x in range(N):
            for rho in 'RL':
                ls={w.count('L') for w in map(''.join,itertools.product('RL',repeat=t)) if run(N,w,'R',g)[1][-1]==x and w[-1]==rho}
                if len(ls)>1: bad.append((t,x,rho,ls))
    chk(f'no port of length<=M has two k, N={N}',not bad,bad[:2])
# line: (i),(ii)
g=carrier(); a,b,c,d=g; gam=c/a; al,be=rnd()*0.6,rnd()*0.8; kap=al.conjugate()*be*gam
chk('line (i)',abs(P(None,3,[None]*3,(1,'R'),g,al,be)-abs(al)**2/2)<tol and abs(P(None,3,[None]*3,(-1,'L'),g,al,be)-abs(be)**2/2)<tol)
# Q6: port (2, 2 mod N, R), no mask, N=1,2; eta=-1 and eta arbitrary; alpha=1 and |alpha|=0.5
for N in (1,2,3,4):
    for eta in (-1,rnd()):
        g=carrier(eta); a,b,c,d=g; u=b*c/a**2
        p,ws=P(N,2,[None]*2,(2,'R'),g,1,0,True); ph=P(N,2,[None]*2,(2,'R'),g,0.5,0)
        print(f'Q6 N={N} eta={"-1" if eta==-1 else "generic"} words={ws} P-(1+Re u)/2={p-(1+u.real)/2:+.3e}  alpha=0.5: P/((1+Re u)/2)={ph/((1+u.real)/2):.3f}')
# N<=2: sum over two rails at length t, no mask, both-rail start, eta=-1 vs eta=+1
for N in (1,2):
    for eta in (-1,1):
        out=[]
        for _ in range(2):
            g=carrier(eta); al,be=rnd()*0.6,rnd()*0.8
            out.append([round(sum(P(N,t,[None]*t,(t,r),g,al,be) for r in 'RL'),6) for t in (1,2,3)])
        print(f'N={N} eta={eta} rail-summed P at t=1,2,3 for two random data (n=1):',out)
# Q3: rings (b) with M1=M2 and M=1
for M1,M2 in ((2,2),(3,3),(2,3),(2,4),(1,2),(1,1)):
    roots=lambda M:[cmath.exp(2j*math.pi*k/M) for k in range(1,M)]
    if not roots(M1) or not roots(M2): print(f'rings(b) M1={M1} M2={M2}: construction impossible (no root of unity != 1 of order dividing 1); statement false for M=1 since Re u = Re u\' forces u\' in {{u, conj u}}'); continue
    e,tau=roots(M1)[0],roots(M2)[0]; u=cmath.sqrt(tau/e); v=e*u
    chk(f'rings(b) M1={M1} M2={M2}',abs(v-u)>1e-6 and abs(v-u.conjugate())>1e-6 and abs((u**M1).real-(v**M1).real)<tol and abs((u**M2).real-(v**M2).real)<tol)
# Q4: degenerate starts in fork/(iv): alpha=0, beta=0, Re kappa=+-1/2
N=5;M=5;s=1;g=carrier();a,b,c,d=g;om=(b*c/a**2)**M;gam=c/a
for name,al,be in (('alpha=0',0,1),('beta=0',1,0),('Re kappa=+1/2',2**-.5,2**-.5/gam),('Re kappa=-1/2',2**-.5,-2**-.5/gam)):
    kap=complex(al).conjugate()*be*gam
    m4=[{1}]+[{(1+j)%N,(1-j)%N} for j in range(1,M)]+[{(1+M)%N},None]
    m5=[{(-1)%N}]+[{(-1-j)%N,(-1+j)%N} for j in range(1,M)]+[{(-1-M)%N},None]
    p4=P(N,M+2,m4,(M+2,'R'),g,al,be); p5=P(N,M+2,m5,(-M-2,'L'),g,al,be)
    print(f'Q4 {name}: (iv) P={p4:.6f} formula={(0.5+kap.real)*(2+2*s*om.real)/2**(M+1):.6f}; mirror P={p5:.6f} formula={(0.5-kap.real)*(2+2*s*om.real)/2**(M+1):.6f}')
