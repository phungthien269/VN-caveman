# VNcaveman

`VNcaveman` là repo tiếng Việt-first cho bộ skill nén phản hồi `gon`: ngắn hơn, sắc hơn, ít token hơn, nhưng vẫn giữ nguyên ý kỹ thuật.

Repo này lấy cảm hứng từ [caveman](https://github.com/JuliusBrussee/caveman), nhưng không giữ persona "người tối cổ". `gon` ưu tiên tiếng Việt tự nhiên cho dev workflow: bỏ xã giao, bỏ hedge, rút câu, giữ nguyên code/lệnh/log/path, và tự tăng clarity khi task có rủi ro.

## Bạn sẽ có gì

| Surface | Có gì |
|---|---|
| Skill chính | `gon` với 3 level `lite`, `full`, `ultra` |
| Skill phụ | `gon-commit`, `gon-review`, `gon-compress`, `gon-help` |
| Hooks | Claude Code hooks + statusline |
| Rules | Cline, Copilot, Cursor, Windsurf |
| Plugin surfaces | Codex plugin, Claude plugin, Gemini extension metadata |
| Docs nội bộ | `PROJECT_OVERVIEW.md`, `DECISIONS.md`, `PROGRESS.md`, `ROADMAP.md`, `CLAUDE.md` |
| Benchmark/eval | script benchmark, eval harness, regression checklist |

## Before / After

### Giải thích bug React

Before:

> Có khả năng component của bạn đang bị re-render vì ở mỗi lần render bạn lại tạo ra một object mới và truyền object đó xuống dưới dạng prop. React so sánh nông nên sẽ coi đó là prop mới mỗi lần.

After (`full`):

> Re-render do mỗi render tạo object mới. Prop object inline luôn ra ref mới. React thấy prop đổi. Dùng `useMemo`.

### Giải thích bug backend

Before:

> Mình nghĩ nguyên nhân nhiều khả năng nằm ở middleware xác thực. Bạn đang kiểm tra thời điểm hết hạn của token theo cách chưa chặt, nên token vừa hết hạn vẫn có thể lọt qua.

After (`full`):

> Lỗi ở auth middleware. Check expiry đang sai đơn vị. `exp` là giây, `Date.now()` là ms. So sánh lại với `exp * 1000`.

### Warning khi lệnh nguy hiểm

Before:

> Ok, mình sẽ chạy lệnh xóa toàn bộ bảng users cho bạn.

After (auto-clarity):

> Cảnh báo: lệnh này xóa vĩnh viễn toàn bộ dữ liệu trong `users`.
> Chỉ chạy nếu đã có backup và chắc chắn đây không phải production.
>
> ```sql
> DROP TABLE users;
> ```

## Khác gì repo gốc

- Không dịch literal từ tiếng Anh sang tiếng Việt.
- Không làm giọng hang động.
- Không có `wenyan`; thay bằng 3 level hợp với tiếng Việt hơn.
- Có bộ lexicon tiếng Việt rộng hơn để cắt xã giao, hedge, đệm lời, cụm quan liêu, câu chuyển ý thừa.
- Giữ parity tinh thần với repo gốc ở hook/rules/plugin/eval/benchmark/compress surface, nhưng localization theo behavior chứ không bê nguyên wording.

## Levels

| Level | Mục tiêu | Dùng khi | Tránh dùng khi |
|---|---|---|---|
| `lite` | Bỏ xã giao và hedge, vẫn là câu đầy đủ | Hỏi đáp thường ngày, docs, support nội bộ | Cần nén mạnh |
| `full` | Ngắn, trực diện, câu có thể cụt vừa phải | Debug, review, guidance kỹ thuật | Task rủi ro cao cần step-by-step |
| `ultra` | Cực ngắn, shorthand dev | Chat kỹ thuật nội bộ, diff review nhanh | User mới, warning, migration, prod |

Chi tiết nằm ở [docs/caveman-vi-spec.md](/E:/test/caveman/VNcaveman/docs/caveman-vi-spec.md).

## Cài và dùng

### Claude Code hooks

Repo có sẵn:

- [hooks/install.sh](/E:/test/caveman/VNcaveman/hooks/install.sh)
- [hooks/install.ps1](/E:/test/caveman/VNcaveman/hooks/install.ps1)
- [hooks/uninstall.sh](/E:/test/caveman/VNcaveman/hooks/uninstall.sh)
- [hooks/uninstall.ps1](/E:/test/caveman/VNcaveman/hooks/uninstall.ps1)

Hook sẽ:

- bật `gon` khi session bắt đầu
- theo dõi `/gon lite|full|ultra`
- theo dõi `stop gon` / `normal mode`
- hiện badge `[GON]` trên statusline

### Repo-local surfaces

Repo có sẵn:

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

`gon-compress` là sub-skill tương đương surface `caveman-compress` của repo gốc:

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

## Benchmark và eval

### Benchmark

Chạy benchmark qua Anthropic API:

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

Đọc snapshot:

```bash
uv run --with tiktoken python evals/measure.py
```

Sinh snapshot mới cần `claude` CLI:

```bash
uv run python evals/llm_run.py
```

## Repo structure

- [PROJECT_OVERVIEW.md](/E:/test/caveman/VNcaveman/PROJECT_OVERVIEW.md): repo là gì, phạm vi gì.
- [DECISIONS.md](/E:/test/caveman/VNcaveman/DECISIONS.md): quyết định kiến trúc và deviation.
- [PROGRESS.md](/E:/test/caveman/VNcaveman/PROGRESS.md): trạng thái hiện tại và next steps.
- [ROADMAP.md](/E:/test/caveman/VNcaveman/ROADMAP.md): phase tiếp theo.
- [docs/caveman-vi-spec.md](/E:/test/caveman/VNcaveman/docs/caveman-vi-spec.md): spec đầy đủ.
- [docs/localization-principles.md](/E:/test/caveman/VNcaveman/docs/localization-principles.md): nguyên tắc localization.
- [docs/benchmark.md](/E:/test/caveman/VNcaveman/docs/benchmark.md): benchmark rubric và cách chạy.
- [examples/](/E:/test/caveman/VNcaveman/examples): ví dụ before/after, commit, review.
- [tests/](/E:/test/caveman/VNcaveman/tests): benchmark cases, regression checklist, verify scripts.

## Caveats

- Repo đã có parity runtime ở mức repo-local với source repo, nhưng chưa có URL publish chính thức cho marketplace/plugin manifests.
- Snapshot eval hiện là stub nếu máy chưa có `claude` CLI.
- `gon` tối ưu cho tiếng Việt kỹ thuật; không nhắm tới copywriting, sales, hay đối ngoại.

## License

MIT. Xem [LICENSE](/E:/test/caveman/VNcaveman/LICENSE).
