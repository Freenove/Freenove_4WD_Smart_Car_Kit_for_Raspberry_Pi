#!/usr/bin/env python3

import socket          # For network communication
import fcntl           # For I/O control (Linux-specific)
import struct          # For packing/unpacking data
import threading       # To run HTTP server alongside TCP servers (if needed)
import queue           # For type hints and queue handling
import json            # For JSON encode/decode
import urllib.parse    # For parsing request paths
import time            # For buzzer beep timing
from http.server import SimpleHTTPRequestHandler
from socketserver import ThreadingTCPServer
from pathlib import Path

from tcp_server import TCPServer  # Your existing TCP server class

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

WEB_ROOT = Path(__file__).resolve().parent / "webapp"

HTTP_PORT = 8080
TELMY_PORT = 5000
VIDEO_PORT = 8000

# -----------------------------------------------------------------------------
# Custom ThreadingTCPServer with address reuse
# -----------------------------------------------------------------------------

class WebThreadingTCPServer(ThreadingTCPServer):
    # Allow quick restart on the same port after Ctrl+C
    allow_reuse_address = True

# -----------------------------------------------------------------------------
# Shared application context
#   Populated from main.py or main_web.py via set_app_context(...)
# -----------------------------------------------------------------------------

APP_CONTEXT = {
    "car": None,
    "camera": None,
    "tcp_server": None,
    "led": None,
    "buzzer": None,
    "sensors": {
        "sonic": True,
        "light": True,
    },
    "mode": None,
    "led_mode": 0,
}


def set_app_context(car=None, camera=None, tcp_server=None, led=None, buzzer=None):
    """
    Called from main.py or main_web.py to give the HTTP handler access
    to Car/Camera/Server/etc. Any argument can be None; we only overwrite
    what is provided.
    """
    global APP_CONTEXT
    if car is not None:
        APP_CONTEXT["car"] = car
    if camera is not None:
        APP_CONTEXT["camera"] = camera
    if tcp_server is not None:
        APP_CONTEXT["tcp_server"] = tcp_server
    if led is not None:
        APP_CONTEXT["led"] = led
    if buzzer is not None:
        APP_CONTEXT["buzzer"] = buzzer

# -----------------------------------------------------------------------------
# HTTP handler: static web UI + API + video stream
# -----------------------------------------------------------------------------

class WebAppHandler(SimpleHTTPRequestHandler):
    """HTTP handler serving static files from WEB_ROOT and handling /api/* & /video/*."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_ROOT), **kwargs)

    def log_message(self, format, *args):
        print(f"[HTTP] {self.address_string()} - {format % args}")

    # -------------------------------------------------------------------------
    # Helper: JSON response
    # -------------------------------------------------------------------------
    def _send_json(self, status_code: int, payload: dict):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # -------------------------------------------------------------------------
    # Helper: telemetry snapshot from car
    # -------------------------------------------------------------------------
    def _get_telemetry_snapshot(self):
        """
        Build a telemetry snapshot from APP_CONTEXT['car'].
        Returns a dict or raises RuntimeError if car is missing.
        """
        car = APP_CONTEXT.get("car")
        if car is None:
            raise RuntimeError("Car object not available")

        try:
            adc = car.adc
            sonic = car.sonic
        except AttributeError:
            raise RuntimeError("Car object missing adc/sonic attributes")

        # Power / voltage
        try:
            raw_power = adc.read_adc(2)
            factor = 3 if getattr(adc, "pcb_version", 1) == 1 else 2
            voltage = raw_power * factor
        except Exception:
            voltage = 0.0

        # Distance
        try:
            distance = sonic.get_distance()
        except Exception:
            distance = 0.0

        # Light sensors
        try:
            light_left = adc.read_adc(0)
            light_right = adc.read_adc(1)
        except Exception:
            light_left = 0.0
            light_right = 0.0

        power_pct = max(0, min(100, int((voltage / 12.0) * 100)))  # rough guess

        return {
            "power": power_pct,
            "voltage": round(voltage, 2),
            "sonic": round(distance, 2),
            "light_left": round(light_left, 2),
            "light_right": round(light_right, 2),
            "status": "OK",
        }

    # -------------------------------------------------------------------------
    # GET handler
    # -------------------------------------------------------------------------
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Simple health check
        if path == "/api/health":
            self._send_json(200, {"status": "ok"})
            return

        # Telemetry snapshot (used by app.js polling)
        if path == "/api/telemetry":
            try:
                snapshot = self._get_telemetry_snapshot()
                self._send_json(200, snapshot)
            except RuntimeError as e:
                self._send_json(503, {"error": str(e)})
            return

        # MJPEG video stream
        if path.startswith("/video/mjpeg"):
            camera = APP_CONTEXT.get("camera")
            if camera is None:
                self.send_error(503, "Camera not available")
                return

            boundary = "FRAME"
            self.send_response(200)
            self.send_header("Age", "0")
            self.send_header("Cache-Control", "no-cache, private")
            self.send_header("Pragma", "no-cache")
            self.send_header("Content-Type", f"multipart/x-mixed-replace; boundary={boundary}")
            self.end_headers()

            print("[VIDEO] MJPEG client connected")

            try:
                try:
                    camera.start_stream()
                except Exception as e:
                    print(f"[VIDEO] camera.start_stream() error: {e}")

                while True:
                    frame = camera.get_frame()
                    if not frame:
                        continue

                    try:
                        self.wfile.write(b"--" + boundary.encode("ascii") + b"\r\n")
                        self.wfile.write(b"Content-Type: image/jpeg\r\n")
                        self.wfile.write(
                            b"Content-Length: " + str(len(frame)).encode("ascii") + b"\r\n\r\n"
                        )
                        self.wfile.write(frame)
                        self.wfile.write(b"\r\n")
                        self.wfile.flush()
                    except (BrokenPipeError, ConnectionResetError):
                        print("[VIDEO] MJPEG client disconnected")
                        break
                    except Exception as e:
                        print(f"[VIDEO] stream error: {e}")
                        break
            finally:
                try:
                    camera.stop_stream()
                except Exception:
                    pass

            return

        # Fallback: static files (index.html, app.js, styles.css, ...)
        return super().do_GET()

    # -------------------------------------------------------------------------
    # POST handler: API endpoints
    # -------------------------------------------------------------------------
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length) if length > 0 else b"{}"

        try:
            payload = json.loads(body.decode("utf-8") or "{}")
        except Exception:
            payload = {}

        print(f"[API] {path} payload: {payload}")

        # ===== API: DRIVE (mecanum) ==========================================
        if path == "/api/drive/mecanum":
            car = APP_CONTEXT.get("car")
            if car is None or getattr(car, "motor", None) is None:
                self._send_json(503, {"error": "Car motor not available"})
                return

            try:
                fl = int(payload.get("fl", 0))
                fr = int(payload.get("fr", 0))
                bl = int(payload.get("bl", 0))
                br = int(payload.get("br", 0))
            except Exception:
                self._send_json(400, {"error": "Invalid drive payload"})
                return

            try:
                # Freenove order: left front, left rear, right front, right rear
                car.motor.set_motor_model(fl, bl, fr, br)
            except Exception as e:
                print(f"[API] drive error: {e}")
                self._send_json(500, {"error": str(e)})
                return

            self._send_json(200, {
                "ok": True,
                "action": "drive_mecanum",
                "fl": fl, "fr": fr, "bl": bl, "br": br,
            })
            return

        # ===== API: SERVO =====================================================
        if path == "/api/servo":
            car = APP_CONTEXT.get("car")
            if car is None or getattr(car, "servo", None) is None:
                self._send_json(503, {"error": "Servo controller not available"})
                return

            try:
                channel = int(payload.get("channel", 0))
                angle = int(payload.get("angle", 90))
            except Exception:
                self._send_json(400, {"error": "Invalid servo payload"})
                return

            try:
                # original Freenove code uses string channel
                car.servo.set_servo_pwm(str(channel), angle)
            except Exception as e:
                print(f"[API] servo error: {e}")
                self._send_json(500, {"error": str(e)})
                return

            self._send_json(200, {
                "ok": True,
                "action": "servo",
                "channel": channel,
                "angle": angle,
            })
            return

        # ===== API: LEDS (mask + RGB) ========================================
        if path == "/api/leds":
            led = APP_CONTEXT.get("led")
            mask = int(payload.get("mask", 0))
            r = int(payload.get("r", 0))
            g = int(payload.get("g", 0))
            b = int(payload.get("b", 0))

            if led is None:
                # Just acknowledge so the UI shows success even without hardware
                self._send_json(200, {
                    "ok": True,
                    "action": "leds_stub_no_hw",
                    "mask": mask,
                    "rgb": [r, g, b],
                })
                return

            # Simple implementation: set each LED in the mask to the same color
            try:
                # Assuming Led.ledIndex(index, r, g, b) with 1-based index
                for idx in range(8):
                    if mask & (1 << idx):
                        led.ledIndex(idx + 1, r, g, b)
            except Exception as e:
                print(f"[API] leds error: {e}")
                self._send_json(500, {"error": str(e)})
                return

            self._send_json(200, {
                "ok": True,
                "action": "leds",
                "mask": mask,
                "rgb": [r, g, b],
            })
            return

        # ===== API: LED MODE (simple state, hook for your LED process) ========
        if path == "/api/leds/mode":
            mode = int(payload.get("mode", 0))
            APP_CONTEXT["led_mode"] = mode
            led = APP_CONTEXT.get("led")

            if led is None:
                self._send_json(200, {
                    "ok": True,
                    "action": "leds_mode_stub_no_hw",
                    "mode": mode,
                })
                return

            # Here we avoid long blocking patterns; you can integrate this
            # with your process_led_running via APP_CONTEXT["led_mode"].
            try:
                if mode == 0:
                    # Off
                    led.colorBlink(0)
                elif mode == 1:
                    # Simple blink / placeholder
                    led.colorBlink(1)
                # Modes 2..4 left as TODO for your own patterns
            except Exception as e:
                print(f"[API] leds mode error: {e}")
                self._send_json(500, {"error": str(e)})
                return

            self._send_json(200, {
                "ok": True,
                "action": "leds_mode",
                "mode": mode,
            })
            return

        # ===== API: BUZZER (1 second beep) ===================================
        if path == "/api/buzzer":
            buzzer = APP_CONTEXT.get("buzzer")
            if buzzer is None:
                self._send_json(503, {"error": "Buzzer not available"})
                return

            # Ignore payload; always produce a 1-second beep
            try:
                buzzer.set_state(1)
                time.sleep(1.0)   # 1 second beep
                buzzer.set_state(0)
            except Exception as e:
                print(f"[API] buzzer error: {e}")
                self._send_json(500, {"error": str(e)})
                return

            self._send_json(200, {
                "ok": True,
                "action": "buzzer",
                "beep": True,
                "duration_ms": 1000,
            })
            return

        # ===== API: MODE (car high-level mode; stored only for now) ==========
        if path == "/api/mode":
            mode = payload.get("mode")
            APP_CONTEXT["mode"] = mode
            # You can integrate this with car_mode in main.py if desired.
            self._send_json(200, {"ok": True, "action": "mode", "mode": mode})
            return

        # ===== API: SENSORS TOGGLE (stores flags) ============================
        if path.startswith("/api/sensors/"):
            sensor_name = path.rsplit("/", 1)[-1]
            enabled = bool(payload.get("enabled", True))
            APP_CONTEXT["sensors"][sensor_name] = enabled
            self._send_json(
                200,
                {
                    "ok": True,
                    "action": "sensor",
                    "sensor": sensor_name,
                    "enabled": enabled,
                },
            )
            return

        # ===== API: RAW ======================================================
        if path == "/api/raw":
            cmd = payload.get("command", "")
            # For now, just echo. You can route this into your existing
            # command-processing stack if you want complete legacy compatibility.
            self._send_json(
                200,
                {
                    "ok": True,
                    "action": "raw",
                    "echo": cmd,
                },
            )
            return

        # Unknown API
        self.send_error(404, f"Unknown API endpoint: {path}")


# -----------------------------------------------------------------------------
# HTTP server startup
# -----------------------------------------------------------------------------

def start_http_server(port: int = HTTP_PORT) -> None:
    """Start a simple multithreaded HTTP server for the web UI."""
    with WebThreadingTCPServer(("", port), WebAppHandler) as httpd:
        print(f"[HTTP] Serving {WEB_ROOT} on http://0.0.0.0:{port}/")
        httpd.serve_forever()

# -----------------------------------------------------------------------------
# Existing robot TCP server logic (for legacy TCP clients, ports 5000/8000)
# -----------------------------------------------------------------------------

class Server:
    def __init__(self):
        """Initialize the Server class (command + video TCP servers)."""
        self.ip_address = self.get_interface_ip()
        self.command_server = TCPServer()
        self.video_server = TCPServer()
        self.command_server_is_busy = False
        self.video_server_is_busy = False

    def get_interface_ip(self) -> str:
        """Get the IP address of the wlan0 interface."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ip = socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,
                struct.pack('256s', b'wlan0'[:15])
            )[20:24])
            return ip
        except Exception as e:
            print(f"Error getting IP address: {e}")
            return "127.0.0.1"

    def start_tcp_servers(
        self,
        command_port: int = TELMY_PORT,
        video_port: int = VIDEO_PORT,
        max_clients: int = 1,
        listen_count: int = 1
    ) -> None:
        """Start the TCP servers on specified ports."""
        try:
            print(f"[TCP] Starting command server on {self.ip_address}:{command_port}")
            self.command_server.start(self.ip_address, command_port, max_clients, listen_count)

            print(f"[TCP] Starting video server on {self.ip_address}:{video_port}")
            self.video_server.start(self.ip_address, video_port, max_clients, listen_count)
        except Exception as e:
            print(f"Error starting TCP servers: {e}")

    def stop_tcp_servers(self) -> None:
        """Stop the TCP servers."""
        try:
            print("[TCP] Stopping TCP servers...")
            self.command_server.close()
            self.video_server.close()
        except Exception as e:
            print(f"Error stopping TCP servers: {e}")

    def set_command_server_busy(self, state: bool) -> None:
        self.command_server_is_busy = state

    def set_video_server_busy(self, state: bool) -> None:
        self.video_server_is_busy = state

    def get_command_server_busy(self) -> bool:
        return self.command_server_is_busy

    def get_video_server_busy(self) -> bool:
        return self.video_server_is_busy

    def send_data_to_command_client(self, data: bytes, ip_address: str = None) -> None:
        self.set_command_server_busy(True)
        try:
            if ip_address is not None:
                self.command_server.send_to_client(ip_address, data)
            else:
                self.command_server.send_to_all_client(data)
        except Exception as e:
            print(e)
        finally:
            self.set_command_server_busy(False)

    def send_data_to_video_client(self, data: bytes, ip_address: str = None) -> None:
        self.set_video_server_busy(True)
        try:
            if ip_address is not None:
                self.video_server.send_to_client(ip_address, data)
            else:
                self.video_server.send_to_all_client(data)
        finally:
            self.set_video_server_busy(False)

    def read_data_from_command_server(self) -> 'queue.Queue':
        return self.command_server.message_queue

    def read_data_from_video_server(self) -> 'queue.Queue':
        return self.video_server.message_queue

    def is_command_server_connected(self) -> bool:
        return self.command_server.active_connections > 0

    def is_video_server_connected(self) -> bool:
        return self.video_server.active_connections > 0

    def get_command_server_client_ips(self) -> list:
        return self.command_server.get_client_ips()

    def get_video_server_client_ips(self) -> list:
        return self.video_server.get_client_ips()


# -----------------------------------------------------------------------------
# Standalone mode (optional: if you ever run server.py directly)
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    print('Program is starting ... ')
    server = Server()
    server.start_tcp_servers(command_port=TELMY_PORT, video_port=VIDEO_PORT)

    http_thread = threading.Thread(
        target=start_http_server,
        kwargs={"port": HTTP_PORT},
        daemon=True
    )
    http_thread.start()

    print(f"[MAIN] Command server on {server.ip_address}:{TELMY_PORT}")
    print(f"[MAIN] Video server   on {server.ip_address}:{VIDEO_PORT}")
    print(f"[MAIN] Web UI         on http://{server.ip_address}:{HTTP_PORT}/")

    try:
        while True:
            cmd_queue = server.read_data_from_command_server()
            if cmd_queue.qsize() > 0:
                client_address, message = cmd_queue.get()
                print("[CMD]", client_address, message)
                server.send_data_to_command_client(message, client_address)

            video_queue = server.read_data_from_video_server()
            if video_queue.qsize() > 0:
                client_address, message = video_queue.get()
                print("[VIDEO]", client_address, "<message>")
                server.send_data_to_video_client(message, client_address)

    except KeyboardInterrupt:
        print("\nReceived interrupt signal, stopping server...")
        server.stop_tcp_servers()
