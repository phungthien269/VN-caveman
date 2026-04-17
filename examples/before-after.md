# Before / After

## 1. React re-render

Before:

> Có khả năng component của bạn bị re-render vì bạn đang truyền một object được tạo mới ở mỗi lần render xuống prop.

After:

> Re-render do mỗi render tạo object mới. Prop inline ra ref mới. Dùng `useMemo`.

## 2. Backend auth bug

Before:

> Mình nghĩ middleware auth của bạn đang kiểm tra hạn token chưa chính xác nên token hết hạn vẫn có thể lọt qua.

After:

> Auth middleware check expiry sai. Token hết hạn vẫn lọt. So `Date.now()` với `exp * 1000`.

## 3. Counter race condition

Before:

> Trong trường hợp có nhiều request cùng lúc thì logic hiện tại có thể dẫn tới việc hai request cùng đọc một giá trị rồi ghi đè lên nhau.

After:

> Race do read rồi write tách rời. 2 req đọc cùng giá trị, rồi ghi đè nhau. Dùng atomic update hoặc transaction.

## 4. Git Q&A

Before:

> Bạn có thể cân nhắc dùng rebase khi muốn giữ lịch sử gọn hơn, còn merge phù hợp khi muốn giữ đầy đủ bối cảnh tích hợp branch.

After:

> `rebase` để lịch sử thẳng, sạch. `merge` để giữ đủ nhánh và context tích hợp. Đừng rebase branch đã share rộng.

## 5. Dangerous SQL

Before:

> Ok, mình sẽ chạy lệnh xóa bảng cho bạn.

After:

> Cảnh báo: lệnh này xóa vĩnh viễn bảng `users`. Xác nhận môi trường và backup trước khi chạy.
