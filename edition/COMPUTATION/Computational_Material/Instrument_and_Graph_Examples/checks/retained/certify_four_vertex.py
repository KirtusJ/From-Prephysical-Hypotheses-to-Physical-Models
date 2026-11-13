"""An exact rational contraction certificate for the single-pair four-vertex witness.
SymPy computes exact rational bounds. Numerical eigenvalue guesses only select brackets that are then certified.
"""
from pathlib import Path
import json
import sympy as sp

ROOT=Path(__file__).resolve().parent
x,y,z=sp.symbols('x y z')
variables=(x,y,z)
center=tuple(sp.Rational(t) for t in ['15.68999845828313460641124773061129857188423904485787',
 '3.96887190378120738276018210798761110889672715693172',
 '0.02356285637341516688523308001635257730023101101810'])
radius=sp.Rational(1,10**34)

def require(condition, message):
    if not condition:raise ArithmeticError(message)

def at(poly,c=center):
    return poly.eval(dict(zip(variables,c)))

def bound(poly):
    return sum(abs(coeff)*sp.prod((abs(c)+radius)**k for c,k in zip(center,powers)) for powers,coeff in poly.terms())

def range_poly(poly):
    midpoint=at(poly);error=radius*sum(bound(poly.diff(v)) for v in variables)
    return midpoint-error,midpoint+error

def add(A,B):return (A[0]+B[0],A[1]+B[1])
def diff(A,B):return (A[0]-B[1],A[1]-B[0])
def mul(A,B):
    values=[a*b for a in A for b in B];return min(values),max(values)
def div(A,B):
    require(B[0]*B[1]>0,'zero in interval denominator')
    return mul(A,(1/B[1],1/B[0]))

def enclosure(A,k):
    unit=10**k;return [str(sp.floor(A[0]*unit)/unit),str(sp.ceiling(A[1]*unit)/unit)]

def main():
    L=sp.zeros(4);base=sp.Rational(1,50)
    for (i,j),w in { (0,1):base,(0,2):x,(0,3):base,(1,2):y,(1,3):z,(2,3):base }.items():
        L[i,i]+=w;L[j,j]+=w;L[i,j]-=w;L[j,i]-=w
    S=sp.eye(4)[:,:3]-sp.eye(4)[:,3]*sp.ones(1,3);B=(L*S)[:3,:];C=S.T*S
    require(L*S==S*B,'zero-sum restriction')
    determinant=sp.Poly(B.det(),*variables);adj=B.adjugate();pair=sp.Matrix([1,-1,0]);v=pair
    target=[sp.Rational(5,32),sp.Rational(7,256),sp.Rational(11,2048)];polys=[];numerators=[]
    for k in range(1,5):
        v=(adj*v).applyfunc(sp.expand)
        num=sp.Poly((pair.T*C*v)[0]/2,*variables);numerators.append(num)
        if k<4:polys.append(num-target[k-1]*determinant**k)
    jac=sp.Matrix([[at(P.diff(v)) for v in variables] for P in polys]);inverse=jac.inv()
    displacement=max(abs(t) for t in inverse*sp.Matrix([at(P) for P in polys]))
    variation=sp.Matrix(3,3,lambda i,j:radius*sum(bound(polys[i].diff(variables[j]).diff(k)) for k in variables))
    product=inverse.applyfunc(abs)*variation
    contraction=max(sum(product[i,j] for j in range(3)) for i in range(3));det_bounds=range_poly(determinant)
    require(min(center)>radius and det_bounds[0]>0,'nonpositive edge or determinant')
    require(displacement<sp.Rational(1,10**48) and contraction<sp.Rational(1,10**19),'certificate thresholds')
    require(displacement+contraction*radius<radius,'box is not mapped into itself')
    m4=div(range_poly(numerators[3]),(det_bounds[0]**4,det_bounds[1]**4))
    require(m4[0]>sp.Rational(6804,10**6) and m4[1]<sp.Rational(6805,10**6),'fourth moment interval')
    # Rational brackets for all eigenvalues, independent of any root finder's reliability.
    t=sp.symbols('t');char=B.charpoly(t).as_expr();roots_at_center=sp.nroots(char.subs(dict(zip(variables,center))),n=36,maxsteps=100)
    eigenintervals=[]
    for guess in sorted(roots_at_center):
        a=sp.floor(guess*10**11)/10**11;b=a+sp.Rational(1,10**11)
        lo=range_poly(sp.Poly(char.subs(t,a),*variables));hi=range_poly(sp.Poly(char.subs(t,b),*variables))
        require(lo[1]*hi[1]<0 and lo[0]*hi[0]<0 and lo[0]*lo[1]>0 and hi[0]*hi[1]>0,'eigenvalue not bracketed')
        eigenintervals.append((a,b))
    require(all(eigenintervals[i][1]<eigenintervals[i+1][0] for i in [0,1]),'overlapping eigenvalue intervals')
    v=S*pair;first=range_poly(sp.Poly((v.T*L*v)[0]/2,*variables));second=range_poly(sp.Poly((v.T*L**2*v)[0]/2,*variables));weights=[]
    for i in range(3):
        a=eigenintervals[i];b,d=[eigenintervals[k] for k in range(3) if k!=i]
        num=add(diff(second,mul(add(b,d),first)),mul(b,d));den=mul(diff(a,b),diff(a,d));weights.append(div(num,den))
    require(min(v[0] for v in weights)>0,'uncoupled atom')
    # Preserve the queried single-pair response in a 16-site connected complete graph.
    eps=sp.Rational(3,500);tau=sp.Rational(1,100)
    Q4=sp.eye(4)-sp.ones(4)/4
    large=sp.zeros(16)
    large[:4,:4]=L-12*eps*Q4+12*eps*sp.eye(4)
    large[:4,4:]=-eps*sp.ones(4,12);large[4:,:4]=-eps*sp.ones(12,4)
    large[4:,4:]=tau*(12*sp.eye(12)-sp.ones(12))+4*eps*sp.eye(12)
    embed=sp.zeros(16,3);embed[:4,:]=S
    require(large*embed==embed*B and large*sp.ones(16,1)==sp.zeros(16,1),'16-site invariant subspace')
    require(base-3*eps>0 and min(center)-radius-3*eps>0,'16-site positivity')
    require(eigenintervals[0][1]<16*eps<12*tau+4*eps,'16-site lowest eigenvalue')
    moment_jac_det=jac.det()/at(determinant)**6
    result={'method':'Exact-rational contraction mapping on a closed sup-norm box, no external interval library',
       'center':[str(c) for c in center],'radius':str(radius),'displacement_strict_upper':'1e-48','jacobian_variation_infty_strict_upper':'1e-19',
       'actual_displacement_approx':str(sp.N(displacement,9)),'actual_contraction_bound_approx':str(sp.N(contraction,9)),
       'unknown_edges_in_order':['02','12','13'],'fixed_edges_01_03_23':'1/50','input':'(e0-e1)/sqrt(2)',
       'moments_m0_m1_m2_m3':['1','5/32','7/256','11/2048'],'alternative_m4_outward_rational':enclosure(m4,15),
       'original_m4':'19/16384','positive_eigenvalues_outward_rational':[enclosure(a,11) for a in eigenintervals],
       'pair_weights_outward_rational':[enclosure(a,13) for a in weights],'normalized_moment_jacobian_det_near_center':str(sp.N(moment_jac_det,10)),
       'sixteen_site_lift':{'vertices':16,'old_edge_change':'subtract 3 epsilon','cross_weights':str(eps),'new_clique_weight':str(tau),'extra_eigenvalues':{'12/125':1,'18/125':11},'single_pair_full_measure_preserved':True,'smallest_positive_eigenvalue_preserved':True},
       'scope':'Existence and uniqueness in this box with three specified edges fixed. Agreement concerns the one normalized pair, not graph-wide observations.'}
    ROOT.joinpath('graph_certificate.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Certified graph',result['actual_displacement_approx'],result['actual_contraction_bound_approx'],[float(a) for a in m4],[float(a) for a in weights[0]])

if __name__=='__main__':main()
