# VNcaveman

Vietnamese-first AI skill repo for coding agents. Cut filler, cut hedging, cut token waste. Keep technical accuracy.

`VNcaveman` ships a concise-response skill set centered on `gon`: shorter Vietnamese answers for debugging, code review, commit writing, and docs compression without breaking code, commands, logs, paths, or warnings.

Repo này lấy cảm hứng từ [caveman](https://github.com/JuliusBrussee/caveman), nhưng không giữ persona "người tối cổ". Mục tiêu là câu trả lời ngắn hơn, tự nhiên hơn với dev Việt, và vẫn đủ sắc để dùng trong workflow thật.

## Why it exists

Prompt terse kiểu tiếng Anh thường rút theo telegraph English. Cách đó không map thẳng sang tiếng Việt.

`VNcaveman` xử lý bài toán đúng hơn cho tiếng Việt:

- bỏ xã giao dư
- bỏ hedge và đệm lời
- rút cấu trúc dài dòng
- giữ nguyên artifact kỹ thuật
- tự tăng clarity khi đụng destructive ops, prod, security, migration

## What you get

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

### React bug explanation

Before:

> Có khả năng component của bạn đang bị re-render vì ở mỗi lần render bạn lại tạo ra một object mới và truyền object đó xuống dưới dạng prop. React so sánh nông nên sẽ coi đó là prop mới mỗi lần.

After (`full`):

> Re-render do mỗi render tạo object mới. Prop object inline luôn ra ref mới. React thấy prop đổi. Dùng `useMemo`.

### Backend auth bug

Before:

> Mình nghĩ nguyên nhân nhiều khả năng nằm ở middleware xác thực. Bạn đang kiểm tra thời điểm hết hạn của token theo cách chưa chặt, nên token vừa hết hạn vẫn có thể lọt qua.

After (`full`):

> Lỗi ở auth middleware. Check expiry đang sai đơn vị. `exp` là giây, `Date.now()` là ms. So sánh lại với `exp * 1000`.

### Risky SQL warning

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

## Install / Use

### Claude Code hooks

- [hooks/install.sh](/E:/test/caveman/VNcaveman/hooks/install.sh)
- [hooks/install.ps1](/E:/test/caveman/VNcaveman/hooks/install.ps1)
- [hooks/uninstall.sh](/E:/test/caveman/VNcaveman/hooks/uninstall.sh)
- [hooks/uninstall.ps1](/E:/test/caveman/VNcaveman/hooks/uninstall.ps1)

Hook behavior:

- bật `gon` khi session bắt đầu
- theo dõi `/gon lite|full|ultra`
- theo dõi `stop gon` / `normal mode`
- hiện badge `[GON]` trên statusline

### Repo-local surfaces

- [AGENTS.md](/E:/test/caveman/VNcaveman/AGENTS.md)
- [CLAUDE.md](/E:/test/caveman/VNcaveman/CLAUDE.md)
- [GEMINI.md](/E:/test/caveman/VNcaveman/GEMINI.md)
- [.codex/config.toml](/E:/test/caveman/VNcaveman/.codex/config.toml)
- [.codex/hooks.json](/E:/test/caveman/VNcaveman/.codex/hooks.json)
- [rules/gon-activate.md](/E:/test/caveman/VNcaveman/rules/gon-activate.md)

### Skills

- [skills/gon/SKILL.md](/E:/test/caveman/VNcaveman/skills/gon/SKILL.md)
- [skills/gon-commit/SKILL.md](/E:/test/caveman/VNcaveman/skills/gon-commit/SKILL.md)
- [skills/gon-review/SKILL.md](/E:/test/caveman/VNcaveman/skills/gon-review/SKILL.md)
- [skills/gon-compress/SKILL.md](/E:/test/caveman/VNcaveman/skills/gon-compress/SKILL.md)
- [skills/gon-help/SKILL.md](/E:/test/caveman/VNcaveman/skills/gon-help/SKILL.md)

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

`gon-compress` là sub-skill tương đương `caveman-compress` nhưng cho prose/docs tiếng Việt.

- runtime scripts: [gon-compress/scripts/](/E:/test/caveman/VNcaveman/gon-compress/scripts)
- synced surface cho generic `compress`: [skills/compress/](/E:/test/caveman/VNcaveman/skills/compress)
- plugin copy: [plugins/gon/skills/compress/](/E:/test/caveman/VNcaveman/plugins/gon/skills/compress)

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

<!-- BENCHMARK-TABLE-START -->
_Chưa có số benchmark commit cùng repo này. Chạy `python benchmarks/run.py --update-readme` khi môi trường có API key._
<!-- BENCHMARK-TABLE-END -->

### Evals

Harness eval nằm ở [evals/](/E:/test/caveman/VNcaveman/evals). Nó đo:

- `__baseline__`
- `__terse__`
- từng skill trong `skills/`

```bash
uv run --with tiktoken python evals/measure.py
uv run python evals/llm_run.py
```

## Market Readiness

Nếu mục tiêu là tăng star thật và tăng khả năng được duyệt market, xem thêm:

- [docs/market-readiness.md](/E:/test/caveman/VNcaveman/docs/market-readiness.md)
- [docs/social-copy.md](/E:/test/caveman/VNcaveman/docs/social-copy.md)

## Repo structure

- [PROJECT_OVERVIEW.md](/E:/test/caveman/VNcaveman/PROJECT_OVERVIEW.md)
- [DECISIONS.md](/E:/test/caveman/VNcaveman/DECISIONS.md)
- [PROGRESS.md](/E:/test/caveman/VNcaveman/PROGRESS.md)
- [ROADMAP.md](/E:/test/caveman/VNcaveman/ROADMAP.md)
- [docs/caveman-vi-spec.md](/E:/test/caveman/VNcaveman/docs/caveman-vi-spec.md)
- [docs/localization-principles.md](/E:/test/caveman/VNcaveman/docs/localization-principles.md)
- [docs/benchmark.md](/E:/test/caveman/VNcaveman/docs/benchmark.md)
- [examples/](/E:/test/caveman/VNcaveman/examples)
- [tests/](/E:/test/caveman/VNcaveman/tests)

## Caveats

- Repo đã có parity runtime ở mức repo-local với source repo, nhưng benchmark thật và eval snapshot thật còn phụ thuộc model access/CLI.
- Skill/runtime chính hiện giữ tên `gon`; repo name là `VNcaveman`.
- Plugin/manifests nên trỏ về URL public thật của repo.

## License

MIT. Xem [LICENSE](/E:/test/caveman/VNcaveman/LICENSE).
