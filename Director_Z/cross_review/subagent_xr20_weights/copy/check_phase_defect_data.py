"""Xue, Qin & Tang (2014): reported photon data versus two specified optical readout laws."""
import argparse
from collections import defaultdict
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path


def norm2(a):
    return a.real*a.real+a.imag*a.imag


def summary(b, q, site):
    def moments(p):
        avg=sum(x*w for x,w in p.items())
        return dict(recurrence=p.get(site,0),mean=avg,variance=sum(x*x*w for x,w in p.items())-avg*avg)
    return dict(born=moments(b),local_fourth=moments(q),
                position_TV=sum(abs(b[x]-q[x]) for x in b)/2)


def walk(site, phase, angle, ticks, coin=-1j, literal_adjoint=False):
    """Floating recurrence implementing both polarization actions beneath Eq. (2)."""
    cs,sn=math.cos(math.radians(2*angle)),math.sin(math.radians(2*angle))
    g=complex(math.cos(math.radians(phase)),math.sin(math.radians(phase)))
    g={0:1,90:1j,180:-1}.get(phase,g)
    v={0:[1/math.sqrt(2),coin/math.sqrt(2)]}
    p={0:[.5,.5]}
    rows=[]
    for _ in range(ticks):
        out=defaultdict(lambda:[0j,0j])
        weights=defaultdict(lambda:[0.,0.])
        for x,(a,b) in v.items():
            h=(cs*a+sn*b)*(g if x==site else 1)
            if literal_adjoint:
                gv=g.conjugate() if x+1==site else 1
            else:
                gv=g if x==site else 1
            z=(sn*a-cs*b)*gv
            m=sum(p[x])
            denominator=norm2(h)**2+norm2(z)**2
            left=m*norm2(h)**2/denominator if denominator else 0.
            out[x-1][0],out[x+1][1]=h,z
            weights[x-1][0],weights[x+1][1]=left,m-left
        v,p=out,weights
        b={x:sum(map(norm2,vs)) for x,vs in v.items()}
        q={x:sum(qs) for x,qs in p.items()}
        assert abs(sum(b.values())-1)<2e-13 and abs(sum(q.values())-1)<2e-13
        rows.append(summary(b,q,site))
    return rows


def exact_origin_pi(ticks):
    """Independent integer path sum plus exact rational transport for the Fig. 2 settings."""
    phase_rows=[]
    probabilities={0:[F(1,2)]*2}
    amplitude={0:[1,-1j]}
    for t in range(1,ticks+1):
        v=defaultdict(lambda:[0j,0j])
        # Enumerate historical words from both source polarizations. The only
        # scalar amplitudes are Gaussian integers divided by sqrt(2^(t+1)).
        for source in (0,1):
            for word in range(1<<t):
                x,previous,sign=0,source,1
                for bit in reversed(range(t)):
                    new=(word>>bit)&1
                    if x==0:
                        sign=-sign
                    if previous==new==1:
                        sign=-sign
                    x+=2*new-1
                    previous=new
                v[x][previous]+=sign*(1 if source==0 else -1j)
        q=defaultdict(lambda:[F(0),F(0)])
        for x,(left,right) in amplitude.items():
            mass=sum(probabilities[x])
            n1,n2=int(norm2(left+right)),int(norm2(left-right))
            qa=mass*F(n1*n1,n1*n1+n2*n2) if n1 or n2 else F(0)
            q[x-1][0],q[x+1][1]=qa,mass-qa
        b={x:F(int(sum(map(norm2,z))),1<<(t+1)) for x,z in v.items()}
        qx={x:sum(z) for x,z in q.items()}
        assert sum(b.values())==sum(qx.values())==1
        row=summary(b,qx,0)
        phase_rows.append(dict(tick=t,**row,sites=sorted(b),
                               born_positions=[b[x] for x in sorted(b)],
                               quartic_positions=[qx[x] for x in sorted(b)]))
        amplitude,probabilities=v,q
    return phase_rows


# Original-pixel inclusive vertical bounds of red symbols (and caps where
# present). Infer central y from the midrange; positions are not raw counts.
# Calibration anchors are (y_px, axis_value). Figures 2B and 2C display only even ticks.
CHARTS = [
    ("2b", "tick", "variance", [0,2,4,6,8,10], (409,0,41.5,12),
     [(405,412),(343,351),(312,320),(254,268),(185,198),(90,120)]),
    ("2c", "tick", "recurrence", [0,2,4,6,8,10], (451,.4,76,1),
     [(72,79),(381,395),(308,324),(311,327),(293,316),(297,317)]),
    ("3b", "phase", "variance", [0,45,90,135,180], (437,5,79,30),
     [(94,120),(263,283),(364,379),(363,379),(358,373)]),
    ("3b inset", "phase", "recurrence", [0,45,90,135,180], (265.5,0,41.5,.8),
     [(239,244),(156,161),(87,95),(82,91),(86,95)]),
    ("5b inset", "angle", "recurrence", [9,18,22.5,30], (203,0,28,.8),
     [(181,185),(100,107),(63,69),(28,35)]),
    ("6b", "offsite_angle", "variance", [9,18,22.5,30], (460,0,99.5,50),
     [(109,134),(314,332),(354,367),(399,408)]),
    ("6b inset", "offsite_angle", "recurrence", [9,18,22.5,30], (226.5,0,38,.6),
     [(199,203),(130,137),(103,111),(56,64)]),
]
IMAGE_HASHES={
    2:"7b2daa43df39e8f0d6ca972995f5bc082d721593f28e170f3005ace53c7fa95e",
    3:"5a428e3e6478a1c0b808267e45da8902638ae68c21de3f32c172d477dc90535b",
    5:"11951db56833779738b80fd9fafc5b60800b01e349013903b7671515d9ba5b06",
    6:"7ac4df121e2521cd3f2980fa85345c7b84bbe893f3a033d90bbe4b21b735bfd9",
}


def chart_data():
    result=[]
    for panel,kind,stat,settings,anchors,bounds in CHARTS:
        p0,a0,p1,a1=anchors
        slope=(a1-a0)/(p1-p0)
        obs=[]
        for setting,(low,high) in zip(settings,bounds):
            site=int(kind=="offsite_angle")
            angle=setting if "angle" in kind else 22.5
            phase=setting if kind=="phase" else 180
            t=setting if kind=="tick" else (9 if site else 10)
            row=walk(site,phase,angle,t)[-1] if t else summary({0:1},{0:1},site)
            value=a0+((low+high)/2-p0)*slope
            obs.append(dict(setting=setting,clock=t,defect_site=site,phase_degrees=phase,
                            HWP_degrees=angle,symbol_y_extent=[low,high],estimated_centre=value,
                            squared_prediction=row["born"][stat],local_fourth_prediction=row["local_fourth"][stat],
                            pixel_geometry_scale_2px=2*abs(slope)))
        result.append(dict(panel=panel,setting_axis=kind,statistic=stat,
                           y_calibration=list(anchors),readings=obs))
    return result


def calibration_row(name,row,stat,observed,sd):
    b,q=row["born"][stat],row["local_fourth"][stat]
    data=dict(name=name,metric=stat,reported=observed,reported_statistical_SD=sd,
              born=float(b),local_fourth=float(q),
              signed_residual_in_quoted_SD={k:float((row[k][stat]-observed)/sd)
                                           for k in ("born","local_fourth")},
              midpoint_equal_absolute_error=float((q+b)/2),
              required_observation_shift_to_midpoint=float((q+b)/2-observed))
    if stat=="recurrence":
        data["center_vs_rest_detection_efficiency_needed_for_exact_fit"]={
            k:float(observed*(1-row[k][stat])/((1-observed)*row[k][stat])) for k in ("born","local_fourth")}
    return data


def main(out):
    exact=exact_origin_pi(10)
    numeric=walk(0,180,22.5,10)
    for r,w in zip(exact,numeric):
        assert abs(float(r["position_TV"])-w["position_TV"])<1e-13
        for law in ("born","local_fourth"):
            for m in r[law]:
                assert abs(float(r[law][m])-w[law][m])<1e-12
    assert exact[3]["born"]["recurrence"]==F(5,8) and exact[3]["local_fourth"]["recurrence"]==F(75,104)
    assert exact[9]["born"]["variance"]==F(611,64)
    special=walk(0,135,22.5,10)[-1]
    assert abs(special["born"]["recurrence"]-.667)<.0005
    free=walk(0,0,22.5,10)[-1]
    literal=walk(0,180,22.5,10,literal_adjoint=True)
    real_check=walk(0,135,22.5,10,coin=-1)[-1]
    conjugate=walk(0,-135,22.5,10,coin=1j)[-1]
    assert abs(conjugate["local_fourth"]["recurrence"]-special["local_fourth"]["recurrence"])<1e-12
    assert abs(real_check["born"]["recurrence"]-special["born"]["recurrence"])>.01
    mean=sum(r["position_TV"] for r in exact)/10
    tables=chart_data()
    assert abs(tables[1]["readings"][2]["estimated_centre"]-.615)<.0032
    printed=[
        calibration_row("Fig. 2a,c, origin, tick 4, 180 degree phase",exact[3],"recurrence",.615,.011),
        calibration_row("Fig. 2b, tick 10, 180 degree phase",exact[9],"variance",9.586,.463),
        calibration_row("Fig. 3b inset, origin, tick 10, 135 degree phase",special,"recurrence",.660,.012),
    ]
    result=dict(source=dict(article="Peng Xue, Hao Qin, Bao Tang. Scientific Reports 4, 4825 (2014).",
                doi="https://doi.org/10.1038/srep04825",publisher_pdf="https://www.nature.com/articles/srep04825.pdf",
                open_text="https://pmc.ncbi.nlm.nih.gov/articles/PMC4001091/",
                preprint="https://arxiv.org/pdf/1401.6109",update_check="Publisher, PMID 24769869, "
                "and Crossref work record showed no linked correction in the inspection; Crossref relation {}. "
                "The preprint's Fig. 4 explanatory paragraph shows a real sign where the published version "
                "gives -i. Fig. 4 describes theory. The measured configurations in Figs. 2,3,5,6 use the "
                "antisymmetric circular input. A real-input experiment was not identified in this paper."),
        apparatus="Source localized at site 0, circular (H-iV)/sqrt(2) in H/V order. Eq. (1) coin "
                  "C(theta)=[[cos2theta,sin2theta],[sin2theta,-cos2theta]]. At the defect n multiply both "
                  "outgoing amplitudes by exp(+i phi) on departure, H goes left and V right. Eq. (2)'s "
                  "two explicitly stated basis actions and the polarization-independent phase plate specify "
                  "this convention. Its symbol S-dagger is not literally the inverse of the stated left shift.",
        alternative="At each physical site split its actual incoming probability between coin outputs "
                    "in proportion to their complex modulus to the fourth power, then stream; zero-total cells "
                    "carry zero mass. Born uses the same coherent amplitudes. Sum both outgoing coin weights "
                    "at a final site. For nonbalanced HWP settings this explicitly extends the tested rule. "
                    "Equal initial circular moduli give initial weights 1/2,1/2.",
        measurement="Site coincidence counts divided by total detected counts at the respective step. "
                    "7 ns coincidence window, roughly 300 coincidences/s collected over 60 s as an apparatus "
                    "statement, visibility 0.998 per interferometer pair. No absolute detection probabilities, "
                    "per-bin raw counts or covariance matrix were obtained. Common attenuation cancels; "
                    "unequal efficiencies, dephasing, state errors and drift need independent calibration.",
        printed_observations=printed,error_semantics="Statistical-only Monte Carlo standard deviations. "
                    "The discrepancy/SD ratios use the printed standard deviations as units; they are not "
                    "calibrated p-values and the different plot entries are not independent trials.",
        fig2_mean_TV=dict(printed=.046,ideal_separation=float(mean),exact_ideal_separation=str(mean),
                    interpretation="If the stated average is the equally weighted average over depths 1–10, "
                    "the triangle lower bound on empirical/quartic TV is below the reported empirical/Born TV. "
                    "The average alone does not rank these two predictions.",
                    nominal_lower_bound=float(mean)-.046),
        fig2_exact_by_depth=exact,fig2_no_defect_controls=dict(printed_theory_variance_Q=29.951,
                  our_Q_variance=free["born"]["variance"],printed_classical_random_walk_variance=10,
                  defect_theory_variance_printed=9.547,defect_our_variance=float(exact[9]["born"]["variance"])),
        graphic_provenance=dict(url_template="https://media.springernature.com/full/springer-static/image/"
              "art%3A10.1038%2Fsrep04825/MediaObjects/41598_2014_Article_BFsrep04825_Fig{number}_HTML.jpg",
              file_sha256=IMAGE_HASHES,dimensions_px={"2":[1985,558],"3":[1378,538],"5":[1362,501],"6":[1382,546]},
              method="Secondary readings from publisher JPEG. Red marker/visible caps in narrow x window; "
                     "centre is midrange of inclusive y bounds. Pixel coordinates from top left. Linear "
                     "axis anchors and two-pixel scale are included; this scale describes digitization only. "
                     "Do not treat cap bounds as independent counts or assign plotted centres printed precision. "
                     "3D occluded histograms not converted into raw per-position data; Fig. 2a model "
                     "profiles at all ten depths are included independently."),
        digitized_secondary=tables,
        adverse_controls=dict(fourth_neutral_depths=[r["tick"] for r in exact if r["position_TV"]==0],
             Fig2b_printed_and_plotted="Printed tick-10 variance 9.586; Fig. 2b red marker reads about 9.93. "
                     "Those central values are retained separately. The difference is within the printed SD.",
             Fig3b_printed_and_plotted="The written 135-degree return is 0.660 +/- 0.012; the inset's 135-degree red "
                     "symbol is near 0.639. Both are preserved. Its plotted centre is still nearer the squared "
                     "prediction; the point estimates are not independent measurements.",
             Fig6b_offsite_control="At balanced angle 22.5 degrees the digitized offsite variance near 13.8 "
                     "is closer to 14.416 (local fourth) than 11.874 (squared). For the same setting the return "
                     "near 0.38 is closer to 0.398 (squared) than 0.449 (local fourth).",
             wrong_literal_adjoint_origin_tick4=literal[3],real_initial_alternative_135degrees_tick10=real_check,
             opposite_phase_and_conjugate_input_tick10=conjugate,
             efficiency_assumption="Ratio e_center/e_rest that would bring each prediction to the observed "
                     "conditional recurrence is computed holding all noncentre efficiencies common. These "
                     "ratios are sensitivity controls, not measured optical efficiencies.",
             selection="Published scalars take priority. No threshold, likelihood, sigma rejection, or raw-data "
                     "confidence interval is claimed. Some nonbalanced/offsite plotted variances are closer to "
                     "quartic; report all tabulated settings irrespective of which rule fits better."))
    out.mkdir(parents=True,exist_ok=True)
    target=out/"phase_defect_data.json"
    target.write_bytes((json.dumps(result,indent=1,default=str)+"\n").encode())
    print(target,hashlib.sha256(target.read_bytes()).hexdigest())


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("output_directory",type=Path)
    main(p.parse_args().output_directory)
