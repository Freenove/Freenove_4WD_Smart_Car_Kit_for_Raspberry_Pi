// app.js - FreeKap 4WD minimal web UI + smart assist

const DEFAULT_TELEMETRY = "";
const DEFAULT_VIDEO = "";

const state = {
  telemetryUrl: localStorage.getItem("fk_telemetry") || DEFAULT_TELEMETRY,
  videoUrl: localStorage.getItem("fk_video") || DEFAULT_VIDEO,
  videoConnected: false,

  driveActive: null,     // "front", "rear", "left", "right", "stop"…
  holdMode: false,       // HOLD button toggle

  // Smart assist state
  sonicDistance: null,   // latest distance in cm
  lastBuzzerTime: 0,     // ms timestamp
  smartStopped: false,   // already hard-stopped for obstacle
};

const el = {};

let lastVideoBase = null;
let telemetryTimer = null;

console.log("FreeKap minimal UI app.js loaded");

// ---------------------------------------------------------------------------
// Boot
// ---------------------------------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {
  cacheElements();
  hydrateEndpoints();
  loadRaspUrlFile()
    .catch(() => {})
    .finally(() => {
      bindEvents();
      preventContextMenus();
      setVideoFeed();
      startTelemetryPolling();
    });
});

// ---------------------------------------------------------------------------
// Element cache
// ---------------------------------------------------------------------------

function cacheElements() {
  el.telemetryUrl = document.getElementById("telemetry-url");
  el.videoUrl = document.getElementById("video-url");
  el.connectBtn = document.getElementById("connect-btn");

  el.video = document.getElementById("video-feed");
  el.videoOverlay = document.getElementById("video-overlay");
  el.autoReconnect = document.getElementById("auto-reconnect");

  el.driveButtons = [...document.querySelectorAll("[data-drive]")];
  el.holdBtn = document.getElementById("hold-btn");

  el.servoPan = document.getElementById("servo-pan");
  el.servoTilt = document.getElementById("servo-tilt");
  el.servoPanValue = document.getElementById("servo-pan-value");
  el.servoTiltValue = document.getElementById("servo-tilt-value");

  el.buzzerToggle = document.getElementById("buzzer-toggle");
  el.cmd1Btn = document.getElementById("cmd1-btn"); // RESET / SERVO
  el.cmd2Btn = document.getElementById("cmd2-btn");

  el.telemetryPower = document.getElementById("power");
  el.telemetrySonic = document.getElementById("sonic");
  el.telemetryLight = document.getElementById("light");
  el.status = document.getElementById("status");

  el.batterySummary = document.getElementById("battery-summary");
  el.apiStatus = document.getElementById("api-status");
  el.wsStatus = document.getElementById("ws-status");
}

// ---------------------------------------------------------------------------
// URL helpers
// ---------------------------------------------------------------------------

function hydrateEndpoints() {
  el.telemetryUrl.value = state.telemetryUrl;
  el.videoUrl.value = state.videoUrl;
}

function normalizeBase(input, fallback) {
  if (!input) return fallback || state.telemetryUrl;
  let url = input.trim();
  if (!/^https?:\/\//i.test(url)) {
    url = `http://${url}`;
  }
  return url.replace(/\/$/, "");
}

// ---------------------------------------------------------------------------
// Event binding
// ---------------------------------------------------------------------------

function bindEvents() {
  el.connectBtn.addEventListener("click", () => {
    state.telemetryUrl = normalizeBase(el.telemetryUrl.value, state.telemetryUrl);
    state.videoUrl = normalizeBase(el.videoUrl.value, state.videoUrl);
    localStorage.setItem("fk_telemetry", state.telemetryUrl);
    localStorage.setItem("fk_video", state.videoUrl);
    setVideoFeed();
    startTelemetryPolling(true);
  });

  el.video.addEventListener("load", () => setVideoState(true));
  el.video.addEventListener("error", () => setVideoState(false));

  // Drive buttons
  el.driveButtons.forEach((btn) => {
    const kind = btn.dataset.drive;

    if (kind === "hold") {
      btn.addEventListener("click", toggleHoldMode);
    } else if (kind === "stop") {
      btn.addEventListener("click", () => {
        state.driveActive = null;
        state.holdMode = false;
        state.smartStopped = false;
        updateHoldIndicator(false);
        handleDrive("stop");
      });
    } else {
      // Directional buttons – press to move, release to stop (unless HOLD)
      btn.addEventListener("pointerdown", () => handleDrive(kind));
      btn.addEventListener("pointerup", () => {
        if (!state.holdMode) {
          state.smartStopped = false;
          handleDrive("stop");
        }
      });
      btn.addEventListener("pointerleave", () => {
        if (!state.holdMode) {
          state.smartStopped = false;
          handleDrive("stop");
        }
      });
    }
  });

  const setServoFromSlider = (slider, label, channel) => {
    label.textContent = `${slider.value}°`;
    sendServo(channel, Number(slider.value));
  };

  el.servoPan.addEventListener("input", () =>
    setServoFromSlider(el.servoPan, el.servoPanValue, 0)
  );
  el.servoTilt.addEventListener("input", () =>
    setServoFromSlider(el.servoTilt, el.servoTiltValue, 1)
  );

  // BEEP
  el.buzzerToggle.addEventListener("click", () => {
    sendJson("/api/buzzer", {})
      .then(() => setStatus("Beep!"))
      .catch((err) => console.error("Buzzer error:", err));
  });

  // RESET / SERVO
  el.cmd1Btn.addEventListener("click", () => {
    const neutral = 90;
    el.servoPan.value = neutral;
    el.servoTilt.value = neutral;
    el.servoPanValue.textContent = `${neutral}°`;
    el.servoTiltValue.textContent = `${neutral}°`;
    sendServo(0, neutral);
    sendServo(1, neutral);
    setStatus("Servos centered");
  });

  // CMD2 placeholder
  el.cmd2Btn.addEventListener("click", () => {
    console.log("CMD2 pressed (placeholder)");
  });
}

// ---------------------------------------------------------------------------
// Disable context menus / long-press menus on controls
// ---------------------------------------------------------------------------

function preventContextMenus() {
  const selectors = [
    "button",
    ".drive-pad",
    ".action-buttons",
    ".servo-controls",
    ".video-servos",
  ];
  const blockers = document.querySelectorAll(selectors.join(", "));

  blockers.forEach((el) => {
    el.addEventListener("contextmenu", (e) => {
      e.preventDefault();
    });
    el.addEventListener("pointerdown", (e) => {
      if (e.button === 2) {
        e.preventDefault();
      }
    });
  });
}

// ---------------------------------------------------------------------------
// Video
// ---------------------------------------------------------------------------

function setVideoFeed() {
  const base = state.videoUrl || state.telemetryUrl;

  if (!base) {
    el.videoOverlay.textContent = "No video base URL configured";
    el.videoOverlay.style.display = "grid";
    return;
  }

  if (base === lastVideoBase && state.videoConnected) {
    // Already streaming from this base
    return;
  }

  lastVideoBase = base;
  const src = `${withPath(base, "/video/mjpeg")}?ts=${Date.now()}`;
  el.video.src = src;
  el.videoOverlay.textContent = "Connecting…";
  el.videoOverlay.style.display = "grid";
}

function setVideoState(ok) {
  state.videoConnected = ok;
  if (ok) {
    el.videoOverlay.textContent = "";
    el.videoOverlay.style.display = "none";
  } else {
    el.videoOverlay.textContent = "Stream unavailable";
    el.videoOverlay.style.display = "grid";
    if (el.autoReconnect.checked) {
      setTimeout(setVideoFeed, 1500);
    }
  }
}

// ---------------------------------------------------------------------------
// Telemetry (HTTP polling)
// ---------------------------------------------------------------------------

async function fetchTelemetryOnce() {
  if (!state.telemetryUrl) return;
  try {
    const url = withPath(state.telemetryUrl, "/api/telemetry");
    const res = await fetch(url);
    if (!res.ok) throw new Error(`status ${res.status}`);
    const data = await res.json();
    updateTelemetryFromJson(data);
    setBadge(el.wsStatus, "online", "success");
    setBadge(el.apiStatus, "online", "success");
  } catch (err) {
    setBadge(el.wsStatus, "offline", "error");
    setBadge(el.apiStatus, "offline", "error");
  }
}

function startTelemetryPolling(force = false) {
  if (telemetryTimer && !force) return;
  if (telemetryTimer) {
    clearInterval(telemetryTimer);
    telemetryTimer = null;
  }
  setBadge(el.wsStatus, "probing…", "warn");
  setBadge(el.apiStatus, "probing…", "warn");
  telemetryTimer = setInterval(fetchTelemetryOnce, 500);
  fetchTelemetryOnce();
}

function stopTelemetryPolling() {
  if (telemetryTimer) {
    clearInterval(telemetryTimer);
    telemetryTimer = null;
  }
  setBadge(el.wsStatus, "offline", "error");
  setBadge(el.apiStatus, "offline", "error");
}

// ---------------------------------------------------------------------------
// Telemetry parsing + Smart assist
// ---------------------------------------------------------------------------

function updateTelemetryFromJson(msg) {
  if (msg.power !== undefined) {
    const powerText = `${msg.power}%${msg.voltage ? ` (${msg.voltage}V)` : ""}`;
    el.telemetryPower.textContent = powerText;
    if (el.batterySummary) {
      el.batterySummary.textContent = powerText;
    }
  }
  if (msg.sonic !== undefined) {
    el.telemetrySonic.textContent = `${msg.sonic} cm`;
    state.sonicDistance = Number(msg.sonic);
  }
  if (msg.light_left !== undefined && msg.light_right !== undefined) {
    el.telemetryLight.textContent = `${msg.light_left} / ${msg.light_right} V`;
  }
  if (msg.status) {
    el.status.textContent = msg.status;
  }

  // Smart assist logic runs after updating telemetry
  maybeSmartAssist();
}

// Smart assist: distance-based forward braking
function maybeSmartAssist() {
  const d = state.sonicDistance;

  // Only assist when actively driving forward
  if (state.driveActive !== "front") {
    state.smartStopped = false;
    return;
  }
  if (d == null || isNaN(d) || d <= 0) return;

  // Emergency stop at very close range
  if (d <= 15) {
    if (!state.smartStopped) {
      console.log("[ASSIST] Obstacle ≤15 cm -> STOP");
      state.smartStopped = true;
      state.holdMode = false;
      updateHoldIndicator(false);
      handleDrive("stop");
      maybeSmartBeep();
    }
    return;
  }

  // From here on, we are not in hard-stop
  state.smartStopped = false;

  // Decide speed level based on distance
  let factor;
  let modeLabel;

  if (d > 80) {
    // Far away: let manual command dominate, no override
    return;
  } else if (d > 50) {
    factor = 0.7;
    modeLabel = "ASSIST: CAUTION";
  } else if (d > 30) {
    factor = 0.4;
    modeLabel = "ASSIST: BRAKE";
  } else {
    // 30 >= d > 15
    factor = 0.2;
    modeLabel = "ASSIST: HARD BRAKE";
    maybeSmartBeep();
  }

  factor = Math.max(0, Math.min(1, factor));

  const base = drivePayload("front");
  const scaled = {
    fl: Math.round(base.fl * factor),
    fr: Math.round(base.fr * factor),
    bl: Math.round(base.bl * factor),
    br: Math.round(base.br * factor),
  };

  sendDrive(
    scaled,
    `${modeLabel} – FRONT @ ${Math.round(d)} cm (${Math.round(factor * 100)}%)`
  );
}

// Cooldown beep to avoid spam
function maybeSmartBeep() {
  const now = Date.now();
  const intervalMs = 1500;
  if (now - state.lastBuzzerTime < intervalMs) return;
  state.lastBuzzerTime = now;

  console.log("[ASSIST] Beep: obstacle close");
  sendJson("/api/buzzer", {})
    .then(() => setStatus("Assist: Beep (obstacle close)"))
    .catch((err) => console.error("Smart assist buzzer error:", err));
}

// ---------------------------------------------------------------------------
// Drive logic
// ---------------------------------------------------------------------------

function toggleHoldMode() {
  state.holdMode = !state.holdMode;
  updateHoldIndicator(state.holdMode);
}

function updateHoldIndicator(on) {
  if (!el.holdBtn) return;
  if (on) el.holdBtn.classList.add("active");
  else el.holdBtn.classList.remove("active");
}

// Single place to send drive commands
function sendDrive(body, statusText) {
  return sendJson("/api/drive/mecanum", body)
    .then(() => {
      if (statusText) setStatus(statusText);
    })
    .catch((err) => console.error("Drive error:", err));
}

function drivePayload(kind) {
  // Base speed (tuned for Freenove; adjust if needed)
  const fast = 1500;
  const zero = { fl: 0, fr: 0, bl: 0, br: 0 };

  const mappings = {
    front: { fl: fast, fr: fast, bl: fast, br: fast },
    rear: { fl: -fast, fr: -fast, bl: -fast, br: -fast },
    left: { fl: -fast, fr: fast, bl: 0, br: fast },
    right: { fl: fast, fr: -fast, bl: fast, br: 0 },
    diagLeft: { fl: 0, fr: fast, bl: 0, br: 0 },
    diagRight: { fl: fast, fr: 0, bl: 0, br: 0 },
    diagBackLeft: { fl: 0, fr: 0, bl: 0, br: -fast },
    diagBackRight: { fl: 0, fr: 0, bl: -fast, br: 0 },
    stop: zero,
  };

  const key = camel(kind);
  return mappings[key] || zero;
}

function handleDrive(kind) {
  const payload = drivePayload(kind);
  if (!payload) return;

  if (kind === "stop") {
    state.driveActive = null;
  } else {
    state.driveActive = kind;
  }

  sendDrive(payload, `Drive: ${kind}`);
}

// ---------------------------------------------------------------------------
// Servos
// ---------------------------------------------------------------------------

function sendServo(channel, angle) {
  return sendJson("/api/servo", { channel, angle })
    .then(() => setStatus(`Servo ${channel} → ${angle}`))
    .catch((err) => console.error("Servo error:", err));
}

// ---------------------------------------------------------------------------
// HTTP helper
// ---------------------------------------------------------------------------

async function sendJson(path, body) {
  if (!state.telemetryUrl) throw new Error("No telemetry URL set");
  const url = withPath(state.telemetryUrl, path);
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  try {
    return await res.json();
  } catch (_) {
    return {};
  }
}

// ---------------------------------------------------------------------------
// UI helpers
// ---------------------------------------------------------------------------

function setBadge(elm, text, variant) {
  if (!elm) return;
  elm.textContent = text;
  elm.classList.remove("success", "error", "warn");
  if (variant) elm.classList.add(variant);
}

function setStatus(text) {
  if (!el.status) return;
  el.status.textContent = text;
}

// ---------------------------------------------------------------------------
// Misc helpers
// ---------------------------------------------------------------------------

function camel(text) {
  return text.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
}

async function loadRaspUrlFile() {
  try {
    const res = await fetch("RaspURL.txt", { cache: "no-cache" });
    if (!res.ok) return;
    const text = await res.text();
    const [telemetryLine, videoLine] = text
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean);
    if (telemetryLine) {
      state.telemetryUrl = normalizeBase(telemetryLine, DEFAULT_TELEMETRY);
      localStorage.setItem("fk_telemetry", state.telemetryUrl);
    }
    if (videoLine) {
      state.videoUrl = normalizeBase(videoLine, state.telemetryUrl || DEFAULT_VIDEO);
      localStorage.setItem("fk_video", state.videoUrl);
    }
    hydrateEndpoints();
    setVideoFeed();
  } catch (err) {
    console.warn("Could not read RaspURL.txt:", err.message);
  }
}

function withPath(base, path) {
  try {
    const url = new URL(base);
    const cleanPath = path.startsWith("/") ? path : `/${path}`;
    if (url.pathname === "/" || url.pathname === "") {
      url.pathname = cleanPath;
    } else if (!url.pathname.endsWith(path)) {
      url.pathname = `${url.pathname.replace(/\/$/, "")}${cleanPath}`;
    }
    return url.toString();
  } catch (_) {
    return `${base}${path}`;
  }
}
