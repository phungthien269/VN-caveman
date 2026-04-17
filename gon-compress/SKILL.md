---
name: gon-compress
description: >
  Vietnamese-first prose and documentation compressor. Rewrite markdown or text
  prose into shorter Vietnamese while preserving code blocks, inline code, links,
  paths, commands, config snippets, tables, and important markdown structure.
  Use when the user asks to compress docs, notes, ADRs, guides, or memory files
  without breaking technical artifacts.
---

Nén prose/docs. Không phá code/config/data.

## Scope

Chỉ áp dụng cho:

- `.md`
- `.txt`
- `.rst`
- note/prose file trộn ít code

Không áp dụng cho:

- `.py`, `.js`, `.ts`, `.json`, `.yaml`, `.yml`, `.toml`, `.sql`, `.env`
- file dữ liệu
- file config

## Process

1. Xác định file chủ yếu là prose.
2. Nếu sửa in-place, tạo backup dạng `<filename>.original.<ext>` trước.
3. Nén prose theo level user yêu cầu, mặc định `full`.
4. Giữ nguyên:
   - fenced code block
   - inline code
   - link
   - path
   - command
   - heading structure
   - bảng
5. Nếu file có warning/runbook rủi ro cao, ưu tiên rõ hơn thay vì ngắn hơn.

## Compression Rules

- Cắt xã giao, hedge, câu chuyển ý thừa.
- Rút câu dài thành action sentence.
- Gộp các bullet trùng ý.
- Không đổi heading đang là anchor/link target nếu chưa chắc.
- Không sửa bất kỳ ký tự nào bên trong code/config snippet.

## Validation Checklist

Sau khi nén, tự kiểm:

- số heading có còn hợp lý không
- code block có giữ nguyên không
- link còn đúng không
- command còn chạy được không
- warning có bị làm mờ không

## Boundaries

- Nếu không chắc đoạn nào là code, bỏ qua đoạn đó.
- Nếu user muốn nén file nhạy cảm hoặc có secret, cảnh báo trước và không tự ý gửi nội dung ra ngoài.
