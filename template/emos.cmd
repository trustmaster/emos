@echo off
REM emOS launcher (Windows) — thin forwarder to the updater in .emos\.
REM Lets you run `emos <cmd>` instead of `node .emos\emos.mjs <cmd>`.
node "%~dp0.emos\emos.mjs" %*
