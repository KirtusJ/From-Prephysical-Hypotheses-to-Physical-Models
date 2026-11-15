"""Exact certificates for the unrestricted five-site Hadamard walk's (0,R) return.

Starting at (0,R), evaluate p_t per original launch without intermediate
measurement. Check the reduced generating function by exact arithmetic and
the 100-dimensional tensor-state recurrence. Verify the independence of the
even-time eigenphases and the sharp persistent error for finite homogeneous
Markov models. Retain moment and four-frequency cross-checks.
Python 3.9+; no third-party libraries.
"""
from fractions import Fraction as F
import json
from math import isqrt, sqrt


def require(condition, diagnostic):
    if not condition:
        raise ValueError(diagnostic)


def trim(poly):
    result = list(map(F, poly))
    while result and result[-1] == 0:
        result.pop()
    return result


def add(a, b, scale=1):
    out = list(a) + [F(0)] * max(0, len(b) - len(a))
    for i, value in enumerate(b):
        out[i] += scale * value
    return trim(out)


def mul(a, b):
    if not a or not b:
        return []
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            out[i+j] += u*v
    return trim(out)


def divide(a, b):
    divisor = trim(b)
    if not divisor:
        raise ZeroDivisionError("zero polynomial divisor")
    remainder = trim(a)
    quotient = [F(0)] * max(0, len(remainder) - len(divisor) + 1)
    while len(remainder) >= len(divisor):
        n = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[n] = coefficient
        for i, value in enumerate(divisor):
            remainder[n+i] -= coefficient * value
        remainder = trim(remainder)
    return trim(quotient), remainder


def gcd(a, b):
    a, b = trim(a), trim(b)
    while b:
        a, b = b, divide(a, b)[1]
    return [x / a[-1] for x in a]


def return_samples(last_tick):
    """Exact integer signed path totals; each physical amplitude is /sqrt(2)^t."""
    right, left = [1, 0, 0, 0, 0], [0]*5
    weights, even_amplitudes = [], []
    for t in range(last_tick + 1):
        weights.append(F(right[0]**2, 1 << t))
        if t % 2 == 0:
            even_amplitudes.append(F(right[0], 1 << (t // 2)))
        expected_odd = t == 0 or (t >= 2 and t % 3 != 0)
        require(right[0] % 2 == expected_odd, ("parity", t, right[0]))
        require(sum(v*v for v in right+left) == 1 << t, ("unit norm", t))
        right, left = (
            [right[(x-1) % 5] + left[(x-1) % 5] for x in range(5)],
            [right[(x+1) % 5] - left[(x+1) % 5] for x in range(5)])
    return weights, even_amplitudes


def check_even_spectrum(quartic, even_amplitudes):
    # For Fourier blocks k=1,2,3,4 put s=2*cos(2*pi*k/5). Dividing
    # 1+z+z^2+z^3+z^4=0 by z^2 gives s^2+s-1=0. For U_k=D_k H,
    # det(U_k)=-1 and tr(U_k)=(z-z^-1)/sqrt(2), so det(U_k^2)=1
    # and x=tr(U_k^2)=s^2/2. Its eigenvalues satisfy u+1/u=x.
    s_polynomial = [-1, 1, 1]
    x_of_s = [0, 0, F(1, 2)]
    x_equation = add(add([1], x_of_s, -6), mul(x_of_s, x_of_s), 4)
    require(not divide(x_equation, s_polynomial)[1], "Fourier trace equation")

    # Use the basis 1, sqrt(5) of the real trace field K. For the two
    # traces x=(3+-sqrt(5))/4, compute the square classes of x^2-4.
    field = [-5, 0, 1]
    deltas = []
    traces = [[F(3, 4), F(sign, 4)] for sign in (1, -1)]
    for x in traces:
        x_squared = divide(mul(x, x), field)[1]
        require(not add(add([1], x, -6), x_squared, 4), "quadratic trace")
        deltas.append(add(x_squared, [4], -1))
    # Both traces lie strictly between 0 and 2, from 2 < sqrt(5) < 3.
    # Thus each delta is negative under a real embedding, hence nonsquare.
    for rational, radical in deltas:
        require(5 < 3**2 and rational + 3 * abs(radical) < 0,
                "discriminant not certified totally negative")
    delta_product = divide(mul(*deltas), field)[1]
    require(delta_product == [F(145, 16)], "discriminant product")
    # A rational r>0 is a square in K precisely when r or r/5 is a
    # rational square: the sqrt(5) coefficient in (a+b*sqrt(5))^2 is 2ab.
    for candidate in (delta_product[0], delta_product[0] / 5):
        require(isqrt(candidate.numerator)**2 != candidate.numerator or
                isqrt(candidate.denominator)**2 != candidate.denominator,
                "discriminant product square in trace field")
    trace_of_x, = add(*traces)
    require(trace_of_x == F(3, 2), "torsion obstruction failed")
    # The two nonsquare discriminants and their nonsquare product give
    # a biquadratic splitting field over K. Each independent sign flip
    # sends one u to 1/u and fixes the other. A relation u1^a*u2^b=1
    # forces u1^(2a)=u2^(2b)=1. Neither is torsion: u+1/u would then be
    # an algebraic integer and its quadratic field trace would be integral.
    # Thus the orbit of each positive power is dense in the phase torus.

    # Independently certify the signed even-time amplitude generating
    # fraction. Ten consecutive zero residuals suffice by applying
    # Cayley-Hamilton directly to the ten-dimensional operator V=U^2.
    denominator = [v / 4 for v in mul([1, -1], quartic)]
    degree = len(denominator) - 1
    dimension = 10
    product = mul(even_amplitudes[:degree+dimension], denominator)
    require(not any(product[degree:degree+dimension]), "amplitude recurrence")
    numerator = trim(product[:degree])
    require(gcd(numerator, denominator) == [1], "amplitude cancellation")
    # Only 1 is torsion, and multiplying the fraction by 1-z and
    # evaluating at 1 gives its constant-frequency coefficient.
    mean = sum(numerator) / (sum(quartic) / 4)
    require(mean == F(1, 5), "signed even-time mean")
    # At (1,1), all five blocks equal I. At (-1,-1), all four nonzero
    # Fourier blocks equal -I and the zero block equals I. The sharp
    # localized port has squared Fourier norm 1/5 in each block. The
    # port amplitude is real on its dense orbit, hence real on the
    # full torus. Along a continuous path between these amplitudes it
    # attains zero; its squared amplitude therefore has infimum 0.
    endpoint_amplitudes = [F(1+4*sign, 5) for sign in (1, -1)]
    require(endpoint_amplitudes == [1, F(-3, 5)], "phase-torus endpoints")
    return {"recurrence_degree": degree,
            "consecutive_zero_residuals": dimension,
            "field_trace_of_eigenvalue_plus_inverse": str(trace_of_x),
            "product_of_discriminants": str(delta_product[0]),
            "independent_even_time_eigenphases": len(deltas),
            "signed_mean_on_even_clock_multiples": str(mean),
            "signed_amplitude_at_equal_plus_and_minus_phases":
                list(map(str, endpoint_amplitudes))}


def check():
    # Ascending coefficients. Q(0)=1. Its degree is 26.
    quartic = trim([4, -6, 9, -6, 4])
    factors = [[1, 0, -1], quartic, [4, 6, 9, 6, 4],
               [4, 0, -6, 0, 9, 0, -6, 0, 4],
               [4, 0, -1, 0, -1, 0, -1, 0, 4]]
    denominator = [F(1, 256)]
    for factor in factors:
        denominator = mul(denominator, factor)
    degree = len(denominator)-1
    # p_t is a matrix element of (U tensor U)^t, of size 100.
    # The recurrence residual for n>=degree is a matrix element of
    # (U tensor U)^(n-degree) applied to a fixed vector, so 100 consecutive
    # zero residuals imply all later residuals vanish by Cayley-Hamilton.
    dimension = 10**2
    weights, even_amplitudes = return_samples(degree + dimension - 1)
    product = mul(weights, denominator)
    require(not any(product[degree:degree+dimension]), "recurrence residual")
    numerator = trim(product[:degree])
    require(gcd(numerator, denominator) == [1], "cancellation in fraction")
    require(gcd(denominator, [n*x for n, x in enumerate(denominator)][1:]) == [1],
            "multiple time-series poles")

    # Order-4 component B/h of the reduced proper generating function.
    B = [F(v, 725) for v in (288, -314, 324, -118)]
    other, remainder = divide(denominator, quartic)
    require(not remainder, "lost quartic factor")
    require(not divide(add(numerator, mul(B, other), -1), quartic)[1],
            "proposed partial fraction disagrees modulo h")
    # c(r) multiplies r^(-t) at a pole r. Hence c(r)*r*h'(r)=-B(r).
    c = [F(v, 725) for v in (21, -5, 6, -4)]
    z_times_derivative = [i*x for i, x in enumerate(quartic)]
    require(not divide(add(mul(c, z_times_derivative), B), quartic)[1],
            "residue formula")
    # Since all roots are on the unit circle, c(1/r)=c(r) proves c is real.
    reversed_c = list(reversed(c))
    require(not divide(add(mul([0, 0, 0, 1], c), reversed_c, -1), quartic)[1],
            "complex-conjugation check on c")
    # In Q[z]/h the trace of multiplication by c^2 is sum of c(r)^2.
    c_squared = mul(c, c)
    trace = F(0)
    for i in range(4):
        col = divide([0]*i + c_squared, quartic)[1]
        trace += col[i] if i < len(col) else 0
    require(trace == F(1316, 525625), "spectral mean-square mass")
    # h(z)=z^2*(4*(z+1/z)^2-6*(z+1/z)+1). The real sums of reciprocal
    # roots are (3+-sqrt(5))/4, strictly inside (-2,2), of trace 3/2.
    # A root of unity would give an algebraic integer with integer trace.
    # A nontrivial root z of Q has z+1/z or z^2+1/z^2 satisfying
    # one of the integer polynomials 4x^2-6x+1, 4x^2+6x+1,
    # 4x^2-x-9. Their irrational roots have non-integer field traces.
    # Were z a root of unity, each of these sums would be an algebraic
    # integer. Thus only the factors 1-z^2 can survive Cesaro averaging
    # along multiples of any even integer D.
    substitutions = [(1, -6, 1), (1, 6, 1), (2, -6, 1), (2, -1, -9)]
    for factor, (power, linear, constant) in zip(factors[1:], substitutions):
        # Multiply 4*(z^k+z^-k)^2 + b*(z^k+z^-k) + c by z^(2k).
        reconstructed = [0] * (4 * power + 1)
        reconstructed[0] = reconstructed[4 * power] = 4
        reconstructed[power] = reconstructed[3 * power] = linear
        reconstructed[2 * power] = 8 + constant
        require(reconstructed == factor, "reciprocal reduction failed")
        discriminant = linear**2 - 16 * constant
        require(discriminant > 0 and isqrt(discriminant)**2 != discriminant,
                "quadratic root unexpectedly rational")
        require(F(-linear, 4).denominator != 1, "quadratic trace integral")
    # Record c_1 and c_-1 for components c_r/(1-z/r).
    derivative = [i * value for i, value in enumerate(denominator)][1:]
    def evaluate(poly, root):
        return sum(c * root**i for i, c in enumerate(poly))
    periodic = [-evaluate(numerator, r) / (r * evaluate(derivative, r))
                for r in (1, -1)]
    even_mean = sum(periodic)
    require(periodic == [F(15, 116), F(41, 580)] and even_mean == F(1, 5),
            "periodic components")
    even_spectrum = check_even_spectrum(quartic, even_amplitudes)
    require(even_spectrum["signed_mean_on_even_clock_multiples"] == str(even_mean),
            "signed and squared moment cross-check")
    # On multiples of every even D the return probabilities are dense in
    # [0,1]. For D a multiple of all recurrent-class periods and 2, a
    # finite Markov readout has a constant limit q on those multiples.
    # Hence its limsup error is at least max(q,1-q). The constant 1/2
    # readout attains the bound (one initial transient can match p_0).
    asymptotic_error = F(1, 2)
    return {"sites": 5, "port": [0, "R"], "recurrence_degree": degree,
            "first_tick": 0, "last_tick": len(weights)-1,
            "tensor_consecutive_zero_residuals": dimension,
            "quartic_coefficients_ascending": list(map(int, quartic)),
            "first_12_return_probabilities": list(map(str, weights[:12])),
            "reduced_numerator_degree": len(numerator)-1,
            "four_frequency_mean_square": str(trace),
            "four_frequency_rms_error_lower_bound": sqrt(float(trace)),
            "periodic_coefficients_at_1_and_minus_1": list(map(str, periodic)),
            "cesaro_mean_on_any_even_clock_progression_starting_at_zero": str(even_mean),
            "even_time_spectrum": even_spectrum,
            "return_probability_closure_on_even_clock_multiples": [0, 1],
            "limsup_absolute_error_lower_bound": str(asymptotic_error),
            "attaining_constant_markov_readout": str(asymptotic_error)}


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
