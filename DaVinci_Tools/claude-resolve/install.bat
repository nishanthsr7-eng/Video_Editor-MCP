@echo off
REM Claude Resolve installer launcher.
REM Runs install.ps1 AS THE CURRENT USER (no up-front elevation). Node/npm,
REM the Claude CLI, and Playwright Chromium must live in the user's profile;
REM install.ps1 elevates only the final plugin copy into ProgramData.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"
