 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/PyCode/Client/webapp/README.md b/PyCode/Client/webapp/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..6ef6c4a1444c020c9556048bcd33da8ca73ebcf7
--- /dev/null
+++ b/PyCode/Client/webapp/README.md
@@ -0,0 +1,57 @@
+# FreeKap 4WD web client
+
+A lightweight HTML/JS client that mirrors the PyQt controls and targets the proposed REST/WebSocket API wrapper around the legacy TCP interfaces (commands on 5000, video on 8000).
+
+## Features
+- MJPEG viewer (`/video/mjpeg`) with auto-reconnect.
+- Drive pad sending mecanum power (`POST /api/drive/mecanum`).
+- Servo sliders and nudges (`POST /api/servo`).
+- LED mask + RGB and mode buttons (`POST /api/leds`, `/api/leds/mode`).
+- Buzzer trigger (`POST /api/buzzer`).
+- Mode radio buttons (`POST /api/mode`).
+- Sensor toggles (`POST /api/sensors/sonic`, `/api/sensors/light`).
+- Raw command console (`POST /api/raw`) for direct `<CMD>#...\n` strings.
+- Telemetry WebSocket consumer (`/ws/telemetry`) that accepts either JSON payloads or legacy `CMD_*#...` lines.
+
+## Run locally
+From this folder:
+
+```bash
+python -m http.server 5500
+```
+
+Then open <http://localhost:5500> in your browser.
+
+### Point the client at the Pi
+
+1) Make sure the repo contains `PyCode/Client/RaspURL.txt` with two lines (host + port on each line):
+   - Line 1: Telemetry/API base (e.g., `http://192.168.129.51:5000`).
+   - Line 2: Video base (e.g., `http://192.168.129.51:8000`).
+
+2) The page reads those values automatically on load (no hardcoded defaults). The header shows the ports from `RaspURL.txt` and fills the editable URL fields:
+   - **Telemetry/API URL** drives REST calls and the WebSocket at `<telemetry-url>/ws/telemetry` (port label shows the parsed port).
+   - **Video URL** feeds MJPEG at `<video-url>/video/mjpeg` (port label shows the parsed port).
+
+3) Click **Connect**. If the telemetry badge stays red, the WebSocket couldn’t open on the specified host/port—double-check that the Pi wrapper is running and that no other client has occupied the legacy TCP connection.
+
+### “max connections (1) reached” from the Pi server
+The legacy TCP server on the Pi only accepts one active client at a time. If you see `rejected connection … max connections (1) reached`, another client (e.g., the old PyQt app or a leftover test session) is still connected to port 5000. Disconnect or close the other client and try again; if needed, restart the Pi server script to clear the slot.
+
+### Can I just double-click `index.html`?
+Opening the file directly (`file:///.../index.html`) will render the page, but most features will fail because browsers block `fetch`/WebSocket requests to `http://raspberrypi.local` from a `file://` origin. Always use a local web server (e.g., the `python -m http.server` command above) so the page loads from `http://localhost`.
+
+### Quick smoke test
+1. Run the local web server and load the page.
+2. Enter your Pi base URL and click **Connect**.
+3. Confirm the **API** badge flips to green after a ping (optional `/api/health`).
+4. Confirm the video pane shows MJPEG frames.
+5. Move a slider or tap a drive control and watch for success in the log panel.
+
+## Expected backend surface
+The page assumes the Pi exposes the wrapper outlined in `WEB_MIGRATION_PLAN.md`:
+
+- REST: `/api/drive/mecanum`, `/api/servo`, `/api/leds`, `/api/leds/mode`, `/api/buzzer`, `/api/mode`, `/api/sensors/sonic`, `/api/sensors/light`, `/api/raw`, optional `/api/health` for status.
+- WebSocket: `/ws/telemetry` streaming JSON (e.g., `{power, voltage, sonic, light_left, light_right}`) or legacy newline-delimited `CMD_*` strings.
+- Video: `/video/mjpeg` wrapping the existing length-prefixed JPEG feed on port 8000.
+
+If your wrapper uses different paths, adjust `app.js` constants to match.
 
EOF
)