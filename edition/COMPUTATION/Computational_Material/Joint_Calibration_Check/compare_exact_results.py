"""Compare supplied exact calibration outputs with the declared-model check.

This compares stored fractions; it does not itself run either probability
calculation. Use verify_declared_calibration_experiment.py in a new directory
to regenerate the declared-model result first.
"""
from pathlib import Path
from fractions import Fraction
import argparse
import hashlib
import json


def main():
    root=Path(__file__).resolve().parents[2]
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fresh',type=Path,default=Path(__file__).with_name('Declared_Calibration_Exact_Checks.json'))
    args=parser.parse_args()
    fresh=json.loads(args.fresh.read_text())
    material=root/'Related_Source_Editions/Assessment_and_Further_Results/computations/results'
    reports=[]
    for title,name,extra in [('primary','joint_calibration_results.json',True),('secondary','Joint_Calibration_Independent_Arithmetic.json',False)]:
        source=material/name;data=json.loads(source.read_text())
        rows={(r['p'],r['f'],r['s']):r for r in data['rows']}
        count=0;sets=0
        assert len(rows)==len(fresh['laws'])==45
        for r in fresh['laws']:
            law=r['law'];s=rows[law['p'],law['f'],law['s']]
            assert set(r['identified_targets'])==set(s['population_identified_set']);sets+=1
            def equal(a,b):
                nonlocal count
                if Fraction(a['fraction'])!=Fraction(b['fraction']):raise AssertionError((title,law,a,b))
                count+=1
            equal(r['true_law_admission'],s['true_joint_law_acceptance'])
            for method in ['joint','plugin','known']:
                equal(r['methods'][method]['whole_set_coverage'],s['whole_set_coverage'][method])
                assert set(r['methods'][method]['point_coverage'])==set(s['point_coverage'][method])
                for theta,val in r['methods'][method]['point_coverage'].items():equal(val,s['point_coverage'][method][theta])
                if extra:
                    for field in ['empty_probability','expected_cardinality']:equal(r['methods'][method][field],s[field][method])
        expected=639 if extra else 369
        if count!=expected:raise AssertionError((count,expected))
        reports.append({'source':source.relative_to(root).as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                        'exact_fraction_comparisons':count,'identified_sets_compared':sets,'mismatches':0})
    print(json.dumps({'fresh_result_sha256':hashlib.sha256(args.fresh.read_bytes()).hexdigest(),
                      'scope':'Stored exact-fraction and fibre comparisons, not new executions or independent replication.',
                      'comparisons':reports},indent=2))


if __name__=='__main__':main()
