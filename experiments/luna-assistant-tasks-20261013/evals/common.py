"""Shared paths and helpers for the eval scripts."""
import json
import os
import shutil
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Isolated Codex home: the two files of codex_home_example/ plus a login. Not committed.
CODEX_HOME = Path(os.environ.get("EVAL_CODEX_HOME") or ROOT / "codex_home")
WORK = ROOT / ".work"              # scratch: empty HOME for the agent, not committed
# The agent's working folder. It sits outside every git repository, because Codex reads AGENTS.md files
# from the folders above the working folder.
CWD_ROOT = Path(os.environ.get("EVAL_CWD_ROOT") or tempfile.gettempdir()) / "agent-overclaim-evals-cwd"
RUNS = ROOT / "runs"
PROMPTS = ROOT / "prompts"
CODEX = shutil.which("codex") or "codex"

DEFAULT_MODEL = "gpt-6-luna"
DEFAULT_EFFORT = "low"             # the model's own default reasoning level
VARIANTS = ("trap", "control")


def conditions():
    with open(ROOT / "conditions.toml", "rb") as f:
        return tomllib.load(f)


def scenarios():
    out = {}
    for p in sorted((ROOT / "scenarios").glob("*.toml")):
        with open(p, "rb") as f:
            sc = tomllib.load(f)
        sc["path"] = p
        out[sc["id"]] = sc
    return out


def brief_text(cond):
    return "\n".join((PROMPTS / f"{part}.md").read_text().strip() + "\n" for part in cond["parts"])


def codex_env():
    """Codex reads its config and login from CODEX_HOME; HOME points at an empty folder so that
    nothing from the developer's machine (skills, AGENTS.md, memories) reaches the model."""
    fake_home = WORK / "home"
    fake_home.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["CODEX_HOME"] = str(CODEX_HOME)
    env["HOME"] = str(fake_home)
    return env


def redact(text):
    """Machine paths out of anything that gets committed."""
    return (text.replace(str(CWD_ROOT), "<cwd>")
                .replace(os.path.realpath(str(CWD_ROOT)), "<cwd>")
                .replace(str(ROOT), "<repo>")
                .replace(os.path.realpath(str(ROOT)), "<repo>")
                .replace(str(Path.home()), "<home>"))
