# Benchmark Framework

## Mục tiêu benchmark

Benchmark của `gon` phải trả lời đồng thời 5 câu hỏi:

- output có ngắn hơn không
- có mất nghĩa không
- có phá code / markdown không
- tiếng Việt có tự nhiên không
- có fallback đúng lúc không

## Nhóm benchmark bắt buộc

| Nhóm | Mô tả | Kỳ vọng chính |
|---|---|---|
| technical Q&A | câu hỏi kỹ thuật chung | ngắn hơn, vẫn đủ ý, tự nhiên |
| bug explanation | giải thích bug frontend/backend | giữ root cause và fix |
| code review | comment review ngắn | actionable, dễ scan |
| commit writing | commit message | đúng format, không lan man |
| prose compression | nén docs/prose | giữ markdown/code/config |

## Rubric chấm

Mỗi case chấm theo thang `0/1/2` cho từng tiêu chí:

- `ngắn hơn`
- `đúng nghĩa`
- `tự nhiên`
- `không phá artifact`
- `fallback đúng`

Tổng tối đa: `10`.

## Cách chạy benchmark thật

### 1. API benchmark

So sánh `normal` vs `gon` qua Anthropic API:

```bash
uv run python benchmarks/run.py --dry-run
uv run python benchmarks/run.py --update-readme
```

Yêu cầu:

- `ANTHROPIC_API_KEY` trong `.env.local` hoặc env hiện tại

Output:

- `benchmarks/results/benchmark_<timestamp>.json`
- bảng benchmark trong `README.md` nếu dùng `--update-readme`

### 2. Eval harness

So sánh `__baseline__`, `__terse__`, và từng skill:

```bash
uv run python evals/llm_run.py
uv run --with tiktoken python evals/measure.py
uv run --with tiktoken --with plotly --with kaleido python evals/plot.py
```

Yêu cầu:

- `claude` CLI trên `PATH`

Nếu chưa có CLI, snapshot sẽ ở trạng thái stub. Không thay bằng output bịa.

## Fallback benchmark

Phải có ít nhất 3 case riêng cho fallback clarity:

1. `DROP TABLE`
2. migration nhiều bước có rollback
3. security issue cần giải thích impact

Pass nếu:

- `gon` bỏ nén quá mức
- warning explicit
- các bước tuần tự rõ ràng

## Case outline theo nhóm

### 1. Technical Q&A

Ví dụ:

- `git rebase` vs `git merge`
- khi nào dùng connection pool

Pass nếu:

- ngắn hơn bản verbose
- không mất tradeoff chính
- không đánh rơi điều kiện sử dụng

### 2. Bug explanation

Ví dụ:

- React re-render do object ref mới
- backend race condition khi increment counter

Pass nếu:

- nêu rõ triệu chứng
- nêu đúng nguyên nhân
- nêu được fix hoặc bước debug tiếp

### 3. Code review

Ví dụ:

- null dereference
- thiếu retry 429
- SQL injection

Pass nếu:

- comment dễ paste
- có location/problem/fix
- không throat-clearing

### 4. Commit writing

Ví dụ:

- fix auth expiry bug
- refactor queue retry
- migration breaking change

Pass nếu:

- subject đúng dạng
- body chỉ có khi cần
- lý do rõ hơn mô tả diff

### 5. Prose compression

Ví dụ:

- onboarding guide có code block
- ADR ngắn có bullet list
- runbook có warning

Pass nếu:

- heading vẫn đúng
- code block giữ nguyên
- câu prose ngắn hơn
- warning không bị làm mờ
