"""Reconstruct the two controlled-H truth tables and bound a different Ramsey port."""
import argparse
import json
import math
from fractions import Fraction
from pathlib import Path


# Transcribed from the image of Fig. 4b, including both printed bounds. These
# are conditional truth-table averages, not counts of individual photon trials.
TOP = Fraction(9368, 10000)
BOTTOM = Fraction(9605, 10000)
TOP_ERROR = Fraction(27, 10000)
BOTTOM_ERROR = Fraction(21, 10000)


def pairs(angle):
    c, s = math.cos(angle), math.sin(angle)
    return ((c, s), (s, -c))


def ray(w):
    norm = math.sqrt(sum(v*v for v in w))
    return tuple(v/norm for v in w)


def cartesian(u, v):
    return tuple(a*b for a in u for b in v)


def dot(u, v):
    return sum(a*b for a,b in zip(u,v))


def controlled_h(state, sign):
    a,b,c,d = state
    return a,b, sign*(c+d)/math.sqrt(2),sign*(c-d)/math.sqrt(2)


def tables(control_basis, target_basis, gate_sign, transport_target):
    # Under sqrt(2) -> -sqrt(2), both real traceless target observables
    # (Z+X)/sqrt(2), (Z-X)/sqrt(2) change sign. Their labelled projectors swap.
    target = target_basis[::-1] if transport_target else target_basis
    basis = [cartesian(a,b) for a in control_basis for b in target]
    return [[dot(controlled_h(v,gate_sign),w)**2 for w in basis] for v in basis]


def reconstruct():
    control_z = ((1,0),(0,1))
    control_x = (ray((1,1)),ray((1,-1)))
    h_eigen = pairs(math.pi/8)
    complementary = pairs(-math.pi/8)
    # J,K in the published caption can be ordered oppositely. A consistent
    # relabel of the two inputs AND two outputs gives the same truth score.
    assert all(abs(dot(u,v)**2-.5)<2e-15 for u in h_eigen for v in complementary)
    output = {}
    for name, cb, tb in [('top',control_x,h_eigen),('bottom',control_z,complementary)]:
        ordinary = tables(cb,tb,1,False)
        alternate = tables(cb,tb,-1,False)
        transported = tables(cb,tb,-1,True)
        for setting in (ordinary, alternate, transported):
            for row in setting:
                assert abs(sum(row)-1)<2e-14 and max(row)>1-2e-14
        correct = [row.index(max(row)) for row in ordinary]
        score = lambda table: sum(row[d] for row,d in zip(table,correct))/4
        assert abs(score(alternate)-(0 if name=='top' else 1))<2e-14
        assert all(abs(a-b)<2e-14 for u,v in zip(ordinary,transported) for a,b in zip(u,v))
        output[name] = dict(ordinary=ordinary, held_axes_reversed_arm=alternate,
                            jointly_transformed=transported, desired_labels=correct)
    return output


def probability_interval(fidelity, ideal_probability):
    a = math.acos(math.sqrt(ideal_probability))
    da = math.acos(math.sqrt(max(0.,min(1.,fidelity))))
    return [math.cos(min(math.pi/2,a+da))**2,math.cos(max(0.,a-da))**2]


def margin(delta):
    # d=4; maximal input-column weight at a given complementary error.
    if delta >= .75:
        return 1.
    return (math.sqrt(1-delta)+math.sqrt(3*delta))**2/4


def unweighted_bounds(f1, f2):
    wrong = [4*(1-f1),4*(1-f2)]
    delta = [min(1.,d) for d in wrong]
    steps = []
    for _ in range(32):
        # Upward numerical guard. Any finite iterate already gives a valid bound.
        next_delta = [min(delta[j],wrong[j]*margin(delta[1-j])+1e-14) for j in range(2)]
        steps.append(next_delta)
        delta = next_delta
    return dict(max_weighted_errors=steps,choi_lower=max(0,1-sum(delta)))


def split_certificate(f1, f2):
    # f,x,z,w are the masses in the four joint eigenspaces of the two
    # correct-port projectors. Use q_i <= (sqrt(f)+sqrt(3x))²/4
    # + (sqrt(z)+sqrt(3w))²/4, and the analogous inequality with x,z exchanged.
    def coeff(t):
        return 1+t,3+3/t
    a,b=1-f1,1-f2
    az,bz=coeff(Fraction(60,100))
    cz,dz=coeff(Fraction(26,100))
    ax,bx=coeff(Fraction(73,100))
    cx,dx=coeff(Fraction(28,100))
    # z <= zf*f + zx*x + zw*w, and x <= xf*f + xz*z + xw*w.
    zf,zx,zw=(v/(1-a*cz) for v in (a*az,a*bz,a*dz-1))
    xf,xz,xw=(v/(1-b*cx) for v in (b*ax,b*bx,b*dx-1))
    assert 1-a*cz>0 and 1-b*cx>0 and 0<zx*xz<1
    scale_f=(zf*(1+xz)+xf*(1+zx))/(1-zx*xz)
    scale_w=1+(zw*(1+xz)+xw*(1+zx))/(1-zx*xz)
    assert scale_w<=0
    return dict(wrong_mass_coefficient_on_f=str(scale_f),wrong_mass_coefficient_on_w=str(scale_w),
                choi_lower=str(1/(1+scale_f)),decimal_lower=float(1/(1+scale_f)))


def single_error_certificate(f1, f2):
    # z, wrong in the first test alone, obeys z <= a by MUB projection
    # of the column residuals. Bound all wrong mass in the second test at once.
    a,b=1-f1,1-f2
    s=Fraction(47,100)
    assert 0<=a and 0<=b<Fraction(1,4)
    lower=(1-a*(1+b*(3+3/s)/(1-4*b)))/(1+b*(1+s)/(1-4*b))
    return dict(choi_lower=str(lower),decimal_lower=float(lower),s=str(s),
                fit_example_choi_upper_on_any_guarantee=str(f1+f2-1))


def checks():
    top,bottom=float(TOP),float(BOTTOM)
    # Preserve both the printed lower bound and the arithmetic of the printed
    # central table scores. Use the smaller bound for transfer to an unmeasured port.
    proc=min(.8971,top+bottom-1)
    ideal=(2+math.sqrt(2))/4
    port=cartesian(ray((1,1)),(1,0))
    for gate_sign in (1,-1):
        a,b,c,d=controlled_h(port,gate_sign)
        plus=((a+c)**2+(b+d)**2)/2
        assert abs(plus-(ideal if gate_sign==1 else 1-ideal))<1e-15
    f_tp=(max(0,4*math.sqrt(proc)-3))**2
    f_loss=max(0.,4*proc-3)
    bounds = unweighted_bounds(top,bottom)
    assert bounds['choi_lower']>.7610
    return dict(
        source=dict(doi='10.1038/ncomms1392',panel='4b',paper_year=2011,
                    figure='https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fncomms1392/MediaObjects/41467_2011_Article_BFncomms1392_Fig4_HTML.jpg',
                    retrieved_figure_sha256='d228a77247aadb68f2b634e3522026a3b7cbfd6f30c0dacddd8dbf474a3fd46b',
                    conditional_correct_top=top,conditional_correct_bottom=bottom,
                    printed_top_uncertainty=float(TOP_ERROR),printed_bottom_uncertainty=float(BOTTOM_ERROR),
                    published_process_lower=.8971,published_process_upper=.9368,
                    published_average_gate_lower=.9177,published_average_gate_upper=.9494,
                    protocol='Photon-pair coincidences at selected ports. Sixteen measurements per table. '
                    'Low probabilities received a longer integration. No raw event counts were inferred.'),
        computed_tables=reconstruct(),
        comparisons=dict(ideal_held_top=[1,0],ideal_held_bottom=[1,1],
                         possible_ideal_flipped_fraction_upper=1-top,
                         dephasing_only_inferred_real_overlap=2*top-1,
                         dephasing_only_predicted_bottom=1,bottom_discrepancy=1-bottom,
                         dephasing_extrapolated_ramsey_plus=(1+(2*top-1)/math.sqrt(2))/2,
                         ordinary_ramsey=ideal,flipped_ramsey=1-ideal),
        success_weighted_or_equal_success=dict(process_lower=proc,table_sum_minus_one=top+bottom-1,
                    common_TP_worst_input_fidelity=f_tp,
                    common_TP_unmeasured_ramsey_interval=probability_interval(f_tp,ideal),
                    normalized_Choi_worst_input_fidelity=f_loss,
                    normalized_Choi_unmeasured_ramsey_interval=probability_interval(f_loss,ideal)),
        unweighted_unknown_success=bounds,
        unweighted_split_certificate=split_certificate(TOP,BOTTOM),
        unweighted_single_error_certificate=single_error_certificate(TOP,BOTTOM),
        printed_error_sensitivity=single_error_certificate(TOP-TOP_ERROR,BOTTOM-BOTTOM_ERROR),
        reduced_scores_sensitivity=unweighted_bounds(float(TOP-TOP_ERROR),float(BOTTOM-BOTTOM_ERROR)),
        scope='The alternative flips only the controlled Hadamard with fixed named analyzers. '
              'Joint transport preserves the ideal tables. Quantum CP-map bounds assume well-defined '
              'conditional data for all input rays of the same device and calibrated complementary '
              'preparations and reads. The eight-sheet port and the Ramsey port were not measured here.')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    folder=parser.parse_args().output
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'optical_bypass_calibration.json').write_bytes((json.dumps(checks(),indent=2)+'\n').encode())
