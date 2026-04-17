"""
Run each prompt through Claude Code under three conditions and snapshot
the real LLM outputs:

  1. baseline      — no extra system prompt
  2. terse         — "Answer concisely in Vietnamese."
  3. terse+skill   — "Answer concisely in Vietnamese.\n\n{SKILL.md}"

The honest delta is (3) vs (2): how much does the skill add on top of a
plain terse instruction?
"""

from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

EVALS = Path(__file__).parent
SKILLS = EVALS.parent / "skills"
DEFAULT_PROMPTS = EVALS / "prompts" / "vi.txt"
FALLBACK_PROMPTS = EVALS / "prompts" / "en.txt"
SNAPSHOT = EVALS / "snapshots" / "results.json"

TERSE_PREFIX = "Answer concisely in Vietnamese."
MODEL_ENV = "GON_EVAL_MODEL"
PROMPTS_ENV = "GON_EVAL_PROMPTS"


def prompt_file() -> Path:
    env_value = os.environ.get(PROMPTS_ENV)
    if env_value:
        return Path(env_value)
    if DEFAULT_PROMPTS.exists():
        return DEFAULT_PROMPTS
    return FALLBACK_PROMPTS


def run_claude(prompt: str, system: str | None = None) -> str:
    cmd = ["claude", "-p"]
    if system:
        cmd += ["--system-prompt", system]
    if model := os.environ.get(MODEL_ENV):
        cmd += ["--model", model]
    cmd.append(prompt)
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def claude_version() -> str:
    try:
        result = subprocess.run(
            ["claude", "--version"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def ensure_claude_available() -> None:
    if shutil.which("claude") is None:
        print(
            "claude CLI not found on PATH. Install/login Claude Code first, then rerun.",
            file=sys.stderr,
        )
        raise SystemExit(1)


def main() -> None:
    ensure_claude_available()

    prompts_path = prompt_file()
    prompts = [
        line.strip()
        for line in prompts_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    skills = sorted(path.name for path in SKILLS.iterdir() if (path / "SKILL.md").exists())

    print(
        f"=== {len(prompts)} prompts × ({len(skills)} skills + 2 control arms) ===",
        flush=True,
    )

    snapshot: dict[str, object] = {
        "metadata": {
            "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "claude_cli_version": claude_version(),
            "model": os.environ.get(MODEL_ENV, "default"),
            "n_prompts": len(prompts),
            "prompt_file": str(prompts_path.relative_to(EVALS.parent)),
            "terse_prefix": TERSE_PREFIX,
        },
        "prompts": prompts,
        "arms": {},
    }

    print("baseline", flush=True)
    snapshot["arms"]["__baseline__"] = [run_claude(prompt) for prompt in prompts]

    print("terse", flush=True)
    snapshot["arms"]["__terse__"] = [
        run_claude(prompt, system=TERSE_PREFIX) for prompt in prompts
    ]

    for skill in skills:
        skill_md = (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8")
        system = f"{TERSE_PREFIX}\n\n{skill_md}"
        print(f"  {skill}", flush=True)
        snapshot["arms"][skill] = [
            run_claude(prompt, system=system) for prompt in prompts
        ]

    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {SNAPSHOT}")


if __name__ == "__main__":
    main()
