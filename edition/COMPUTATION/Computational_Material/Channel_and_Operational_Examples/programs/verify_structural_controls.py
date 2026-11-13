"""Fresh exact controls for the scoped structural dependency audit.

These are finite mathematical checks and analytic proof controls, not physical
observations or an audit of the entire supplied research corpus.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json


def require(name, truth):
    if not truth:
        raise RuntimeError(name)
    return name


def binary_structures(n):
    pairs = list(product(range(n), repeat=2))
    for mask in range(1 << (n*n)):
        yield {p for i, p in enumerate(pairs) if mask >> i & 1}


def hom_count(n, relation, m, target):
    return sum(all((f[a], f[b]) in target for a, b in relation)
               for f in product(range(m), repeat=n))


def partition_pairs(n):
    def rec(labels):
        if len(labels) == n:
            yield {(i, j) for i in range(n) for j in range(n)
                   if labels[i] == labels[j]}
            return
        for x in range(max(labels, default=-1)+2):
            yield from rec(labels+[x])
    yield from rec([])


def induced_output(relations, f, n):
    return {(i, j) for i in range(n) for j in range(n)
            if i == j or f[sum((int((i, j) in r) << k)
                              for k, r in enumerate(relations))]}


def transitive(r, n):
    return all((i, k) in r for i in range(n) for j in range(n)
               for k in range(n) if (i, j) in r and (j, k) in r)


report = {'evidence_kind': 'fresh exact finite controls with separate analytic reductions'}
full2 = set(product(range(2), repeat=2))
full1 = {(0, 0)}
counts = []
for n in (1, 2, 3):
    for relation in binary_structures(n):
        require('all maps to full two-point target',
                hom_count(n, relation, 2, full2) == 2**n)
        require('exactly one map to full singleton',
                hom_count(n, relation, 1, full1) == 1)
    require('empty-relation singleton has n target arrows',
            all(hom_count(1, set(), n, target) == n
                for target in binary_structures(n)))
    counts.append({'carrier_size': n, 'binary_relations_examined': 2**(n*n),
                   'arrows_to_full_two_point_target': 2**n})
report['initiality_controls'] = counts

triples = list(partition_pairs(3))
natural_candidates = {}
for arity in (2, 3):
    accepted = []
    inputs = list(product(triples, repeat=arity))
    for mask in range(1 << (1 << arity)):
        f = tuple((mask >> i) & 1 for i in range(1 << arity))
        if all(transitive(induced_output(rs, f, 3), 3) for rs in inputs):
            accepted.append(mask)
    predicted = [0]
    for subset in range(1 << arity):
        predicted.append(sum(1 << pair_bits for pair_bits in range(1 << arity)
                             if pair_bits & subset == subset))
    require('classification on triple controls', sorted(accepted) == sorted(predicted))
    require('number is 2**arity+1', len(accepted) == 2**arity+1)
    natural_candidates[str(arity)] = {'accepted_truth_tables': accepted,
                                     'expected_count': 2**arity+1,
                                     'input_partition_tuples': len(inputs)}
report['deterministic_natural_operation_controls'] = natural_candidates

top = (0, 1)
left = ('a',)
right = ('b',)
families = [(x, a, b) for x, a, b in product(top, left, right)]
require('top-fiber count survives compatible restrictions', len(families) == len(top) == 2)
report['greatest_context_control'] = {'top_fiber_size': 2, 'limit_size': 2,
                                     'lower_fiber_sizes': [1, 1]}
report['surjection_probability_control'] = {
    'uniform_three_pushforward': [str(F(2,3)), str(F(1,3))],
    'uniform_two': [str(F(1,2)), str(F(1,2))],
    'total_variation': str(F(1,6))}

# Positive row-stochastic visible kernels, hidden kernels and product lifting.
visible = [[[F(3,4), F(1,4)], [F(1,3), F(2,3)]],
           [[F(1,5), F(4,5)], [F(2,5), F(3,5)]]]
hidden = [[[F(1,2), F(1,2)], [F(1,4), F(3,4)]],
          [[F(3,5), F(2,5)], [F(2,7), F(5,7)]]]
for a in range(2):
    lifted = [[visible[a][x][xp]*hidden[a][z][zp]
               for xp, zp in product(range(2), repeat=2)]
              for x, z in product(range(2), repeat=2)]
    for x, z, xp in product(range(2), repeat=3):
        require('actionwise exact strong lumping',
                sum(lifted[2*x+z][2*xp+zp] for zp in range(2)) == visible[a][x][xp])
report['controlled_hidden_lift'] = {
    'visible_state_count': 2, 'lifted_state_count': 4,
    'action_count': 2,
    'all_actionwise_fiber_sums_equal_visible_kernels': True,
    'scope': 'Induction gives all visible history laws for common observed-history policies and common visible starts; hidden starts may vary. No distinct physical ontology is inferred.'}
report['limitations'] = [
    'Finite enumeration alone does not establish all-size structural naturality.',
    'The all-size deterministic classification uses an analytic reduction to pair truth tables and triple transitivity, provided separately.',
    'No apparatus, probabilities or physical states are selected by these structural checks.',
    'Common model lineage and supplied-source exposure; no independent empirical replication.'
]
report['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(Path(__file__).resolve().parents[1]/'results'/'Structural_Controls.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
