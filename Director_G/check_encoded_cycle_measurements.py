"""Reanalyze deposited four- and eight-position quantum-processor histograms."""
import argparse
import ast
from fractions import Fraction
import hashlib
from io import BytesIO
import json
from math import comb
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ARCHIVE_SHA = 'caeb0702714bc830c3fff572c2809f04995d19528bb2823caa695732ad9301af'
SOURCE = 'https://doi.org/10.15128/r15x21tf47n'
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'


def require(test, message):
    if not test:
        raise ValueError(message)


def count_tables(data, n):
    with ZipFile(BytesIO(data)) as wb:
        names = [s.get('name') for s in ET.fromstring(wb.read('xl/workbook.xml')).iter(NS+'sheet')]
        require(names[:2] == ['Simulator','ibmq_quito'], 'unrecognized worksheets')
        out = {}
        for idx,name in enumerate(names[:2],1):
            root = ET.fromstring(wb.read(f'xl/worksheets/sheet{idx}.xml'))
            numeric = {c.get('r'): Fraction(c.findtext(NS+'v')) for c in root.iter(NS+'c')
                       if c.get('t') != 's' and c.findtext(NS+'v') is not None}
            rows = []
            for t in range(n+1):
                col = chr(ord('C')+t)
                values = [1000*numeric[f'{col}{j+5}'] for j in range(n)]
                counts = [round(v) for v in values]
                require(all(abs(v-k)<Fraction(1,10**9) for k,v in zip(counts,values))
                        and sum(counts)==1000 and min(counts)>=0, 'not a 1000-shot row')
                rows.append(counts)
            out[name] = rows
        return out


def source_measurements(code):
    module = ast.parse(code)
    build, = [n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='Build']
    loop, = build.body
    require(isinstance(loop,ast.For), 'expected a loop over steps')
    measures = [n for n in ast.walk(loop) if isinstance(n,ast.Call)
                and isinstance(n.func,ast.Attribute) and n.func.attr=='measure']
    targets = sorted((a.slice.value,b.slice.value) for a,b in (node.args for node in measures))
    require(targets==[(0,2),(1,1),(2,0)], 'expected three repeated measurements')
    return targets


def literal_shift():
    """Matrix expansion of the published cnx recursion on logical (position, coin)."""
    import numpy as np
    unitary = np.eye(16,dtype=complex)

    def gate(control, target, matrix):
        for i in range(16):
            if i & (1<<target) or (control is not None and not i & (1<<control)):
                continue
            pair = [i, i+(1<<target)]
            unitary[pair,:] = matrix @ unitary[pair,:]

    flip = np.array([[0,1],[1,0]])
    def cnx(*bits):
        if len(bits)==2:
            gate(*bits,flip)
            return
        c,t = bits[-2:]
        def rz(theta):
            gate(c,t,np.diag([np.exp(-.5j*theta),np.exp(.5j*theta)]))
        def real_u(theta):
            z = theta/2
            gate(c,t,np.array([[np.cos(z),-np.sin(z)],[np.sin(z),np.cos(z)]]))
        rz(np.pi/2)
        real_u(np.pi/2)
        cnx(*bits[:-2],t)
        real_u(-np.pi/2)
        cnx(*bits[:-2],t)
        rz(-np.pi/2)

    # qr[2], qr[1], qr[0] have place values 1, 2, 4 in the printed position.
    cnx(3,0,1,2)
    cnx(3,0,1)
    cnx(3,0)
    gate(None,3,flip)
    gate(None,0,flip)
    gate(None,1,flip)
    cnx(3,0,1,2)
    gate(None,1,flip)
    cnx(3,0,1)
    gate(None,0,flip)
    cnx(3,0)
    gate(None,3,flip)
    edges = []
    for i in range(16):
        coin,x = divmod(i,8)
        y = (x+(1 if coin else -1))%8
        target = 8*coin+y
        phase = min((1,1j,-1,-1j),key=lambda z:abs(unitary[target,i]-z))
        ideal = np.zeros(16,dtype=complex)
        ideal[target] = phase
        require(np.max(np.abs(unitary[:,i]-ideal))<1e-12,'not a phased shift')
        edges.append([coin,x,y,round(phase.real),round(phase.imag)])
    return edges


def coherent(steps, edges):
    state = [0j]*16
    state[0] = 1
    for _ in range(steps):
        nxt = [0j]*16
        for coin,x,y,a,b in edges:
            amp = state[x] + (1 if coin==0 else -1)*state[8+x]
            nxt[8*coin+y] = amp * complex(a,b)
        state = nxt
    weights = [round(state[x].real**2+state[x].imag**2+
                     state[8+x].real**2+state[8+x].imag**2) for x in range(8)]
    require(sum(weights)==2**steps, 'lost coherent norm')
    return weights


def tv(counts, numerators, denominator):
    return sum(abs(Fraction(r,1000)-Fraction(p,denominator))
               for r,p in zip(counts,numerators))/2


def analyze(path):
    require(hashlib.sha256(path.read_bytes()).hexdigest()==ARCHIVE_SHA,'unexpected archive')
    with ZipFile(path) as archive:
        digests = {n:hashlib.sha256(archive.read(n)).hexdigest() for n in archive.namelist()}
        books = {n:count_tables(archive.read(f'{n}_node_DTQW_data.xlsx'),n) for n in (4,8)}
        wiring = source_measurements(archive.read('8_node_DTQW_code.py').decode())
    edges = literal_shift()
    plain = [[c,x,y,1,0] for c,x,y,a,b in edges]
    results = {}
    for n,tables in books.items():
        panel = []
        for t,(sim,device) in enumerate(zip(tables['Simulator'],tables['ibmq_quito'])):
            row = {'step':t,'simulator':sim,'quito':device,
                   'simulator_wrong_parity':sum(sim[1-t%2::2]),
                   'quito_wrong_parity':sum(device[1-t%2::2])}
            if n==8:
                normalizer = 2**t
                monitored = [sum(comb(t,k) for k in range(t+1) if (2*k-t)%8==x) for x in range(8)]
                nominal = coherent(t,plain)
                literal = coherent(t,edges)
                row.update(ideal_denominator=normalizer, monitored_numerators=monitored,
                           coherent_plain_numerators=nominal, coherent_archived_shift_numerators=literal,
                           simulator_TV_monitored=str(tv(sim,monitored,normalizer)),
                           simulator_TV_plain=str(tv(sim,nominal,normalizer)),
                           simulator_TV_archived_coherent=str(tv(sim,literal,normalizer)))
            panel.append(row)
        results[str(n)] = panel
    return {'deposit':SOURCE,'archive_sha256':ARCHIVE_SHA,'member_sha256':digests,
            'entry_kind':'Integer equivalents of workbook probabilities; configured shots = 1000. Step zero is a listed initial row.',
            'position_qr_to_classical_bit':wiring,
            'eight_site_shift_coin_source_destination_phase_real_imag':edges,'cycles':results}


if __name__=='__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('archive',type=Path)
    ap.add_argument('output',type=Path)
    args = ap.parse_args()
    results = analyze(args.archive)
    with args.output.open('x',encoding='utf8',newline='\n') as f:
        json.dump(results,f,indent=2)
        f.write('\n')
