#!/usr/bin/env node
/*
 * emOS framework tool — init / update / check / baseline.
 *
 * Cross-platform (macOS / Linux / Windows) Node CLI, zero runtime dependencies.
 * Published npm package: emos-vault. Command: emos (bootstrap via `npx emos-vault`).
 *
 * Operates on the CURRENT WORKING DIRECTORY (the vault). The ownership boundary
 * lives in `.emos/manifest`: framework-owned paths are overwritten from an
 * upstream source; everything else in your vault is yours and never touched.
 * `.emos/version` records the sha256 of each framework file at last install, so
 * a locally-edited framework file is detected and preserved (written alongside
 * as `<file>.emos-new`) instead of being clobbered.
 *
 * Usage (command is `emos`; first run via `npx emos-vault`):
 *   emos init     [--source <dir|git-url>]   # scaffold a fresh vault in the CWD
 *   emos check    [--source <dir|git-url>]   # dry-run: show what update would do
 *   emos update   [--source <dir|git-url>]   # apply framework updates
 *   emos baseline                            # record current framework hashes (no copy)
 *
 * --source may be omitted when the tool ships bundled with a `template/` dir
 * (the published-package model); otherwise it is required for check/update/init.
 */
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import crypto from "node:crypto";
import { execFileSync } from "node:child_process";

// Directory of THIS script. This file ships at template/.emos/emos.mjs and the
// npm package's `bin` points straight at it — so SCRIPT_DIR/.. is the bundled
// framework root used as the default init/update source. The vault we operate on
// is always the CWD.
const SCRIPT_DIR = path.dirname(new URL(import.meta.url).pathname);
const ROOT = process.env.EMOS_ROOT || process.cwd();
const VERSION_FILE = path.join(ROOT, ".emos", "version");

const die = (m) => { console.error("emos: " + m); process.exit(1); };
const sha = (p) => {
  try { return crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex"); }
  catch { return ""; }
};

// rel path in posix form (manifest patterns always use "/")
const rel = (base, p) => path.relative(base, p).split(path.sep).join("/");

// Recursively list files under dir (posix rel paths), skipping .git.
// Symlinks (e.g. a vault's .claude -> .agents) are neither files nor dirs here,
// so they are skipped — the framework set is the real files only.
function walk(dir, base = dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name === ".git") continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full, base, out);
    else if (e.isFile()) out.push(rel(base, full));
  }
  return out;
}

// ── Manifest ─────────────────────────────────────────────────────────────────
// The manifest that defines the framework set comes from the SOURCE for
// check/update/init (upstream is authoritative), and from the vault itself for
// baseline.
function loadManifest(manifestPath) {
  if (!fs.existsSync(manifestPath)) die("manifest not found: " + manifestPath);
  const includes = [], excludes = [];
  for (let line of fs.readFileSync(manifestPath, "utf8").split("\n")) {
    line = line.replace(/#.*$/, "").trim();
    if (!line) continue;
    if (line.startsWith("-")) excludes.push(line.replace(/^-\s*/, ""));
    else includes.push(line);
  }
  return { includes, excludes };
}
// glob → regex; `*` and `**` both match any chars incl "/"
const toRe = (g) =>
  new RegExp("^" + g.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*+/g, ".*") + "$");
const isFramework = (relPath, mf) => {
  if (mf.excludes.some((p) => toRe(p).test(relPath))) return false;
  return mf.includes.some((p) => toRe(p).test(relPath));
};

// ── Version record ─────────────────────────────────────────────────────────
function readRecorded() {
  const map = new Map();
  if (!fs.existsSync(VERSION_FILE)) return map;
  for (const line of fs.readFileSync(VERSION_FILE, "utf8").split("\n")) {
    if (!line || line.startsWith("#")) continue;
    const m = line.match(/^(\S+)\s+(.+)$/);
    if (m) map.set(m[2], m[1]);
  }
  return map;
}
function writeRecorded(map, sourceLabel) {
  fs.mkdirSync(path.dirname(VERSION_FILE), { recursive: true });
  const lines = ["# emOS framework install record — <sha256>  <path>",
                 "# source: " + sourceLabel];
  for (const k of [...map.keys()].sort()) lines.push(`${map.get(k)}  ${k}`);
  fs.writeFileSync(VERSION_FILE, lines.join("\n") + "\n");
}

// ── Source resolution ────────────────────────────────────────────────────────
let TMP_SRC = null;
function resolveSource(src) {
  if (!src) {
    // Bundled framework root = SCRIPT_DIR/.. (this file ships at .emos/emos.mjs
    // inside the package's template/). The equality guard stops a vault from
    // trying to update from itself when run as ./emos with no --source.
    const bundled = path.join(SCRIPT_DIR, "..");
    if (fs.existsSync(path.join(bundled, ".emos", "manifest")) &&
        path.resolve(bundled) !== path.resolve(ROOT)) return bundled;
    die("missing --source <dir|git-url> — run via `npx emos-vault` for the bundled framework, or pass --source");
  }
  if (/^(https?:\/\/|git@|git:)/.test(src) || src.endsWith(".git")) {
    TMP_SRC = fs.mkdtempSync(path.join(os.tmpdir(), "emos-src-"));
    const [url, refPart] = src.split("#");
    const args = ["clone", "--depth", "1"];
    if (refPart) args.push("--branch", refPart);
    args.push(url, TMP_SRC);
    try { execFileSync("git", args, { stdio: "ignore" }); }
    catch { die("git clone failed: " + src); }
    return TMP_SRC;
  }
  if (!fs.existsSync(src)) die("source not found: " + src);
  return src;
}
const cleanup = () => { if (TMP_SRC) fs.rmSync(TMP_SRC, { recursive: true, force: true }); };

// ── Core sync (used by check/update/init) ────────────────────────────────────
function syncFrom(src, apply, sourceLabel) {
  const mf = loadManifest(path.join(src, ".emos", "manifest"));
  const recorded = readRecorded();
  const next = new Map(recorded);
  let nNew = 0, nUpd = 0, nConf = 0, nCur = 0;

  for (const r of walk(src)) {
    if (!isFramework(r, mf)) continue;
    const from = path.join(src, r.split("/").join(path.sep));
    const to = path.join(ROOT, r.split("/").join(path.sep));
    const sh = sha(from), th = sha(to), rh = recorded.get(r);

    if (!fs.existsSync(to)) {
      console.log("  NEW       " + r); nNew++;
      if (apply) { fs.mkdirSync(path.dirname(to), { recursive: true }); fs.copyFileSync(from, to); }
      next.set(r, sh);
    } else if (th === sh) {
      nCur++; next.set(r, sh);
    } else if (rh && th !== rh) {
      console.log(`  CONFLICT  ${r}  (locally modified — writing ${r}.emos-new)`); nConf++;
      if (apply) { fs.mkdirSync(path.dirname(to), { recursive: true }); fs.copyFileSync(from, to + ".emos-new"); }
      // keep recorded hash; do not advance baseline for a conflicted file
    } else {
      console.log("  UPDATE    " + r); nUpd++;
      if (apply) { fs.mkdirSync(path.dirname(to), { recursive: true }); fs.copyFileSync(from, to); }
      next.set(r, sh);
    }
  }
  if (apply) writeRecorded(next, sourceLabel);
  return { nNew, nUpd, nConf, nCur };
}

// Create the `.claude -> .agents` symlink Claude Code needs, with fallbacks for
// platforms/filesystems that don't support symlinks (e.g. Windows without
// Developer Mode).
function linkClaude() {
  const link = path.join(ROOT, ".claude");
  const agents = path.join(ROOT, ".agents");
  if (fs.existsSync(link)) return;
  if (!fs.existsSync(agents)) return;
  try {
    fs.symlinkSync(".agents", link, "dir");
    console.log("  linked .claude -> .agents");
    return;
  } catch { /* fall through */ }
  try {
    fs.symlinkSync(agents, link, "junction"); // Windows dir junction (absolute target)
    console.log("  linked .claude -> .agents (junction)");
    return;
  } catch { /* fall through */ }
  fs.cpSync(agents, link, { recursive: true });
  console.log("  note: symlinks unavailable — copied .agents -> .claude.");
  console.log("        they will diverge on update; re-copy or enable symlinks. See README.");
}

// ── Subcommands ──────────────────────────────────────────────────────────────
function getSource(argv) {
  const i = argv.indexOf("--source");
  return i >= 0 ? argv[i + 1] : "";
}
const summary = (s, extra = "") =>
  console.log(`  ── new:${s.nNew} update:${s.nUpd} conflict:${s.nConf} current:${s.nCur}${extra}`);

function cmdCheck(argv) {
  const label = getSource(argv); const src = resolveSource(label);
  console.log("emos check — vault: " + ROOT + " — source: " + (label || "bundled template"));
  summary(syncFrom(src, false, label), " (dry-run, nothing written)");
}
function cmdUpdate(argv) {
  const label = getSource(argv); const src = resolveSource(label);
  console.log("emos update — vault: " + ROOT + " — source: " + (label || "bundled template"));
  const s = syncFrom(src, true, label);
  summary(s);
  if (s.nConf) console.log("  review *.emos-new files and merge by hand.");
}
function cmdBaseline() {
  const mf = loadManifest(path.join(ROOT, ".emos", "manifest"));
  const map = new Map();
  for (const r of walk(ROOT)) {
    if (isFramework(r, mf)) map.set(r, sha(path.join(ROOT, r.split("/").join(path.sep))));
  }
  writeRecorded(map, "baseline (current working tree)");
  console.log(`emos baseline — recorded ${map.size} framework files to .emos/version`);
}
function cmdInit(argv) {
  const label = getSource(argv); const src = resolveSource(label);
  console.log("emos init — scaffolding into: " + ROOT);
  const dirs = ["00-inbox","01-weekly","02-people","03-projects","04-decisions","05-incidents",
                "06-hiring","07-strategy","08-meetings","09-knowledge","10-reports"];
  for (const d of dirs) fs.mkdirSync(path.join(ROOT, d), { recursive: true });
  syncFrom(src, true, label);
  linkClaude();
  // Seed the two personalization files from their examples (user fills them / runs /configure).
  const seed = (example, real, note) => {
    const ex = path.join(ROOT, example), rp = path.join(ROOT, real);
    if (!fs.existsSync(rp) && fs.existsSync(ex)) { fs.copyFileSync(ex, rp); console.log("  " + note); }
  };
  seed(".agents/config.example.yaml", ".agents/config.yaml", "seeded .agents/config.yaml from example");
  seed("CONFIG.example.md", "CONFIG.md", "seeded CONFIG.md from example");
  console.log("  done. Next: run /configure (or edit .agents/config.yaml), then start capturing.");
}

const HELP = `emOS framework tool — operates on the current directory
  emos init     [--source <dir|git-url>]   scaffold a fresh vault in the CWD
  emos check    [--source <dir|git-url>]   dry-run: show what update would do
  emos update   [--source <dir|git-url>]   apply framework updates
  emos baseline                            record current framework hashes (no copy)`;

try {
  const [cmd, ...argv] = process.argv.slice(2);
  switch (cmd) {
    case "check": cmdCheck(argv); break;
    case "update": cmdUpdate(argv); break;
    case "baseline": cmdBaseline(argv); break;
    case "init": cmdInit(argv); break;
    case undefined: case "help": case "-h": case "--help": console.log(HELP); break;
    default: die(`unknown command: ${cmd} (try: check | update | baseline | init | help)`);
  }
} finally { cleanup(); }
