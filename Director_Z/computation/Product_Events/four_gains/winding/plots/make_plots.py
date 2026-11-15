"""Write the inputs of three exact plots from the result files of this folder, render them with the PCP OS plot
instrument (pcpos plot, host built from pcp-os commit e8d62e4, branch director-g/science-math-svg) and check each
SVG with the instrument visualization.ranges. Values are copied from the result files, not recomputed, except
plot 3, which is counted here by exact propagation. Usage: python3 make_plots.py PCPOS_PLOT_BINARY  (run in plots/;
refuses to overwrite)."""
import json, sys, os, subprocess, hashlib, collections
B = sys.argv[1]
def rd(f): return json.load(open(os.path.join("..", f)))
def dims(prefix, cuts, T0):
    out = []
    for c in cuts:
        r = rd(prefix % c)["restricted"]
        if T0 <= len(r): out.append([c, r[T0 - 1]["solution_dim"], r[T0 - 1]["solution_dim"]])
    return out
cuts = list(range(6, 15))
p1 = {"title": "Rules left on a ring of 4 sites, three classes", "provenance": "mathematics",
      "source": "winding_truncated_general.py, Z2 x Z3, exact ranks modulo 1000003", "x_label": "Longest event length used (cut)",
      "y_label": "Dimension of rules on early multisets", "x_domain": [5, 15], "y_domain": [0, 21],
      "series": [{"name": "Multisets first seen by length 5", "data": dims("result_general_N4_K3_T%d.json", cuts, 5)},
                 {"name": "Multisets first seen by length 6", "data": dims("result_general_N4_K3_T%d.json", cuts, 6)},
                 {"name": "Multisets first seen by length 7", "data": dims("result_general_N4_K3_T%d.json", cuts, 7)},
                 {"name": "Count and two squares", "data": [[c, 3, 3] for c in cuts]}]}
p2 = {"title": "Rules left on a ring of 3 sites, by classes", "provenance": "mathematics",
      "source": "Multisets first seen by length 7; exact ranks modulo 1000003", "x_label": "Longest event length used (cut)",
      "y_label": "Dimension of rules on early multisets", "x_domain": [7, 12], "y_domain": [0, 24],
      "series": [{"name": "One class (known rules: 2)", "data": dims("result_general_N3_K1_T%d.json", [9, 10], 7)},
                 {"name": "Two classes (known rules: 3)", "data": dims("result_general_N3_K4_T%d.json", [9, 10], 7)},
                 {"name": "Three classes (known rules: 3)", "data": dims("result_truncated_followup_T%d.json", [8, 9, 10, 11], 7)}]}
# plot 3: all walks of length 12 on the ring of 4 sites, vertex (0,R): number of walks by number of left steps
N, T = 4, 12
st = collections.Counter({(0, 0, 0): 1})
for _ in range(T):
    new = collections.Counter()
    for (x, r, l), c in st.items():
        new[((x + 1) % N, 0, l)] += c; new[((x - 1) % N, 1, l + 1)] += c
    st = new
prof = sorted((l, c) for (x, r, l), c in st.items() if (x, r) == (0, 0))
assert all(prof[i][1] * (prof[i][1] - 1) >= prof[i - 1][1] * prof[i + 1][1] for i in range(1, len(prof) - 1))
assert all(prof[i + 1][0] - prof[i][0] == 2 for i in range(len(prof) - 1))
p3 = {"title": "Walks at one vertex by number of left steps", "provenance": "mathematics",
      "source": "All walks of length 12 on the ring of 4 sites, vertex (0,R); exact count", "x_label": "Number of left steps",
      "y_label": "Number of walks", "x_domain": [-1, 13], "y_domain": [0, max(c for _, c in prof) + 40],
      "series": [{"name": "Count (levels differ by M = 2)", "data": [[l, c, c] for l, c in prof]}]}
rec = {"host": B, "host_sha256": hashlib.sha256(open(B, "rb").read()).hexdigest(), "plots": []}
for name, p in (("dimension_ring4_three_classes", p1), ("dimension_ring3_by_classes", p2), ("winding_profile_ring4", p3)):
    js, svg = name + ".json", name + ".svg"
    assert not os.path.exists(js) and not os.path.exists(svg)
    raw = json.dumps(p, indent=1).encode(); open(js, "xb").write(raw)
    r = subprocess.run([B, "plot"], input=raw, capture_output=True)
    assert r.returncode == 0, r.stderr.decode()[:400]
    open(svg, "xb").write(r.stdout); d = hashlib.sha256(r.stdout).hexdigest()
    c = subprocess.run([B, "instrument", "visualization.ranges", json.dumps({"plot": p, "expected_svg_sha256": d})], capture_output=True, text=True)
    open(name + ".receipt.txt", "x").write(c.stdout + c.stderr + "exit %d\n" % c.returncode)
    rec["plots"].append({"name": name, "input_sha256": hashlib.sha256(raw).hexdigest(), "svg_sha256": d, "instrument_exit": c.returncode, "rows": sum(len(s["data"]) for s in p["series"])})
json.dump(rec, open("plots_record.json", "x"), indent=1); print(json.dumps(rec["plots"], indent=1)); print(prof)
