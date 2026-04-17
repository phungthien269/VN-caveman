# Gon Hooks

Các hook này dùng cho Claude Code.

## Thành phần

- `gon-activate.js`: SessionStart hook, ghi mode hiện tại và inject rules.
- `gon-mode-tracker.js`: UserPromptSubmit hook, theo dõi `/gon`, `/gon-commit`, `/gon-review`, `/gon-compress`.
- `gon-statusline.sh` / `gon-statusline.ps1`: badge `[GON]`, `[GON:ULTRA]`, ...
- `gon-config.js`: đọc default mode và xử lý flag an toàn.

## Install

Từ local clone:

```bash
bash hooks/install.sh
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File hooks\install.ps1
```

## Uninstall

```bash
bash hooks/uninstall.sh
```

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File hooks\uninstall.ps1
```
