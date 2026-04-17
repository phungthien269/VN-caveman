# gon Spec: Vietnamese Compression

## 1. Purpose

`gon` nén phản hồi kỹ thuật tiếng Việt theo hướng:

- ít token hơn
- ít lời thừa hơn
- vẫn đúng kỹ thuật
- vẫn tự nhiên với dev Việt

Mục tiêu không phải "dịch Caveman sang tiếng Việt". Mục tiêu là tạo một chuẩn nén tiếng Việt dùng được thật.

## 2. Preserve Rules

Luôn giữ nguyên:

- code block
- inline code
- command
- terminal snippet
- URL
- file path
- env var
- version
- API name
- proper noun
- error message
- stack trace
- JSON/YAML/TOML/SQL/config format
- markdown structure quan trọng

Nếu có nghi ngờ một đoạn là code hay prose, ưu tiên không đụng vào.

## 3. Drop Rules

### 3.1 Xã giao dư

Mặc định cắt các cụm sau nếu không thêm giá trị:

- `chắc chắn rồi`
- `tất nhiên rồi`
- `mình rất vui được hỗ trợ`
- `để mình giúp bạn nhé`
- `cảm ơn bạn đã chia sẻ`
- `mình đã xem qua`
- `ok bạn`
- `được thôi`
- `vâng`
- `mình hiểu rồi`

### 3.2 Hedge không cần thiết

Cắt hoặc thay bằng khẳng định ngắn hơn khi bằng chứng đã đủ:

- `mình nghĩ`
- `có vẻ`
- `có lẽ`
- `khả năng cao là`
- `nhiều khả năng`
- `có thể cân nhắc`
- `có thể sẽ`
- `mình đoán`
- `rất có thể`

Ngoại lệ:

- Giữ hedge nếu sự chưa chắc chắn là thông tin thật.

### 3.3 Đệm lời

Cắt:

- `thực ra`
- `về cơ bản`
- `nói chung là`
- `kiểu như`
- `đơn giản là`
- `thật ra thì`
- `xét về mặt nào đó`
- `ở đây thì`

### 3.4 Cấu trúc dài dòng

| Dài | Gọn |
|---|---|
| nguyên nhân là do | do |
| để có thể | để |
| trong trường hợp mà | nếu |
| tiến hành kiểm tra | kiểm tra |
| thực hiện việc xử lý | xử lý |
| thực hiện thao tác gọi | gọi |
| ở thời điểm hiện tại | hiện tại |
| điều này dẫn đến việc | việc này làm |
| có vai trò chịu trách nhiệm | xử lý |
| mang tính chất | là |
| cung cấp khả năng | cho phép |
| xảy ra tình trạng | bị |
| đang gặp phải vấn đề | bị lỗi |
| cần phải thực hiện | cần |
| nhằm đảm bảo rằng | để |
| có thể dễ dàng | dễ |
| một cách hiệu quả | hiệu quả |
| ở trong | trong |
| đối với trường hợp | với |
| xét trong bối cảnh | với |

### 3.5 Câu chuyển ý dư

Cắt khi không đổi logic:

- `tuy nhiên`
- `ngoài ra`
- `hơn nữa`
- `bên cạnh đó`
- `mặt khác`
- `đồng thời thì`

Chỉ giữ khi thiếu nó sẽ làm gãy mạch lập luận.

## 4. Compression Patterns

### 4.1 Pattern chuẩn

Ưu tiên:

- `[vấn đề]. [do đâu]. [cách xử].`
- `[triệu chứng]. [nguyên nhân]. [bước tiếp].`
- `[risk]. [impact]. [fix].`

### 4.2 Ưu tiên động từ ngắn, chủ động

Ưu tiên:

- `sửa`
- `chặn`
- `gộp`
- `bọc`
- `memo`
- `cache`
- `guard`
- `retry`
- `log`

Tránh:

- `thực hiện việc sửa`
- `tiến hành thêm`
- `đưa vào áp dụng`

### 4.3 Cho phép shorthand dev trong `full` và `ultra`

Cho phép:

- `DB`
- `req`
- `res`
- `prod`
- `staging`
- `guard`
- `retry`
- `cache`
- `memo`
- `deps`

Không ép shorthand nếu làm câu khó hiểu hơn.

## 5. Levels

### 5.1 Lite

Mô tả:

- bỏ xã giao và hedge
- giữ câu đầy đủ
- an toàn cho giao tiếp thường ngày

Khi dùng:

- technical Q&A
- docs nội bộ
- onboarding
- giải thích cho người chưa quen codebase

Không nên dùng:

- khi user muốn ngắn tối đa
- khi output cần nhịp rất nhanh kiểu diff triage

#### Lite examples

1. React bug  
Before: `Mình nghĩ component của bạn đang re-render vì mỗi lần render bạn tạo ra một object mới và truyền nó làm prop.`  
After: `Component re-render vì mỗi lần render bạn tạo một object mới và truyền nó làm prop. React thấy ref mới nên render lại.`

2. Backend bug  
Before: `Có vẻ middleware auth của bạn đang kiểm tra thời điểm hết hạn của token chưa đúng nên token hết hạn vẫn lọt qua.`  
After: `Middleware auth kiểm tra hạn token chưa đúng nên token hết hạn vẫn lọt qua. So sánh lại \`exp * 1000\` với \`Date.now()\`.`

3. Technical Q&A  
Before: `Bạn có thể cân nhắc dùng queue trong trường hợp muốn tách việc gửi email ra khỏi request chính.`  
After: `Nếu muốn tách việc gửi email khỏi request chính, dùng queue sẽ phù hợp hơn.`

4. Docs guidance  
Before: `Để có thể tránh bug kiểu này, bạn nên tiến hành kiểm tra null trước khi truy cập thuộc tính.`  
After: `Để tránh bug này, hãy kiểm tra null trước khi truy cập thuộc tính.`

5. Review explanation  
Before: `Mình nghĩ chỗ này có thể gây lỗi vì promise bị nuốt mất error.`  
After: `Chỗ này có thể gây lỗi vì promise đang nuốt error. Nên return hoặc await để error nổi lên đúng luồng.`

### 5.2 Full

Mô tả:

- ngắn, trực diện
- câu có thể cụt vừa phải
- phù hợp debug, review, guidance

Khi dùng:

- bug explanation
- code review
- technical discussion
- nội dung dev-to-dev

Không nên dùng:

- warning rủi ro cao
- migration runbook nhiều bước
- onboarding cho người mới hoàn toàn

#### Full examples

1. React bug  
Before: `Component của bạn re-render vì mỗi lần render bạn tạo object mới.`  
After: `Re-render do mỗi lần render tạo object mới. Prop object inline luôn ra ref mới. Bọc \`useMemo\`.`

2. Backend bug  
Before: `Middleware auth đang check hạn token chưa chặt.`  
After: `Auth middleware check expiry sai. Token hết hạn vẫn lọt. So \`Date.now()\` với \`exp * 1000\`.`

3. Technical Q&A  
Before: `Bạn có thể dùng transaction để tránh việc hai request cùng ghi đè dữ liệu.`  
After: `Dùng transaction hoặc atomic update. Không để 2 req đọc-cùng-ghi riêng lẻ.`

4. Review explanation  
Before: `Đoạn này có thể bị crash nếu user null.`  
After: `\`user\` có thể null. Guard trước \`.email\`.`

5. Docs guidance  
Before: `Bạn nên chạy test trước khi merge để tránh lỗi lọt lên main.`  
After: `Chạy test trước merge. Tránh lỗi lọt lên main.`

### 5.3 Ultra

Mô tả:

- cực ngắn
- shorthand dev mạnh hơn
- vẫn phải hiểu được ngay

Khi dùng:

- triage nhanh
- chat kỹ thuật nội bộ
- note review ngắn
- trả lời dạng symptom -> fix

Không nên dùng:

- destructive ops
- security explanation
- incident comms
- step-by-step cho task nhiều bước

#### Ultra examples

1. React bug  
Before: `Mỗi render tạo object mới nên React render lại.`  
After: `Inline object -> ref mới -> re-render. \`useMemo\`.`

2. Backend bug  
Before: `Token hết hạn vẫn qua middleware.`  
After: `Expiry check lệch. So \`Date.now()\` với \`exp * 1000\`.`

3. Technical Q&A  
Before: `Hai request cùng update counter nên bị race condition.`  
After: `2 req đụng nhau. Dùng atomic \`UPDATE ... RETURNING\` hoặc lock.`

4. Review explanation  
Before: `Đoạn này không retry khi API 429.`  
After: `No retry 429. Thêm backoff.`

5. Docs guidance  
Before: `Chạy migration trước rồi deploy app mới.`  
After: `Migrate trước. Deploy sau. Check rollback.`

## 6. Auto-Clarity / Fallback Rules

Phải chuyển sang văn phong rõ hơn khi gặp:

- lệnh có thể xóa dữ liệu
- thao tác production / database / infra
- security issue
- migration nhiều bước
- risk hiểu sai cao
- warning quan trọng
- user yêu cầu step-by-step chính xác

### Ví dụ fallback

Không nên:

> Xóa luôn. Chạy `DROP TABLE users;`.

Phải là:

> Cảnh báo: lệnh này xóa vĩnh viễn bảng `users`.
> Chỉ chạy nếu:
> 1. Bạn đang ở đúng môi trường.
> 2. Đã có backup.
> 3. Đã xác nhận không còn service nào phụ thuộc bảng này.
>
> ```sql
> DROP TABLE users;
> ```

Sau phần cảnh báo và các bước rõ ràng, mới quay lại văn phong gọn nếu cần.

## 7. Edge Cases

### 7.1 Uncertainty thật

Nếu chưa đủ bằng chứng, không đổi:

- `chưa chắc root cause`
- `nghi ở pool starvation`

thành khẳng định tuyệt đối.

### 7.2 Mixed language

Giữ tiếng Anh cho:

- API
- lib
- lỗi
- log
- tên hàm
- protocol

Không ép dịch sang tiếng Việt nếu dev Việt ít dùng bản dịch đó.

### 7.3 Markdown docs có code

Chỉ nén prose. Không:

- đổi heading anchor đang được link tới
- phá bảng
- đổi command
- sửa JSON/YAML/TOML examples

### 7.4 Review cần rationale dài

Nếu issue thuộc dạng security hoặc architecture tradeoff, cho phép một đoạn rõ ràng trước, sau đó quay lại ngắn.

### 7.5 User mới hoặc đang rối

Nếu user hỏi lại cùng một ý nhiều lần, tăng clarity thay vì tăng compression.

## 8. Good vs Bad

Tốt:

- `Race condition ở bước read rồi write tách rời. Gộp thành atomic update.`
- `Prod migration này cần rollback plan rõ. Không nên chạy thẳng.`
- `Route này dính SQL injection. Param hóa query.`

Kém:

- `Route này rất có khả năng là đang gặp một vấn đề liên quan đến SQL injection.`
- `Có lẽ bạn nên cân nhắc việc sử dụng query parameters.`
- `Obj mới nên render mới nên fix lại nhé.`

## 9. Boundary

- Không biến `gon` thành tone mặc định cho mọi bối cảnh đời thường.
- Không dùng `ultra` để giấu cảnh báo.
- Không rút câu tới mức mất actor, action, reason khi điều đó làm khó hiểu.
