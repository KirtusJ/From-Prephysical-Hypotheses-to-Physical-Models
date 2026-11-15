"""When are the 12-tick scalar walk's rail channels entanglement breaking?

Run python -I -O check_position_memory.py. Exact integers, no external
libraries. x=0,2,...,14 are physical sites. The channel is from an arbitrary
input rail at site 0 to the terminal rail. All block boundaries were written,
the ideal position instrument retained its local rail, and the unreported
position records are traced out. A different instrument can change the result.
"""
from itertools import combinations, permutations, product
from pathlib import Path
from runpy import run_path


def require(value, message):
    if not value:
        raise AssertionError(message)


def zero(n):
    return [[0]*n for _ in range(n)]


def signs(permutation):
    inversions=sum(a>b for a,b in combinations(permutation,2))
    return -1 if inversions%2 else 1


def det(A):
    return sum(signs(p)*term(A,p) for p in permutations(range(len(A))))


def term(A,p):
    value=1
    for i,j in enumerate(p):
        value*=A[i][j]
    return value


def ppt(A):
    """Positive semidefinite iff all principal minors are nonnegative.
    Indices are (output rail, reference rail); transpose the reference."""
    P=[[A[2*(i//2)+j%2][2*(j//2)+i%2] for j in range(4)] for i in range(4)]
    require(all(P[i][j]==P[j][i] for i in range(4) for j in range(4)), "PPT symmetry")
    for size in range(1,5):
        for indices in combinations(range(4),size):
            if det([[P[i][j] for j in indices] for i in indices])<0:
                return False
    return True


def apply(K,A):
    """Apply K on the first of two qubits, to an unnormalized Choi matrix."""
    return [[sum(K[i//2][r]*A[2*r+i%2][2*s+j%2]*K[j//2][s]
                 for r in range(2) for s in range(2))
             for j in range(4)] for i in range(4)]


def plus(A,B):
    return [[a+b for a,b in zip(ar,br)] for ar,br in zip(A,B)]


def scalar_kraus():
    walk=run_path(str(Path(__file__).with_name("check_scalar_walk.py")))
    word=walk["ALL_SCALAR"]
    matrices=[zero(2) for _ in range(8)]
    for i,row in enumerate(walk["kernels"](word)):
        q=((2*i-len(word))%16)//2
        matrices[q]=plus(matrices[q],[row[:2],row[2:]])
    for M,n in zip(matrices,[58,10,2,10,26,10,2,10]):
        (a,b),(c,d)=M
        require((a*a+c*c,a*b+c*d,b*b+d*d)==(n,0,n), "initial coin scalar effect")
    return matrices


def add_moment(a,b):
    return tuple(x+y for x,y in zip(a,b))


def signed_sector(M):
    """Mass and second angular harmonic within each O(2) determinant sector."""
    (a,b),(c,d)=M
    mass=a*a+c*c
    vector=(mass,a*a-c*c,2*a*c)
    empty=(0,0,0)
    return vector+empty if a*d-b*c>0 else empty+vector


def compose(left,right):
    out=[0]*6
    for sign1,sign2 in product((0,1),repeat=2):
        n,x,y=left[3*sign1:3*sign1+3]
        k,a,b=right[3*sign2:3*sign2+3]
        # Reflection conjugates the phase from the preceding rotation.
        if sign1:
            b=-b
        off=3*(sign1^sign2)
        out[off]+=n*k
        out[off+1]+=x*a-y*b
        out[off+2]+=x*b+y*a
    return tuple(out)


def sector_ppt(sectors):
    """Bell-state mixture is locally equivalent to a Bell-diagonal law.
    Within each determinant sector its unnormalized Choi eigenvalues
    are p ± |angular harmonic|. Largest <= sum of all four / 2 iff PPT.
    """
    p,a,b,n,c,d=sectors
    return a*a+b*b<=n*n and c*c+d*d<=p*p


def main():
    matrices=scalar_kraus()
    identity=[1,0,0,1]
    choi=[zero(4) for _ in range(8)]
    choi[0]=[[a*b for b in identity] for a in identity]
    coeff=[(0,)*6 for _ in range(8)]
    coeff[0]=(1,1,0,0,0,0)
    weights=[1]+[0]*7
    single=[58,10,2,10,26,10,2,10]
    non_eb=[set(range(0,16,2)),set(range(0,16,2)),{0,2,6,8,10,14},
            {0,8},{0,8},{0},set()]
    for m,expected in enumerate(non_eb,1):
        updated=[zero(4) for _ in range(8)]
        moments=[(0,)*6 for _ in range(8)]
        next_weights=[0]*8
        for j,k in product(range(8),repeat=2):
            target=(j+k)%8
            updated[target]=plus(updated[target],apply(matrices[k],choi[j]))
            moments[target]=add_moment(moments[target],compose(signed_sector(matrices[k]),coeff[j]))
            next_weights[target]+=weights[j]*single[k]
        choi,coeff,weights=updated,moments,next_weights
        flag=set()
        overall=zero(4)
        summed=(0,)*6
        for j,F in enumerate(choi):
            trace=sum(F[i][i] for i in range(4))
            require(trace==2*weights[j] and trace>0,"positive terminal branch/Choi normalization")
            result=ppt(F)
            require(result==sector_ppt(coeff[j]),"PPT vs orthogonal-sector criterion")
            if not result:
                flag.add(2*j)
            overall=plus(overall,F)
            summed=add_moment(summed,coeff[j])
        all_eb=ppt(overall)
        require(all_eb==sector_ppt(summed) and all_eb==(m>=5),"unconditional PPT boundary")
        require(sum(weights)==128**m and flag==expected,"conditional branch boundary")
        print(f"blocks={m} unconditional_EB={all_eb}; non-EB final sites: {sorted(flag)}")
    print("At block 7 every final-site Choi matrix is PPT. Later matrices are sums "
          "of local Kraus conjugations of those matrices, hence remain PPT.")


if __name__=="__main__":
    main()
