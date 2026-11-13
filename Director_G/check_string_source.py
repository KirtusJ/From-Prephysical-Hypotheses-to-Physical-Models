"""Run python -B check_string_source.py OUTPUT_DIRECTORY. Requires NumPy."""
import argparse
import json
import os
from itertools import combinations
from pathlib import Path

for variable in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS'):
    os.environ[variable]='1'
import numpy as np


def reduce(rows):
    """Left-multiply on adjacent rows. The eliminated row also receives phase i."""
    reduced=rows.copy()
    gates=[]
    for col in range(2):
        for j in reversed(range(col,len(rows)-1)):
            x,y=reduced[j:j+2,col]
            radius=float(np.hypot(abs(x),abs(y)))
            if radius==0:
                continue
            g=np.array([[x.conjugate(),y.conjugate()],[-1j*y,1j*x]])/radius
            assert np.linalg.norm(g.conj().T@g-np.eye(2))<1e-14
            assert abs(np.linalg.det(g)-1j)<1e-14
            reduced[j:j+2,:]=g@reduced[j:j+2,:]
            gates.append((j,g))
    error=float(np.linalg.norm(reduced-np.eye(len(rows),2)))
    assert error<2e-14
    return gates,error


def dressed_gate(state,j,u,wrong):
    out={}
    for (m,e),v in state.items():
        b=(m>>j)&3
        if b in (0,3):
            k=m,e
            value=v*(np.linalg.det(u) if b==3 and not wrong else 1)
            out[k]=out.get(k,0j)+value
        else:
            col=int(b==2)
            for row in (0,1):
                k=(m,e) if row==col else (m^(3<<j),e^(1<<j))
                out[k]=out.get(k,0j)+u[row,col]*v
    return out


def run(gates,wrong=False,bare=False):
    # Starting at 01 with link 0 set; a local vacuum-to-pair toggle prepares it.
    v={(3,0 if bare else 1):1.}
    errors=[]
    for j,g in reversed(gates):
        v=dressed_gate(v,j,g.conj().T,wrong)
        errors.append(abs(sum(abs(a)**2 for a in v.values())-1))
    return v,max(errors)


def data_complex(z):
    return [float(z.real),float(z.imag)]


def packet_columns(n):
    # Antiperiodic finite-cell chart of the staggered one-mode band. The open
    # source circuit synthesizes the resulting finite columns directly.
    cells=n//2
    ks=np.pi*(2*np.arange(cells)+1)/cells
    orbitals=[]
    for direction in (1,-1):
        amp=np.exp(-2*(1-np.cos(ks-direction*.75)))*np.exp(-1j*ks*(1 if direction==1 else 3))
        vecs=[]
        for k in ks:
            U=np.array([[4,3j*np.exp(-1j*k)],[3j*np.exp(1j*k),4]])@np.array([[3,-4j],[-4j,3]])/25
            omega=np.arccos(.48*(1+np.cos(k)))
            pole=np.array([1.,1.])/np.sqrt(2)
            v=(np.exp(1j*omega)*pole-U@pole)/(2j*np.sin(omega))
            assert np.linalg.norm(U@v-np.exp(-1j*omega)*v)<1e-14
            vecs.append(v/np.linalg.norm(v))
        physical=(np.exp(1j*np.outer(np.arange(cells),ks))@(amp[:,None]*np.array(vecs)))/np.sqrt(cells)
        # Both orbitals must use the same one-mode gauge.
        physical[:,1]*=-1j
        orbitals.append(physical.ravel())
    v,w=orbitals
    v=v/np.linalg.norm(v)
    w=w-v*np.vdot(v,w)
    return np.column_stack((v,w/np.linalg.norm(w)))


def certify(name,C,exact=None):
    n=len(C)
    orth_error=float(np.linalg.norm(C.conj().T@C-np.eye(2)))
    assert orth_error<2e-14
    pairs=list(combinations(range(n),2))
    wanted=np.array([C[p,0]*C[q,1]-C[p,1]*C[q,0] for p,q in pairs])
    if exact is not None:
        assert np.max(abs(wanted-np.array(exact)/8))<2e-15
    Q,err=reduce(C)
    v,unit=run(Q)
    wrong,_=run(Q,wrong=True)
    bare,_=run(Q,bare=True)
    keys=[((1<<p)|(1<<q),(1<<q)-(1<<p)) for p,q in pairs]
    assert all(m^e^(e<<1)==0 for m,e in v)
    assert all(m^e^(e<<1)==3 for m,e in bare)
    compiled=np.array([v.get(k,0j) for k in keys])
    faulty=np.array([wrong.get(k,0j) for k in keys])
    assert np.linalg.norm(compiled-wanted)<3e-14
    p=abs(compiled)**2
    bare_array=np.array([bare.get((m,e^1),0j) for m,e in keys])
    assert np.linalg.norm(bare_array-compiled)<3e-14
    echo=v
    for j,g in Q:
        echo=dressed_gate(echo,j,g,False)
    assert abs(echo[3,1]-1)<3e-14
    washed=float(p@p)
    assert 0<washed<.99
    faulty_echo=abs(np.vdot(wanted,faulty))**2
    assert faulty_echo<.99
    return dict(case=name,sites=n,source_columns=[list(map(data_complex,col)) for col in C.T],
        direct_qr_gates=[dict(left=j,elimination=[[data_complex(z) for z in line] for line in g])
                         for j,g in Q],eliminations=len(Q),allowed_max=2*n-3,
        orthogonality_error=orth_error,QR_residual=err,largest_norm_drift=unit,
        full_dressed_state_error=float(np.linalg.norm(compiled-wanted)),
        physical_ports=[dict(pair=[a,b],matter_mask=m,occupied_link_mask=e,desired=data_complex(z),
                             compiled=data_complex(zz),probability=float(pp))
                        for (a,b),(m,e),z,zz,pp in zip(pairs,keys,wanted,compiled,p)],
        exact_gaussian_integer_numerator_over_eight=None if exact is None else
                [[int(z.real),int(z.imag)] for z in exact],
        wrong_contact_one=dict(sharp_TV=float(np.sum(abs(abs(faulty)**2-p))/2),
                          overlap_squared_with_target=float(faulty_echo)),
        right_QR_inverse_return=float(abs(echo[3,1])**2),
        decohered_links_inverse_return=washed,
        blank_links=dict(static_defect_mask=3,overlap_with_target=0,
                        aligned_string_complement_mask=1,maximum_matter_probability_error=float(np.max(abs(abs(bare_array)**2-p)))))


def main(directory):
    phase=[(1j)**i for i in range(8)]
    second=[z*((1,1j,-1,-1j)[(i//2)%4]) for i,z in enumerate(phase)]
    exact=[phase[i]*second[j]-phase[j]*second[i] for i,j in combinations(range(8),2)]
    assert sum(int(z.real)**2+int(z.imag)**2 for z in exact)==64
    C=np.column_stack((phase,second))/np.sqrt(8)
    data=dict(method='Any finite pair of orthonormal complex orbitals supplied as two columns can be triangularized with at most 2N-3 addressed complex Givens rotations on consecutive modes: clear column zero bottom-up, then clear column one on rows >=1. Here each eliminating gate uses determinant +i, sends the chosen two entries to (positive length,0), and its synthesis inverse has determinant -i. The occupied adjacent neutral pair is produced from blank vacuum by a gauge-preserving two-charge source that also sets the intervening link. From this seat the time-reversed gate list builds the target exterior product on physical charge AND link coordinates; hopping toggles its edge. Addressable arbitrary complex rotations, determinant contacts, coherent phase convention and state preparation time are explicit apparatus resources.',
        controls='Uncoherently reading which string is occupied dephases every distinct position pair. The matched inverse echo then returns with sum p_xy squared, since the undisturbed source column has entries of squared modulus p_xy. Bare links at the launch violate Gauss at the two charge sites and stay in a disjoint syndrome despite identical charge marginals. Numerical checks use complex binary64 with absolute thresholds 3e-14; the first target has an independently exact integer specification, but the finite-angle compiler uses floating parameters.',
        cases=[certify('two_delocalized_orthonormal_complex_columns',C,exact),
               certify('finite_positive_band_two_wavepackets',packet_columns(10))])
    directory.mkdir(parents=True,exist_ok=True)
    (directory/'string_source.json').write_bytes((json.dumps(data,separators=(',',':'))+'\n').encode())


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    main(p.parse_args().output)
