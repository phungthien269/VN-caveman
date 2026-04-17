#!/usr/bin/env node
// gon — UserPromptSubmit hook to track which gon mode is active

const fs = require('fs');
const path = require('path');
const os = require('os');
const { getDefaultMode, safeWriteFlag, readFlag } = require('./gon-config');

const claudeDir = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
const flagPath = path.join(claudeDir, '.gon-active');

let input = '';
process.stdin.on('data', chunk => { input += chunk; });
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);
    const prompt = (data.prompt || '').trim().toLowerCase();

    if (
      /\b(activate|enable|turn on|start)\b.*\bgon\b/i.test(prompt) ||
      /\bgon\b.*\b(mode|activate|enable|turn on|start)\b/i.test(prompt) ||
      /trả lời gọn|tra loi gon|nói ngắn|noi ngan|ít token|it token/.test(prompt)
    ) {
      if (!/\b(stop|disable|turn off|deactivate)\b/i.test(prompt)) {
        const mode = getDefaultMode();
        if (mode !== 'off') safeWriteFlag(flagPath, mode);
      }
    }

    if (prompt.startsWith('/gon')) {
      const parts = prompt.split(/\s+/);
      const cmd = parts[0];
      const arg = parts[1] || '';
      let mode = null;

      if (cmd === '/gon-commit') mode = 'commit';
      else if (cmd === '/gon-review') mode = 'review';
      else if (cmd === '/gon-compress' || cmd === '/gon:gon-compress') mode = 'compress';
      else if (cmd === '/gon' || cmd === '/gon:gon') {
        if (arg === 'lite') mode = 'lite';
        else if (arg === 'full') mode = 'full';
        else if (arg === 'ultra') mode = 'ultra';
        else mode = getDefaultMode();
      }

      if (mode && mode !== 'off') safeWriteFlag(flagPath, mode);
      else if (mode === 'off') {
        try { fs.unlinkSync(flagPath); } catch (e) {}
      }
    }

    if (
      /\b(stop|disable|deactivate|turn off)\b.*\bgon\b/i.test(prompt) ||
      /\bgon\b.*\b(stop|disable|deactivate|turn off)\b/i.test(prompt) ||
      /\bnormal mode\b/i.test(prompt) ||
      /trả lời bình thường|tra loi binh thuong/.test(prompt)
    ) {
      try { fs.unlinkSync(flagPath); } catch (e) {}
    }

    const INDEPENDENT_MODES = new Set(['commit', 'review', 'compress']);
    const activeMode = readFlag(flagPath);
    if (activeMode && !INDEPENDENT_MODES.has(activeMode)) {
      process.stdout.write(JSON.stringify({
        hookSpecificOutput: {
          hookEventName: 'UserPromptSubmit',
          additionalContext:
            'GON MODE ACTIVE (' + activeMode + '). ' +
            'Tra loi tieng Viet gon, truc dien, bo xa giao va hedge. ' +
            'Code/commits/security: write normal.'
        }
      }));
    }
  } catch (e) {
    // Silent fail
  }
});
