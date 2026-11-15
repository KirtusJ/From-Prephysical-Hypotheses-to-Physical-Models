"""Check the fixed-length Wilson coefficient. Uses mpmath, tested with 1.3.0.

Run python -I -B fixed.py. Spectral values are high-precision
numerical controls. The derivation and endpoint estimates are in fixed.md.
"""
import mpmath as mp


def require(test, message):
    if not test:
        raise ValueError(message)


def sine_reference(length):
    size = 2 * length
    result = mp.matrix(size)
    for i in range(size):
        for j in range(size):
            d = i - j
            if d == 0:
                result[i,j] = mp.mpf("0.5")
            elif d % 2:
                result[i,j] = (-1) ** ((d-1)//2) / (mp.pi*d)
    return result


def orbital_reference(length):
    size = 2 * length
    result = mp.matrix(size)
    for i in range(size):
        for j in range(size):
            d = i//2 - j//2
            if i % 2 == j % 2:
                z = -1/(mp.pi*(1-4*d*d))
                result[i,j] = (mp.mpf("0.5") if i == j else 0) + (-1)**(i%2)*z
            else:
                result[i,j] = -mp.j*d/(2*mp.pi*(d*d-mp.mpf("0.25")))
    return result


def h(x):
    return mp.log(x)-mp.log1p(-x)


def f(x):
    return x*mp.log(x) + (1-x)*mp.log1p(-x)


def divided(x, y):
    if x == y:
        return 1/(x*(1-x))
    return (h(x)-h(y))/(x-y)


def coefficient(length):
    size = 2*length
    values, vec = mp.eigsy(sine_reference(length))
    weights = [abs(sum(vec[j,i]*(-1)**(j//2) for j in range(size)))**2 / size
               for i in range(size)]
    return mp.fsum(weights[i]*weights[j]*divided(values[i],values[j])
                   for i in range(size) for j in range(size))/(4*mp.pi**2)


def orbital_hessian(length):
    size = 2*length
    values, vec = mp.eighe(orbital_reference(length))
    tangent = mp.matrix(size)
    for i in range(size):
        for j in range(size):
            if i%2 == j%2:
                tangent[i,j] = -(-1)**(i%2)/(2*mp.pi*length)
    tangent = vec.H*tangent*vec
    return mp.fsum(abs(tangent[i,j])**2*divided(values[i],values[j])
                   for i in range(size) for j in range(size))/2


def actual_ratio(length, mu):
    size = 2*length
    m = mu/length
    b = orbital_reference(length)
    e0, q = mp.eighe(b)
    delta = mp.matrix(size)
    nodes = [0, m, mp.sqrt(m), 1, mp.pi]
    def orbital_integrand(k, d, odd):
        s = mp.sin(k/2)
        em = mp.sqrt(m*m+4*(1+m)*s*s)
        if odd:
            return -mp.j*mp.sin(d*k)*(mp.sin(k)/em-mp.cos(k/2))/(2*mp.pi)
        return -mp.cos(d*k)*((m+2*s*s)/em-s)/(2*mp.pi)
    for d in range(length):
        z = mp.quad(lambda k: orbital_integrand(k,d,False), nodes)
        x = mp.quad(lambda k: orbital_integrand(k,d,True), nodes)
        for a in range(d,length):
            bindex = a-d
            for spin in range(2):
                i,j = 2*a+spin, 2*bindex+spin
                delta[i,j] = delta[j,i] = (-1)**spin*z
                j_opposite = 2*bindex+1-spin
                delta[i,j_opposite] = x
                delta[j_opposite,i] = x.conjugate()
    e1 = mp.eighe(b+delta, eigvals_only=True)
    deltaref = q.H*delta*q
    rel = mp.fsum(f(v) for v in e1)-mp.fsum(f(v) for v in e0)
    rel -= mp.fsum(deltaref[j,j]*h(e0[j]) for j in range(size))
    return mp.re(rel)/(mu*mp.log(1/mu))**2


def main():
    for length in [1,2,3,4,6,8,12,16]:
        mp.mp.dps = max(60, 4*length)
        k = coefficient(length)
        if length <= 6:
            require(abs(orbital_hessian(length)-k)<mp.mpf("1e-40"),
                    "orbital and scalar Hessians differ")
        if length == 1:
            require(abs(k-1/(mp.pi**2-4))<mp.mpf("1e-50"), "one-cell formula failed")
        print(f"L={length:2d} coefficient {mp.nstr(k,24)}")
    mp.mp.dps = 100
    for length in [1,2,3]:
        k = coefficient(length)
        ratios = [actual_ratio(length,mp.mpf(10)**(-decimals)) for decimals in [8,16,24]]
        require(all(abs(ratios[i+1]-k)<abs(ratios[i]-k) for i in range(2)),
                "direct small-mass results do not approach Hessian in these controls")
        print(f"L={length} exact-covariance quadrature at mu=1e-8,1e-16,1e-24:",
              ", ".join(mp.nstr(r,18) for r in ratios))
    density = lambda t: mp.log1p(1/t)**2 if t else mp.inf
    require(abs(mp.quad(density,[0,1,mp.inf])-mp.pi**2/3)<mp.mpf("1e-70"),
            "uniform spectral integral disagrees")
    print("limiting Stieltjes integral =", mp.nstr(mp.pi**2/3,24))


if __name__ == "__main__":
    main()
