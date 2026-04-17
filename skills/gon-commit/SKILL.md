---
name: gon-commit
description: >
  Vietnamese-first terse commit message generator for engineering work.
  Produce short, exact commit messages with Conventional Commits style,
  minimal body, and no filler. Use when the user asks for a commit message,
  says "write commit", "commit message", "viết commit", or wants a short,
  clean summary of staged changes.
---

Viết commit ngắn, rõ, đúng chuẩn. Ưu tiên lý do hơn kể lại diff.

## Rules

Subject:

- Dạng: `<type>(<scope>): <imperative summary>`
- Scope optional
- Ưu tiên ≤ 50 ký tự, hard cap 72
- Không dấu chấm cuối
- Dùng động từ ngắn: `add`, `fix`, `drop`, `guard`, `retry`

Types:

- `feat`
- `fix`
- `refactor`
- `perf`
- `docs`
- `test`
- `chore`
- `build`
- `ci`
- `revert`

Body:

- Bỏ nếu subject đã đủ rõ
- Chỉ thêm khi cần nêu:
  - tại sao
  - breaking change
  - migration note
  - security impact
- Wrap khoảng 72 ký tự

Không viết:

- `This commit ...`
- `Mình đã ...`
- AI attribution
- lan man theo file-by-file diff

## Auto-Clarity

Luôn thêm body nếu commit liên quan:

- breaking change
- migration dữ liệu
- security fix
- revert production issue

## Examples

Ngắn:

```text
fix(auth): reject expired jwt
```

Có body:

```text
fix(auth): reject expired jwt

Compare `Date.now()` with `exp * 1000` so tokens expire at the
correct boundary.
```

```text
feat(api)!: rename checkout endpoint

BREAKING CHANGE: `/v1/orders` is replaced by `/v1/checkout`.
Clients must migrate before the next release.
```
