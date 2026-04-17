# DECISIONS

## 1. Tạo repo mới thay vì sửa repo gốc

Quyết định:

- Tạo repo mới độc lập `VNcaveman`.

Lý do:

- Repo gốc tối ưu cho tiếng Anh và persona-based compression.
- Tiếng Việt cần rule khác ở tầng discourse, không phải chỉ trim từ đơn.
- Sửa trực tiếp repo gốc sẽ biến dự án thành locale patch thay vì implementation riêng.

## 2. Chọn tên repo `VNcaveman`, giữ skill `gon`

Quyết định:

- Repo dùng tên `VNcaveman`.
- Skill/runtime chính giữ tên `gon`.

Lý do:

- `VNcaveman` nói rõ đây là bản Việt hóa lấy cảm hứng từ repo gốc.
- `gon` vẫn là tên implementation tốt cho skill/runtime vì ngắn và hợp tiếng Việt.
- Tách repo name và skill name giúp giữ branding gần source repo mà không làm vỡ wiring đã có.

## 3. Giữ mental model 3 level: `lite`, `full`, `ultra`

Quyết định:

- Giữ 3 level chính như repo gốc ở mặt UX.
- Không thêm nhánh gimmick.

Lý do:

- Người dùng tooling đã quen 3 mức nén.
- Đủ đơn giản để hook, slash command, docs, examples thống nhất.

## 4. Bỏ `wenyan` và mọi persona mode

Quyết định:

- Không port `wenyan`.
- Không tạo "người tối cổ Việt".

Lý do:

- Không phục vụ productivity của dev Việt.
- Dễ thành giả giọng, khó đọc, giảm tín nhiệm khi review/debug/docs.

Deviation so với repo gốc:

- Repo gốc có `wenyan-lite`, `wenyan-full`, `wenyan-ultra`.
- Repo mới thay bằng localization sâu hơn cho tiếng Việt + clarity fallback mạnh hơn.

## 5. Preserve artifact kỹ thuật là hard boundary

Quyết định:

- Không nén code block, inline code, command, URL, path, env var, version, error, stack trace, JSON/YAML/TOML/SQL/config.

Lý do:

- Token savings phải đến từ prose.
- Sửa một ký tự trong artifact kỹ thuật có thể làm sai hoàn toàn.

## 6. Thêm lexicon tiếng Việt rộng hơn

Quyết định:

- `gon` có bộ từ/cấu trúc cần cắt rộng hơn bản gốc.

Lý do:

- Tiếng Việt có nhiều lớp xã giao, hedge, đệm lời, cụm động từ quan liêu.
- Cần mapping đủ rộng để output không drift về verbose Vietnamese.

## 7. Port lại runtime surfaces thay vì dừng ở spec

Quyết định:

- Không dừng ở docs/spec.
- Port hầu hết runtime surfaces quan trọng của repo gốc:
  - hook system
  - rule copies
  - plugin/manifests
  - benchmark runner
  - eval harness
  - sync workflow
  - compress scripts

Lý do:

- Nếu chỉ có spec, repo không thật sự parity với source repo.
- User yêu cầu "khớp với bản gốc" ở mức repo behavior, không chỉ wording.

## 8. Giữ nguồn sự thật rõ ràng, chấp nhận một ít surface sync

Quyết định:

- `skills/gon/SKILL.md` và `rules/gon-activate.md` là nguồn sự thật cho skill chính và rule.
- `skills/gon-compress/SKILL.md` + `gon-compress/scripts/` là nguồn cho compress.
- Vẫn có bản sync cho plugin/rules/copies vì cần parity distribution.

Lý do:

- Repo gốc sync nhiều surface.
- Bỏ hoàn toàn sync sẽ làm lệch runtime parity.
- Nhưng vẫn cần một nơi sửa chính để tránh drift.

## 9. Auto-clarity là bắt buộc

Quyết định:

- Khi task có risk cao, `gon` phải tăng clarity và giảm nén.

Trigger:

- destructive op
- security issue
- production / infra / database
- migration nhiều bước
- warning quan trọng
- user cần step-by-step chính xác

Lý do:

- Ngắn hơn không quan trọng bằng đúng hơn trong high-risk context.

## 10. Snapshot eval không được bịa

Quyết định:

- Nếu máy chưa có `claude` CLI, `evals/snapshots/results.json` chỉ là stub metadata.

Lý do:

- Repo gốc commit snapshot thật.
- Ở môi trường hiện tại không có `claude` CLI, nên bịa snapshot sẽ sai phương pháp.

Deviation so với repo gốc:

- Harness đã có parity.
- Snapshot chưa được regenerate vì thiếu CLI tại thời điểm cập nhật repo.

## 11. Plugin/manifests dùng URL placeholder cho tới khi publish

Quyết định:

- Giữ manifest structure đầy đủ, nhưng các URL publish để placeholder trung tính.

Lý do:

- Chưa có canonical public repo URL cho `VNcaveman`.
- Tự bịa URL cụ thể còn sai hơn placeholder.

## 12. Assumptions

- Dev Việt quen shorthand kỹ thuật như `prod`, `DB`, `retry`, `guard`, `ref`, `payload`.
- Tone nên trung tính toàn quốc, tránh slang vùng miền quá mạnh.
- `gon` ưu tiên technical productivity, không tối ưu cho content marketing hay giao tiếp đối ngoại.
