"""Test full-site readout and coherent coin-only postselection on the signed walk."""

import argparse
import cmath
import csv
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

from check_walk import fibre_step, positive_eigenvector


def integer_step(state):
    output = {}
    for (x, coin), amplitude in state.items():
        for direction in (1, -1):
            key = (x + direction, direction)
            gain = -1 if coin == direction == -1 else 1
            output[key] = output.get(key, 0) + gain * amplitude
    return output


def exact_filter_trials():
    rows = []
    state = {(0, 1): 1}
    for m in range(1, 41):
        state = integer_step(integer_step(state))
        direction = (-1)**m
        state = {key: value for key, value in state.items() if key[1] == direction}
        counts = {x: value for (x, _), value in state.items()}
        total = sum(value**2 for value in counts.values())
        centre = -(m % 2)
        support = range(centre-m, centre+m+1, 2)
        binomial_counts = [math.comb(m, j) for j in range(m+1)]
        weights = [counts.get(x, 0) for x in support]
        norm = math.comb(2*m, m)
        variance = Fraction(sum((x-centre)**2*v*v for x,v in counts.items()), total)
        correlations = {}
        for lag in (1, 2):
            correlations[lag] = Fraction(sum(v*counts.get(x+2*lag, 0) for x,v in counts.items()), total)
        sin_squared = (1+correlations[1])/2
        sin_fourth = (3+4*correlations[1]+correlations[2])/8
        # sin(q)^2=cos(k)^2, q measured relative to the nearest band edge.
        checks = dict(counts_match=all(abs(v)==b for v,b in zip(weights,binomial_counts)) and
                      all(a*b<0 for a,b in zip(weights,weights[1:])),
                      total_mass=total==norm, position_variance=variance==Fraction(m*m,2*m-1),
                      momentum_second=sin_squared==Fraction(1,2*m+2),
                      momentum_fourth=sin_fourth==Fraction(3,4*(m+1)*(m+2)))
        rows.append(dict(blocks=m, centre=centre, counts=weights, joint_probability=str(Fraction(total,4**m)),
                         position_variance=str(variance), sin_q_second=str(sin_squared),
                         sin_q_fourth=str(sin_fourth), checks=checks))
    return rows


def coherent_coin_sheet(m, order):
    """Full integer sheet counts on the line; prepare localized base in a tagged sector by Fourier evaluation."""
    state = {(0, 1, 0): 1}
    for block in range(1,m+1):
        for _ in range(2):
            new_state = {}
            for (x,c,y), a in state.items():
                for d in (1,-1):
                    key = (x+d, d, (y+x)%order)
                    new_state[key] = new_state.get(key,0) + (-a if c==d==-1 else a)
            state = new_state
        state = {key:v for key,v in state.items() if key[1]==(-1)**block}
    return state


def finite_field_trials():
    rows=[]
    grid = np.arange(256)*2*np.pi/256-np.pi
    for order in (5, 11, 31):
        for r in (1,(order-1)//2):
            h=2*np.pi*r/order
            for m in (1,2,4,8):
                sheet=coherent_coin_sheet(m,order)
                actual=np.zeros_like(grid,dtype=complex)
                for (x,_,y), count in sheet.items():
                    actual += (count/2**m)*cmath.exp(-1j*h*y)*np.exp(-1j*grid*x)
                k0=grid+2*m*h
                curve=np.ones_like(grid,dtype=complex)
                for j in range(m):
                    k1=k0-(2*j+1)*h
                    k2=k1-h
                    direction=(-1)**(j+1)
                    curve *= -1j*np.sin(k1)*np.exp(-1j*direction*k2)
                residual=float(np.max(abs(actual-curve)))
                shifted=grid+m*h
                proxy=abs(np.sin(shifted))**m
                changed=np.linalg.norm(abs(actual)-proxy)/np.sqrt(grid.size)
                allowed=m*(m-1)*abs(h)
                rows.append(dict(M=order,r=r,blocks=m,probability=float(np.mean(abs(actual)**2)),
                                 normalized_shape_change=float(changed/np.sqrt(np.mean(proxy**2))),
                                 direct_max_error=residual, finite_product_bound=allowed,
                                 amplitude_bound_holds=bool(np.max(abs(abs(actual)-proxy))<=allowed+1e-12)))
    return rows


def full_read_control():
    grid = np.arange(1024)*2*np.pi/1024-np.pi
    errors=[]
    for field in (0.,2*np.pi/13,12*np.pi/13):
        for coin in (0,1):
            spin=np.zeros((len(grid),2),complex)
            spin[:,coin]=np.exp(-3j*grid)
            for t in range(17):
                errors.append(float(np.max(abs(np.sum(abs(spin)**2,axis=1)-1))))
                spin=fibre_step(spin,grid-(t+1)*field)
    return errors


def flight_trials(writer):
    rows=[]
    mass_error = 0.
    mean_error = 0.
    for diagonal, order in ((flag,order) for flag in (True, False) for order in (127,509,2039,8179)):
        delta=(np.pi/order)**(1/(4 if diagonal else 3))
        action=delta if diagonal else 1.
        h=np.pi/order
        m=2*max(1,round(0.5/(delta**2*action**0.5)))
        n=math.floor(0.75/(action*delta**2))
        grid=np.arange(2048)*2*np.pi/2048-np.pi
        # Track log magnitude to avoid underflow of a long postselection product.
        with np.errstate(divide="ignore"):
            log_mag=np.zeros_like(grid)
            for j in range(m):
                log_mag+=np.log(abs(np.sin(grid+(2*j+1)*h)))
        w=np.exp(2*(log_mag-max(log_mag)))
        w/=sum(w)
        cone=(grid>=-np.pi) & (grid<0)
        u=positive_eigenvector(grid)
        bplus=abs(u[:,0])**2
        target_mass=float(w[cone] @ bplus[cone])
        window=float(w[abs(grid+np.pi/2)<delta].sum())
        characteristic_residuals = []
        for force_sign in (-1,1):
            # For negative h, reflection conjugates the density; symmetric cone/band totals
            # are computed directly on the reflected initial data.
            w0 = w if force_sign==1 else np.roll(w[::-1],1)
            # Preserve the signs of the spinor Fourier amplitudes for the position law.
            initial_sign = np.ones_like(grid)
            for j in range(m):
                initial_sign *= np.sign(np.sin(grid+(2*j+1)*force_sign*h))
            initial_mag = initial_sign*np.sqrt(w0)
            spin=np.zeros((len(grid),2),complex)
            spin[:,0]=1.
            disp=0.
            for t in range(n+1):
                tau=t*action*delta**2
                wave=np.fft.ifft(initial_mag[:,None]*spin,axis=0,norm="ortho")
                probability=np.sum(abs(wave)**2,axis=1)
                positions=np.fft.fftfreq(len(grid))*len(grid)*action*delta
                xi=3.0
                observed=probability @ np.exp(1j*xi*positions)
                # At the two parity-related edges two curvature signs have equal
                # asymptotic mass. Preparation accelerates the centre to -m*h/delta.
                central_ray=(m*h/delta*tau+tau**2/2)
                expected=np.cos(xi*central_ray)
                norm_sum = float(np.sum(probability))
                mean_position = float(positions @ probability)
                mass_error = max(mass_error,abs(norm_sum-1))
                mean_error = max(mean_error,abs(mean_position-action*delta*disp))
                if t==n:
                    characteristic_residuals.append(float(abs(observed-expected)))
                writer.writerow((order,diagonal,force_sign,m,t,tau,action*delta*disp,
                                 float(np.max(abs(np.sum(abs(spin)**2,axis=1)-1))),
                                 float(observed.real),float(observed.imag),float(expected),
                                 norm_sum,mean_position))
                disp+=w0 @ (2*np.real(np.conj(spin[:,0])*spin[:,1]))
                spin=fibre_step(spin,grid-(t+1)*force_sign*h)
        rows.append(dict(M=order,diagonal=diagonal,delta=delta,action=action,blocks=m,steps=n,
                         centre_shift_scaled=m*h/delta, cone_plus_mass=target_mass, single_chart_window=window,
                         terminal_two_ray_residuals=characteristic_residuals,
                         # Physical fields remain on throughout preparation.
                         joint_probability=float(np.exp(2*max(log_mag))*np.mean(np.exp(2*(log_mag-max(log_mag)))))))
    return rows, mass_error, mean_error


def main(out):
    out.mkdir(parents=True,exist_ok=True)
    exact=exact_filter_trials()
    field=finite_field_trials()
    flat=full_read_control()
    with (out/"band_preparation_flights.csv").open("w",encoding="utf8",newline="") as f:
        writer=csv.writer(f)
        writer.writerow(("M","diagonal","force_sign","blocks","flight_step","scaled_time","scaled_displacement","norm_error",
                         "position_characteristic_real_xi3","position_characteristic_imag_xi3",
                         "two_central_rays_characteristic_xi3","position_total","position_mean"))
        flights,mass_error,mean_error=flight_trials(writer)
    checks=dict(integer_recursions=all(all(row["checks"].values()) for row in exact),
                finite_field_amplitudes=all(row["direct_max_error"]<1e-12 and row["amplitude_bound_holds"] for row in field),
                full_read_flat=max(flat)<1e-13, cone_control=all(0<row["cone_plus_mass"]<0.5 for row in flights),
                flight_total_mass=mass_error<2e-12, flight_position_vs_current=bool(mean_error<2e-11))
    report=dict(checks=checks,exact_zero_field=exact,finite_field=field,
                full_read_flat_residuals=flat,prepared_flights=flights,
                maximum_flight_mass_error=mass_error, maximum_position_current_error=float(mean_error))
    (out/"band_preparation.json").write_text(json.dumps(report,indent=2,allow_nan=False)+"\n",encoding="utf8")
    print(checks)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("output",type=Path)
    main(parser.parse_args().output)
