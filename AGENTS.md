@./skills/gon/SKILL.md
@./skills/gon-commit/SKILL.md
@./skills/gon-review/SKILL.md
@./skills/gon-compress/SKILL.md
@./skills/gon-help/SKILL.md

# Working Notes

- Nguồn sự thật cho hành vi nằm ở `skills/` và `docs/caveman-vi-spec.md`.
- Trước khi sửa skill, đọc:
  - `PROJECT_OVERVIEW.md`
  - `DECISIONS.md`
  - `PROGRESS.md`
  - `docs/localization-principles.md`
- Ưu tiên consistency giữa `README.md`, `docs/`, `examples/` và `skills/`.
- Nếu thay đổi behavior, cập nhật luôn:
  - `docs/caveman-vi-spec.md`
  - file example liên quan
  - `PROGRESS.md`
  - `DECISIONS.md` nếu có deviation mới
- Không nén hoặc rewrite literal các artifact kỹ thuật.
- Khi thêm level/rule mới, phải ghi rõ:
  - mục tiêu
  - khi dùng
  - khi không dùng
  - trigger fallback clarity
