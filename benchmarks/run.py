#!/usr/bin/env python3
"""Benchmark `gon` vs a normal assistant on Vietnamese technical prompts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import anthropic

_env_file = Path(__file__).parent.parent / ".env.local"
if _env_file.exists():
    for line in _env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

SCRIPT_VERSION = "1.1.0"
SCRIPT_DIR = Path(__file__).parent
REPO_DIR = SCRIPT_DIR.parent
PROMPTS_PATH = SCRIPT_DIR / "prompts.json"
SKILL_PATH = REPO_DIR / "skills" / "gon" / "SKILL.md"
README_PATH = REPO_DIR / "README.md"
RESULTS_DIR = SCRIPT_DIR / "results"

NORMAL_SYSTEM = "You are a helpful technical assistant. Answer in clear Vietnamese."
BENCHMARK_START = "<!-- BENCHMARK-TABLE-START -->"
BENCHMARK_END = "<!-- BENCHMARK-TABLE-END -->"
MODEL_ENV = "GON_BENCHMARK_MODEL"
DEFAULT_MODEL = "claude-sonnet-4-5"


def load_prompts() -> list[dict[str, str]]:
    return json.loads(PROMPTS_PATH.read_text(encoding="utf-8"))["prompts"]


def load_gon_system() -> str:
    return SKILL_PATH.read_text(encoding="utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def call_api(
    client: anthropic.Anthropic,
    model: str,
    system: str,
    prompt: str,
    *,
    max_retries: int = 3,
) -> dict[str, object]:
    delays = [5, 10, 20]
    for attempt in range(max_retries + 1):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=4096,
                temperature=0,
                system=system,
                messages=[{"role": "user", "content": prompt}],
            )
            return {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "text": response.content[0].text,
                "stop_reason": response.stop_reason,
            }
        except anthropic.RateLimitError:
            if attempt >= max_retries:
                raise
            delay = delays[min(attempt, len(delays) - 1)]
            print(f"  Rate limited. Retry in {delay}s...", file=sys.stderr)
            time.sleep(delay)


def run_benchmarks(
    client: anthropic.Anthropic,
    model: str,
    prompts: list[dict[str, str]],
    gon_system: str,
    trials: int,
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    total = len(prompts)

    for index, prompt_entry in enumerate(prompts, 1):
        prompt_id = prompt_entry["id"]
        prompt_text = prompt_entry["prompt"]
        entry: dict[str, object] = {
            "id": prompt_id,
            "category": prompt_entry["category"],
            "prompt": prompt_text,
            "normal": [],
            "gon": [],
        }

        for mode, system in [("normal", NORMAL_SYSTEM), ("gon", gon_system)]:
            for trial in range(1, trials + 1):
                print(
                    f"  [{index}/{total}] {prompt_id} | {mode} | trial {trial}/{trials}",
                    file=sys.stderr,
                )
                result = call_api(client, model, system, prompt_text)
                entry[mode].append(result)
                time.sleep(0.5)

        results.append(entry)

    return results


def compute_stats(results: list[dict[str, object]]) -> tuple[list[dict[str, object]], dict[str, int]]:
    rows: list[dict[str, object]] = []
    all_savings: list[float] = []

    for entry in results:
        normal_median = statistics.median(
            [trial["output_tokens"] for trial in entry["normal"]]  # type: ignore[index]
        )
        gon_median = statistics.median(
            [trial["output_tokens"] for trial in entry["gon"]]  # type: ignore[index]
        )
        savings = 1 - (gon_median / normal_median) if normal_median > 0 else 0
        all_savings.append(savings)

        rows.append(
            {
                "id": entry["id"],
                "category": entry["category"],
                "prompt": entry["prompt"],
                "normal_median": int(normal_median),
                "gon_median": int(gon_median),
                "savings_pct": round(savings * 100),
            }
        )

    avg_savings = round(statistics.mean(all_savings) * 100)
    min_savings = round(min(all_savings) * 100)
    max_savings = round(max(all_savings) * 100)
    avg_normal = round(statistics.mean([row["normal_median"] for row in rows]))
    avg_gon = round(statistics.mean([row["gon_median"] for row in rows]))

    return rows, {
        "avg_savings": avg_savings,
        "min_savings": min_savings,
        "max_savings": max_savings,
        "avg_normal": avg_normal,
        "avg_gon": avg_gon,
    }


def format_prompt_label(prompt_id: str) -> str:
    labels = {
        "react-rerender": "Bug React re-render",
        "auth-middleware-fix": "Bug auth middleware JWT",
        "postgres-pool": "Pool PostgreSQL Node.js",
        "git-rebase-merge": "Git rebase vs merge",
        "async-refactor": "Refactor callback -> async/await",
        "microservices-monolith": "Monolith vs microservices",
        "pr-security-review": "Security review Express route",
        "docker-multi-stage": "Docker multi-stage build",
        "race-condition-debug": "Race condition PostgreSQL counter",
        "error-boundary": "React error boundary",
    }
    return labels.get(prompt_id, prompt_id)


def format_table(rows: list[dict[str, object]], summary: dict[str, int]) -> str:
    lines = [
        "| Task | Normal (tokens) | Gon (tokens) | Saved |",
        "|------|----------------:|-------------:|------:|",
    ]
    for row in rows:
        lines.append(
            f"| {format_prompt_label(str(row['id']))} | "
            f"{row['normal_median']} | {row['gon_median']} | {row['savings_pct']}% |"
        )
    lines.append(
        f"| **Average** | **{summary['avg_normal']}** | **{summary['avg_gon']}** | "
        f"**{summary['avg_savings']}%** |"
    )
    lines.append("")
    lines.append(
        f"*Range: {summary['min_savings']}%–{summary['max_savings']}% savings across prompts.*"
    )
    return "\n".join(lines)


def save_results(
    results: list[dict[str, object]],
    rows: list[dict[str, object]],
    summary: dict[str, int],
    model: str,
    trials: int,
    skill_hash: str,
) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    payload = {
        "metadata": {
            "script_version": SCRIPT_VERSION,
            "model": model,
            "date": datetime.now(timezone.utc).isoformat(),
            "trials": trials,
            "skill_md_sha256": skill_hash,
        },
        "summary": summary,
        "rows": rows,
        "raw": results,
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = RESULTS_DIR / f"benchmark_{timestamp}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def update_readme(table_md: str) -> None:
    content = README_PATH.read_text(encoding="utf-8")
    start_index = content.find(BENCHMARK_START)
    end_index = content.find(BENCHMARK_END)
    if start_index == -1 or end_index == -1:
        print("ERROR: benchmark markers not found in README.md", file=sys.stderr)
        sys.exit(1)

    before = content[: start_index + len(BENCHMARK_START)]
    after = content[end_index:]
    README_PATH.write_text(before + "\n" + table_md + "\n" + after, encoding="utf-8")
    print("README.md updated.", file=sys.stderr)


def dry_run(prompts: list[dict[str, str]], model: str, trials: int) -> None:
    print(f"Model:  {model}")
    print(f"Trials: {trials}")
    print(f"Prompts: {len(prompts)}")
    print(f"Total API calls: {len(prompts) * 2 * trials}")
    print()
    for prompt in prompts:
        preview = prompt["prompt"][:96]
        if len(prompt["prompt"]) > 96:
            preview += "..."
        print(f"  [{prompt['id']}] ({prompt['category']})")
        print(f"    {preview}")
    print()
    print("Dry run complete. No API calls made.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark gon vs normal output length")
    parser.add_argument(
        "--trials",
        type=int,
        default=3,
        help="Trials per prompt per mode (default: 3)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print config, no API calls")
    parser.add_argument(
        "--update-readme",
        action="store_true",
        help="Update README benchmark table between markers",
    )
    parser.add_argument(
        "--model",
        default=os.environ.get(MODEL_ENV, DEFAULT_MODEL),
        help=f"Model to use (default: ${MODEL_ENV} or {DEFAULT_MODEL})",
    )
    args = parser.parse_args()

    prompts = load_prompts()
    if args.dry_run:
        dry_run(prompts, args.model, args.trials)
        return

    gon_system = load_gon_system()
    skill_hash = sha256_file(SKILL_PATH)
    client = anthropic.Anthropic()

    print(
        f"Running benchmarks: {len(prompts)} prompts x 2 modes x {args.trials} trials",
        file=sys.stderr,
    )
    print(f"Model: {args.model}", file=sys.stderr)
    print(file=sys.stderr)

    results = run_benchmarks(client, args.model, prompts, gon_system, args.trials)
    rows, summary = compute_stats(results)
    table_md = format_table(rows, summary)
    json_path = save_results(results, rows, summary, args.model, args.trials, skill_hash)

    print(f"\nResults saved to {json_path}", file=sys.stderr)
    if args.update_readme:
        update_readme(table_md)

    print(table_md)


if __name__ == "__main__":
    main()
