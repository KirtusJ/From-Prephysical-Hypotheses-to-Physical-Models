"""CONTROL (known answer), written before the first run.
From the note's definitions only: words from (0,R); right step -> (x+1,R), left -> (x-1,L);
arc gains RR=a, RL=b, LR=c, LL=d (incoming rail, outgoing rail); carrier a=c=1, b=g, d=z g in C2 x Cq;
position masks retain whole wells per tick; port law 2^-t |sum_w chi(G(w))|^2; fair count = #words / 2^t.
Predicates:
 C1: N=7,q=3, fork masks ({+j,-j} for 1<=j<7, {0} at tick 7, {1} at tick 8), port (1,R):
     chi(g)=1 -> 1/64 ; chi(g)=w -> 1/256 ; fair count 1/128.
 C2: reference masks {j mod 7}: 1/256, 1/256, 1/256.
 C3 (review's numbers): N=9: 1/256 and 1/256 ; N=8: 0 and 3/32 ; C2xC4, chi(g)=i, N=7: 1/128.
Exact arithmetic: gains as (i mod 2, j mod q); |sum|^2 as integer autocorrelation reduced with 1+w+w^2=0 or i^2=-1.
"""
import itertools, json, sys
from fractions import Fraction
def words_at(N,t,masks,q):
    a=(0,0);b=(0,1);c=(0,0);d=(1,1)
    arc={('R','R'):a,('R','L'):b,('L','R'):c,('L','L'):d}
    out={}
    for w in itertools.product('RL',repeat=t):
        x=0;rail='R';g=(0,0);ok=True
        for j,s in enumerate(w,1):
            ga=arc[(rail,s)]; g=((g[0]+ga[0])%2,(g[1]+ga[1])%q)
            x=(x+1)%N if s=='R' else (x-1)%N; rail=s
            if x not in masks[j-1]: ok=False;break
        if ok: out.setdefault((x,rail),[]).append((''.join(w),g))
    return out
def prob(gs,q,r,t):
    # chi(z)=-1, chi(g)=zeta_q^r ; exact for q=3 (w) and q=4 (i)
    v=[0]*q
    for (i,j) in gs: v[(r*j)%q]+= (-1)**i
    A=[sum(v[j]*v[(j+k)%q] for j in range(q)) for k in range(q)]  # |s|^2=sum_k A_k zeta^k
    if q==3: assert A[1]==A[2]; val=A[0]-A[1]          # w+w^2=-1
    elif q==4: assert A[1]==A[3]; val=A[0]-A[2]        # i+i^3=0, i^2=-1
    return Fraction(val,2**t)
def fork(N):
    D=N//2 if N%2==0 else N
    return D,[{j%N,(-j)%N} for j in range(1,D)]+[{D%N},{(D+1)%N}]
res={}
D,m=fork(7); P=words_at(7,8,m,3); assert list(P)==[(1,'R')]
ws=P[(1,'R')]; gs=[g for _,g in ws]
res['C1']={'words':ws,'chi0':str(prob(gs,3,0,8)),'chi1':str(prob(gs,3,1,8)),'fair':str(Fraction(len(ws),256))}
P=words_at(7,8,[{j%7} for j in range(1,9)],3); gs=[g for _,g in P[(1,'R')]]
res['C2']={'chi0':str(prob(gs,3,0,8)),'chi1':str(prob(gs,3,1,8)),'fair':str(Fraction(len(gs),256))}
D,m=fork(9); P=words_at(9,10,m,3); (port,ws),=P.items(); gs=[g for _,g in ws]
res['C3_N9']={'port':port,'chi0':str(prob(gs,3,0,10)),'chi1':str(prob(gs,3,1,10))}
D,m=fork(8); P=words_at(8,5,m,3); (port,ws),=P.items(); gs=[g for _,g in ws]
res['C3_N8']={'port':port,'chi0':str(prob(gs,3,0,5)),'chi1':str(prob(gs,3,1,5))}
D,m=fork(7); P=words_at(7,8,m,4); gs=[g for _,g in P[(1,'R')]]
res['C3_C2xC4']={'chi_i':str(prob(gs,4,1,8)),'fair':str(Fraction(len(gs),256))}
ok=(res['C1']['chi0'],res['C1']['chi1'],res['C1']['fair'])==('1/64','1/256','1/128') and \
   set(res['C2'].values())=={'1/256'} and res['C3_N9']['chi0']==res['C3_N9']['chi1']=='1/256' and \
   (res['C3_N8']['chi0'],res['C3_N8']['chi1'])==('0','3/32') and res['C3_C2xC4']['chi_i']=='1/128'
res['all_control_predicates_met']=ok
with open('control_result.json','x') as f: json.dump(res,f,indent=1)
print(json.dumps(res,indent=1))
