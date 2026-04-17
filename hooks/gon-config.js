#!/usr/bin/env node
// gon — shared configuration resolver
//
// Resolution order for default mode:
//   1. GON_DEFAULT_MODE environment variable
//   2. Config file defaultMode field:
//      - $XDG_CONFIG_HOME/gon/config.json
//      - ~/.config/gon/config.json
//      - %APPDATA%\gon\config.json
//   3. 'full'

const fs = require('fs');
const path = require('path');
const os = require('os');

const VALID_MODES = ['off', 'lite', 'full', 'ultra', 'commit', 'review', 'compress'];

function getConfigDir() {
  if (process.env.XDG_CONFIG_HOME) {
    return path.join(process.env.XDG_CONFIG_HOME, 'gon');
  }
  if (process.platform === 'win32') {
    return path.join(
      process.env.APPDATA || path.join(os.homedir(), 'AppData', 'Roaming'),
      'gon'
    );
  }
  return path.join(os.homedir(), '.config', 'gon');
}

function getConfigPath() {
  return path.join(getConfigDir(), 'config.json');
}

function getDefaultMode() {
  const envMode = process.env.GON_DEFAULT_MODE;
  if (envMode && VALID_MODES.includes(envMode.toLowerCase())) {
    return envMode.toLowerCase();
  }

  try {
    const config = JSON.parse(fs.readFileSync(getConfigPath(), 'utf8'));
    if (config.defaultMode && VALID_MODES.includes(config.defaultMode.toLowerCase())) {
      return config.defaultMode.toLowerCase();
    }
  } catch (e) {
    // Best effort
  }

  return 'full';
}

function safeWriteFlag(flagPath, content) {
  try {
    const flagDir = path.dirname(flagPath);
    fs.mkdirSync(flagDir, { recursive: true });

    try {
      if (fs.lstatSync(flagDir).isSymbolicLink()) return;
    } catch (e) {
      return;
    }

    try {
      if (fs.lstatSync(flagPath).isSymbolicLink()) return;
    } catch (e) {
      if (e.code !== 'ENOENT') return;
    }

    const tempPath = path.join(flagDir, `.gon-active.${process.pid}.${Date.now()}`);
    const O_NOFOLLOW = typeof fs.constants.O_NOFOLLOW === 'number' ? fs.constants.O_NOFOLLOW : 0;
    const flags = fs.constants.O_WRONLY | fs.constants.O_CREAT | fs.constants.O_EXCL | O_NOFOLLOW;
    let fd;
    try {
      fd = fs.openSync(tempPath, flags, 0o600);
      fs.writeSync(fd, String(content));
      try { fs.fchmodSync(fd, 0o600); } catch (e) {}
    } finally {
      if (fd !== undefined) fs.closeSync(fd);
    }
    fs.renameSync(tempPath, flagPath);
  } catch (e) {
    // Silent fail
  }
}

const MAX_FLAG_BYTES = 64;

function readFlag(flagPath) {
  try {
    let st;
    try {
      st = fs.lstatSync(flagPath);
    } catch (e) {
      return null;
    }
    if (st.isSymbolicLink() || !st.isFile()) return null;
    if (st.size > MAX_FLAG_BYTES) return null;

    const O_NOFOLLOW = typeof fs.constants.O_NOFOLLOW === 'number' ? fs.constants.O_NOFOLLOW : 0;
    const flags = fs.constants.O_RDONLY | O_NOFOLLOW;
    let fd;
    let out;
    try {
      fd = fs.openSync(flagPath, flags);
      const buf = Buffer.alloc(MAX_FLAG_BYTES);
      const n = fs.readSync(fd, buf, 0, MAX_FLAG_BYTES, 0);
      out = buf.slice(0, n).toString('utf8');
    } finally {
      if (fd !== undefined) fs.closeSync(fd);
    }

    const raw = out.trim().toLowerCase();
    if (!VALID_MODES.includes(raw)) return null;
    return raw;
  } catch (e) {
    return null;
  }
}

module.exports = { getDefaultMode, getConfigDir, getConfigPath, VALID_MODES, safeWriteFlag, readFlag };
