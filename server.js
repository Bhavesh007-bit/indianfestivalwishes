/* Indian Festival Wishes — web server (Railway)
 *
 * Serves the built static site from ./public, the admin panel from ./admin,
 * and a small authenticated JSON API that edits the live site settings kept
 * on the persistent volume (DATA_DIR).
 */
"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const express = require("express");

/* ------------------------------------------------------------------ config */

const ROOT = __dirname;
const PUBLIC_DIR = path.join(ROOT, "public");
const ADMIN_DIR = path.join(ROOT, "admin");
const SEED_SETTINGS = path.join(ROOT, "static", "site-settings.json");

const PORT = parseInt(process.env.PORT, 10) || 3000;
const IS_PROD = process.env.NODE_ENV === "production";
const ADMIN_USER = process.env.ADMIN_USER || "";
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || "";

const CANON_APEX = "indianfestivalwishes.com";
const CANON_HOST = "www.indianfestivalwishes.com";

const SESSION_COOKIE = "ifw_s";
const SESSION_TTL_MS = 12 * 60 * 60 * 1000;
const LOGIN_WINDOW_MS = 15 * 60 * 1000;
const LOGIN_MAX_FAILS = 5;
const MAX_BACKUPS = 50;
const MAX_UPLOAD = 2 * 1024 * 1024;

let SESSION_SECRET = process.env.SESSION_SECRET || "";
if (!SESSION_SECRET) {
  if (IS_PROD) {
    console.error("[fatal] SESSION_SECRET is required when NODE_ENV=production");
    process.exit(1);
  }
  SESSION_SECRET = crypto.randomBytes(32).toString("hex");
  console.warn("[warn] SESSION_SECRET not set; using a random one (sessions reset on restart)");
}
if (!ADMIN_USER || !ADMIN_PASSWORD) {
  console.warn("[warn] ADMIN_USER / ADMIN_PASSWORD not set; admin login is disabled until they are");
}

function writableDir(dir) {
  try {
    if (!fs.statSync(dir).isDirectory()) return false;
    fs.accessSync(dir, fs.constants.W_OK);
    return true;
  } catch (e) {
    return false;
  }
}
const DATA_DIR = path.resolve(
  process.env.DATA_DIR || (writableDir("/data") ? "/data" : path.join(ROOT, "data"))
);
const SETTINGS_FILE = path.join(DATA_DIR, "site-settings.json");
const AUTH_FILE = path.join(DATA_DIR, "admin-auth.json");
const BACKUP_DIR = path.join(DATA_DIR, "backups");
const UPLOAD_DIR = path.join(DATA_DIR, "uploads");

for (const d of [DATA_DIR, BACKUP_DIR, UPLOAD_DIR]) fs.mkdirSync(d, { recursive: true });

if (!fs.existsSync(SETTINGS_FILE)) {
  if (fs.existsSync(SEED_SETTINGS)) {
    fs.copyFileSync(SEED_SETTINGS, SETTINGS_FILE);
    console.log("[boot] seeded " + SETTINGS_FILE + " from static/site-settings.json");
  } else {
    console.warn("[warn] no settings file and no seed found");
  }
}

/* ----------------------------------------------------------------- helpers */

function atomicWrite(file, data) {
  const tmp = file + ".tmp-" + process.pid + "-" + crypto.randomBytes(4).toString("hex");
  const fd = fs.openSync(tmp, "w", 0o600);
  try {
    fs.writeSync(fd, data);
    fs.fsyncSync(fd);
  } finally {
    fs.closeSync(fd);
  }
  fs.renameSync(tmp, file);
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function b64u(buf) {
  return Buffer.from(buf).toString("base64url");
}

function sha256(s) {
  return crypto.createHash("sha256").update(String(s), "utf8").digest();
}

// Constant-time compare for strings of any length.
function safeEqual(a, b) {
  return crypto.timingSafeEqual(sha256(a), sha256(b));
}

function clientIp(req) {
  return req.ip || (req.socket && req.socket.remoteAddress) || "unknown";
}

function hostOf(req) {
  return String(req.headers.host || "").toLowerCase().replace(/:\d+$/, "");
}

function isLocalHost(h) {
  return h === "localhost" || h === "127.0.0.1" || h === "[::1]" || h === "0.0.0.0";
}

function isRailwayHost(h) {
  return h === "railway.app" || h.endsWith(".railway.app");
}

/* ----------------------------------------------------- password / sessions */

let authCache; // undefined = not loaded, null = no file
function loadAuth() {
  if (authCache !== undefined) return authCache;
  try {
    const a = readJson(AUTH_FILE);
    authCache = a && a.hash && a.salt ? a : null;
  } catch (e) {
    authCache = null;
  }
  return authCache;
}

function scryptHash(password, salt) {
  return crypto.scryptSync(String(password), salt, 64, { N: 16384, r: 8, p: 1 });
}

function checkPassword(pw) {
  const a = loadAuth();
  if (a) {
    const got = scryptHash(pw, Buffer.from(a.salt, "base64"));
    const want = Buffer.from(a.hash, "base64");
    return got.length === want.length && crypto.timingSafeEqual(got, want);
  }
  if (!ADMIN_PASSWORD) return false;
  return safeEqual(pw, ADMIN_PASSWORD);
}

// Password "generation" — changes when the password changes, so older
// sessions stop working after a password change.
function passwordGen() {
  const a = loadAuth();
  const src = a ? a.hash : "env:" + ADMIN_PASSWORD;
  return crypto.createHmac("sha256", SESSION_SECRET).update(src).digest("base64url").slice(0, 12);
}

function sign(payload) {
  return crypto.createHmac("sha256", SESSION_SECRET).update(payload).digest("base64url");
}

function makeToken(user) {
  const payload = b64u(JSON.stringify({ u: user, exp: Date.now() + SESSION_TTL_MS, g: passwordGen() }));
  return payload + "." + sign(payload);
}

function readToken(tok) {
  if (typeof tok !== "string" || tok.length > 1024) return null;
  const i = tok.indexOf(".");
  if (i < 1) return null;
  const payload = tok.slice(0, i);
  const sig = tok.slice(i + 1);
  const want = sign(payload);
  if (sig.length !== want.length || !crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(want))) return null;
  let data;
  try {
    data = JSON.parse(Buffer.from(payload, "base64url").toString("utf8"));
  } catch (e) {
    return null;
  }
  if (!data || typeof data.u !== "string" || typeof data.exp !== "number") return null;
  if (data.exp < Date.now()) return null;
  if (data.g !== passwordGen()) return null;
  if (!ADMIN_USER || data.u !== ADMIN_USER) return null;
  return data;
}

function parseCookies(req) {
  const out = {};
  const h = req.headers.cookie;
  if (!h) return out;
  for (const part of h.split(";")) {
    const i = part.indexOf("=");
    if (i < 0) continue;
    const k = part.slice(0, i).trim();
    if (!k || out[k] !== undefined) continue;
    try {
      out[k] = decodeURIComponent(part.slice(i + 1).trim());
    } catch (e) {
      out[k] = part.slice(i + 1).trim();
    }
  }
  return out;
}

function setSessionCookie(req, res, value, maxAgeSec) {
  const bits = [
    SESSION_COOKIE + "=" + value,
    "Path=/",
    "HttpOnly",
    "SameSite=Strict",
    "Max-Age=" + maxAgeSec,
  ];
  if (req.secure) bits.push("Secure");
  res.append("Set-Cookie", bits.join("; "));
}

/* ------------------------------------------------------ login rate limiter */

const loginFails = new Map(); // ip -> [timestamps]

function recentFails(ip) {
  const now = Date.now();
  const list = (loginFails.get(ip) || []).filter((t) => now - t < LOGIN_WINDOW_MS);
  if (list.length) loginFails.set(ip, list);
  else loginFails.delete(ip);
  return list;
}

setInterval(() => {
  for (const ip of loginFails.keys()) recentFails(ip);
}, 5 * 60 * 1000).unref();

/* ---------------------------------------------------------- settings store */

const REQUIRED_KEYS = ["affiliate", "telegram", "announcement", "ads", "custom"];

function isPlainObject(v) {
  return v !== null && typeof v === "object" && !Array.isArray(v);
}

function validateSettings(s) {
  if (!isPlainObject(s)) return "Settings must be a JSON object";
  for (const k of REQUIRED_KEYS) {
    if (!isPlainObject(s[k])) return "Missing or invalid section: " + k;
  }
  if (!Array.isArray(s.affiliate.products)) return "affiliate.products must be a list";
  if (s.affiliate.products.some((p) => !isPlainObject(p))) return "Every product must be an object";
  return "";
}

function backupStamp() {
  return new Date().toISOString().replace(/:/g, "-").replace(".", "-");
}

const BACKUP_RE = /^settings-\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}-\d{3}Z(?:-\d{1,3})?\.json$/;

function listBackupNames() {
  return fs
    .readdirSync(BACKUP_DIR)
    .filter((n) => BACKUP_RE.test(n))
    .sort()
    .reverse();
}

function backupCurrent() {
  if (!fs.existsSync(SETTINGS_FILE)) return;
  let name = "settings-" + backupStamp() + ".json";
  for (let i = 1; fs.existsSync(path.join(BACKUP_DIR, name)) && i < 1000; i++) {
    name = "settings-" + backupStamp() + "-" + i + ".json";
  }
  fs.copyFileSync(SETTINGS_FILE, path.join(BACKUP_DIR, name));
  for (const old of listBackupNames().slice(MAX_BACKUPS)) {
    try {
      fs.unlinkSync(path.join(BACKUP_DIR, old));
    } catch (e) {
      /* ignore */
    }
  }
}

function saveSettings(obj) {
  obj.version = Date.now();
  backupCurrent();
  atomicWrite(SETTINGS_FILE, JSON.stringify(obj, null, 2) + "\n");
  return obj;
}

/* --------------------------------------------------------------------- app */

const app = express();
app.disable("x-powered-by");
app.set("trust proxy", 1); // Railway's edge proxy
app.set("etag", true);

// Health check first: no redirects, no auth.
app.get("/healthz", (req, res) => {
  res.set("Cache-Control", "no-store").type("text/plain").send("ok");
});

// Security headers on everything.
app.use((req, res, next) => {
  res.set({
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "X-Frame-Options": "SAMEORIGIN",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
  });
  if (req.secure) res.set("Strict-Transport-Security", "max-age=31536000");
  next();
});

// Canonical host + https.
app.use((req, res, next) => {
  const h = hostOf(req);
  if (h === CANON_APEX) {
    return res.redirect(301, "https://" + CANON_HOST + req.originalUrl);
  }
  const proto = String(req.headers["x-forwarded-proto"] || "").split(",")[0].trim().toLowerCase();
  if (proto === "http" && h && !isLocalHost(h) && !isRailwayHost(h)) {
    return res.redirect(301, "https://" + h + req.originalUrl);
  }
  next();
});

// Private areas: never indexed, never cached.
app.use(["/admin", "/api"], (req, res, next) => {
  res.set({ "X-Robots-Tag": "noindex, nofollow", "Cache-Control": "no-store" });
  next();
});

/* ------------------------------------------------------------------- API */

const api = express.Router();

// CSRF guard for anything that changes state.
api.use((req, res, next) => {
  if (req.method === "GET" || req.method === "HEAD" || req.method === "OPTIONS") return next();
  if (req.get("X-IFW") !== "1") return res.status(403).json({ error: "Missing request header" });
  const origin = req.get("Origin");
  if (origin) {
    let ok = false;
    try {
      ok = new URL(origin).host.toLowerCase() === String(req.headers.host || "").toLowerCase();
    } catch (e) {
      ok = false;
    }
    if (!ok) return res.status(403).json({ error: "Cross-origin request blocked" });
  }
  next();
});

function currentUser(req) {
  const t = parseCookies(req)[SESSION_COOKIE];
  return t ? readToken(t) : null;
}

function requireAuth(req, res, next) {
  const s = currentUser(req);
  if (!s) return res.status(401).json({ error: "Login required" });
  req.session = s;
  next();
}

const jsonSmall = express.json({ limit: "10kb", strict: true });
const jsonSettings = express.json({ limit: "1mb", strict: true });

api.post("/login", jsonSmall, (req, res) => {
  const ip = clientIp(req);
  const fails = recentFails(ip);
  if (fails.length >= LOGIN_MAX_FAILS) {
    const retry = Math.max(1, Math.ceil((fails[0] + LOGIN_WINDOW_MS - Date.now()) / 1000));
    res.set("Retry-After", String(retry));
    return res.status(429).json({ error: "Too many failed attempts", retryAfter: retry });
  }
  if (!ADMIN_USER || (!ADMIN_PASSWORD && !loadAuth())) {
    return res.status(503).json({ error: "Admin login is not configured on the server" });
  }
  const body = isPlainObject(req.body) ? req.body : {};
  const user = typeof body.username === "string" ? body.username.trim() : "";
  const pass = typeof body.password === "string" ? body.password : "";
  const userOk = safeEqual(user, ADMIN_USER);
  const passOk = pass.length > 0 && pass.length <= 256 && checkPassword(pass);
  if (!(userOk && passOk)) {
    fails.push(Date.now());
    loginFails.set(ip, fails);
    const left = LOGIN_MAX_FAILS - fails.length;
    if (left <= 0) {
      const retry = Math.ceil(LOGIN_WINDOW_MS / 1000);
      res.set("Retry-After", String(retry));
      return res.status(429).json({ error: "Too many failed attempts", retryAfter: retry });
    }
    return res.status(401).json({ error: "Wrong username or password", attemptsLeft: left });
  }
  loginFails.delete(ip);
  setSessionCookie(req, res, makeToken(ADMIN_USER), Math.floor(SESSION_TTL_MS / 1000));
  res.json({ user: ADMIN_USER, exp: Date.now() + SESSION_TTL_MS });
});

api.post("/logout", (req, res) => {
  setSessionCookie(req, res, "", 0);
  res.json({ ok: true });
});

api.get("/me", (req, res) => {
  const s = currentUser(req);
  if (!s) return res.status(401).json({ error: "Login required" });
  res.json({ user: s.u, exp: s.exp, customPassword: !!loadAuth() });
});

api.get("/settings", requireAuth, (req, res, next) => {
  try {
    res.type("application/json").send(fs.readFileSync(SETTINGS_FILE, "utf8"));
  } catch (e) {
    next(e);
  }
});

api.put("/settings", requireAuth, jsonSettings, (req, res, next) => {
  const s = req.body;
  const err = validateSettings(s);
  if (err) return res.status(400).json({ error: err });
  // Optional optimistic concurrency: client says which version it edited.
  const base = req.get("X-IFW-Base-Version");
  if (base) {
    try {
      const cur = readJson(SETTINGS_FILE);
      if (String(cur.version) !== base) {
        return res.status(409).json({ error: "Settings were changed elsewhere", version: cur.version });
      }
    } catch (e) {
      /* no current file: nothing to conflict with */
    }
  }
  try {
    const saved = saveSettings(s);
    res.json({ ok: true, version: saved.version });
  } catch (e) {
    next(e);
  }
});

api.get("/backups", requireAuth, (req, res, next) => {
  try {
    const list = listBackupNames().map((name) => {
      const st = fs.statSync(path.join(BACKUP_DIR, name));
      return { name, size: st.size, date: st.mtime.toISOString() };
    });
    res.json({ backups: list });
  } catch (e) {
    next(e);
  }
});

function backupPath(req, res) {
  const name = String(req.params.name || "");
  if (!BACKUP_RE.test(name)) {
    res.status(400).json({ error: "Invalid backup name" });
    return null;
  }
  const p = path.join(BACKUP_DIR, name);
  if (!fs.existsSync(p)) {
    res.status(404).json({ error: "Backup not found" });
    return null;
  }
  return { name, p };
}

api.get("/backups/:name", requireAuth, (req, res) => {
  const b = backupPath(req, res);
  if (!b) return;
  res.set("Content-Disposition", 'attachment; filename="' + b.name + '"');
  res.type("application/json").send(fs.readFileSync(b.p));
});

api.post("/backups/:name/restore", requireAuth, (req, res, next) => {
  const b = backupPath(req, res);
  if (!b) return;
  let data;
  try {
    data = readJson(b.p);
  } catch (e) {
    return res.status(422).json({ error: "Backup file is not valid JSON" });
  }
  const err = validateSettings(data);
  if (err) return res.status(422).json({ error: err });
  try {
    const saved = saveSettings(data);
    res.json({ ok: true, version: saved.version });
  } catch (e) {
    next(e);
  }
});

const IMAGE_TYPES = {
  "image/jpeg": { ext: "jpg", magic: (b) => b.length > 3 && b[0] === 0xff && b[1] === 0xd8 && b[2] === 0xff },
  "image/png": {
    ext: "png",
    magic: (b) => b.length > 8 && b.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])),
  },
  "image/webp": {
    ext: "webp",
    magic: (b) => b.length > 12 && b.toString("latin1", 0, 4) === "RIFF" && b.toString("latin1", 8, 12) === "WEBP",
  },
};

api.post(
  "/upload",
  requireAuth,
  express.raw({ type: Object.keys(IMAGE_TYPES), limit: MAX_UPLOAD }),
  (req, res, next) => {
    const type = String(req.get("Content-Type") || "").split(";")[0].trim().toLowerCase();
    const kind = IMAGE_TYPES[type];
    if (!kind) return res.status(415).json({ error: "Only JPEG, PNG or WebP images are allowed" });
    const buf = req.body;
    if (!Buffer.isBuffer(buf) || !buf.length) return res.status(400).json({ error: "Empty upload" });
    if (!kind.magic(buf)) return res.status(415).json({ error: "File content does not match its type" });
    const name = crypto.randomBytes(12).toString("hex") + "." + kind.ext;
    try {
      atomicWrite(path.join(UPLOAD_DIR, name), buf);
      res.status(201).json({ url: "/uploads/" + name });
    } catch (e) {
      next(e);
    }
  }
);

api.post("/password", requireAuth, jsonSmall, (req, res, next) => {
  const body = isPlainObject(req.body) ? req.body : {};
  const cur = typeof body.current === "string" ? body.current : "";
  const nxt = typeof body.next === "string" ? body.next : "";
  if (!checkPassword(cur)) return res.status(403).json({ error: "Current password is wrong" });
  if (nxt.length < 10) return res.status(400).json({ error: "New password must be at least 10 characters" });
  if (nxt.length > 256) return res.status(400).json({ error: "New password is too long" });
  try {
    const salt = crypto.randomBytes(16);
    const rec = {
      alg: "scrypt",
      N: 16384,
      salt: salt.toString("base64"),
      hash: scryptHash(nxt, salt).toString("base64"),
      updated: new Date().toISOString(),
    };
    atomicWrite(AUTH_FILE, JSON.stringify(rec, null, 2) + "\n");
    authCache = rec;
    // Old sessions are now invalid; hand this browser a fresh one.
    setSessionCookie(req, res, makeToken(ADMIN_USER), Math.floor(SESSION_TTL_MS / 1000));
    res.json({ ok: true });
  } catch (e) {
    next(e);
  }
});

api.use((req, res) => res.status(404).json({ error: "Not found" }));

app.use("/api", api);

/* ----------------------------------------------------------------- admin */

app.use("/admin", (req, res, next) => {
  res.set(
    "Content-Security-Policy",
    "default-src 'self'; script-src 'self'; style-src 'self' https://fonts.googleapis.com; " +
      "font-src 'self' https://fonts.gstatic.com; img-src 'self' https: data: blob:; connect-src 'self'; " +
      "frame-ancestors 'none'; base-uri 'none'; form-action 'self'; object-src 'none'"
  );
  next();
});
app.use("/admin", express.static(ADMIN_DIR, { index: "index.html", cacheControl: false, etag: true, lastModified: true }));

/* ---------------------------------------------------- live settings file */

app.get("/static/site-settings.json", (req, res, next) => {
  if (!fs.existsSync(SETTINGS_FILE)) return next();
  res.set("Cache-Control", "no-cache");
  res.sendFile(SETTINGS_FILE, { headers: { "Content-Type": "application/json; charset=utf-8" } }, (err) => {
    if (err && !res.headersSent) next(err);
  });
});

/* ------------------------------------------------------------ uploads */

app.use(
  "/uploads",
  express.static(UPLOAD_DIR, {
    index: false,
    dotfiles: "deny",
    setHeaders(res) {
      res.set("Cache-Control", "public, max-age=2592000, immutable");
      res.set("Content-Security-Policy", "default-src 'none'; sandbox");
    },
  })
);

/* -------------------------------------------------------- static site */

app.use(
  express.static(PUBLIC_DIR, {
    extensions: ["html"],
    index: "index.html",
    dotfiles: "ignore",
    setHeaders(res, filePath) {
      const rel = "/" + path.relative(PUBLIC_DIR, filePath).split(path.sep).join("/");
      if (rel.endsWith(".html") || rel.endsWith("/site-settings.json")) {
        res.set("Cache-Control", "no-cache");
      } else if (rel.startsWith("/cards/")) {
        res.set("Cache-Control", "public, max-age=2592000");
      } else if (rel.startsWith("/static/")) {
        res.set("Cache-Control", "public, max-age=604800");
      } else {
        res.set("Cache-Control", "public, max-age=3600");
      }
    },
  })
);

/* --------------------------------------------------------- 404 / errors */

const NOT_FOUND_PAGE = path.join(PUBLIC_DIR, "404.html");
app.use((req, res) => {
  res.status(404).set("Cache-Control", "no-cache");
  if ((req.method === "GET" || req.method === "HEAD") && fs.existsSync(NOT_FOUND_PAGE)) {
    return res.sendFile(NOT_FOUND_PAGE, (err) => {
      if (err && !res.headersSent) res.type("text/plain").send("Not found");
    });
  }
  res.type("text/plain").send("Not found");
});

// eslint-disable-next-line no-unused-vars
app.use((err, req, res, next) => {
  let status = err && (err.status || err.statusCode);
  let msg = "Something went wrong";
  if (err && err.type === "entity.too.large") {
    status = 413;
    msg = "Request is too large";
  } else if (err && err.type === "entity.parse.failed") {
    status = 400;
    msg = "Invalid JSON";
  } else if (!status || status < 400 || status > 599) {
    status = 500;
  } else if (status < 500) {
    msg = "Bad request";
  }
  if (status >= 500) console.error("[error]", req.method, req.originalUrl, err && err.stack ? err.stack : err);
  if (res.headersSent) return;
  if (req.originalUrl.startsWith("/api/")) return res.status(status).json({ error: msg });
  res.status(status).type("text/plain").send(msg);
});

/* ---------------------------------------------------------------- start */

const server = app.listen(PORT, () => {
  console.log("[boot] listening on :" + PORT + " (data: " + DATA_DIR + ")");
});

function shutdown(sig) {
  console.log("[boot] " + sig + " received, closing");
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(0), 8000).unref();
}
process.on("SIGTERM", () => shutdown("SIGTERM"));
process.on("SIGINT", () => shutdown("SIGINT"));
process.on("unhandledRejection", (e) => console.error("[error] unhandledRejection", e));
