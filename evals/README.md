# Evals

`evals/` đo mức nén thật của `gon` bằng cách chạy cùng một bộ prompt qua Claude Code theo ba điều kiện, rồi so token output.

## Ba arm

| Arm | System prompt |
|-----|--------------|
| `__baseline__` | không thêm system prompt |
| `__terse__` | `Answer concisely in Vietnamese.` |
| `<skill>` | `Answer concisely in Vietnamese.\n\n{SKILL.md}` |

Delta đáng tin là **`<skill>` vs `__terse__`**. So `<skill>` với baseline sẽ trộn lẫn tác dụng của skill với tác dụng của câu "hãy trả lời ngắn".

## Vì sao thiết kế như vậy

- Dùng output thật từ LLM, không lấy ví dụ viết tay.
- Dùng đúng surface skill đang nhắm tới: Claude Code CLI.
- Snapshot commit vào repo để review được diff và CI không cần gọi model.
- Có control arm để tách riêng hiệu ứng "viết ngắn" chung.

## File

- `prompts/vi.txt`: bộ prompt kỹ thuật tiếng Việt, mỗi dòng một prompt.
- `llm_run.py`: chạy `claude -p --system-prompt ...`, ghi `snapshots/results.json`.
- `measure.py`: đọc snapshot, đếm token bằng `tiktoken o200k_base`, in bảng markdown.
- `plot.py`: vẽ boxplot từ snapshot.
- `snapshots/results.json`: source of truth gần nhất. Nếu chưa có `claude` CLI, file này có thể ở trạng thái stub.

## Làm mới snapshot

Yêu cầu:

- `claude` CLI có trên `PATH`
- đã login

```bash
uv run python evals/llm_run.py
```

Dùng model nhỏ nếu muốn tiết kiệm:

```bash
GON_EVAL_MODEL=claude-haiku-4-5 uv run python evals/llm_run.py
```

Đổi file prompt nếu cần:

```bash
GON_EVAL_PROMPTS=evals/prompts/vi.txt uv run python evals/llm_run.py
```

## Đọc snapshot

Không cần gọi model:

```bash
uv run --with tiktoken python evals/measure.py
```

Vẽ chart:

```bash
uv run --with tiktoken --with plotly --with kaleido python evals/plot.py
```

## Trạng thái hiện tại của repo này

Repo có đủ harness để chạy eval như repo gốc. Snapshot đang phụ thuộc việc máy chạy có `claude` CLI hay không. Nếu CLI chưa có, `results.json` giữ metadata stub thay vì số liệu bịa.

## Không đo cái gì

- Độ đúng nghĩa: skill có thể ngắn hơn nhưng sai hơn.
- Latency hay cost end-to-end.
- Hành vi cross-model.
- Claude tokenizer chính xác tuyệt đối; `tiktoken` chỉ là xấp xỉ.
