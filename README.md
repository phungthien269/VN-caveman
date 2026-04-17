<p align="center">
  <a href="./README.en.md">
    <img src="https://img.shields.io/badge/README-EN-2563eb?style=for-the-badge" alt="English README" />
  </a>
</p>

<h1 align="center">VNcaveman</h1>

<p align="center">
  <strong>ít token hơn, ít filler hơn, vẫn giữ nguyên ý kỹ thuật</strong>
</p>

<p align="center">
  <a href="https://github.com/phungthien269/VN-caveman/stargazers">
    <img src="https://img.shields.io/github/stars/phungthien269/VN-caveman?style=flat&color=yellow" alt="Stars">
  </a>
  <a href="https://github.com/phungthien269/VN-caveman/commits/main">
    <img src="https://img.shields.io/github/last-commit/phungthien269/VN-caveman?style=flat" alt="Last Commit">
  </a>
  <a href="./LICENSE">
    <img src="https://img.shields.io/github/license/phungthien269/VN-caveman?style=flat" alt="License">
  </a>
</p>

<p align="center">
  <a href="#before--after">Before/After</a> •
  <a href="#install">Install</a> •
  <a href="#levels">Levels</a> •
  <a href="#skills">Skills</a> •
  <a href="#benchmarks">Benchmarks</a> •
  <a href="#evals">Evals</a>
</p>

---

`VNcaveman` là repo **Vietnamese-first** cho bộ skill nén phản hồi `gon`: ngắn hơn, sắc hơn, ít token hơn, nhưng vẫn giữ nguyên ý kỹ thuật.

Repo này lấy cảm hứng từ [caveman](https://github.com/JuliusBrussee/caveman), nhưng không giữ persona "người tối cổ". Mục tiêu là câu trả lời ngắn hơn, tự nhiên hơn với dev Việt, và vẫn đủ sắc để dùng trong workflow thật.

`gon` tối ưu token bằng cách xử lý cả **input** lẫn **output** text:

- chuẩn hóa intent từ prompt verbose sang chỉ thị ngắn, rõ, dev-like
- cắt xã giao, hedge, đệm lời và các cấu trúc dài dòng không thêm ý
- giữ nguyên code, command, URL, path, log, warning và proper noun
- nén prose mạnh hơn, nhưng tự tăng clarity khi task có rủi ro cao
- ưu tiên ratio `ít token hơn / không mất nghĩa` thay vì rút câu máy móc

## Before / After

<table>
<tr>
<td width="50%">

### 🗣️ Agent bình thường

> "Có khả năng component của bạn đang bị re-render vì ở mỗi lần render bạn lại tạo ra một object mới và truyền object đó xuống dưới dạng prop. React so sánh nông nên sẽ coi đó là prop mới mỗi lần."

</td>
<td width="50%">

### ⚡ `gon` (`full`)

> "Re-render do mỗi render tạo object mới. Prop object inline luôn ra ref mới. React thấy prop đổi. Dùng `useMemo`."

</td>
</tr>
<tr>
<td>

### 🗣️ Agent bình thường

> "Mình nghĩ nguyên nhân nhiều khả năng nằm ở middleware xác thực. Bạn đang kiểm tra thời điểm hết hạn của token theo cách chưa chặt, nên token vừa hết hạn vẫn có thể lọt qua."

</td>
<td>

### ⚡ `gon` (`full`)

> "Lỗi ở auth middleware. Check expiry đang sai đơn vị. `exp` là giây, `Date.now()` là ms. So sánh lại với `exp * 1000`."

</td>
</tr>
</table>

**Cùng ý kỹ thuật. Ít chữ hơn. Dễ scan hơn.**

**Chọn mức nén bạn muốn:**

<table>
<tr>
<td width="33%">

#### 🪶 Lite

> "Component re-render vì mỗi lần render bạn tạo object mới. React thấy ref mới nên render lại. Dùng `useMemo`."

</td>
<td width="33%">

#### ⚡ Full

> "Re-render do mỗi render tạo object mới. Prop inline ra ref mới. Dùng `useMemo`."

</td>
<td width="33%">

#### 🔥 Ultra

> "Inline obj -> ref mới -> re-render. `useMemo`."

</td>
</tr>
</table>

**Cùng ý. Bạn chọn độ gọn.**

```text
┌─────────────────────────────────────┐
│  TOKEN WASTE DOWN       ████████    │
│  TECHNICAL FIDELITY     ████████    │
│  READ SPEED             ████████    │
│  FILLER                 ██          │
└─────────────────────────────────────┘
```

- **Đọc nhanh hơn** — ít chữ thừa, vào thẳng vấn đề
- **Scan tốt hơn** — debug, review, commit message, docs đều gọn hơn
- **Không phá kỹ thuật** — code, command, path, URL, log vẫn giữ nguyên
- **An toàn hơn khi cần** — gặp destructive ops, prod, security, migration thì tự tăng clarity

## Install

Chọn surface phù hợp. Repo này hiện mạnh nhất ở dạng clone + dùng local rules/hooks/plugin surfaces.

| Surface | Cách dùng |
|--------|-----------|
| **Claude Code hooks** | clone repo rồi chạy `./hooks/install.sh` hoặc `./hooks/install.ps1` |
| **Codex repo-local** | clone repo, mở trong Codex, dùng `.codex/config.toml` + `.codex/hooks.json` |
| **Gemini CLI** | dùng `GEMINI.md` + `gemini-extension.json` trong repo |
| **Cursor / Windsurf / Cline / Copilot** | dùng các rule files có sẵn trong repo |
| **Skill files trực tiếp** | mở `skills/` và dùng `SKILL.md` tương ứng |

Install once. Dùng lại trong workflow hằng ngày.

### What You Get

| Feature | Claude Code | Codex | Gemini CLI | Cursor | Windsurf | Cline | Copilot |
|---------|:-----------:|:-----:|:----------:|:------:|:--------:|:-----:|:-------:|
| `gon` mode | Y | Y | Y | Y | Y | Y | Y |
| Auto-activate every session | Y | Y¹ | Y | Y² | Y² | Y² | Y² |
| Mode switching (`lite/full/ultra`) | Y | Y¹ | Y | Y | Y | — | — |
| Statusline badge | Y | — | — | — | — | — | — |
| `gon-commit` | Y | Y | Y | Y | Y | Y | Y |
| `gon-review` | Y | Y | Y | Y | Y | Y | Y |
| `gon-compress` | Y | Y | Y | Y | Y | Y | Y |
| `gon-help` | Y | Y | Y | Y | Y | Y | Y |

> [!NOTE]
> ¹ Codex repo-local auto-start phụ thuộc `.codex/hooks.json` trong repo này.
>
> ² Cursor, Windsurf, Cline, Copilot dùng rule/instruction files nằm ngay trong repo. Nếu mang skill đi repo khác, bạn cần copy surface tương ứng hoặc cấu hình lại.

## Levels

| Level | Trigger | Mục tiêu |
|-------|---------|----------|
| **Lite** | `/gon lite` | Bỏ filler nhưng vẫn là câu đầy đủ |
| **Full** | `/gon full` | Ngắn, trực diện, cân bằng nhất |
| **Ultra** | `/gon ultra` | Cực ngắn, shorthand dev, vẫn đủ nghĩa |

Trigger phổ biến:

- `gon mode`
- `trả lời gọn`
- `nói ngắn hơn`
- `ít token hơn`

Tắt bằng:

- `stop gon`
- `normal mode`
- `trả lời bình thường`

## Skills

### `gon`

Skill chính cho response compression tiếng Việt kỹ thuật.

- [skills/gon/SKILL.md](./skills/gon/SKILL.md)

### `gon-commit`

Commit message ngắn, đúng chuẩn, ít lan man.

- [skills/gon-commit/SKILL.md](./skills/gon-commit/SKILL.md)

### `gon-review`

Code review ngắn, dễ scan, tập trung bug/risk/fix.

- [skills/gon-review/SKILL.md](./skills/gon-review/SKILL.md)

### `gon-help`

Quick reference cho mode, trigger và skill surfaces.

- [skills/gon-help/SKILL.md](./skills/gon-help/SKILL.md)

### `gon-compress`

Nén prose/docs để agent **đọc ít token hơn**, không chỉ **trả ít token hơn**.

- [gon-compress/scripts/](./gon-compress/scripts)
- [skills/gon-compress/SKILL.md](./skills/gon-compress/SKILL.md)
- [skills/compress/](./skills/compress)

Nó:

- phát hiện prose/docs vs code/config
- tạo backup `.original.md`
- nén prose tiếng Việt
- validate heading, code block, URL, path
- retry fix tối đa 2 lần nếu validation fail
- chặn path có dấu hiệu chứa secret/key

## Benchmarks

Hiện repo đã có benchmark runner, nhưng **chưa commit benchmark thật** vào README.

Chạy benchmark:

```bash
uv run python benchmarks/run.py --dry-run
```

Nếu có `ANTHROPIC_API_KEY`:

```bash
uv run python benchmarks/run.py --update-readme
```

> [!IMPORTANT]
> Repo này không bịa số benchmark. Chỉ chèn số vào README khi có run thật.

## Evals

`evals/` đo mức nén token thật theo mô hình:

- `__baseline__`
- `__terse__`
- từng skill trong `skills/`

```bash
# chạy eval (cần claude CLI)
uv run python evals/llm_run.py

# đọc kết quả offline
uv run --with tiktoken python evals/measure.py
```

Mục tiêu là đo đúng phần skill đóng góp, không gian lận kiểu so với output verbose mặc định.

## Star This Repo

Nếu repo này giúp agent trả lời gọn hơn, dễ đọc hơn, ít token hơn, hãy để lại một star.

Repo đang cần **star thật** từ người dùng thật, không phải star rác.

## More Docs

- [README English](./README.en.md)
- [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)
- [DECISIONS.md](./DECISIONS.md)
- [PROGRESS.md](./PROGRESS.md)
- [ROADMAP.md](./ROADMAP.md)
- [docs/caveman-vi-spec.md](./docs/caveman-vi-spec.md)
- [docs/localization-principles.md](./docs/localization-principles.md)
- [docs/benchmark.md](./docs/benchmark.md)
- [docs/market-readiness.md](./docs/market-readiness.md)
- [docs/social-copy.md](./docs/social-copy.md)
- [examples/](./examples)
- [tests/](./tests)

## License

MIT. Xem [LICENSE](./LICENSE).
