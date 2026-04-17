#!/usr/bin/env python3
"""Gon memory/document compression orchestrator."""

import os
import re
import subprocess
from pathlib import Path
from typing import List

from .detect import should_compress
from .validate import validate

OUTER_FENCE_REGEX = re.compile(r"\A\s*(`{3,}|~{3,})[^\n]*\n(.*)\n\1\s*\Z", re.DOTALL)
MAX_RETRIES = 2

SENSITIVE_BASENAME_REGEX = re.compile(
    r"(?ix)^("
    r"\.env(\..+)?"
    r"|\.netrc"
    r"|credentials(\..+)?"
    r"|secrets?(\..+)?"
    r"|passwords?(\..+)?"
    r"|id_(rsa|dsa|ecdsa|ed25519)(\.pub)?"
    r"|authorized_keys"
    r"|known_hosts"
    r"|.*\.(pem|key|p12|pfx|crt|cer|jks|keystore|asc|gpg)"
    r")$"
)
SENSITIVE_PATH_COMPONENTS = frozenset({".ssh", ".aws", ".gnupg", ".kube", ".docker"})
SENSITIVE_NAME_TOKENS = ("secret", "credential", "password", "passwd", "apikey", "accesskey", "token", "privatekey")


def is_sensitive_path(filepath: Path) -> bool:
    name = filepath.name
    if SENSITIVE_BASENAME_REGEX.match(name):
        return True
    lowered_parts = {p.lower() for p in filepath.parts}
    if lowered_parts & SENSITIVE_PATH_COMPONENTS:
        return True
    lower = re.sub(r"[_\-\s.]", "", name.lower())
    return any(tok in lower for tok in SENSITIVE_NAME_TOKENS)


def strip_llm_wrapper(text: str) -> str:
    m = OUTER_FENCE_REGEX.match(text)
    if m:
        return m.group(2)
    return text


def call_claude(prompt: str) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=api_key)
            msg = client.messages.create(
                model=os.environ.get("GON_MODEL", "claude-sonnet-4-5"),
                max_tokens=8192,
                messages=[{"role": "user", "content": prompt}],
            )
            return strip_llm_wrapper(msg.content[0].text.strip())
        except ImportError:
            pass

    try:
        result = subprocess.run(
            ["claude", "--print"],
            input=prompt,
            text=True,
            capture_output=True,
            check=True,
        )
        return strip_llm_wrapper(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Claude call failed:\n{e.stderr}")


def build_compress_prompt(original: str) -> str:
    return f"""
Rewrite this markdown into concise Vietnamese technical prose.

STRICT RULES:
- Do NOT modify anything inside ``` code blocks
- Do NOT modify anything inside inline backticks
- Preserve ALL URLs exactly
- Preserve ALL headings exactly unless changing them is absolutely unnecessary
- Preserve file paths and commands
- Return ONLY the compressed markdown body
- Remove social filler, hedging, and verbose phrasing
- Keep warnings clear; do not over-compress risky instructions

TEXT:
{original}
"""


def build_fix_prompt(original: str, compressed: str, errors: List[str]) -> str:
    errors_str = "\n".join(f"- {e}" for e in errors)
    return f"""You are fixing a gon-compressed markdown file. Specific validation errors were found.

CRITICAL RULES:
- DO NOT recompress or rephrase the whole file
- ONLY fix the listed errors
- The ORIGINAL is reference only
- Preserve concise Vietnamese style in untouched sections

ERRORS TO FIX:
{errors_str}

ORIGINAL:
{original}

COMPRESSED:
{compressed}

Return ONLY the fixed compressed file.
"""


def compress_file(filepath: Path) -> bool:
    filepath = filepath.resolve()
    max_file_size = 500_000
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    if filepath.stat().st_size > max_file_size:
        raise ValueError(f"File too large to compress safely (max 500KB): {filepath}")
    if is_sensitive_path(filepath):
        raise ValueError(
            f"Refusing to compress {filepath}: filename looks sensitive. "
            "Compression may send file contents to Anthropic."
        )

    print(f"Processing: {filepath}")
    if not should_compress(filepath):
        print("Skipping (not natural language)")
        return False

    original_text = filepath.read_text(errors="ignore")
    backup_path = filepath.with_name(filepath.stem + ".original.md")
    if backup_path.exists():
        print(f"⚠️ Backup file already exists: {backup_path}")
        print("Aborting to prevent overwriting the original backup.")
        return False

    print("Compressing with Claude...")
    compressed = call_claude(build_compress_prompt(original_text))
    backup_path.write_text(original_text)
    filepath.write_text(compressed)

    for attempt in range(MAX_RETRIES):
        print(f"\nValidation attempt {attempt + 1}")
        result = validate(backup_path, filepath)
        if result.is_valid:
            print("Validation passed")
            break

        print("❌ Validation failed:")
        for err in result.errors:
            print(f"   - {err}")

        if attempt == MAX_RETRIES - 1:
            filepath.write_text(original_text)
            backup_path.unlink(missing_ok=True)
            print("❌ Failed after retries — original restored")
            return False

        print("Fixing with Claude...")
        compressed = call_claude(build_fix_prompt(original_text, compressed, result.errors))
        filepath.write_text(compressed)

    return True
