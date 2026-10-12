"""The six failing examples, each with no added sentence and with one of four short general sentences.

Written before any of these runs. The examples are unchanged:
  company, pharm                    from first_study.py  (a copy of codex-cli-causes-and-fixes-20261012/conditions.py)
  dental, climbing, books, person   from new_examples.py (a copy of fix-on-new-examples-20261012/conditions.py)

Version names: <example>_<arm>; a name ending in _own is a check task, where the records do hold the asked-for fact.
"""
import first_study
import new_examples

# Each sentence is added to the end of the first paragraph of the agent's instructions. Nothing else changes.
SENTENCE = {
    "correct": "State facts correctly.",
    "nomakeup": "Do not make things up.",
    "unknown": "You are allowed to say that you do not know.",
    "ask": "Ask the user when something is unclear.",
}
EXAMPLES = ["company", "pharm", "dental", "climbing", "books", "person"]
ARMS = ["base"] + list(SENTENCE)
MAIN = [f"{e}_{arm}" for e in EXAMPLES for arm in ARMS]
CONTROLS = [f"{e}_{arm}_own" for e in EXAMPLES for arm in SENTENCE]
TRANSFER, TRANSFER_CONTROLS, FIELD_SET, FIELD_CONTROLS = [], [], [], []


def build(name):
    """Return (instructions, records, turns) for a version."""
    own = "_own" if name.endswith("_own") else ""
    example, arm = (name[:-4] if own else name).split("_")
    if example == "company":
        inst, rec, turns = first_study.build("base" + own)
    elif example == "pharm":
        inst, rec, turns = first_study.build("pharm_base" + own)
    else:
        inst, rec, turns = new_examples.build(f"{example}_base{own}")
    if arm != "base":
        head, sep, facts = inst.partition("\n\n")
        inst = head + " " + SENTENCE[arm] + sep + facts
    return inst, rec, turns
