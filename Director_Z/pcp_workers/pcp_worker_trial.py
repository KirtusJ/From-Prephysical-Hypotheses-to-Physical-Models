#!/usr/bin/env python3
"""PCP worker trial in the Director Z container: two model workers run through the ACR reference host (acr_host.Host of the ACR 1.0
implementation packet), each with the kernel card in context and its own PCP OS register, (1) nested: a Claude worker may delegate a
question to a local Qwen worker through a host tool, both invocations recorded; (2) asynchronous: a supervisor runs a Claude worker, a
Qwen worker and an exact enumerator concurrently and re-reads every output after exit.
Fixed before the run.  Question (the one of Director G's trial, for comparison): on Z/11Z with unit cycle edges, the shortest-path
distances from 0 of 3*1 and of (3^-1)*1; is the claim that both are at most 3 true?  Exact answer: 3 and 4; claim false.
Scoring of a reply, by this program: CORRECT if it contains the distances 3 and 4 and rejects the claim; otherwise INCORRECT.
Controls put to each worker alone: 17*23 (391); the inverse of 3 modulo 11 (4).
Writes pcp_worker_trial_result.json; refuses to overwrite."""
import hashlib, json, os, re, subprocess, sys, threading, time
OUT = "pcp_worker_trial_result.json"
if os.path.exists(OUT): sys.exit("refusing to overwrite " + OUT)
S = "/tmp/claude-0/-home-user/1b3e59a6-be8f-5e36-be7c-26b1885eea91/scratchpad"
IMPL = S + "/acrimpl/ACR_1.0_Implementation"; sys.path.insert(0, IMPL + "/TOOLS")
import acr_host
CARD = open(IMPL + "/KERNEL_CARD.md").read(); sha = lambda b: hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()
PCPOS = S + "/plug/servers/pcpos"; PCPCLI = S + "/pcpcli/pcpcli.py"
QUESTION = ("Independently calculate this finite case: on Z/11Z with unit cycle edges, what are the shortest-path distances from 0 of the image of unit displacement 1 "
            "under multiplication by 3 and under its multiplicative inverse? Is the claim that both distances are at most 3 true? Provide the calculation.")
def score(text):
    t = text.lower(); has = bool(re.search(r"\b3\b", t)) and bool(re.search(r"\b4\b", t)); rej = any(w in t for w in ("false", "refuted", "not true", "is not at most", "does not hold", "incorrect"))
    return "CORRECT" if has and rej else "INCORRECT"
def flat(system, messages, extra=""):
    parts = []
    if system: parts.append("[Method card supplied by the host]\n" + system)
    if extra: parts.append(extra)
    for m in messages: parts.append(("[Message]\n" if m["role"] == "user" else "[Your earlier reply]\n") + m["content"])
    return "\n\n".join(parts)
calls = []                                                   # every model invocation: who, prompt digest, reply digest, seconds
def claude_model(system, messages, tools_hint=""):
    prompt = flat(system, messages, tools_hint); t0 = time.time()
    r = subprocess.run(["claude", "-p", prompt, "--max-turns", "1"], capture_output=True, text=True, timeout=300, cwd=S + "/pcphost/empty")
    text = r.stdout.strip(); calls.append(dict(model="claude (headless CLI)", prompt_sha256=sha(prompt), reply_sha256=sha(text), seconds=round(time.time() - t0, 2), exit=r.returncode))
    m = re.search(r"^CALL consult_pcp_reviewer:\s*(\{.*\})\s*$", text, re.M)
    if m:
        try: return {"text": text, "tool_calls": [{"name": "consult_pcp_reviewer", "arguments": json.loads(m.group(1))}]}
        except Exception: pass
    return text
_llm = None; _llm_lock = threading.Lock()
def qwen_model(system, messages):
    global _llm
    with _llm_lock:
        if _llm is None:
            from llama_cpp import Llama
            _llm = Llama(model_path=S + "/pcphost/models/qwen.gguf", n_ctx=4096, n_threads=3, verbose=False, seed=1)
        msgs = ([{"role": "system", "content": system}] if system else []) + messages; t0 = time.time()
        out = _llm.create_chat_completion(messages=msgs, max_tokens=220, temperature=0.0)["choices"][0]["message"]["content"].strip()
    calls.append(dict(model="Qwen2.5-0.5B-Instruct GGUF Q4_0 (llama.cpp, local)", prompt_sha256=sha(json.dumps(msgs)), reply_sha256=sha(out), seconds=round(time.time() - t0, 2)))
    return out
def register(name, items):
    """A PCP OS register for one worker: begun by the program, the items recorded as artifacts whose digests the server computes, then verified."""
    d = S + "/pcphost/ws_" + name; os.makedirs(d, exist_ok=True)
    subprocess.run([PCPOS, "init", d + "/.pcp/register.jsonl", "--principal", "principal", "--name", name], capture_output=True, text=True)
    cl = [{"name": "acr_begin", "arguments": {}}] + [{"name": "acr_artifact", "arguments": {"text": t, "origin": o, "name": n}} for n, o, t in items]
    json.dump(cl, open(d + "/calls.json", "w")); env = dict(os.environ, CLAUDE_PLUGIN_ROOT=S + "/plug")
    r = subprocess.run([sys.executable, PCPCLI, d, d + "/calls.json"], capture_output=True, text=True, env=env, cwd=S + "/pcpcli")
    v = subprocess.run([PCPOS, "verify", d + "/.pcp/register.jsonl"], capture_output=True, text=True).stdout
    head = re.search(r"chain intact: (\d+) events, head ([0-9a-f]+)", v); prob = re.search(r"guards replayed: (\d+) problem", v)
    return dict(events=int(head.group(1)) if head else None, head=head.group(2) if head else None, guard_problems=int(prob.group(1)) if prob else None,
                written=r.stdout.count("WRITTEN"), register_sha256=sha(open(d + "/.pcp/register.jsonl", "rb").read()))
os.makedirs(S + "/pcphost/empty", exist_ok=True); R = {"kernel_card_sha256": sha(CARD), "host": "acr_host.Host of the ACR 1.0 implementation packet; registers by pcpos 1.0.22"}
# ---- controls: each worker alone, through a host with ACR adopted ----
ctrl = {}
for name, model in (("claude", claude_model), ("qwen", qwen_model)):
    rows = []
    for q, want in (("What is 17*23? Reply with the number.", "391"), ("What is the multiplicative inverse of 3 modulo 11? Reply with the number.", "4"), (QUESTION, None)):
        h = acr_host.Host(model, adopted=True); h._kernel = CARD; rep = h.user(q)["text"]
        rows.append(dict(question_sha256=sha(q), reply=rep[:400], verdict=("CORRECT" if want in rep else "INCORRECT") if want else score(rep)))
    ctrl[name] = rows; print(name, [r["verdict"] for r in rows], flush=True)
R["bounded_checks_each_worker_alone"] = ctrl
# ---- nested: parent Claude may consult child Qwen through a host tool ----
child_log = {}
def consult(question):
    ch = acr_host.Host(qwen_model, adopted=True); ch._kernel = CARD; ans = ch.user(question)["text"]; receipt = sha(os.urandom(16).hex() + ans)[:20]
    child_log.update(question=question, answer=ans, receipt=receipt, kernel_in_context=ch.system_text() is not None); return {"reviewer_reply": ans, "receipt_id": receipt}
HINT = ("[Host note] One tool exists: consult_pcp_reviewer, a separate reviewer model running under the same method card. To use it, reply with exactly one line and nothing else:\n"
        "CALL consult_pcp_reviewer: {\"question\": \"<the question you want checked>\"}\nYou will then receive its reply as data with a receipt ID. You decide whether to use it. "
        "In your final answer, state your own calculation, say what you did with the reviewer's reply if you asked for one, and quote the receipt ID if you received one.")
parent = acr_host.Host(lambda s, m: claude_model(s, m, HINT), tools={"consult_pcp_reviewer": acr_host.Tool(consult, kind="model")}, allow=lambda n, a: n == "consult_pcp_reviewer", adopted=True)
parent._kernel = CARD; ans = parent.user(QUESTION)["text"]
R["nested"] = dict(question=QUESTION, parent="claude (headless CLI)", child_model="Qwen2.5-0.5B-Instruct GGUF Q4_0", parent_chose_to_delegate=bool(child_log), child=child_log or None,
                   parent_answer=ans, parent_quotes_receipt=bool(child_log) and child_log["receipt"] in ans, host_log=parent.log, effects=parent.effects,
                   content_score=dict(parent=score(ans), child=score(child_log["answer"]) if child_log else None),
                   parent_register=register("parent_claude", [("kernel_card", "SUPPLIED", CARD), ("question", "SUPPLIED", QUESTION), ("answer", "PRODUCED", ans)]),
                   child_register=register("child_qwen", [("kernel_card", "SUPPLIED", CARD), ("question", "SUPPLIED", child_log.get("question", "")), ("answer", "PRODUCED", child_log.get("answer", ""))]) if child_log else None)
print("nested: delegated", bool(child_log), "| parent", score(ans), "| child", score(child_log["answer"]) if child_log else None, flush=True)
# ---- asynchronous: a supervisor runs three tasks at once and re-reads their outputs after exit ----
tasks = {}
def run(name, fn):
    t0 = time.time(); out = fn(); path = S + "/pcphost/out_" + name + ".txt"; open(path, "w").write(out); tasks[name] = dict(start=t0, end=time.time(), result_sha256=sha(out), path=path)
def enumerator():
    d = lambda k: min(k % 11, (-k) % 11); inv = next(x for x in range(1, 11) if 3 * x % 11 == 1); return json.dumps(dict(distance_of_3=d(3), inverse=inv, distance_of_inverse=d(inv), claim_both_at_most_3=d(3) <= 3 and d(inv) <= 3))
def w_claude(): h = acr_host.Host(claude_model, adopted=True); h._kernel = CARD; return h.user(QUESTION)["text"]
def w_qwen(): h = acr_host.Host(qwen_model, adopted=True); h._kernel = CARD; return h.user(QUESTION)["text"]
th = [threading.Thread(target=run, args=(n, f)) for n, f in (("claude", w_claude), ("qwen", w_qwen), ("enumerator", enumerator))]
[t.start() for t in th]; [t.join() for t in th]
ov = max(0.0, min(tasks["claude"]["end"], tasks["qwen"]["end"]) - max(tasks["claude"]["start"], tasks["qwen"]["start"]))
for n, t in tasks.items(): t["read_back_sha256"] = sha(open(t["path"]).read()); t["read_back_matches"] = t["read_back_sha256"] == t["result_sha256"]; t["seconds"] = round(t["end"] - t["start"], 2); t["verdict"] = score(open(t["path"]).read()) if n != "enumerator" else "EXACT"
R["asynchronous"] = dict(overlap_seconds_of_the_two_model_workers=round(ov, 2), tasks={n: {k: v for k, v in t.items() if k not in ("start", "end", "path")} for n, t in tasks.items()},
                         register=register("supervisor", [("kernel_card", "SUPPLIED", CARD)] + [("output_" + n, "PRODUCED", open(t["path"]).read()) for n, t in sorted(tasks.items())]))
R["model_invocations"] = calls
json.dump(R, open(OUT, "w"), indent=1); print(json.dumps({k: R[k] for k in ("asynchronous",)}, indent=1)[:1500])
