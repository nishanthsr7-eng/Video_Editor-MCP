// Platform-aware paths for Claude Resolve plugin.
// Centralizes Windows ↔ macOS path differences and executable resolution.

const os = require('os');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const isMac = process.platform === 'darwin';

// Base application-support directory (APPDATA equivalent on macOS)
const APP_SUPPORT = isMac
    ? path.join(os.homedir(), 'Library', 'Application Support')
    : process.env.APPDATA;

const RESOLVE_DATA = path.join(APP_SUPPORT, 'Blackmagic Design', 'DaVinci Resolve');

// Rendered .mov output directory
const RENDER_DIR = path.join(RESOLVE_DATA, 'Claude Resolve', 'renders');

// Thumbnail directory (one PNG per render, written by render.js)
const THUMBNAIL_DIR = path.join(RENDER_DIR, 'thumbnails');

// Plugin config directory
const CONFIG_DIR = path.join(RESOLVE_DATA, 'Claude Resolve');

// Resolve an executable: try a shell lookup first (inherits whatever PATH
// the lookup shell has), then known install locations. Falls back to the
// first candidate. Shared by claude.js and overlay.js.
function findExecutable(candidates, verifyCmd) {
    try {
        const out = execSync(verifyCmd, { encoding: 'utf-8', shell: true, timeout: 5000 }).trim();
        for (const line of out.split(/\r?\n/)) {
            const found = line.trim();
            if (found && fs.existsSync(found)) return found;
        }
    } catch (_e) { /* fall through to candidates */ }
    for (const p of candidates) {
        if (fs.existsSync(p)) return p;
    }
    return candidates[0]; // last resort
}

// ── Claude Code CLI ──────────────────────────────────────────────
// DaVinci Resolve is a launchd GUI app: it never inherits the user's
// terminal PATH, so a bare `claude` lookup fails on macOS. Resolve an
// absolute path from known locations, plus a login+interactive shell
// (`zsh -lic`) which sources the user's rc files and so sees nvm / fnm /
// Homebrew installs the static list can't enumerate.
const CLAUDE_CANDIDATES = [
    '/usr/local/bin/claude',
    '/opt/homebrew/bin/claude',
    path.join(os.homedir(), '.claude', 'local', 'claude'),
    path.join(os.homedir(), '.npm-global', 'bin', 'claude'),
    path.join(os.homedir(), '.bun', 'bin', 'claude'),
    path.join(os.homedir(), '.volta', 'bin', 'claude'),
    path.join(os.homedir(), '.local', 'bin', 'claude'),
    'claude'
];
// nvm / fnm install global bins under version-specific dirs the static list
// can't enumerate — the login+interactive shell probe sources the user's rc
// and so resolves those.
const CLAUDE_VERIFY_CMD = "zsh -lic 'command -v claude' 2>/dev/null";

// Resolve per-OS. macOS uses the login-shell probe + candidates (launchd strips
// PATH). Windows GUI apps inherit a usable PATH, but a custom npm prefix / fnm /
// Volta can move the CLI off the default %APPDATA%\npm path, so try `where
// claude` plus a candidate list there too.
const WIN_CLAUDE_CANDIDATES = [
    path.join(process.env.APPDATA || '', 'npm', 'claude.cmd'),
    path.join(process.env.LOCALAPPDATA || '', 'npm', 'claude.cmd'),
    path.join(os.homedir(), '.volta', 'bin', 'claude.exe'),
    path.join(os.homedir(), '.claude', 'local', 'claude.exe'),
    'claude.cmd'
];
const CLAUDE_PATH = isMac
    ? findExecutable(CLAUDE_CANDIDATES, CLAUDE_VERIFY_CMD)
    : findExecutable(WIN_CLAUDE_CANDIDATES, 'where claude 2>nul');

// Augmented environment for spawning the CLI. On macOS the launchd PATH is
// stripped down to /usr/bin:/bin:/usr/sbin:/sbin — prepend the resolved
// CLI's own bin dir plus the common Homebrew/Node locations so `claude`
// (a `#!/usr/bin/env node` script) and anything it shells out to resolve.
function buildEnv() {
    if (!isMac) return process.env;
    const claudeDir = path.dirname(CLAUDE_PATH);
    const prepend = [
        (claudeDir && claudeDir !== '.') ? claudeDir : null,
        '/usr/local/bin',
        '/opt/homebrew/bin'
    ].filter(Boolean);
    const merged = [];
    for (const dir of [...prepend, ...(process.env.PATH || '').split(':')]) {
        if (dir && !merged.includes(dir)) merged.push(dir);
    }
    return { ...process.env, PATH: merged.join(':') };
}
const ENV = buildEnv();

// FFmpeg executable candidates
const FFMPEG_CANDIDATES = isMac
    ? [
        '/opt/homebrew/bin/ffmpeg',
        '/usr/local/bin/ffmpeg',
        'ffmpeg'
    ]
    : [
        path.join(process.env.PROGRAMFILES || '', 'FFmpeg', 'ffmpeg.exe'),
        path.join(process.env.PROGRAMFILES || '', 'FFmpeg', 'bin', 'ffmpeg.exe'),
        // ProgramW6432 = native Program Files even from a 32-bit process.
        path.join(process.env.ProgramW6432 || '', 'FFmpeg', 'bin', 'ffmpeg.exe'),
        // winget shim + scoop shim (choco/PATH installs are caught by `where`).
        path.join(process.env.LOCALAPPDATA || '', 'Microsoft', 'WinGet', 'Links', 'ffmpeg.exe'),
        path.join(os.homedir(), 'scoop', 'shims', 'ffmpeg.exe'),
        'ffmpeg'
    ];

// macOS: a login+interactive shell sees Homebrew/nvm PATHs that launchd's
// stripped PATH (and a plain `which`) would miss — match the claude probe.
const FFMPEG_VERIFY_CMD = isMac
    ? "zsh -lic 'command -v ffmpeg' 2>/dev/null"
    : 'where ffmpeg';

// Playwright browser cache. Pin it so install-time and run-time resolve the
// SAME per-user location (these values match Playwright's per-OS default).
const PLAYWRIGHT_BROWSERS_PATH = isMac
    ? path.join(os.homedir(), 'Library', 'Caches', 'ms-playwright')
    : path.join(process.env.LOCALAPPDATA || path.join(os.homedir(), 'AppData', 'Local'), 'ms-playwright');

module.exports = {
    isMac,
    findExecutable,
    CLAUDE_PATH,
    ENV,
    RENDER_DIR,
    THUMBNAIL_DIR,
    CONFIG_DIR,
    FFMPEG_CANDIDATES,
    FFMPEG_VERIFY_CMD,
    PLAYWRIGHT_BROWSERS_PATH
};
