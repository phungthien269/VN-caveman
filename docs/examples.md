# Example Set

## 1. Giải thích bug React

Normal:

> Component này re-render vì bạn đang tạo object mới ở mỗi lần render và truyền object đó qua prop. React so sánh shallow nên lần nào cũng thấy prop mới.

`lite`:

> Component re-render vì mỗi lần render bạn tạo object mới và truyền nó qua prop. React so sánh shallow nên lần nào cũng thấy prop mới.

`full`:

> Re-render do mỗi render tạo object mới. Prop inline luôn ra ref mới. React thấy đổi. Dùng `useMemo`.

`ultra`:

> Inline object -> ref mới -> re-render. `useMemo`.

## 2. Giải thích bug backend

Normal:

> Middleware xác thực của bạn đang so sánh sai đơn vị thời gian nên token vừa hết hạn vẫn được xem là hợp lệ.

`lite`:

> Middleware auth đang so sánh sai đơn vị thời gian nên token vừa hết hạn vẫn được xem là hợp lệ.

`full`:

> Auth middleware lệch đơn vị thời gian. `exp` là giây, `Date.now()` là ms. Nhân `exp * 1000`.

`ultra`:

> `exp` giây, `Date.now()` ms. Nhân `1000`.

## 3. Commit message

Verbose:

> `fix: fix the issue where expired tokens are still accepted by the authentication middleware`

`gon-commit`:

```text
fix(auth): reject expired jwt
```

Có body khi cần:

```text
fix(auth): reject expired jwt

Compare `Date.now()` against `exp * 1000` so tokens expire on time.
```

## 4. Code review finding

Verbose:

> Có vẻ ở đây `user` có thể là null, nên việc truy cập `user.email` sẽ có khả năng làm route bị crash.

`gon-review`:

> `users.ts:L42: bug: \`user\` có thể null. Fix: guard trước \`.email\`.`

## 5. Docs compression

Before:

> Để có thể tránh được việc merge code lỗi lên nhánh chính, bạn nên tiến hành chạy test đầy đủ trước khi merge pull request.

After:

> Chạy test đầy đủ trước merge PR. Tránh đẩy lỗi lên main.

## 6. Trả lời câu hỏi kỹ thuật

Question:

> Khi nào nên dùng queue để gửi email?

Answer:

> Dùng queue khi gửi email không cần block request chính, cần retry, hoặc có burst lớn. Request trả nhanh hơn. Failure handling cũng tách rõ hơn.

## 7. Warning khi lệnh nguy hiểm

Không đúng:

> Chạy lệnh này là xong.

Đúng:

> Cảnh báo: lệnh này xóa dữ liệu vĩnh viễn. Xác nhận môi trường, backup, và rollback plan trước khi chạy.

## 8. Fallback clarity khi nhiều bước

Không đúng:

> Migrate trước. Deploy sau. Check rollback.

Đúng:

> Thứ tự an toàn:
> 1. Chạy migration backward-compatible.
> 2. Deploy app mới.
> 3. Kiểm tra traffic và error rate.
> 4. Chỉ xóa field cũ ở đợt sau.
>
> Nếu migration fail, rollback app trước, rồi mới xử lý dữ liệu.
