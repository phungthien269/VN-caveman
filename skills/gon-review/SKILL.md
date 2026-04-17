---
name: gon-review
description: >
  Vietnamese-first terse code review comments. Output short, actionable findings
  with location, problem, impact, and fix, without praise or throat-clearing.
  Use when reviewing diffs, pull requests, patches, or when the user asks for
  code review comments in a concise developer-friendly format.
---

Viết review comment ngắn, quét nhanh được, paste vào PR được.

## Format

- Một dòng mỗi finding
- Dạng:
  - `file:L42: bug: ... Fix: ...`
  - `L42: risk: ... Fix: ...`

Severity:

- `bug`
- `risk`
- `nit`
- `q`

## Rules

- Nêu đúng vấn đề trước.
- Nêu fix cụ thể, không nói chung chung.
- Dùng symbol/tên biến/hàm đúng nguyên văn trong backticks nếu cần.
- Không khen từng comment.
- Không hedge kiểu `có vẻ`, `có thể`, `mình nghĩ` trừ khi thật sự chưa chắc.

## Auto-Clarity

Nếu finding thuộc:

- security
- architecture tradeoff lớn
- onboarding context

thì cho phép viết 1 đoạn ngắn rõ ràng hơn trước, sau đó quay lại format ngắn.

## Examples

- `auth.ts:L38: bug: \`exp\` đang so với ms trực tiếp. Fix: đổi sang \`exp * 1000\`.`
- `users.ts:L42: bug: \`user\` có thể null. Fix: guard trước \`.email\`.`
- `jobs.ts:L21: risk: retry 429 chưa có backoff. Fix: thêm exponential backoff.`
- `api.ts:L88: q: route này có cần auth không. Hiện public toàn bộ payload.`
