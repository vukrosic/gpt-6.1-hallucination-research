#!/usr/bin/env python3
"""Run the company example and its one-change versions in Codex CLI, one fresh conversation per run.

Each run folder  runs/<version>/rNN/  holds
  instructions.md   the instructions the agent was given
  records.json      the fictional records the tools serve
  turns.json        the user's messages, in order
  events.jsonl      Codex's event stream: every tool call with its result and every reply
  tool_log.jsonl    what the records server recorded
  reply_tN.txt      the agent's reply after message N
  meta.json         version, model, timing, exit codes, token use

Runs follow one shuffled schedule (SCHEDULE.json), so versions are interleaved. Finished runs are skipped.

usage: run.py [--repeats 10] [--control-repeats 4] [--jobs 6] [--budget 540] [--only base named]

Setup: copy codex_home_example/ to .work/codex_home and log in to Codex there
(CODEX_HOME=$PWD/.work/codex_home codex login). EVAL_CODEX_HOME points to another folder if needed.
"""
import argparse
import json
import os
import random
import shutil
import subprocess
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from conditions import CONTROLS, FIELD_CONTROLS, FIELD_SET, MAIN, TRANSFER, TRANSFER_CONTROLS, build

ROOT = Path(__file__).resolve().parent
RUNS = ROOT / "runs"
FAILED = ROOT / "runs_failed"
# An isolated Codex home: the two files from codex_home_example/ plus your own Codex login.
CODEX_HOME = Path(os.environ.get("EVAL_CODEX_HOME", ROOT / ".work" / "codex_home"))
CWD_ROOT = Path(tempfile.gettempdir()) / "company-hypotheses-cwd"   # outside every git repository
FAKE_HOME = ROOT / ".work" / "home"
CODEX = shutil.which("codex") or "codex"
MODEL, EFFORT = "gpt-6.1-sol", "low"
lock = threading.Lock()


def redact(text, thread_id=None):
    for path in (str(CWD_ROOT), os.path.realpath(str(CWD_ROOT))):
        text = text.replace(path, "<cwd>")
    for path in (str(ROOT), os.path.realpath(str(ROOT))):
        text = text.replace(path, "<study>")
    text = text.replace(str(Path.home()), "<home>")
    return text.replace(thread_id, "<thread>") if thread_id else text


def turn(rdir, cwd, prompt, n, thread_id):
    server = [str(ROOT / "records_server.py"), "--fixture", str(rdir / "records.json"),
              "--log", str(rdir / "tool_log.jsonl"), "--turn", str(n)]
    cmd = [CODEX, "exec", "-p", "agent", "-C", str(cwd)] + (["resume", thread_id] if thread_id else [])
    cmd += ["--json", "--skip-git-repo-check", "-o", str(rdir / f"reply_t{n}.txt"), "-m", MODEL,
            "-c", f'model_reasoning_effort="{EFFORT}"', "-c", 'model_reasoning_summary="none"',
            "-c", f'model_instructions_file="{rdir / "instructions.md"}"', "-c", "project_doc_max_bytes=0",
            "-c", "mcp_servers.world.args=" + json.dumps(server), prompt]
    env = dict(os.environ, CODEX_HOME=str(CODEX_HOME), HOME=str(FAKE_HOME))
    try:
        r = subprocess.run(cmd, env=env, cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, timeout=110)
        return r.returncode, r.stdout.decode(errors="replace"), r.stderr.decode(errors="replace")
    except subprocess.TimeoutExpired as e:
        return 124, (e.stdout or b"").decode(errors="replace"), "timeout"


def run_one(version, k):
    rdir = RUNS / version / f"r{k:02d}"
    if (rdir / "meta.json").exists():
        return None
    if rdir.exists():  # an unfinished attempt: keep it aside, start again from an empty folder
        FAILED.mkdir(exist_ok=True)
        shutil.move(str(rdir), str(FAILED / f"{version}__r{k:02d}__{int(time.time())}"))
    rdir.mkdir(parents=True)
    inst, records, turns = build(version)
    (rdir / "instructions.md").write_text(inst + "\n")
    (rdir / "records.json").write_text(json.dumps(records, ensure_ascii=False, indent=1) + "\n")
    (rdir / "turns.json").write_text(json.dumps([t for t in turns if t], ensure_ascii=False, indent=1) + "\n")
    cwd = CWD_ROOT / version / f"r{k:02d}_{int(time.time())}"
    cwd.mkdir(parents=True)
    t0, thread_id, out_all, err_all, codes, usage = time.time(), None, "", "", [], []
    for n, prompt in enumerate([t for t in turns if t], start=1):
        code, out, err = turn(rdir, cwd, prompt, n, thread_id)
        codes.append(code)
        out_all += out
        if err.strip() and err.strip() != "Reading additional input from stdin...":
            err_all += f"--- turn {n}\n{err}\n"
        for line in out.splitlines():
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("type") == "thread.started":
                thread_id = thread_id or ev.get("thread_id")
            elif ev.get("type") == "turn.completed":
                usage.append(ev.get("usage", {}))
        reply = rdir / f"reply_t{n}.txt"
        if code != 0 or not thread_id or not reply.exists() or not reply.read_text().strip():
            codes[-1] = code or 1
            break
    (rdir / "events.jsonl").write_text(redact(out_all, thread_id))
    if err_all:
        (rdir / "stderr.txt").write_text(redact(err_all, thread_id))
    ok = len(codes) == len([t for t in turns if t]) and not any(codes)
    meta = {"version": version, "run": k, "model": MODEL, "effort": EFFORT, "ok": ok, "exit_codes": codes,
            "seconds": round(time.time() - t0, 1), "usage": usage}
    if ok:
        (rdir / "meta.json").write_text(json.dumps(meta, indent=1) + "\n")
    else:  # keep the failed attempt, leave the slot open for a later retry
        FAILED.mkdir(exist_ok=True)
        (rdir / "meta_failed.json").write_text(json.dumps(meta, indent=1) + "\n")
        shutil.move(str(rdir), str(FAILED / f"{version}__r{k:02d}__{int(time.time())}"))
    with lock:
        print(f"{'ok  ' if ok else 'FAIL'} {version} r{k:02d} {meta['seconds']}s codes={codes}", flush=True)
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeats", type=int, default=10)
    ap.add_argument("--control-repeats", type=int, default=4)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--budget", type=int, default=540, help="seconds after which no new run starts")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--schedule", default="SCHEDULE.json")
    ap.add_argument("--transfer", action="store_true", help="school and pharmacy examples instead of the company one")
    ap.add_argument("--field", action="store_true", help="the third instruction sentence on all three examples")
    a = ap.parse_args()
    main_set, control_set = (TRANSFER, TRANSFER_CONTROLS) if a.transfer else (MAIN, CONTROLS)
    if a.field:
        main_set, control_set, a.schedule = FIELD_SET, FIELD_CONTROLS, "SCHEDULE_FIELD.json"
    if a.transfer and a.schedule == "SCHEDULE.json":
        a.schedule = "SCHEDULE_TRANSFER.json"
    FAKE_HOME.mkdir(parents=True, exist_ok=True)
    sched_path = ROOT / a.schedule
    if sched_path.exists():
        cells = [tuple(c) for c in json.loads(sched_path.read_text())]
    else:
        cells = [(v, k) for v in main_set for k in range(1, a.repeats + 1)]
        cells += [(v, k) for v in control_set for k in range(1, a.control_repeats + 1)]
        random.Random(20261012).shuffle(cells)
        sched_path.write_text(json.dumps(cells) + "\n")
    if a.only:
        cells = [c for c in cells if c[0] in a.only]
    todo = [c for c in cells if not (RUNS / c[0] / f"r{c[1]:02d}" / "meta.json").exists()]
    print(f"{len(cells) - len(todo)} of {len(cells)} done, {len(todo)} to go", flush=True)
    deadline = time.time() + a.budget

    def guarded(cell):
        if time.time() > deadline:
            return None
        return run_one(*cell)

    with ThreadPoolExecutor(a.jobs) as pool:
        list(pool.map(guarded, todo))
    left = [c for c in cells if not (RUNS / c[0] / f"r{c[1]:02d}" / "meta.json").exists()]
    print(f"left: {len(left)}", flush=True)


if __name__ == "__main__":
    main()
