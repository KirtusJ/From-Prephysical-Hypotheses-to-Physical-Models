"""Run python -B check_string_return_law.py OUTPUT_DIRECTORY (NumPy).

Exact dressed-link and recorded-path checks at short times. A bounded numerical
forward recurrence search is checked by three ways of evaluating the unitary.
"""
import argparse
import json
import os
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path

for variable in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ[variable] = "1"
import numpy as np
from check_gauss_string import FIELDS, TILTS, defect, launch, physical, rationalize


HORIZON = 32768
PHASES = {"zero": (1,0,1), "positive_quarter": (0,-1,1),
          "negative_quarter": (0,1,1), "positive_rational": (3,-4,5),
          "negative_rational": (3,4,5), "real_pi": (-1,0,1)}


def matrices(n, phase, after_each=False):
    """Each local column is the complete occupation gate or its entrywise square."""
    coords = list(combinations(range(n),2))
    dim = len(coords)
    idx = {p:i for i,p in enumerate(coords)}
    kinetic, marked = np.eye(dim,dtype=complex), np.eye(dim)
    string = np.array([phase**(j-i) for i,j in coords])
    for layer,(c,s) in enumerate(TILTS):
        for k in range(layer,n-1,2):
            gate = np.eye(dim)
            for col, pos in enumerate(coords):
                if (k in pos) != (k+1 in pos):
                    other = tuple(sorted(set(pos) ^ {k,k+1}))
                    gate[col,col] = c/5
                    gate[idx[other],col] = (s if k in pos else -s)/5
            kinetic = gate @ kinetic
            marked = (gate*gate) @ marked
        if layer == 1 or after_each:
            kinetic = string[:,None]*kinetic
    assert np.max(abs(kinetic.conj().T@kinetic-np.eye(dim)))<1e-13
    assert np.max(abs(marked.sum(axis=0)-1))<1e-13 and np.max(abs(marked.sum(axis=1)-1))<1e-13
    return coords,kinetic,marked


def pointer_update(paths, n):
    """Append a fresh local hop/stay bit at EVERY gate. Squared path weights
    use denominator 25 per local gate, even on deterministic 00/11 blocks.
    """
    for layer,(c,s) in enumerate(TILTS):
        for k in range(layer,n-1,2):
            nxt={}
            for (m,e,bits),weight in paths.items():
                occ=(m>>k)&3
                nxt[m,e,bits<<1] = weight*(c*c if occ in (1,2) else 25)
                if occ in (1,2):
                    key=m^(3<<k), e^(1<<k), (bits<<1)|1
                    assert key not in nxt
                    nxt[key]=weight*s*s
            assert all(defect(m,e)==0 for m,e,_ in nxt)
            paths=nxt
    return paths


def exact_trial(n, source, tag, cycles, after_each=False):
    i,j=source
    field=PHASES[tag]
    coords,U,T=matrices(n,complex(*field[:2])/field[2],after_each)
    col=coords.index((i,j))
    ref=U[:,col]*0
    ref[col]=1
    prob=abs(ref)**2
    amps=launch(n,i,j)
    den=1
    ((mask,links),)=amps
    paths={(mask,links,0):1}
    rows=[]
    for t in range(cycles+1):
        pointer_den=25**((n-1)*t)
        projected=defaultdict(int)
        for (m,e,_),weight in paths.items():
            projected[m,e]+=weight
        assert sum(projected.values())==pointer_den
        exact_square,exact_marked=[],[]
        precision=0.
        for h,(x,y) in enumerate(coords):
            key=(1<<x)|(1<<y),(1<<y)-(1<<x)
            u,v=amps.get(key,(0,0))
            q=Fraction(u*u+v*v,den*den)
            p=Fraction(projected[key],pointer_den)
            precision=max(precision,abs(complex(u,v)/den-ref[h]),abs(float(p)-prob[h]))
            exact_square.append(str(q))
            exact_marked.append(str(p))
        assert precision<2e-13
        rows.append(dict(tick=t,pointer_bits=(n-1)*t,reachable_pointer_strings=len(paths),
                         signed_positions=exact_square,recorded_positions=exact_marked,
                         max_matrix_amplitude_or_probability_discrepancy=precision))
        if t<cycles:
            for layer in (0,1):
                kick=field if after_each or layer else FIELDS["idle"]
                amps,inc=physical(amps,n,layer,kick,1)
                amps,den=rationalize(amps,den*inc)
            paths=pointer_update(paths,n)
            ref=U@ref
            prob=T@prob
    return dict(sites=n,source=source,phase=tag,field_after_each_layer=after_each,
                ordered_coordinate_bins=coords, snapshots=rows)


def graph_control(n):
    coords,U,T=matrices(n,-1j)
    size=len(coords)
    # The stochastic graph contains all elementary exclusion moves in one full
    # cycle, as well as a self-loop at each configuration.
    hops=[T[i,j] for i,(a,b) in enumerate(coords) for j,(x,y) in enumerate(coords)
          if abs(x-a)+abs(y-b)==1]
    assert all(p>0 for p in hops) and min(T.diagonal())>0
    support=T>0
    for power in range(1,2*n+1):
        if support.all():
            break
        support=(T>0)@support
    assert support.all()
    eig=np.linalg.eigvals(T)
    neutral=np.linalg.matrix_power(T,64)
    return dict(sites=n,two_particle_dimension=size,stationary_return=str(Fraction(1,size)),
                one_cycle_min_hold=float(min(T.diagonal())),number_directed_elementary_hops=len(hops),
                smallest_elementary_hop=float(min(hops)) if hops else None,
                smallest_strictly_positive_power=power,
                eigenvalue_moduli_descending=sorted(map(float,abs(eig)),reverse=True),
                max_deviation_from_uniform_at_64=float(np.max(abs(neutral-1/size))),
                unitary_unit_modulus_error=float(np.max(abs(abs(np.linalg.eigvals(U))-1))))


def recurrence(tag):
    x,y,d=PHASES[tag]
    coords,U,T=matrices(4,complex(x,y)/d)
    values,vec=np.linalg.eig(U)
    coeff=vec*np.linalg.inv(vec).T
    norm_error=float(np.max(abs(abs(values)-1)))
    assert norm_error<1e-13
    # Independent full scan by repeated literal matrix application, with
    # exact same fixed input columns, followed by a spectral scan for all t.
    mat=np.eye(len(coords),dtype=complex)
    scores=np.empty((HORIZON,len(coords)))
    for i in range(HORIZON):
        mat=U@mat
        scores[i]=abs(mat.diagonal())**2
    times=np.arange(1,HORIZON+1)
    spectral=abs(values[None,:]**times[:,None] @ coeff.T)**2
    discrepancy=float(np.max(abs(scores-spectral)))
    assert discrepancy<2e-9
    def one(j):
        best=int(np.argmax(scores[:,j]))
        t=best+1
        q=abs(np.linalg.matrix_power(U,t)[j,j])**2
        p=float(np.linalg.matrix_power(T,t)[j,j])
        gap=float(q-p)
        assert abs(q-scores[best,j])<1e-9 and gap>.5
        # Straight upper bound if an observed lower limit Rmin were 0.99:
        # q <= 1 implies R <= 1-c(1-p). With calibrated q, tighten to
        # R<=q-c(q-p). A q below 0.99 makes the hypothetical rate infeasible.
        return dict(launch=coords[j],best_tick=t,best_return=float(q),marked_return=p,
                    excess_over_marked=gap,broad_c_ceiling_if_R_at_least_0_99=.01/(1-p),
                    calibrated_c_ceiling_if_R_at_least_0_99=float((q-.99)/gap) if q>=.99 else None,
                    direct_scan_score=float(scores[best,j]),eigen_scan_score=float(spectral[best,j]))
    return dict(phase=tag,field=PHASES[tag],tested_all_forward_horizons=[1,HORIZON],
                unitary_eigenphases_radians=sorted(map(float,np.angle(values))),
                spectral_basis_condition=float(np.linalg.cond(vec)),max_unit_modulus_error=norm_error,
                uniform_discrepancy_two_complete_scans=discrepancy,localized_launches=[one(j) for j in range(len(coords))])


def main():
    exact=[exact_trial(4,(0,2),label,4) for label in PHASES]
    exact += [exact_trial(4,(0,2),"positive_quarter",4,True),
              exact_trial(5,(0,4),"positive_rational",3),exact_trial(2,(0,1),"positive_quarter",4)]
    def sq(i):return [z["signed_positions"] for z in exact[i]["snapshots"]]
    def mark(i):return [z["recorded_positions"] for z in exact[i]["snapshots"]]
    assert sq(1)==sq(2) and sq(3)==sq(4)
    assert sq(0)!=sq(1) and sq(1)!=sq(6)
    assert all(mark(i)==mark(0) for i in range(7))
    scans=[recurrence(tag) for tag in ("zero","positive_quarter","positive_rational","real_pi")]
    return dict(model="Open scalar sites 0..n-1 and two occupations i<j. Vacuum exterior flux, with energized links [i,j). In a cycle apply every even bond, then every odd bond. Real-gauge single-occupation rotation [[c,-s],[s,c]], (c,s)=(3,4)/5 or (4,3)/5. Vacuum and double occupation unchanged. Multiply by w on every energized link once, after both layers, with w=exp(-i tau sigma a/(2 epsilon)); selected phases fix this product. A retimed control applies the phase after each layer.",
                mixtures="c is a fixed preparation fraction of the permanently path-recorded sector. Q is the coherent squared read in the unmarked sector; T is the recorded branch's probability kernel. Finite t gives R=(1-c)Q+cP with P=(T^t)_{ii}. Conditional sensitivity entries are hypothetical thresholds, not measured returns. The physical return is to both original sites and hence to their unique vacuum-sector flux pattern.",
                pointer="One fresh bit per active bond per cycle records hop/stay. For a fixed localized input the complete bit string specifies the unique trajectory. A finite binary register of (n-1)t bits suffices at each finite horizon. Tracing permanent orthogonal records adds their squares; retained signed paths with a common final Gauss string interfere without the pointer. Long-time Markov statistics may also be generated by dephasing or discarding freshly reset pointers. A single fixed finite reversible record cannot store arbitrarily long distinct histories.",
                proof="The site exclusion graph is connected: repeatedly move the left particle left to 0, then the right to 1. Each such hop and its reverse have positive one-cycle probability by holding at every other gate. Every configuration has a positive self-loop, and every local squared gate and their product are doubly stochastic. Thus the primitive matrix powers tend to the uniform matrix on binom(n,2) states. Finite-dimensional unitary recurrence supplies forward t_j tending to infinity with W^t_j approaching identity. Along those horizons the mixture return tends to 1-c+c/binom(n,2). For n=2 both laws give one. The observation law and apparatus stability across horizons are hypotheses.",
                geometry=[graph_control(n) for n in range(2,11)], exact_full_distributions=exact,
                bounded_forward_revival_trials=scans,
                negative_controls="For localized and real-gauge launches and position reads, conjugating w conjugates every amplitude; exact position probabilities coincide for either field sign on tested rows. Turning the field off or applying it twice changes signed records here. All marked models are phase- and kick-timing-independent. All trial maxima are reported; the finite search gives no first recurrence time or arbitrary-accuracy runtime estimate.")


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    directory=parser.parse_args().directory
    data=main()
    directory.mkdir(parents=True,exist_ok=True)
    (directory/"string_return_law.json").write_bytes((json.dumps(data,separators=(",",":"))+"\n").encode())
    print(len(data["exact_full_distributions"]),"exact families;",len(data["bounded_forward_revival_trials"]),"complete scans.")
