$ErrorActionPreference = "Stop"

$ClaudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $env:USERPROFILE ".claude" }
$HooksDir = Join-Path $ClaudeDir "hooks"
$Settings = Join-Path $ClaudeDir "settings.json"
$FlagFile = Join-Path $ClaudeDir ".gon-active"
$HookFiles = @("package.json", "gon-config.js", "gon-activate.js", "gon-mode-tracker.js", "gon-statusline.sh", "gon-statusline.ps1")

foreach ($hook in $HookFiles) {
    $path = Join-Path $HooksDir $hook
    if (Test-Path $path) {
        Remove-Item $path -Force
    }
}

if ((Test-Path $Settings) -and (Get-Command node -ErrorAction SilentlyContinue)) {
    Copy-Item $Settings "$Settings.bak" -Force
    $env:GON_SETTINGS = $Settings -replace '\\', '/'
    $env:GON_HOOKS_DIR = $HooksDir -replace '\\', '/'
    $nodeScript = @'
const fs = require('fs');
const settingsPath = process.env.GON_SETTINGS;
const hooksDir = process.env.GON_HOOKS_DIR;
const managedStatusLinePath = hooksDir + '/gon-statusline.ps1';
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
  const cmd = typeof settings.statusLine === 'string'
    ? settings.statusLine
    : (settings.statusLine.command || '');
  if (cmd.includes(managedStatusLinePath)) delete settings.statusLine;
}

fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
'@
    node -e $nodeScript
    Remove-Item "$Settings.bak" -Force
}

if (Test-Path $FlagFile) {
    Remove-Item $FlagFile -Force
}

Write-Host "Done. Restart Claude Code to complete gon uninstall." -ForegroundColor Green
