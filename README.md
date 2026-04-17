# VNcaveman

[![EN](https://img.shields.io/badge/README-EN-2563eb?style=for-the-badge)](./README.en.md)

`VNcaveman` là repo Vietnamese-first cho bộ skill nén phản hồi `gon`: ngắn hơn, sắc hơn, ít token hơn, nhưng vẫn giữ nguyên ý kỹ thuật.

Repo này lấy cảm hứng từ [caveman](https://github.com/JuliusBrussee/caveman), nhưng không giữ persona "người tối cổ". Mục tiêu là câu trả lời ngắn hơn, tự nhiên hơn với dev Việt, và vẫn đủ sắc để dùng trong workflow thật.

`gon` tối ưu token bằng cách xử lý cả input lẫn output text:

- chuẩn hóa intent từ prompt kiểu verbose sang chỉ thị ngắn, rõ, dev-like
- cắt xã giao, hedge, đệm lời và các cấu trúc dài dòng không thêm ý
- giữ nguyên code, command, URL, path, log, warning và proper noun
- nén phần prose mạnh hơn, nhưng tự tăng clarity khi task có rủi ro cao
- ưu tiên ratio `ít token hơn / không mất nghĩa` thay vì rút câu một cách máy móc

## Bạn sẽ có gì

| Surface | Có gì |
|---|---|
| Main skill | `gon` với `lite`, `full`, `ultra` |
| Sub-skills | `gon-commit`, `gon-review`, `gon-compress`, `gon-help` |
| Hooks | Claude Code hooks + statusline |
| Rules | Cline, Copilot, Cursor, Windsurf |
| Plugin surfaces | Codex plugin, Claude plugin, Gemini extension metadata |
| Runtime tooling | `gon-compress`, benchmark runner, eval harness |
| Docs | spec, examples, roadmap, decisions, progress |

## Before / After

### Giải thích bug React

Before:

> Có khả năng component của bạn đang bị re-render vì ở mỗi lần render bạn lại tạo ra một object mới và truyền object đó xuống dưới dạng prop. React so sánh nông nên sẽ coi đó là prop mới mỗi lần.

After (`full`):

> Re-render do mỗi render tạo object mới. Prop object inline luôn ra ref mới. React thấy prop đổi. Dùng `useMemo`.

### Bug backend auth

Before:

> Mình nghĩ nguyên nhân nhiều khả năng nằm ở middleware xác thực. Bạn đang kiểm tra thời điểm hết hạn của token theo cách chưa chặt, nên token vừa hết hạn vẫn có thể lọt qua.

After (`full`):

> Lỗi ở auth middleware. Check expiry đang sai đơn vị. `exp` là giây, `Date.now()` là ms. So sánh lại với `exp * 1000`.

### Warning SQL nguy hiểm

Before:

> Ok, mình sẽ chạy lệnh xóa toàn bộ bảng users cho bạn.

After (auto-clarity):

> Cảnh báo: lệnh này xóa vĩnh viễn toàn bộ dữ liệu trong `users`.
> Chỉ chạy nếu đã có backup và chắc chắn đây không phải production.
>
> ```sql
> DROP TABLE users;
> ```

## Levels

| Level | Mục tiêu | Dùng khi | Tránh dùng khi |
|---|---|---|---|
| `lite` | Bỏ xã giao và hedge, vẫn là câu đầy đủ | Hỏi đáp thường ngày, docs, support nội bộ | Cần nén mạnh |
| `full` | Ngắn, trực diện, câu có thể cụt vừa phải | Debug, review, guidance kỹ thuật | Task rủi ro cao cần step-by-step |
| `ultra` | Cực ngắn, shorthand dev | Chat kỹ thuật nội bộ, diff review nhanh | User mới, warning, migration, prod |

## Cài / Dùng

### Claude Code hooks

- [hooks/install.sh](./hooks/install.sh)
- [hooks/install.ps1](./hooks/install.ps1)
- [hooks/uninstall.sh](./hooks/uninstall.sh)
- [hooks/uninstall.ps1](./hooks/uninstall.ps1)

Hook sẽ:

- bật `gon` khi session bắt đầu
- theo dõi `/gon lite|full|ultra`
- theo dõi `stop gon` / `normal mode`
- hiện badge `[GON]` trên statusline

### Repo-local surfaces

- [AGENTS.md](./AGENTS.md)
- [CLAUDE.md](./CLAUDE.md)
- [GEMINI.md](./GEMINI.md)
- [.codex/config.toml](./.codex/config.toml)
- [.codex/hooks.json](./.codex/hooks.json)
- [rules/gon-activate.md](./rules/gon-activate.md)

### Skills

- [skills/gon/SKILL.md](./skills/gon/SKILL.md)
- [skills/gon-commit/SKILL.md](./skills/gon-commit/SKILL.md)
- [skills/gon-review/SKILL.md](./skills/gon-review/SKILL.md)
- [skills/gon-compress/SKILL.md](./skills/gon-compress/SKILL.md)
- [skills/gon-help/SKILL.md](./skills/gon-help/SKILL.md)

Trigger gợi ý:

- `gon mode`
- `trả lời gọn`
- `nói ngắn hơn`
- `ít token hơn`
- `/gon lite`
- `/gon full`
- `/gon ultra`

Tắt:

- `stop gon`
- `normal mode`
- `trả lời bình thường`

## `gon-compress`

`gon-compress` là sub-skill tương đương `caveman-compress` nhưng cho prose/docs tiếng Việt.

- runtime scripts: [gon-compress/scripts/](./gon-compress/scripts)
- synced surface cho generic `compress`: [skills/compress/](./skills/compress)
- plugin copy: [plugins/gon/skills/compress/](./plugins/gon/skills/compress)

Nó:

- phát hiện prose/docs vs code/config
- tạo backup `.original.md`
- nén prose tiếng Việt
- validate heading, code block, URL, path
- retry fix tối đa 2 lần nếu validation fail
- chặn path có dấu hiệu chứa secret/key

## Benchmark / Eval

### Benchmark

```bash
uv run python benchmarks/run.py --dry-run
```

Nếu có `ANTHROPIC_API_KEY`:

```bash
uv run python benchmarks/run.py --update-readme
```

### Evals

Harness eval nằm ở [evals/](./evals). Nó đo:

- `__baseline__`
- `__terse__`
- từng skill trong `skills/`

```bash
uv run --with tiktoken python evals/measure.py
uv run python evals/llm_run.py
```

## Market readiness

Nếu mục tiêu là tăng star thật và tăng khả năng được duyệt market, xem thêm:

- [docs/market-readiness.md](./docs/market-readiness.md)
- [docs/social-copy.md](./docs/social-copy.md)

## Cấu trúc repo

- [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)
- [DECISIONS.md](./DECISIONS.md)
- [PROGRESS.md](./PROGRESS.md)
- [ROADMAP.md](./ROADMAP.md)
- [docs/caveman-vi-spec.md](./docs/caveman-vi-spec.md)
- [docs/localization-principles.md](./docs/localization-principles.md)
- [docs/benchmark.md](./docs/benchmark.md)
- [examples/](./examples)
- [tests/](./tests)

## Caveats

- Repo đã có parity runtime ở mức repo-local với source repo, nhưng benchmark thật và eval snapshot thật còn phụ thuộc model access/CLI.
- Skill/runtime chính hiện giữ tên `gon`; repo name là `VNcaveman`.
- Plugin/manifests nên trỏ về URL public thật của repo.

## License

MIT. Xem [LICENSE](./LICENSE).
