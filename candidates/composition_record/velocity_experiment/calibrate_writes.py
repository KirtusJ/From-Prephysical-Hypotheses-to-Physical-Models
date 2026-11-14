"""Two identity-phase reference circuits for separate position-write calibrations.
Use --output NEW_DIRECTORY to export them. Standard library, exact rational laws.
"""
import argparse
from fractions import Fraction
from pathlib import Path
from runpy import run_path


BASE = run_path(str(Path(__file__).with_name("generate.py")))
WORDS = BASE["WORDS"]
PATTERNS = BASE["PATTERNS"]
require = BASE["require"]


def reference_circuit(source):
    lines = BASE["circuit"](source, (1, 1)).splitlines()
    require(lines.count("s q[0];") == 2, "intermediate pulse count")
    return "\n".join("id q[0];" if line == "s q[0];" else line for line in lines) + "\n"


def word_law(source, phases):
    """Exact probabilities for the signed-path circuit with each relative phase
    in {1, -1, i, -i}. A negative sign on an identity arm is Z dephasing's
    phase-flip branch. Use the same chronological encoding as the exported QASM.
    """
    from itertools import product
    values = {}
    for path in product((0,1),repeat=9):
        previous, amp, left_count = source, 1, 0
        marks = []
        for clock,rail in enumerate(path,1):
            if rail == previous == 1:
                amp = -amp
            previous = rail
            left_count += rail
            if clock % 3 == 0:
                marks.append(left_count % 4)
                if clock < 9 and rail:
                    amp *= phases[clock//3 - 1]
        key = (tuple(marks),previous)
        values[key] = values.get(key, 0) + amp
    result = {w:Fraction() for w in WORDS}
    for (w,_),a in values.items():
        result[w] += Fraction(int(a.real*a.real+a.imag*a.imag),512)
    require(sum(result.values()) == 1,"normalized word law")
    return result


def noisy_law(source, base_phases, eta1, eta2):
    """A local population-preserving write with real off-diagonal factor eta
    is the channel mixture (1+eta)/2 I and (1-eta)/2 conjugation by Z.
    """
    result = {w:Fraction() for w in WORDS}
    for e1,e2 in PATTERNS:
        weight = (1+e1*eta1)*(1+e2*eta2)/4
        law = word_law(source,(base_phases[0]*e1,base_phases[1]*e2))
        for w in WORDS:
            result[w] += weight*law[w]
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,help="write two new reference circuits in a fresh directory")
    output=parser.parse_args().output
    for source in (0,1):
        text=reference_circuit(source)
        # The small emitted-QASM interpreter has no id gate. Erasing exactly
        # the two identities is semantics-preserving for the ideal check.
        require(text.splitlines().count("id q[0];")==2,"two unaffected reference writes")
        raw=BASE["execute"](text.replace("id q[0];\n",""))
        require(all(Fraction(raw[w],512)==v for w,v in word_law(source,(1,1)).items()),
                "identity reference circuit vs signed paths")
        corners=[(Fraction(a),Fraction(b)) for a in (0,1) for b in (0,1)]
        for a,b in corners+[(Fraction(1,4),Fraction(3,5))]:
            direct=noisy_law(source,(1,1),a,b)
            for i,eta in enumerate((a,b)):
                same,_=BASE["turns"](direct,i,i+1)
                require(same==(5+eta)/8,"separate adjacent reference rates")
        for s,t in PATTERNS:
            phases=(s*1j,t*1j)
            f00=noisy_law(source,phases,Fraction(0),Fraction(0))
            # Every word is bilinear in eta1,eta2. Equality of three
            # corners eliminates both single-factor terms identically.
            for a,b in ((0,1),(1,0)):
                require(noisy_law(source,phases,Fraction(a),Fraction(b))==f00,
                        "quarter-turn word unexpectedly sees one write")
            p=noisy_law(source,phases,Fraction(1),Fraction(1,4))
            q=noisy_law(source,phases,Fraction(1,2),Fraction(1,2))
            require(p==q,"same-product rival")
    if output:
        output.mkdir(parents=True,exist_ok=False)
        for source,tag in [(0,"R"),(1,"L")]:
            (output/f"{tag}_I_I.qasm").write_bytes(reference_circuit(source).encode("ascii"))
    print("All 8 quarter-turn laws agree at (1,1/4) and (1/2,1/2).")
    print("I,I adjacent same-sign fractions = (5+eta1)/8 and (5+eta2)/8.")
    print("At eta1=1/4, eta2=3/5 the reference gives 21/32 and 7/10.")


if __name__=="__main__":
    main()
