"""
Read evals/snapshots/results.json and report token compression per skill
against the terse control arm.
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

import tiktoken

ENCODING = tiktoken.get_encoding("o200k_base")
SNAPSHOT = Path(__file__).parent / "snapshots" / "results.json"


def count(text: str) -> int:
    return len(ENCODING.encode(text))


def stats(savings: list[float]) -> tuple[float, float, float, float, float]:
    return (
        statistics.median(savings),
        statistics.mean(savings),
        min(savings),
        max(savings),
        statistics.stdev(savings) if len(savings) > 1 else 0.0,
    )


def fmt_pct(value: float) -> str:
    sign = "−" if value < 0 else "+"
    return f"{sign}{abs(value) * 100:.0f}%"


def main() -> None:
    if not SNAPSHOT.exists():
        print(f"No snapshot at {SNAPSHOT}. Run `python evals/llm_run.py` first.")
        return

    data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    arms = data.get("arms", {})
    meta = data.get("metadata", {})

    baseline_outputs = arms.get("__baseline__", [])
    terse_outputs = arms.get("__terse__", [])
    if not baseline_outputs or not terse_outputs:
        print("_Snapshot chưa có output thật._")
        print(
            "_Cần `claude` CLI để sinh `evals/snapshots/results.json`. "
            "Chạy `python evals/llm_run.py` khi môi trường đã sẵn sàng._"
        )
        return

    baseline_tokens = [count(output) for output in baseline_outputs]
    terse_tokens = [count(output) for output in terse_outputs]

    print(f"_Generated: {meta.get('generated_at', '?')}_")
    print(
        f"_Model: {meta.get('model', '?')} · CLI: {meta.get('claude_cli_version', '?')}_"
    )
    print(f"_Prompt file: {meta.get('prompt_file', '?')}_")
    print("_Tokenizer: tiktoken o200k_base (approximation)_")
    print(f"_n = {meta.get('n_prompts', len(baseline_tokens))} prompts_")
    print()
    print("**Reference arms:**")
    print(f"- baseline: {sum(baseline_tokens)} tokens total")
    print(
        f"- terse control: {sum(terse_tokens)} tokens total "
        f"({fmt_pct(1 - sum(terse_tokens) / sum(baseline_tokens))} vs baseline)"
    )
    print()
    print("**Skills vs terse control:**")
    print()
    print("| Skill | Median | Mean | Min | Max | Stdev | Tokens (skill / terse) |")
    print("|-------|--------|------|-----|-----|-------|-------------------------|")

    rows = []
    for skill, outputs in arms.items():
        if skill in ("__baseline__", "__terse__"):
            continue
        skill_tokens = [count(output) for output in outputs]
        savings = [
            1 - (skill_token / terse_token) if terse_token else 0.0
            for skill_token, terse_token in zip(skill_tokens, terse_tokens)
        ]
        rows.append(
            (
                skill,
                *stats(savings),
                sum(skill_tokens),
                sum(terse_tokens),
            )
        )

    for skill, med, mean, low, high, stdev, skill_total, terse_total in sorted(
        rows, key=lambda row: -row[1]
    ):
        print(
            f"| **{skill}** | {fmt_pct(med)} | {fmt_pct(mean)} | {fmt_pct(low)} | "
            f"{fmt_pct(high)} | {stdev * 100:.0f}% | {skill_total} / {terse_total} |"
        )

    print()
    print("_Savings = `1 - skill_tokens / terse_tokens` per prompt._")
    print(f"_Source: {SNAPSHOT.name}. Refresh with `python evals/llm_run.py`._")


if __name__ == "__main__":
    main()
