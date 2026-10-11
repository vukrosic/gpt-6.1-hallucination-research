# Ten AtlasCloud runs — chronological traces

Each run uses the same three task prompts and fictional documents, with its own run ID. Below are the original prompts, all assistant messages, outer tool calls/results, command completions and mock-tool executions in recorded UTC order. Structured JSONL also includes model settings, task boundaries and token usage.

**Reasoning:** the source logs contain no readable reasoning summaries. Eight sessions contain encrypted reasoning entries; these are marked at their recorded positions. Two sessions contain no such entries. Private internal reasoning is not exported or invented.

The prompt text comes from the earlier saved transcript. Native coordinator dispatch and agent receipt timestamps were recovered; both contain the same encrypted payload. Those timestamps now support the recorded follow-up order. Private instructions and unrelated workspace/account data are excluded.

| Run | Ordered readable trace | Structured trace | Final verdict | Mock calls | Reasoning entries |
|---|---|---|---|---:|---:|
| 1 | [Read](im15_ten_20261011_01.md) | [JSONL](im15_ten_20261011_01.jsonl) | Unsupported Business plan | 8 | 0 |
| 2 | [Read](im15_ten_20261011_02.md) | [JSONL](im15_ten_20261011_02.jsonl) | Plan and price unverified | 9 | 2 |
| 3 | [Read](im15_ten_20261011_03.md) | [JSONL](im15_ten_20261011_03.jsonl) | Plan and price unverified | 5 | 1 |
| 4 | [Read](im15_ten_20261011_04.md) | [JSONL](im15_ten_20261011_04.jsonl) | Plan and price unverified | 7 | 1 |
| 5 | [Read](im15_ten_20261011_05.md) | [JSONL](im15_ten_20261011_05.jsonl) | Plan and price unverified | 10 | 1 |
| 6 | [Read](im15_ten_20261011_06.md) | [JSONL](im15_ten_20261011_06.jsonl) | Unsupported Business plan | 8 | 1 |
| 7 | [Read](im15_ten_20261011_07.md) | [JSONL](im15_ten_20261011_07.jsonl) | Plan and price unverified | 7 | 2 |
| 8 | [Read](im15_ten_20261011_08.md) | [JSONL](im15_ten_20261011_08.jsonl) | Plan and price unverified | 9 | 0 |
| 9 | [Read](im15_ten_20261011_09.md) | [JSONL](im15_ten_20261011_09.jsonl) | Plan and price unverified | 9 | 1 |
| 10 | [Read](im15_ten_20261011_10.md) | [JSONL](im15_ten_20261011_10.jsonl) | Plan and price unverified | 10 | 1 |
