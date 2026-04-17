# VNcaveman

[![English](https://img.shields.io/badge/README-English-2563eb?style=for-the-badge)](./README.en.md)
[![Tiếng Việt](https://img.shields.io/badge/README-Tiếng%20Việt-16a34a?style=for-the-badge)](./README.vi.md)

Vietnamese-first AI skill repo for coding agents. Fewer tokens, less filler, same technical accuracy.

## Read in your language

- [English README](./README.en.md)
- [README Tiếng Việt](./README.vi.md)

## Quick summary

`VNcaveman` ships a concise-response skill set centered on `gon`:

- shorter Vietnamese answers for debugging, review, commit writing, and docs compression
- preserve code, commands, logs, paths, warnings, and technical meaning
- auto-fallback to clearer language for risky operations, prod, security, and migrations

## Included surfaces

- main skill: `gon`
- sub-skills: `gon-commit`, `gon-review`, `gon-compress`, `gon-help`
- Claude Code hooks + statusline
- Cline, Copilot, Cursor, Windsurf rules
- Codex plugin, Claude plugin, Gemini extension metadata
- benchmark runner, eval harness, examples, docs

## Before / After

Before:

> Có khả năng component của bạn đang bị re-render vì ở mỗi lần render bạn lại tạo ra một object mới và truyền object đó xuống dưới dạng prop.

After (`full`):

> Re-render do mỗi render tạo object mới. Prop inline ra ref mới. Dùng `useMemo`.

## Links

- [English README](./README.en.md)
- [README Tiếng Việt](./README.vi.md)
- [Skill spec](./docs/caveman-vi-spec.md)
- [Examples](./examples/before-after.md)
- [Market readiness](./docs/market-readiness.md)

## License

MIT. See [LICENSE](./LICENSE).
