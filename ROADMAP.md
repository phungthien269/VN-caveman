# ROADMAP

## Phase 1

- Hoàn thiện spec Vietnamese compression.
- Hoàn thiện 4 skill cốt lõi và quick-help.
- Hoàn thiện README, examples, benchmark docs, internal docs.
- Thiết lập repo-local wiring, hooks, manifests, sync workflow.

## Phase 2

- Chạy benchmark thật trên model thật và commit kết quả đầu tiên.
- Sinh snapshot eval thật bằng `claude` CLI.
- Bổ sung fixture docs thực tế cho `gon-compress`.
- Thu thập prompt thật từ debug, review, commit workflow tiếng Việt.

## Phase 3

- Gắn URL publish chính thức vào plugin/manifests nếu phát hành.
- Thêm CI kiểm tra consistency giữa `skills/`, `docs/`, `examples/`.
- Viết script lint rule để bắt các cụm verbose Việt hay gặp.

## Future improvements

- Thêm bilingual mode: đầu ra ngắn tiếng Việt nhưng giữ proper noun và thuật ngữ tiếng Anh theo ngữ cảnh.
- Thêm team-specific lexicon packs cho backend, frontend, data, SRE.
- Thêm rubric fidelity semi-automatic bằng judge model hoặc human review template.
- Thêm profile "external-facing" để bớt gắt khi trả lời khách hàng nhưng vẫn ngắn.
