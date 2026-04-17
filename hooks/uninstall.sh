#!/bin/bash
set -e

CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
HOOKS_DIR="$CLAUDE_DIR/hooks"
SETTINGS="$CLAUDE_DIR/settings.json"
FLAG_FILE="$CLAUDE_DIR/.gon-active"
HOOK_FILES=("package.json" "gon-config.js" "gon-activate.js" "gon-mode-tracker.js" "gon-statusline.sh")

for hook in "${HOOK_FILES[@]}"; do
  if [ -f "$HOOKS_DIR/$hook" ]; then
    rm "$HOOKS_DIR/$hook"
  fi
done

if [ -f "$SETTINGS" ] && command -v node >/dev/null 2>&1; then
  cp "$SETTINGS" "$SETTINGS.bak"
  GON_SETTINGS="$SETTINGS" GON_HOOKS_DIR="$HOOKS_DIR" node -e "
    const fs = require('fs');
    const settingsPath = process.env.GON_SETTINGS;
    const hooksDir = process.env.GON_HOOKS_DIR;
    const managedStatusLinePath = hooksDir + '/gon-statusline.sh';
    const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));

    const isGonEntry = (entry) =>
      entry && entry.hooks && entry.hooks.some(h => h.command && h.command.includes('gon'));

    if (settings.hooks) {
      for (const event of ['SessionStart', 'UserPromptSubmit']) {
        if (Array.isArray(settings.hooks[event])) {
          settings.hooks[event] = settings.hooks[event].filter(e => !isGonEntry(e));
          if (settings.hooks[event].length === 0) delete settings.hooks[event];
        }
      }
      if (Object.keys(settings.hooks).length === 0) delete settings.hooks;
    }

    if (settings.statusLine) {
      const cmd = typeof settings.statusLine === 'string' ? settings.statusLine : (settings.statusLine.command || '');
      if (cmd.includes(managedStatusLinePath)) delete settings.statusLine;
    }

    fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
  "
  rm -f "$SETTINGS.bak"
fi

rm -f "$FLAG_FILE"
echo "Done. Restart Claude Code to complete gon uninstall."
