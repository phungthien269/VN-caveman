#!/usr/bin/env node
// gon — Claude Code SessionStart activation hook

const fs = require('fs');
const path = require('path');
const os = require('os');
const { getDefaultMode, safeWriteFlag } = require('./gon-config');

const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
const flagPath = path.join(claudeDir, '.gon-active');
const settingsPath = path.join(claudeDir, 'settings.json');
const mode = getDefaultMode();

if (mode === 'off') {
  try { fs.unlinkSync(flagPath); } catch (e) {}
  process.stdout.write('OK');
  process.exit(0);
}

safeWriteFlag(flagPath, mode);

const INDEPENDENT_MODES = new Set(['commit', 'review', 'compress']);
if (INDEPENDENT_MODES.has(mode)) {
  process.stdout.write('GON MODE ACTIVE — level: ' + mode + '. Behavior defined by /gon-' + mode + ' skill.');
  process.exit(0);
}

let skillContent = '';
try {
  skillContent = fs.readFileSync(path.join(__dirname, '..', 'skills', 'gon', 'SKILL.md'), 'utf8');
} catch (e) {
  // Standalone install without skill tree
}

let output;
if (skillContent) {
  const body = skillContent.replace(/^---[\s\S]*?---\s*/, '');
  const filtered = body.split('\n').reduce((acc, line) => {
    const tableRowMatch = line.match(/^\|\s*\*\*(\S+?)\*\*\s*\|/);
    if (tableRowMatch) {
      if (tableRowMatch[1] === mode) acc.push(line);
      return acc;
    }
    const exampleMatch = line.match(/^- (\S+?):\s/);
    if (exampleMatch) {
      if (exampleMatch[1] === mode) acc.push(line);
      return acc;
    }
    acc.push(line);
    return acc;
  }, []);
  output = 'GON MODE ACTIVE — level: ' + mode + '\n\n' + filtered.join('\n');
} else {
  output =
    'GON MODE ACTIVE — level: ' + mode + '\n\n' +
    'Trả lời tiếng Việt gọn, trực diện. Giữ ý kỹ thuật. Chỉ cắt phần thừa.\n\n' +
    '## Persistence\n\n' +
    'ACTIVE EVERY RESPONSE. Không drift về verbose. Off only: "stop gon" / "normal mode" / "trả lời bình thường".\n\n' +
    'Current level: **' + mode + '**. Switch: `/gon lite|full|ultra`.\n\n' +
    '## Rules\n\n' +
    'Cắt xã giao, hedge, đệm lời, câu mở đầu không thêm ý. Rút cụm dài về động từ ngắn. Giữ nguyên code block, inline code, command, URL, path, env var, version, proper noun, error.\n\n' +
    'Pattern: `[vấn đề]. [do đâu]. [cách xử].`\n\n' +
    '## Auto-Clarity\n\n' +
    'Bỏ nén mạnh cho: security warning, destructive op, production/database/infra, migration nhiều bước, user cần step-by-step chính xác. Resume after clear part done.\n\n' +
    '## Boundaries\n\n' +
    'Code/commits/PRs: write normal. "stop gon" or "normal mode": revert. Level persist until changed or session end.';
}

try {
  let hasStatusline = false;
  if (fs.existsSync(settingsPath)) {
    const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
    if (settings.statusLine) hasStatusline = true;
  }

  if (!hasStatusline) {
    const isWindows = process.platform === 'win32';
    const scriptName = isWindows ? 'gon-statusline.ps1' : 'gon-statusline.sh';
    const scriptPath = path.join(__dirname, scriptName);
    const command = isWindows
      ? `powershell -ExecutionPolicy Bypass -File "${scriptPath}"`
      : `bash "${scriptPath}"`;
    const statusLineSnippet =
      '"statusLine": { "type": "command", "command": ' + JSON.stringify(command) + ' }';
    output += '\n\n' +
      'STATUSLINE SETUP NEEDED: The gon plugin includes a statusline badge showing active mode ' +
      '(e.g. [GON], [GON:ULTRA]). It is not configured yet. ' +
      'To enable, add this to ' + path.join(claudeDir, 'settings.json') + ': ' +
      statusLineSnippet + ' ' +
      'Proactively offer to set this up for the user on first interaction.';
  }
} catch (e) {
  // Silent fail
}

process.stdout.write(output);
