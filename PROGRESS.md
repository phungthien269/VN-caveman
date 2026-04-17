# PROGRESS

## Đã hoàn thành

- [x] Audit repo gốc Caveman: README, CLAUDE, AGENTS, skills, rules, hooks, benchmark/eval/test, compress scripts.
- [x] Tạo repo mới độc lập `VNcaveman`.
- [x] Chốt 3 level `lite`, `full`, `ultra`.
- [x] Bỏ `wenyan` và persona-based compression không hợp tiếng Việt.
- [x] Viết spec Vietnamese compression và localization principles.
- [x] Tạo skill chính `gon`.
- [x] Tạo skill phụ `gon-commit`, `gon-review`, `gon-compress`, `gon-help`.
- [x] Tạo repo-local wiring cho Codex, Claude, Gemini-style surfaces.
- [x] Port hook system từ repo gốc sang `gon`: activate, mode tracker, statusline, install/uninstall.
- [x] Port rule/plugin surfaces: Cline, Copilot, Cursor, Windsurf, Claude plugin, Codex plugin, Gemini extension.
- [x] Port `gon-compress` thành runtime surface có script detect/compress/validate/benchmark.
- [x] Thêm benchmark runner `benchmarks/run.py`.
- [x] Thêm eval harness `evals/llm_run.py`, `measure.py`, `plot.py`.
- [x] Thêm workflow sync surface `.github/workflows/sync-skill.yml`.
- [x] Thêm `CLAUDE.md` làm internal repo guide tương đương repo gốc.
- [x] Viết README, examples, docs benchmark, tài liệu nội bộ usable ngay.

## Còn dang dở

- [ ] Chạy benchmark thật và commit số liệu đầu tiên.
- [ ] Sinh snapshot eval thật bằng `claude` CLI.
- [ ] Quyết định URL publish chính thức cho plugin/manifests.
- [ ] Bổ sung issue templates/FUNDING nếu muốn parity marketing/community đầy đủ như repo gốc.
- [ ] Thu thập prompt thật từ dev Việt để tinh chỉnh thêm lexicon shorthand.

## Next recommended steps

1. Nếu máy có `claude` CLI, chạy `python evals/llm_run.py` rồi `python evals/measure.py`.
2. Nếu có `ANTHROPIC_API_KEY`, chạy `python benchmarks/run.py --update-readme`.
3. Nếu publish repo công khai, thay các URL placeholder trong manifest/plugin metadata.
4. Chạy user test trên prompt thật của team dev Việt và refine rule cắt từ đệm.

## Handover notes

- Đổi behavior skill chính: sửa `skills/gon/SKILL.md`, rồi sync copies.
- Đổi auto-activation rule: sửa `rules/gon-activate.md`, không sửa copy agent-specific.
- Đổi compress runtime: sửa `gon-compress/scripts/`, rồi sync sang `skills/compress/` và plugin copy.
- Muốn kiểm tra parity: chạy `tests/verify_repo.py` trước.
- Muốn hiểu deviation so với repo gốc: đọc `DECISIONS.md`.
