# CLAUDE.md — gon

## README là front door

README là artifact sản phẩm. Người ngoài repo đọc nó để quyết định có dùng `gon` hay không.

Rule khi sửa README:

- Ưu tiên before/after và install surface trước.
- Bảng level, benchmark, install phải khớp repo thật.
- Không nhét jargon kiểu "inject SessionStart context" nếu có thể nói bằng ngôn ngữ dễ hiểu hơn.
- Không hứa số benchmark nếu chưa có run thật.
- Nếu đổi behavior trong skill, sync README, docs, examples, progress.

## Nguồn sự thật

### Chỉ sửa trực tiếp các file này khi đổi behavior

| File | Vai trò |
|------|--------|
| `skills/gon/SKILL.md` | behavior skill chính |
| `rules/gon-activate.md` | auto-activation rule body |
| `skills/gon-commit/SKILL.md` | skill commit |
| `skills/gon-review/SKILL.md` | skill review |
| `skills/gon-help/SKILL.md` | quick reference |
| `skills/gon-compress/SKILL.md` | behavior skill nén prose/docs |
| `gon-compress/scripts/*` | runtime scripts cho compress |

### File sync/copy

Không sửa trực tiếp nếu vừa sửa nguồn phía trên:

| File | Sync từ |
|------|---------|
| `gon/SKILL.md` | `skills/gon/SKILL.md` |
| `plugins/gon/skills/gon/SKILL.md` | `skills/gon/SKILL.md` |
| `.cursor/skills/gon/SKILL.md` | `skills/gon/SKILL.md` |
| `.windsurf/skills/gon/SKILL.md` | `skills/gon/SKILL.md` |
| `skills/compress/SKILL.md` | `skills/gon-compress/SKILL.md` đã đổi tên frontmatter thành `compress` |
| `plugins/gon/skills/compress/SKILL.md` | `skills/compress/SKILL.md` |
| `.clinerules/gon.md` | `rules/gon-activate.md` |
| `.github/copilot-instructions.md` | `rules/gon-activate.md` |
| `.cursor/rules/gon.mdc` | `rules/gon-activate.md` + Cursor frontmatter |
| `.windsurf/rules/gon.md` | `rules/gon-activate.md` + Windsurf frontmatter |
| `gon.skill` | ZIP của `skills/gon/` |

## Hook system

Hook Claude Code nằm trong `hooks/`:

- `gon-config.js`: resolve config path + symlink-safe flag write
- `gon-activate.js`: SessionStart, inject rules + set mode mặc định
- `gon-mode-tracker.js`: UserPromptSubmit, đổi mode theo slash command / natural trigger
- `gon-statusline.sh` / `.ps1`: hiện badge `[GON]`, `[GON:ULTRA]`, ...

Flag file: `$CLAUDE_CONFIG_DIR/.gon-active` hoặc `~/.claude/.gon-active`.

Rule:

- Hook phải silent-fail khi có lỗi filesystem.
- Không ghi trực tiếp vào flag path ngoài `safeWriteFlag()`.
- Tôn trọng `CLAUDE_CONFIG_DIR`, không hardcode `~/.claude`.

## Benchmark và eval

- `benchmarks/`: gọi Anthropic API trực tiếp, cần `ANTHROPIC_API_KEY`.
- `evals/`: gọi `claude` CLI. Nếu máy chưa có CLI, snapshot có thể là stub.
- Không bịa số. Không tự viết snapshot giả.

## Khi cần parity với repo gốc

Checklist nhanh:

1. Skill copies có sync chưa.
2. Rule copies có sync chưa.
3. `gon-compress` còn chạy được chưa.
4. `tests/verify_repo.py` pass chưa.
5. README có còn mô tả đúng state hiện tại không.
