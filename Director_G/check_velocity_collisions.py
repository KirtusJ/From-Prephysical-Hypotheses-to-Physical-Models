"""Exact dyadic two-flight displacement moments for the signed Hadamard walk.

Usage: python -I check_velocity_collisions.py [first_ticks [second_ticks]]
The initial walker is localized. A site read preserves its local coin.
The comparison records both site and rail at the boundary. Standard library.
"""
import argparse
from fractions import Fraction
from math import sqrt


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def kernels(steps):
    """Matrices taking the sharp source coin to each displacement, times 2^(n/2)."""
    current = [(1, 0, 0, 1)]
    for _ in range(steps):
        nxt = [[0, 0, 0, 0] for _ in range(len(current) + 1)]
        for i, (a, b, c, d) in enumerate(current):
            nxt[i + 1][:2] = a + c, b + d  # R daughter goes right
            nxt[i][2:] = a - c, b - d     # L daughter goes left
        current = nxt
    table = {2*i-steps: tuple(row) for i, row in enumerate(current)}
    require(sum(a*a+c*c for a,b,c,d in current) == 2**steps, "R norm")
    require(sum(b*b+d*d for a,b,c,d in current) == 2**steps, "L norm")
    require(sum(a*b+c*d for a,b,c,d in current) == 0, "source orthogonality")
    return table


def scatter(table, rho, moment, read_rail):
    """Unnormalized averaged output coin, optionally weighted by displacement.

    rho=(A,B,C) stores the real symmetric part [[A,B],[B,C]]. Since all
    walk matrices are real, imaginary antisymmetric parts cannot reach
    the trace of a subsequent real site or rail measurement.
    """
    A, B, C = rho
    out_a = out_b = out_c = 0
    for displacement, (a, b, c, d) in table.items():
        weight = displacement if moment else 1
        out_a += weight * (a*a*A + 2*a*b*B + b*b*C)
        out_b += weight * (a*c*A + (a*d+b*c)*B + b*d*C)
        out_c += weight * (c*c*A + 2*c*d*B + d*d*C)
    return out_a, 0 if read_rail else out_b, out_c


def two_flights(first, second, n, m, rho, rail):
    """Return E[V], E[W], E[VW], Cov(V,W) by two exact instrument maps."""
    def trace(v):
        return v[0]+v[2]
    scale = trace(rho) << (n+m)
    born = scatter(first, rho, False, rail)
    weighted = scatter(first, rho, True, rail)
    require(trace(scatter(second, born, False, False)) == scale, "two-flight mass")
    ev = Fraction(trace(weighted), (trace(rho)<<n)*n)
    ew = Fraction(trace(scatter(second, born, True, False)), scale*m)
    evw = Fraction(trace(scatter(second, weighted, True, False)), scale*n*m)
    return ev, ew, evw, evw-ev*ew


def turns(first, second, n, m, rho, rail):
    """Mass of same strict signs, opposite strict signs, at least one zero."""
    def sign(x):
        return (x>0)-(x<0)
    total = (rho[0]+rho[2]) << (n+m)
    bins = [0,0,0]
    for sx in (-1,0,1):
        a = {x:t for x,t in first.items() if sign(x)==sx}
        post = scatter(a,rho,False,rail)
        for sy in (-1,0,1):
            b = {y:t for y,t in second.items() if sign(y)==sy}
            A,_,C = scatter(b,post,False,False)
            group = 2 if sx*sy==0 else (0 if sx==sy else 1)
            bins[group] += A+C
    require(sum(bins)==total and min(bins)>=0, "turn categories cover incident trials")
    return tuple(Fraction(mass,total) for mass in bins)


def fresh_fair(first, second, n, m, rho):
    """Comparison apparatus explicitly replaces the coin by I/2 at the read.
    This is an independent reset, not the finite three-consecutive-write kernel.
    """
    def law(table, source, steps):
        scale = (source[0]+source[2]) << steps
        A,B,C = source
        p = {x: Fraction((a*a+c*c)*A+2*(a*b+c*d)*B+(b*b+d*d)*C, scale)
             for x,(a,b,c,d) in table.items()}
        require(sum(p.values())==1, "fresh comparison marginal")
        mean = sum((x*mass for x,mass in p.items()), Fraction()) / steps
        neg = sum((mass for x,mass in p.items() if x<0), Fraction())
        tie = p.get(0,Fraction())
        return mean, neg, tie, 1-tie-neg
    v, left,zero,right = law(first,rho,n)
    w, neg,tie,pos = law(second,(1,0,1),m)
    require(w==0 and pos==neg, "independent fair coin gives symmetric displacements")
    return ((v,w,v*w,Fraction()),
            (left*neg+right*pos, left*pos+right*neg, zero+tie-zero*tie))


def path_kernels(ticks):
    """Independent small-clock oracle: sum all signed branches, no recurrence."""
    out = {}
    for word in range(1 << ticks):
        displacement = 2*word.bit_count()-ticks
        row = out.setdefault(displacement, [0, 0, 0, 0])
        for source in (0, 1):  # 0 = R, 1 = L
            last, sign = source, 1
            for t in range(ticks):
                rail = 0 if word & (1 << t) else 1
                if rail == last == 1:
                    sign *= -1
                last = rail
            row[2*last+source] += sign
    return {x: tuple(row) for x,row in out.items()}


def paired_path_check():
    for n,m in ((1,1),(3,5),(5,4)):
        a,b = path_kernels(n),path_kernels(m)
        require(a == kernels(n) and b == kernels(m), "named signed paths")
        for rail in (False,True):
            accum = [0,0,0,0]
            turn = [0,0,0]
            for x,(r,_,l,_) in a.items():
                for y,(u,v,w,z) in b.items():
                    mass = ((u*r)**2+(v*l)**2+(w*r)**2+(z*l)**2 if rail
                            else (u*r+v*l)**2+(w*r+z*l)**2)
                    for i, factor in enumerate((1,x,y,x*y)):
                        accum[i] += factor*mass
                    turn[2 if x*y==0 else (0 if x*y>0 else 1)] += mass
            total, x, y, xy = accum
            require(total == 2**(n+m), "path-pair norm")
            expected = (Fraction(x,n*total),Fraction(y,m*total),Fraction(xy,n*m*total))
            require(two_flights(a,b,n,m,(1,0,0),rail)[:3]==expected, "joint law")
            require(turns(a,b,n,m,(1,0,0),rail)==tuple(Fraction(v,total) for v in turn),
                    "direct turn categories")


def positive(value):
    k = int(value)
    if k <= 0:
        raise argparse.ArgumentTypeError("flight duration must be positive")
    return k


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("first_ticks",nargs="?",type=positive)
    args.add_argument("second_ticks",nargs="?",type=positive)
    args.add_argument("--fractions",action="store_true",help="print exact moment fractions")
    options = args.parse_args()
    schedule = ([(options.first_ticks, options.second_ticks or options.first_ticks)]
                if options.first_ticks else [(16,16),(64,64),(256,256),(96,128)])
    paired_path_check()
    c = 1-1/sqrt(2)
    print("n m source read E[V] E[W] E[VW] Cov(V,W) | limit E[VW],Cov | same opposite tie")
    for n,m in schedule:
        first = kernels(n)
        second = first if n==m else kernels(m)
        for name,rho,h in [("R",(1,0,0),1),("L",(0,0,1),-1),
                           ("+X",(1,1,1),1),("I/2",(1,0,1),0)]:
            def report(tag,k,moments,rates):
                def text(xs):
                    return " ".join(str(x) if options.fractions else f"{float(x):.8f}" for x in xs)
                print(n,m,name,tag,text(moments),"|",f"{k*c**2:.8f}",
                      f"{k*c**2*(1-h*h*c):.8f}","|",text(rates))
            for tag,rail,k in [("site",False,2),("site+rail",True,1)]:
                report(tag,k,two_flights(first,second,n,m,rho,rail),
                       turns(first,second,n,m,rho,rail))
            report("fresh-I/2",0,*fresh_fair(first,second,n,m,rho))


if __name__ == "__main__":
    main()
