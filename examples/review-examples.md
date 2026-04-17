# Review Examples

## Null dereference

Verbose:

> Mình nghĩ chỗ này có thể gây crash vì `user` có thể là null nhưng phía dưới vẫn truy cập `user.email`.

`gon-review`:

> `users.ts:L42: bug: \`user\` có thể null. Fix: guard trước \`.email\`.`

## No retry on 429

Verbose:

> Có vẻ đoạn gọi API này chưa xử lý trường hợp bị rate limit, nên request có thể fail hàng loạt khi upstream trả 429.

`gon-review`:

> `api.ts:L21: risk: chưa retry 429. Fix: thêm exponential backoff.`

## SQL injection

Verbose:

> Route này đang nội suy trực tiếp `req.params.id` vào câu SQL nên có nguy cơ SQL injection.

`gon-review`:

> `routes.ts:L12: bug: nội suy \`req.params.id\` vào SQL. Fix: param hóa query.`

## Question, not assertion

`gon-review`:

> `auth.ts:L55: q: route này có chủ đích public không. Hiện bỏ qua auth guard.`
