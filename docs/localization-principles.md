# Localization Principles

## Mục tiêu localize

Localize theo behavior, không localize theo bề mặt từ ngữ.

Điều cần giữ từ repo gốc:

- token efficiency
- technical fidelity
- persistence
- fallback clarity
- distinct auxiliary skills

Điều không nên giữ nguyên:

- article trimming kiểu tiếng Anh
- persona "caveman"
- gimmick cổ ngữ

## Nguyên tắc 1: Cắt ở tầng discourse trước, từ vựng sau

Với tiếng Việt, phần phình token thường đến từ:

- mở bài xã giao
- xác nhận thừa
- hedge
- câu chuyển ý
- cấu trúc công vụ

Không nên bắt đầu bằng rút mọi từ ngắn nhất. Nên bắt đầu bằng bỏ lớp câu không mang thêm ý.

## Nguyên tắc 2: Giữ thuật ngữ kỹ thuật bằng ngôn ngữ gốc khi đó là cách dev Việt thực sự dùng

Ví dụ nên giữ:

- `re-render`
- `stale closure`
- `race condition`
- `guard`
- `retry`
- `rollback`
- `migration`

Không ép Việt hóa nếu làm output dài hơn hoặc lạ hơn.

## Nguyên tắc 3: Không giả giọng

Repo này không mô phỏng người tối cổ, không viết tiếng Việt ngắc ngứ có chủ ý.

Output tốt là:

- ngắn
- tự nhiên
- dev-like
- đủ sắc

Output xấu là:

- cố tình bẻ ngữ pháp
- cắt từ vô nghĩa
- meme hóa câu trả lời

## Nguyên tắc 4: Rút cụm động từ dài dòng về động từ thật

Ưu tiên:

- `kiểm tra` thay cho `tiến hành kiểm tra`
- `xử lý` thay cho `thực hiện việc xử lý`
- `gọi API` thay cho `thực hiện thao tác gọi API`
- `do` thay cho `nguyên nhân là do`

## Nguyên tắc 5: Không xóa dấu hiệu bất định khi bất định là thông tin quan trọng

Ví dụ:

- Không đổi `chưa xác nhận được root cause` thành `root cause là ...`
- Không đổi `khả năng cao` thành khẳng định chắc chắn nếu chưa đủ bằng chứng

Rule:

- Xóa hedge mặc định.
- Giữ hedge nếu nó thể hiện trạng thái epistemic thật.

## Nguyên tắc 6: Rút gọn nhưng phải giữ hướng hành động

Một câu nén tốt thường có dạng:

- `vấn đề -> nguyên nhân -> fix`
- `rủi ro -> ảnh hưởng -> hành động`
- `triệu chứng -> chỗ lỗi -> bước tiếp theo`

Nếu nén mà mất next step, chất lượng giảm.

## Nguyên tắc 7: Fallback clarity phải mạnh hơn compression

Khi có risk cao, hệ thống phải ưu tiên:

- rõ
- đủ bước
- cảnh báo rõ ràng
- explicit environment check

Không được tiếc token trong:

- production ops
- destructive SQL
- auth/security
- infra change
- migration data

## Nguyên tắc 8: Bộ từ tiếng Việt phải đủ rộng

Spec cần bao quát biến thể thường gặp, không chỉ một vài từ khóa đơn lẻ.

Nhóm tối ưu chính:

- xã giao: `chắc chắn rồi`, `mình rất vui được hỗ trợ`, `để mình giúp bạn nhé`
- hedge: `mình nghĩ`, `có vẻ`, `khả năng cao`, `nhiều khả năng`, `có lẽ`
- đệm lời: `thực ra`, `về cơ bản`, `nói chung là`, `kiểu như`
- cấu trúc dài: `trong trường hợp mà`, `để có thể`, `ở thời điểm hiện tại`, `tiến hành`

## Nguyên tắc 9: Ví dụ phải là tiếng Việt thật

Không dùng ví dụ dịch y chang từ tiếng Anh nếu câu đó không phải cách dev Việt thật sự nói.

Ví dụ tốt:

- `Req nào cũng tạo object options mới nên memo miss.`

Ví dụ kém:

- `Thuộc tính object inline dẫn đến việc tái kết xuất.`

## Nguyên tắc 10: Kiểm tra tự nhiên trước, tiết kiệm token sau

Nếu hai câu tiết kiệm ngang nhau:

- chọn câu tự nhiên hơn
- chọn câu ít gây hiểu nhầm hơn
- chọn câu giống cách dev Việt thực tế nói hơn
