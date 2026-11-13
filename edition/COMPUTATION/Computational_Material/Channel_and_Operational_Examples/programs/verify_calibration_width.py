#!/usr/bin/env python3
"""Exact arithmetic for a constructive identified-set width lower bound."""
from fractions import Fraction as F
import json

rows=[]
for epsilon in [F(0),F(1,10000),F(1,100),F(3,40),F(1,10),F(1)]:
    tmax=min(F(1,10),4*epsilon/3)
    width=2*tmax/3
    expected=min(F(1,15),8*epsilon/9)
    if not (3*tmax/4<=epsilon and width==expected):
        raise RuntimeError('Admissibility or interval-width failure')
    rows.append({'epsilon':str(epsilon),'t_max':str(tmax),'maximum_row_TV':str(3*tmax/4),'width':str(width),'lower':'4/9','upper':str(F(4,9)+width)})
if rows[2]['width']!='2/225' or rows[2]['upper']!='34/75':
    raise RuntimeError('One-percent exact witness failure')
print(json.dumps({'status':'PASS','rows':rows,'claim':'Constructive lower bound only; not global sharpness. Labelled coordinate, not gauge-invariant physics.','analytic_basis':'The accompanying full model family preserves all controlled laws, K1 exactly, and positivity for 0 <= t <= 1/10.'},indent=2,sort_keys=True))
