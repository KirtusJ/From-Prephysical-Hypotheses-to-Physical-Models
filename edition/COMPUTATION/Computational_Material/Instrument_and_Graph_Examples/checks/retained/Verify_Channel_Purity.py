"""Deterministic checks for Channel Purity from a Single Prepared Input.

Research direction and responsibility: Kirtus Justus.
Vancouver, British Columbia, 7 November 2026. Requires NumPy and mpmath.
Numbers refer to exact model probabilities. No trials are generated.
"""
from itertools import product

import mpmath as mp
import numpy as np

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
I4 = np.eye(4)
I16 = np.eye(16)
kron = np.kron


def check(condition, message):
    if not condition:
        raise ArithmeticError(message)


def close(actual, expected, message, tolerance=2e-12):
    check(np.max(np.abs(np.asarray(actual) - np.asarray(expected))) <= tolerance, message)


def ket(matrix):
    return matrix.reshape(-1)/2


def projector(vector):
    return np.outer(vector, vector.conj())


def parameters():
    s = mp.mpf(131)/320
    h = mp.mpf(99)/100
    q = mp.mpf(81711338569043)/224995905216000
    k = (s*h-mp.sqrt(s*h*q))**2/(s*h*(1-h))
    d = s+k
    r = 1-d
    # Stable positive root of 7*f^2+(39*d-7)*f-6*d*r.
    root = 12*d*r/(39*d-7+mp.sqrt((39*d-7)**2+168*d*r))
    return s, h, q, k, d, r, root


def interval_root_check():
    # Strict endpoint signs with outward interval arithmetic.
    iv = mp.iv
    iv.dps = 65
    s = iv.mpf(131)/320
    h = iv.mpf(99)/100
    q = iv.mpf(81711338569043)/224995905216000
    d = s+(s*h-iv.sqrt(s*h*q))**2/(s*h*(1-h))
    def polynomial(value):
        f = iv.mpf(value)
        return 7*f*f+(39*d-7)*f-6*d*(1-d)
    check(polynomial("0.10532298498594176").b < 0
          and polynomial("0.10532298498594177").a > 0, "root enclosure")


def controlled_unitary(d, f):
    """In rotated coordinates, complete two ancilla rotations with the specified overlap."""
    ell = 1-d-f
    c = np.sqrt(d+f)
    alpha = np.arctan2(np.sqrt(f), np.sqrt(d))
    bloch_z = 2*(d+6*ell/13)-1
    target = bloch_z*np.exp(-2j*alpha)
    cosine = (target.real-c*c)/ell
    check(abs(cosine) <= 1+3e-14, "unit axes impossible")
    cosine = np.clip(cosine, -1, 1)
    first = c*I + 1j*np.sqrt(ell)*Z
    second = c*I + 1j*np.sqrt(ell)*(cosine*Z+np.sqrt(1-cosine**2)*X)
    relative = first.conj().T @ second
    quadrature = (relative-relative.conj().T)/(2j)
    values, vectors = np.linalg.eigh(quadrature)
    weight = (target.imag-values[0])/(values[1]-values[0])
    check(-2e-13 <= weight <= 1+2e-13, "target outside the numerical range")
    weight = np.clip(weight, 0, 1)
    ancilla = vectors @ np.sqrt([1-weight, weight])
    basis = np.column_stack([ancilla, [-ancilla[1].conj(), ancilla[0].conj()]])
    minus = np.exp(-1j*alpha) * basis.conj().T @ first @ basis
    plus = np.exp(1j*alpha) * basis.conj().T @ second @ basis
    return kron((I+X)/2, plus) + kron((I-X)/2, minus)


def verify_witness(s, h, q, k, d, r, f):
    unitary = controlled_unitary(d, f)
    close(unitary.conj().T @ unitary, I4, "rotated unitary")
    lab_angle = np.arctan2(np.sqrt(k), np.sqrt(s))
    transform = kron(np.diag(np.exp(np.array([-1j,1j])*lab_angle/2)), I)
    unitary = transform @ unitary @ transform
    vector = ket(unitary)
    phase_p = ket(I4)
    phase_u = ket(1j*kron(Z,I))
    phase_v = ket(1j*kron(X,I))
    close(np.vdot(phase_p, vector), np.sqrt(s), "match amplitude")
    close(np.vdot(phase_u, vector), -np.sqrt(k), "phase amplitude")
    close(abs(np.vdot(phase_v, vector))**2, f, "extra outcome")
    detector = np.sqrt(h)*phase_p+np.sqrt(1-h)*phase_u
    close(abs(np.vdot(detector, vector))**2, q, "ordinary click")
    match = projector(phase_p)
    for angle in [0, 0.4, np.pi/2, 2.3, np.pi]:
        phased = (match+np.exp(1j*angle)*(I16-match)) @ vector
        expected = abs(np.sqrt(h*s)-np.exp(1j*angle)*np.sqrt((1-h)*k))**2
        close(abs(np.vdot(detector, phased))**2, expected, "phase prediction")
    output = unitary[:,0].reshape(2,2)
    p0 = d+6*(r-f)/13
    close(output @ output.conj().T, np.diag([p0,1-p0]), "first-qubit reference")
    eta = (np.sqrt(s)*phase_p-np.sqrt(k)*phase_u)/np.sqrt(d)
    residual = I16-projector(phase_p)-projector(phase_u)-projector(phase_v)
    base = d*projector(eta)+f*projector(phase_v)+(r-f)*residual/13
    J = d*d+f*f+(r-f)**2/13
    close(np.vdot(vector, base @ vector), J, "overlap")
    for weight in (0, .37, 1):
        state = (1-weight)*base+weight*projector(vector)
        close(np.trace(state @ state), J+weight**2*(1-J), "observed purity")
        close(np.trace(state.reshape(4,4,4,4),axis1=0,axis2=2), I4/4, "trace preservation")


def verify_single_output(spectrum):
    """Choi extremizers constructed from a fixed output spectrum, in its eigenbasis."""
    lam = np.sort(np.asarray(spectrum))[::-1]
    sigma = np.diag(lam)
    # Columns of the isometry are orthonormal system/environment pure states.
    isometry = np.zeros((4,4,4),complex)
    for i, value in enumerate(lam):
        isometry[i,i,0] = np.sqrt(value)
    for j in range(1,4):
        isometry[j,0,j] = 1
    columns = isometry.reshape(16,4)
    close(columns.conj().T @ columns, I4, "Stinespring isometry")
    kraus = [isometry[:,e,:] for e in range(4)]
    high = sum(projector(ket(K)) for K in kraus)
    low = kron(sigma,np.diag([1.,0,0,0]))/4 + kron(I4/4,np.diag([0.,1,1,1]))/4
    for state in (low, high):
        close(np.trace(state.reshape(4,4,4,4),axis1=0,axis2=2), I4/4, "TP marginal")
        close(4*state.reshape(4,4,4,4)[:,0,:,0], sigma, "complete product output")
    purity = lam @ lam
    close(np.trace(low @ low), (purity+3/4)/16, "single-output minimum")
    close(np.trace(high @ high), (purity+6*lam[0]+9)/16, "single-output maximum")


def modular_rank(rows, prime=101):
    # A full row rank modulo a prime certifies rational linear independence.
    matrix = np.array(rows, dtype=np.int64) % prime
    rank = 0
    for column in range(matrix.shape[1]):
        nonzero = np.flatnonzero(matrix[rank:,column])
        if not len(nonzero):
            continue
        pivot = rank+nonzero[0]
        matrix[[rank,pivot]] = matrix[[pivot,rank]]
        scale = pow(int(matrix[rank,column]), -1, prime)
        matrix[rank] = matrix[rank]*scale % prime
        factors = matrix[rank+1:,column].copy()
        matrix[rank+1:] = (matrix[rank+1:]-factors[:,None]*matrix[rank]) % prime
        rank += 1
        if rank == len(matrix):
            break
    return rank


def check_local_dimensions():
    paulis = [kron(a,b) for a,b in product((I,X,Y,Z),repeat=2)]
    eta = projector(ket(I4))
    extra = projector(ket(1j*kron(X,I)))
    for label, support, populations, dimension in [
        ("interior", I16-projector(ket(1j*kron(Z,I))), [eta,extra], 15),
        ("zero", I16-projector(ket(1j*kron(Z,I)))-extra, [eta], 14),
    ]:
        common = [kron(I4,H) for H in paulis] + populations
        for name, operators in [('first',[kron(Q,I) for Q in (X,Y,Z)]), ('joint',paulis[1:])]:
            tomography = [kron(Q,np.diag([1.,0,0,0])) for Q in operators]
            for unital in (False, True):
                constraints = common+tomography
                if unital:
                    constraints += [kron(H,I4) for H in paulis[1:]]
                rows = []
                for H in constraints:
                    # All entries are exactly representable Gaussian dyadic rationals.
                    matrix = 64*support @ H @ support
                    flat = np.concatenate([matrix.real.ravel(),matrix.imag.ravel()])
                    check(np.array_equal(flat,np.rint(flat)), "nonintegral row")
                    rows.append(flat.astype(np.int64))
                rank = modular_rank(rows)
                check(rank==len(rows), "dependent row")
                print("Local dimension",label,name,"unital" if unital else "TP",dimension**2-rank)


if __name__ == "__main__":
    mp.mp.dps = 65
    params = parameters()
    interval_root_check()
    s,h,q,k,d,r,root = map(float,params)
    for f in [0, .02, .075590554093, .1, root]:
        verify_witness(s,h,q,k,d,r,f)
    print("Continuous pure-compatible interval ends at", mp.nstr(params[-1],24))
    check_local_dimensions()
    for f in (0, root, r/2, r):
        ell = r-f
        joint = np.array([d+2*ell/13,4*ell/13,f+3*ell/13,4*ell/13])
        verify_single_output(joint)
        upper = (joint @ joint+6*max(joint)+9)/16
        print(f"f={f:.12f}, joint-output ceiling {upper:.12f}")
    verify_single_output([1,0,0,0])
    verify_single_output([.25]*4)
    print("All deterministic checks passed.")
