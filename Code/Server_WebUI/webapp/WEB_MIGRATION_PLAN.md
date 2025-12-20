 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/PyCode/Client/WEB_MIGRATION_PLAN.md b/PyCode/Client/WEB_MIGRATION_PLAN.md
new file mode 100644
index 0000000000000000000000000000000000000000..4cd33d5076abe9721df9710c9978d56cd29edd1b
--- /dev/null
+++ b/PyCode/Client/WEB_MIGRATION_PLAN.md
@@ -0,0 +1,91 @@
+# Web Migration and Protocol Notes
+
+## 1. Existing client flow (PyQt)
+- **Main.py / Ui layout**: `mywindow` wires Qt widgets to robot controls and keeps video/power/telemetry labels in sync with socket events. It loads the saved IP (`IP.txt`) and creates the `VideoStreaming` transport helper. Movement buttons/keyboard shortcuts emit commands via `VideoStreaming.sendData`, with '#' as the field separator and a trailing `\n`. Servo sliders/buttons, LED toggles, buzzer, and mode selections all reuse the same command channel.【F:Main.py†L38-L735】
+- **Command formats**: Constants such as `CMD_M_MOTOR`, `CMD_CAR_ROTATE`, `CMD_SERVO`, `CMD_LED`, `CMD_MODE`, and telemetry keys (`CMD_SONIC`, `CMD_LIGHT`, `CMD_POWER`) are string prefixes from `Command.py`, joined with parameter fields separated by '#' and terminated with `\n`. Example: `CMD_SERVO#0#<angle>\n` for pan and `CMD_SERVO#1#<angle>\n` for tilt.【F:Command.py†L1-L17】【F:Main.py†L625-L644】【F:Main.py†L404-L735】
+- **Networking**: `VideoStreaming.StartTcpClient` opens two raw TCP sockets. The command/telemetry socket (`client_socket1`) connects to port **5000**; a dedicated video socket connects to port **8000** for JPEG frames. Threads are spawned from `on_btn_Connect` to stream video (`Video.streaming`) and to read telemetry (`recvmassage`), while periodic power polling runs on another thread via `Power` sending `CMD_POWER\n` every 60s.【F:Main.py†L754-L838】【F:Video.py†L20-L99】
+- **Telemetry parsing**: Incoming messages are split on `\n`, then on `#`; matches against command keys update UI labels or the progress bar via Qt signals. Ultrasound text: `Obstruction:<cm> cm`; light text: `Left:<v>V Right:<v>V`; power uses `(voltage-7)/1.40` to derive percentage.【F:Main.py†L806-L837】
+- **Threading/cleanup**: Threads are forcibly stopped with `stop_thread` from `Thread.py` using `PyThreadState_SetAsyncExc`. The `close` handler stops timers, threads, TCP sockets, and removes the last JPEG frame.【F:Thread.py†L1-L27】【F:Main.py†L783-L796】
+- **Video handling**: Raw stream frames arrive with a 4-byte little-endian length header, followed by JPEG bytes. After validating JPEG signatures, frames are decoded and saved to `video.jpg`. Optional Haar-cascade face detection updates `face_x/face_y` for servo auto-tracking in `time()`.【F:Video.py†L44-L78】【F:Main.py†L879-L888】
+
+## 2. Observed Pi-side protocol
+- **Ports**: Commands/telemetry over TCP port **5000**; video MJPEG-over-TCP (length-prefixed JPEGs) over port **8000**.【F:Video.py†L58-L99】
+- **Message grammar**:
+  - Outgoing commands: `<CMD><#param1>[#param2 ...]\n`. Examples include motor targets (`CMD_M_MOTOR#<angle>#<speed>#<reserve>#<reserve>\n`), mecanum wheel power (`CMD_MOTOR#FL#FR#BL#BR\n`), servo control (`CMD_SERVO#channel#angle\n`), LEDs (`CMD_LED#mask#R#G#B\n`), buzzer (`CMD_BUZZER#0|1\n`), mode selects (`CMD_MODE#one|two|three|four\n`), and sensor toggles (`CMD_SONIC#0|1\n`, `CMD_LIGHT#0|1\n`).【F:Main.py†L404-L735】
+  - Incoming telemetry: newline-delimited messages with the same command key as the first token, e.g., `CMD_SONIC#<cm>` or `CMD_LIGHT#<left>#<right>`; `CMD_POWER#<voltage>` used for battery percentage calculations.【F:Main.py†L806-L837】
+- **Authentication/encryption**: None observed; sockets are unauthenticated plain TCP.
+- **Video source**: Length-prefixed JPEG frames read from the TCP stream at port 8000; Pi likely serves frames from a camera and does not expose HTTP endpoints.【F:Video.py†L58-L78】
+
+## 3. Proposed backend API wrapper (on the Pi)
+- **Transport**: Replace raw TCP with a lightweight HTTP + WebSocket layer (FastAPI or Flask-SocketIO).
+  - **REST endpoints** (idempotent/configuration):
+    - `POST /api/drive/mecanum` → body `{fl, fr, bl, br}` (PWM or mm/s) mapped to `CMD_MOTOR` semantics.
+    - `POST /api/drive/omni` → body `{angle_deg, speed, rotation}` mapped to current `CMD_M_MOTOR` / `CMD_CAR_ROTATE` fields.
+    - `POST /api/servo` → body `{channel: 0|1, angle}`.
+    - `POST /api/leds` → body `{mask, r, g, b}` and `POST /api/leds/mode` → body `{mode: 0-4}`.
+    - `POST /api/buzzer` → body `{on: bool}`.
+    - `POST /api/mode` → body `{mode: "one"|"two"|"three"|"four"}`.
+    - `POST /api/sensors/sonic` and `/api/sensors/light` → body `{enabled: bool}`.
+  - **WebSocket**: `/ws/telemetry` for real-time push of ultrasonic, light, and power; `/ws/control` optional for low-latency drive commands.
+  - **Video**: Expose MJPEG over HTTP (`/video/mjpeg`), or provide HLS/WebRTC if latency demands. Minimal change: wrap existing JPEG stream in an HTTP multipart boundary.
+  - **Auth**: Add shared secret or bearer tokens; enable HTTPS via self-signed cert for LAN.
+
+## 4. Web/mobile UI design
+- **Layout parity**: Mirror Qt controls in a responsive grid (CSS grid/flex). Sections: connection/IP entry, video pane, drive pad (W/A/S/D + diagonals), wheel/rotate toggles, servo sliders + fine-tune nudges, LEDs (8 toggles + mode buttons + RGB inputs), buzzer, ultrasonic/light toggles, mode radio buttons, power/telemetry indicators.
+- **Control mapping**:
+  - Drive buttons/keyboard map to `POST /api/drive/...` or WebSocket control messages.
+  - Servo sliders/buttons call `/api/servo`; fine-tune buttons send relative deltas.
+  - LED toggles/modes call `/api/leds` and `/api/leds/mode`.
+  - Buzzer/ultrasonic/light/mode buttons hit their respective REST endpoints.
+  - Video pane loads `/video/mjpeg`; overlays face-tracking can be client-side via Canvas if needed.
+- **Responsiveness**: Use CSS breakpoints for tablet/phone; large touch targets for drive controls; status badges for connection and sensor values.
+
+## 5. Frontend client implementation plan
+- **Stack**: Single-page app (e.g., Vue 3 with Vite, or React) served from the Pi.
+- **State/UX**:
+  - Connection manager to open/close WebSocket, track online/offline, and buffer commands until connected.
+  - Drive control via buttons, keyboard (desktop), and touch gestures; send throttled WebSocket messages for low latency.
+  - REST fallbacks for configuration actions; optimistic UI with retries/backoff.
+  - Video component embedding MJPEG `<img>` or HLS player; show reconnect spinner on errors.
+  - Error banner + toast notifications for socket drops or command failures.
+- **Face-tracking parity**: Optional client-side face detection (e.g., MediaPipe/FaceDetector API) sending servo corrections via `/api/servo`.
+
+## 6. Test and hardening checklist
+- LAN tests from tablet/phone: measure drive command round-trip (<100 ms target) and video FPS/latency; verify reconnect after Wi-Fi loss.
+- Validate LED/servo limits and buzzer duration; ensure commands are idempotent and ignored when unauthenticated.
+- Security: enable tokens, rate-limit control endpoints, and prefer HTTPS; restrict CORS to LAN clients.
+
+## 7. Packaging/deployment
+- Serve the SPA and API from the Pi (uvicorn/gunicorn for FastAPI + static files). Configure systemd to start the API and optionally a reverse proxy (nginx) for TLS and caching the video endpoint.
+- Add a PWA manifest/service worker for offline shell and home-screen installability (icons, theme color, start URL). Cache static assets; keep video/WS uncached.
+
+## 8. Recommended next steps
+0) **Pull and read the Pi server scripts**
+   - Fetch the new `PyCode/Server` folder onto your workstation/Pi and open each entrypoint to understand how it binds to the legacy command (5000) and video (8000) sockets.
+   - Cross-check the code against the sample client command log (e.g., `commands_log.txt`) so you have a ground truth list of accepted messages and parameter ranges before wrapping them.
+
+1) **Confirm current Pi services**
+   - SSH into the Pi, list running services/ports (`ss -ltnp`), and capture any existing TCP listeners on 5000/8000.
+   - If the legacy server script exists, snapshot its command handling so API wrappers stay protocol-compatible (or keep it running and proxy through it during the migration).
+
+2) **Stand up a thin API wrapper (non-invasive)**
+   - Create a small FastAPI/Flask process that opens the existing TCP sockets to the motor/telemetry service and exposes the REST/WebSocket surfaces outlined in §3. Start with pass-through endpoints for drive, servo, LEDs, buzzer, mode, and sensor toggles using the exact message strings seen in the command log.
+   - Add an MJPEG HTTP endpoint that reuses the length-prefixed JPEG stream and repackages frames as multipart/x-mixed-replace.
+   - Keep authentication disabled initially to match current behavior, but leave a middleware hook so a shared-token check can be enabled later without changing routes.
+
+3) **Build a minimal SPA scaffold**
+   - Scaffold a Vite + Vue/React app with a connection panel, video `<img>`, basic drive buttons, and WebSocket status badge. Hardcode the Pi IP for the first iteration; add IP entry + localStorage later.
+   - Wire drive/servo/LED buttons to the new REST/WebSocket endpoints; log responses for debugging. Include a “raw command” console so you can send arbitrary strings from the command log during bring-up.
+
+4) **Iterate on control latency and resilience**
+   - Add a 50–100 ms throttle for drive WebSocket messages and reconnection/backoff logic. Show a toast/banner on socket drops and retry transparently.
+   - Measure end-to-end latency (button → motor action) with `time` stamps or audible buzzer toggles; tune transport (e.g., disable Nagle on server sockets) if needed.
+   - Capture packet traces while sending the sample commands to ensure the wrapper preserves framing (`<cmd>#...\n`) and that the Pi responds identically to the legacy client.
+
+5) **Security and deployment hardening**
+   - Introduce a shared token for REST/WebSocket upgrades; enforce CORS to LAN origins. If feasible, enable HTTPS via self-signed cert or nginx TLS termination.
+   - Add systemd units for the API and SPA static host; document how to restart/update. Include a `.env` for port/IP/token settings.
+
+6) **Feature parity sweep**
+   - Port remaining Qt niceties: fine servo nudges, LED mode presets, ultrasonic/light toggles, battery % display, and optional face-tracking overlay.
+   - Add a PWA manifest/service worker once core controls are stable; verify installability on tablet/phone.
 
EOF
)