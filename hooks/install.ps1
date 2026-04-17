param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: node is required to install gon hooks." -ForegroundColor Red
    exit 1
}

$ClaudeDir = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $env:USERPROFILE ".claude" }
$HooksDir = Join-Path $ClaudeDir "hooks"
$Settings = Join-Path $ClaudeDir "settings.json"
$HookFiles = @("package.json", "gon-config.js", "gon-activate.js", "gon-mode-tracker.js", "gon-statusline.sh", "gon-statusline.ps1")
$ScriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { $null }

if (-not $ScriptDir) {
    Write-Host "ERROR: install.ps1 must run from a local clone." -ForegroundColor Red
    exit 1
}

if (-not $Force -and (Test-Path $Settings)) {
    try {
        $settingsObj = Get-Content $Settings -Raw | ConvertFrom-Json
        $hasGonHook = {
            param([string]$eventName)
            if (-not $settingsObj.hooks) { return $false }
            $entries = $settingsObj.hooks.$eventName
            if (-not $entries) { return $false }
            foreach ($entry in $entries) {
                foreach ($hookDef in $entry.hooks) {
                    if ($hookDef.command -and $hookDef.command.Contains("gon")) { return $true }
                }
            }
            return $false
        }
        if ((& $hasGonHook "SessionStart") -and (& $hasGonHook "UserPromptSubmit") -and $null -ne $settingsObj.statusLine) {
            Write-Host "Gon hooks already installed."
            Write-Host "Nothing to do."
            exit 0
        }
    } catch {}
}

if (-not (Test-Path $HooksDir)) {
    New-Item -ItemType Directory -Path $HooksDir -Force | Out-Null
}

foreach ($hook in $HookFiles) {
    Copy-Item (Join-Path $ScriptDir $hook) (Join-Path $HooksDir $hook) -Force
}

if (-not (Test-Path $Settings)) {
    Set-Content -Path $Settings -Value "{}"
}
Copy-Item $Settings "$Settings.bak" -Force

$env:GON_SETTINGS = $Settings -replace '\\', '/'
$env:GON_HOOKS_DIR = $HooksDir -replace '\\', '/'

$nodeScript = @'
const fs = require('fs');
const settingsPath = process.env.GON_SETTINGS;
const hooksDir = process.env.GON_HOOKS_DIR;
const managedStatusLinePath = hooksDir + '/gon-statusline.ps1';
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
      command: 'node "' + hooksDir + '/gon-activate.js"',
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
      command: 'node "' + hooksDir + '/gon-mode-tracker.js"',
      timeout: 5,
      statusMessage: 'Tracking gon mode...'
    }]
  });
}

if (!settings.statusLine) {
  settings.statusLine = {
    type: 'command',
    command: 'powershell -ExecutionPolicy Bypass -File "' + managedStatusLinePath + '"'
  };
}

fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
'@

node -e $nodeScript

Write-Host "Done. Restart Claude Code to activate gon." -ForegroundColor Green
