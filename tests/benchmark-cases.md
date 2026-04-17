# Benchmark Cases

## 1. Technical Q&A

### Case 1

Prompt:

> Giải thích khác nhau giữa `git rebase` và `git merge`. Khi nào dùng mỗi cái?

Pass:

- câu trả lời ngắn hơn bản verbose
- có nêu tradeoff
- có cảnh báo không rebase branch đã share

### Case 2

Prompt:

> Khi nào nên dùng connection pool cho PostgreSQL?

Pass:

- nêu mục đích reuse connection
- nêu impact tới latency hoặc load
- không sa đà định nghĩa textbook

## 2. Bug Explanation

### Case 3

Prompt:

> Vì sao component React của tôi re-render liên tục khi props không đổi nhưng tôi đang truyền object inline?

Pass:

- nói rõ ref mới mỗi render
- nêu `useMemo` hoặc pattern tương đương

### Case 4

Prompt:

> Endpoint increment counter đôi lúc trả cùng giá trị cho nhiều request đồng thời.

Pass:

- nêu race condition
- nêu atomic update / transaction / lock

## 3. Code Review

### Case 5

Prompt:

> Review route SQL này và comment ngắn:
>
> ```js
> app.get('/users/:id', (req, res) => {
>   db.query(`SELECT * FROM users WHERE id = ${req.params.id}`)
> })
> ```

Pass:

- format một dòng
- chỉ ra SQL injection
- fix là parameterized query

## 4. Commit Writing

### Case 6

Scenario:

- staged diff sửa bug token expiry

Pass:

- subject ngắn
- đúng conventional commit
- body chỉ có nếu cần

### Case 7

Scenario:

- breaking change rename endpoint

Pass:

- dùng `!` hoặc body `BREAKING CHANGE`
- có migration note

## 5. Prose Compression

### Case 8

Input:

- file markdown có heading, bullet, code block, command

Pass:

- prose ngắn hơn
- code block giữ nguyên
- heading và structure còn đúng

### Case 9

Input:

- runbook có warning production

Pass:

- warning không bị nén thành mơ hồ
- step order còn rõ

## 6. Fallback Clarity

### Case 10

Prompt:

> Cho tôi lệnh xóa toàn bộ bảng `users`.

Pass:

- có cảnh báo rõ
- yêu cầu xác nhận backup / environment
- không trả lời kiểu `DROP luôn`
