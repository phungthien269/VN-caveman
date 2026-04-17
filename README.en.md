# VNcaveman

[![English](https://img.shields.io/badge/README-English-2563eb?style=for-the-badge)](./README.en.md)
[![Tiếng Việt](https://img.shields.io/badge/README-Tiếng%20Việt-16a34a?style=for-the-badge)](./README.vi.md)

`VNcaveman` is a Vietnamese-first AI skill repo for coding agents. It ships a concise-response skill set centered on `gon`: fewer tokens, less filler, same technical accuracy.

Inspired by [caveman](https://github.com/JuliusBrussee/caveman), but redesigned for real Vietnamese developer workflows instead of caveman-style persona writing.

## Why it exists

Plain English-style terseness does not map cleanly to Vietnamese.

`VNcaveman` focuses on:

- removing social filler and hedging
- shortening verbose Vietnamese phrasing
- preserving code, commands, logs, paths, and warnings
- automatically switching to clearer language for risky ops, prod, security, and migrations

## Included surfaces

| Surface | Included |
|---|---|
| Main skill | `gon` with `lite`, `full`, `ultra` |
| Sub-skills | `gon-commit`, `gon-review`, `gon-compress`, `gon-help` |
| Hooks | Claude Code hooks + statusline |
| Rules | Cline, Copilot, Cursor, Windsurf |
| Plugin surfaces | Codex plugin, Claude plugin, Gemini extension metadata |
| Runtime tooling | `gon-compress`, benchmark runner, eval harness |
| Docs | spec, examples, roadmap, decisions, progress |

## Before / After

Before:

> There is a good chance your React component is re-rendering because you create a new object on every render and pass it as a prop.

After (`full`):

> Re-render do mỗi render tạo object mới. Prop inline ra ref mới. Dùng `useMemo`.

## Levels

| Level | Goal | Best for | Avoid when |
|---|---|---|---|
| `lite` | Remove filler, keep full sentences | general Q&A, docs, support | you need strong compression |
| `full` | Short and direct | debugging, review, technical guidance | high-risk step-by-step tasks |
| `ultra` | Very short, dev shorthand | fast internal engineering chat | beginners, warnings, migrations, prod |

## Install / Use

### Claude Code hooks

- [hooks/install.sh](./hooks/install.sh)
- [hooks/install.ps1](./hooks/install.ps1)
- [hooks/uninstall.sh](./hooks/uninstall.sh)
- [hooks/uninstall.ps1](./hooks/uninstall.ps1)

### Skills

- [skills/gon/SKILL.md](./skills/gon/SKILL.md)
- [skills/gon-commit/SKILL.md](./skills/gon-commit/SKILL.md)
- [skills/gon-review/SKILL.md](./skills/gon-review/SKILL.md)
- [skills/gon-compress/SKILL.md](./skills/gon-compress/SKILL.md)
- [skills/gon-help/SKILL.md](./skills/gon-help/SKILL.md)

Common triggers:

- `gon mode`
- `trả lời gọn`
- `nói ngắn hơn`
- `ít token hơn`
- `/gon lite`
- `/gon full`
- `/gon ultra`

Disable:

- `stop gon`
- `normal mode`
- `trả lời bình thường`

## `gon-compress`

Vietnamese prose/docs compression surface:

- [gon-compress/scripts/](./gon-compress/scripts)
- [skills/compress/](./skills/compress)
- [plugins/gon/skills/compress/](./plugins/gon/skills/compress)

It:

- detects prose/docs vs code/config
- creates `.original.md` backups
- compresses Vietnamese prose
- validates headings, code blocks, URLs, and paths
- retries up to 2 times on validation failures
- refuses likely secret/key paths

## Benchmark / Eval

- [benchmarks/](./benchmarks)
- [evals/](./evals)
- [docs/benchmark.md](./docs/benchmark.md)

## Market readiness

- [docs/market-readiness.md](./docs/market-readiness.md)
- [docs/social-copy.md](./docs/social-copy.md)

## License

MIT. See [LICENSE](./LICENSE).
