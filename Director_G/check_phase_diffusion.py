"""Exact three-direction calibration and an alternating-channel rival. Stdlib."""
from fractions import Fraction as Q
from itertools import product
from math import sqrt
from pathlib import Path
from runpy import run_path


def require(condition, explanation):
    if not condition:
        raise AssertionError(explanation)


HERE = Path(__file__).resolve().parent
KERNEL = run_path(str(HERE/"check_velocity_collisions.py"))["kernels"](3)


def law(source, first, second):
    """Unnormalized density entries A,B,D,C have upper off-diagonal B+iD.
    A phase with parameter x+iy multiplies the upper off-diagonal by x-iy.
    """
    states = {():tuple(map(Q,source))}
    for x,y in [first, second, (1,0)]:
        out={}
        for history,(A,B,D,C) in states.items():
            for step,(a,b,c,d) in KERNEL.items():
                left = c*c*A+2*c*d*B+d*d*C
                right = a*a*A+2*a*b*B+b*b*C
                real = a*c*A+(a*d+b*c)*B+b*d*C
                imag = (a*d-b*c)*D
                out[history+(step,)]=(right,x*real+y*imag,x*imag-y*real,left)
        states=out
    total=512*(Q(source[0])+Q(source[3]))
    result={word:(r+l)/total for word,(r,_,_,l) in states.items()}
    require(len(result)==64 and sum(result.values())==1 and min(result.values())>=0,"word masses")
    return result


def same(word_law,i,j):
    return sum(p for w,p in word_law.items() if w[i]*w[j]>0)


# Field Q(sqrt(2)) pairs; all comparisons in the rival are exact.
def pair(a,b=0):
    return Q(a),Q(b)


def add(u,v):
    return (u[0]+v[0],u[1]+v[1])


def neg(u):
    return -u[0],-u[1]


def mul(u,v):
    a,b=u; c,d=v
    return a*c+2*b*d,a*d+b*c


def div(u,v):
    a,b=v
    m=mul(u,(a,-b));den=a*a-2*b*b
    return m[0]/den,m[1]/den


def real(u):
    return float(u[0])+float(u[1])*sqrt(2)


def mm(A,B):
    return [[add(mul(a,c),mul(b,d)) for c,d in zip(*B)] for a,b in A]


def identity_plus(A,sign):
    return [[add(pair(i==j),mul(pair(sign),A[i][j])) for j in range(2)] for i in range(2)]


def inv(A):
    (a,b),(c,d)=A
    det=add(mul(a,d),neg(mul(b,c)))
    return [[div(d,det),div(neg(b),det)],[div(neg(c),det),div(a,det)]]


C=pair(1,Q(-1,2))
D=pair(-1,1)


def matrix(contact):
    x,y=map(pair,contact)
    return [[mul(C,add(pair(1),x)), neg(mul(D,y))],[mul(C,y),mul(D,x)]]


def alternating_coefficient(first,second):
    def one_order(a,b):
        return mm(identity_plus(a,1),inv(identity_plus(mm(b,a),-1)))[0][0]
    a,b=matrix(first),matrix(second)
    return mul(mul(C,pair(Q(1,2))),add(one_order(a,b),one_order(b,a)))


def main():
    zero=(0,0); unit=(1,0); quarter=(0,1)
    basis=(zero,unit,quarter)
    mixed=(1,0,0,1)
    for u,v in product(basis,repeat=2):
        x,y=u; z,w=v
        board=law(mixed,u,v)
        require(same(board,0,1)==Q(5+x,8) and same(board,1,2)==Q(5+z,8),"adjacent rates")
        require(same(board,0,2)==Q(9+z+x*z-y*w,16),"outer rate")
    print("All nine bilinear interpolation points give the three stated sign probabilities.")

    models=[((Q(1,2),Q(1,2)),(Q(-1,4),Q(1,2))),
            ((Q(1,2),Q(3,8)),(Q(-1,4),Q(2,3)))]
    for contacts in models:
        require(all(x*x+y*y<=1 for x,y in contacts),"contractions in disk")
    for source in [(1,0,0,0),(0,0,0,1),mixed]:
        require(law(source,*models[0])==law(source,*models[1]),"rival: all 64 words")
    diffusions=[alternating_coefficient(*contacts) for contacts in models]
    require(diffusions[0]!=diffusions[1],"alternating diffusion must differ")
    for value in diffusions:
        print("Alternating lambda*D = A + B sqrt(2):",*value,"=",f"{real(value):.10f}")
    for x,y in [(0,0),(1,0),(0,1),(-1,0),(Q(3,5),Q(4,5)),(Q(1,3),Q(-1,4))]:
        board=law(mixed,(x,y),(x,y))
        cosine=8*same(board,0,1)-5
        sin2=9+cosine+cosine*cosine-16*same(board,0,2)
        require(cosine==x and sin2==y*y,"reported-rate reconstruction")
        ux=pair(x)
        num=add(pair(1),neg(mul(D,ux)))
        den=add(mul(add(pair(1),neg(mul(C,add(pair(1),ux)))),num),
                mul(mul(C,D),pair(sin2)))
        require(div(mul(C,num),den)==alternating_coefficient((x,y),(x,y)),
                "diffusion by resolvent versus alternating block resolvent")
    print("Homogeneous rate inversion checked at the origin, circle and disk interior.")


if __name__=="__main__":
    main()
