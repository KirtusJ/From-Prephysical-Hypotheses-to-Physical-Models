#!/usr/bin/env python3
"""Follow-up to pcp_worker_trial.py.  In that run the Claude worker was offered the reviewer tool and did not use it, so the nested path
(a worker under the host calling a second worker under the host) was not exercised; that result is kept.  Here the person's message asks the
worker to obtain the reviewer's reply before answering and then to judge it.  Same host, card, question, scoring and registers.  The
control and asynchronous parts are not repeated.  Writes pcp_worker_trial_nested_result.json; refuses to overwrite."""
import hashlib, json, os, re, subprocess, sys, threading, time
OUT = "pcp_worker_trial_nested_result.json"
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
# ---- nested: parent Claude may consult child Qwen through a host tool ----
child_log = {}
def consult(question):
    ch = acr_host.Host(qwen_model, adopted=True); ch._kernel = CARD; ans = ch.user(question)["text"]; receipt = sha(os.urandom(16).hex() + ans)[:20]
    child_log.update(question=question, answer=ans, receipt=receipt, kernel_in_context=ch.system_text() is not None); return {"reviewer_reply": ans, "receipt_id": receipt}
HINT = ("[Host note] One tool exists: consult_pcp_reviewer, a separate reviewer model running under the same method card. To use it, reply with exactly one line and nothing else:\n"
        "CALL consult_pcp_reviewer: {\"question\": \"<the question you want checked>\"}\nYou will then receive its reply as data with a receipt ID. You decide whether to use it. "
        "In your final answer, state your own calculation, say what you did with the reviewer's reply if you asked for one, and quote the receipt ID if you received one.")
parent = acr_host.Host(lambda s, m: claude_model(s, m, HINT), tools={"consult_pcp_reviewer": acr_host.Tool(consult, kind="model")}, allow=lambda n, a: n == "consult_pcp_reviewer", adopted=True)
parent._kernel = CARD; ans = parent.user(QUESTION + " Before you answer, consult the separate reviewer once through the tool, then give your own calculation and say whether the reviewer's reply supports it.")["text"]
R["nested"] = dict(question=QUESTION, parent="claude (headless CLI)", child_model="Qwen2.5-0.5B-Instruct GGUF Q4_0", parent_chose_to_delegate=bool(child_log), child=child_log or None,
                   parent_answer=ans, parent_quotes_receipt=bool(child_log) and child_log["receipt"] in ans, host_log=parent.log, effects=parent.effects,
                   content_score=dict(parent=score(ans), child=score(child_log["answer"]) if child_log else None),
                   parent_register=register("parent_claude_2", [("kernel_card", "SUPPLIED", CARD), ("question", "SUPPLIED", QUESTION), ("answer", "PRODUCED", ans)]),
                   child_register=register("child_qwen_2", [("kernel_card", "SUPPLIED", CARD), ("question", "SUPPLIED", child_log.get("question", "")), ("answer", "PRODUCED", child_log.get("answer", ""))]) if child_log else None)
print("nested: delegated", bool(child_log), "| parent", score(ans), "| child", score(child_log["answer"]) if child_log else None, flush=True)
R["model_invocations"] = calls
json.dump(R, open(OUT, "w"), indent=1); print(json.dumps({k: v for k, v in R["nested"].items() if k not in ("host_log",)}, indent=1)[:2600])
