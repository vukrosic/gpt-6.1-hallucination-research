"""Initialize a retrieval fixture and print messages for a manual model trial."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("run_id")
parser.add_argument("--control", action="store_true")
args = parser.parse_args()
if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", args.run_id):
    parser.error("Use a run ID containing only letters, digits, underscores or hyphens")
case = json.loads((ROOT / "scenarios/im15.json").read_text())
fixture = case["control_fixture"] if args.control else case["ground_truth"]["fixture"]
state_dir = ROOT / "src/mock_data"
state_dir.mkdir(exist_ok=True)
state_path = state_dir / (args.run_id + ".json")
with state_path.open("x") as handle:
    json.dump({"fixture": fixture, "log": []}, handle, ensure_ascii=False, indent=2)
    handle.write("\n")
client = ROOT / "src/visible/retrieval_client.py"
prompt = case["target_prompt"].replace("{run_id}", args.run_id).replace("/tmp/alex-assistant-workspace/client.py", str(client))
print("Send the following messages one at a time, after each final reply.\n")
for index, message in enumerate([prompt, *case["followups"]], start=1):
    print(f"MESSAGE {index}\n{message}\n")
