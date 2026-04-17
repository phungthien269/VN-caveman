# PROJECT OVERVIEW

## Repo này là gì

`VNcaveman` là repo độc lập chứa implementation skill `gon` cho agent trả lời tiếng Việt kỹ thuật theo phong cách ngắn, trực diện, ít token, nhưng vẫn giữ đầy đủ nội dung quan trọng.

Repo này không phải bản dịch của Caveman. Nó là một redesign cho ngữ cảnh tiếng Việt:

- tiếng Việt có nhiều lớp xã giao và hedge hơn tiếng Anh
- nhiều câu dài là do thói quen diễn đạt, không phải do thiếu ý
- dev Việt thường đọc tốt shorthand vừa phải, nhưng không chấp nhận câu tối nghĩa

## Tại sao repo này tồn tại

Các prompt terse kiểu tiếng Anh thường tối ưu bằng:

- bỏ article
- bỏ preposition
- rút ngắn câu theo telegraph English

Các rule đó không map thẳng sang tiếng Việt. Nếu dịch literal sẽ dẫn tới:

- văn phong giả trân
- mất tự nhiên
- mất nghĩa ngữ dụng
- giảm chất lượng giải thích kỹ thuật

`gon` tồn tại để giải quyết đúng bài toán tiếng Việt:

- cắt token thừa
- giữ nguyên technical fidelity
- tăng tốc đọc
- vẫn an toàn khi đụng production, security, migration, destructive ops

## Mục tiêu

- Tạo skill chính tiếng Việt-first cho agent response compression.
- Tạo skill phụ cho commit, review và docs compression.
- Định nghĩa rõ Vietnamese compression rules.
- Có benchmark và regression checklist để review chất lượng.
- Có tài liệu nội bộ đủ rõ để agent khác tiếp tục ngay.

## Non-goals

- Không tối ưu cho văn phong marketing hoặc sales.
- Không cố bắt chước persona "hang động".
- Không nén bằng cách xóa thông tin rủi ro, cảnh báo hoặc bước thao tác quan trọng.
- Không hứa publish marketplace/public package khi chưa có URL chính thức.

## Phạm vi

Trong repo hiện tại:

- skill chính `gon`
- skill phụ `gon-commit`
- skill phụ `gon-review`
- skill phụ `gon-compress`
- skill phụ `gon-help`
- hook system cho Claude Code
- rule/plugin surfaces cho Codex, Claude, Gemini, Cursor, Windsurf, Cline, Copilot
- benchmark runner, eval harness, verify scripts
- spec, examples, benchmark docs, progress docs

Ngoài phạm vi hiện tại:

- benchmark number thật nếu máy chưa có model access
- snapshot eval thật nếu máy chưa có `claude` CLI
- package publish chính thức

## Cách dùng tổng quan

1. Đọc `README.md` để hiểu nhanh mức độ nén và cách bật/tắt.
2. Đọc `skills/gon/SKILL.md` để dùng skill chính.
3. Đọc `docs/caveman-vi-spec.md` nếu cần chỉnh behavior.
4. Dùng `examples/` và `tests/` để đối chiếu trước khi sửa rule.
5. Cập nhật `PROGRESS.md` và `DECISIONS.md` sau mỗi thay đổi đáng kể.
