#!/bin/bash
# gon — local hook installer for Claude Code
set -e

FORCE=0
for arg in "$@"; do
  case "$arg" in
    --force|-f) FORCE=1 ;;
  esac
done

if ! command -v node >/dev/null 2>&1; then
  echo "ERROR: node is required to install gon hooks."
  exit 1
fi

CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
HOOKS_DIR="$CLAUDE_DIR/hooks"
SETTINGS="$CLAUDE_DIR/settings.json"
HOOK_FILES=("package.json" "gon-config.js" "gon-activate.js" "gon-mode-tracker.js" "gon-statusline.sh")

SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)"
fi

if [ -z "$SCRIPT_DIR" ]; then
  echo "ERROR: install.sh must run from a local clone."
  exit 1
fi

ALREADY_INSTALLED=0
if [ "$FORCE" -eq 0 ]; then
  ALL_FILES_PRESENT=1
  for hook in "${HOOK_FILES[@]}"; do
    if [ ! -f "$HOOKS_DIR/$hook" ]; then
      ALL_FILES_PRESENT=0
      break
    fi
  done
  if [ "$ALL_FILES_PRESENT" -eq 1 ] && [ -f "$SETTINGS" ]; then
    if GON_SETTINGS="$SETTINGS" node -e "
      const fs = require('fs');
      const settings = JSON.parse(fs.readFileSync(process.env.GON_SETTINGS, 'utf8'));
      const hasGonHook = (event) =>
        Array.isArray(settings.hooks?.[event]) &&
        settings.hooks[event].some(e =>
          e.hooks && e.hooks.some(h => h.command && h.command.includes('gon'))
        );
      process.exit(hasGonHook('SessionStart') && hasGonHook('UserPromptSubmit') && !!settings.statusLine ? 0 : 1);
    " >/dev/null 2>&1; then
      ALREADY_INSTALLED=1
    fi
  fi
fi

if [ "$ALREADY_INSTALLED" -eq 1 ] && [ "$FORCE" -eq 0 ]; then
  echo "Gon hooks already installed."
  echo "Nothing to do."
  exit 0
fi

mkdir -p "$HOOKS_DIR"
for hook in "${HOOK_FILES[@]}"; do
  cp "$SCRIPT_DIR/$hook" "$HOOKS_DIR/$hook"
done
chmod +x "$HOOKS_DIR/gon-statusline.sh"

if [ ! -f "$SETTINGS" ]; then
  echo '{}' > "$SETTINGS"
fi
cp "$SETTINGS" "$SETTINGS.bak"

GON_SETTINGS="$SETTINGS" GON_HOOKS_DIR="$HOOKS_DIR" node -e "
  const fs = require('fs');
  const settingsPath = process.env.GON_SETTINGS;
  const hooksDir = process.env.GON_HOOKS_DIR;
  const managedStatusLinePath = hooksDir + '/gon-statusline.sh';
  const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
  if (!settings.hooks) settings.hooks = {};

  if (!settings.hooks.SessionStart) settings.hooks.SessionStart = [];
  const hasStart = settings.hooks.SessionStart.some(e =>
    e.hooks && e.hooks.some(h => h.command && h.command.includes('gon'))
  );
  if (!hasStart) {
    settings.hooks.SessionStart.push({
      hooks: [{
        type: 'command',
        command: 'node \"' + hooksDir + '/gon-activate.js\"',
        timeout: 5,
        statusMessage: 'Loading gon mode...'
      }]
    });
  }

  if (!settings.hooks.UserPromptSubmit) settings.hooks.UserPromptSubmit = [];
  const hasPrompt = settings.hooks.UserPromptSubmit.some(e =>
    e.hooks && e.hooks.some(h => h.command && h.command.includes('gon'))
  );
  if (!hasPrompt) {
    settings.hooks.UserPromptSubmit.push({
      hooks: [{
        type: 'command',
        command: 'node \"' + hooksDir + '/gon-mode-tracker.js\"',
        timeout: 5,
        statusMessage: 'Tracking gon mode...'
      }]
    });
  }

  if (!settings.statusLine) {
    settings.statusLine = {
      type: 'command',
      command: 'bash \"' + managedStatusLinePath + '\"'
    };
  }

  fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
"

echo "Done. Restart Claude Code to activate gon."
