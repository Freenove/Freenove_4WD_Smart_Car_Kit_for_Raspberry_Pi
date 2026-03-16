#!/usr/bin/env python3

"""
Headless launcher for the web-based FreeKap 4WD controller.

- No Qt
- No legacy TCP server
- Exposes:
    * HTTP web UI on HTTP_PORT (default 8080)
    * /video/mjpeg from Camera
    * /api/telemetry, /api/drive/mecanum, /api/servo, /api/leds, etc.
"""

import sys
import time

from car import Car
from camera import Camera
from led import Led
from buzzer import Buzzer

from server import (
    start_http_server,
    set_app_context,
    HTTP_PORT,
)


def main():
    print("[MAIN_WEB] Starting headless web server...")

    # --- Instantiate hardware objects ---------------------------------------
    car = Car()
    camera = Camera(stream_size=(400, 300))
    led = Led()
    buzzer = Buzzer()

    # --- Expose them to server.py via APP_CONTEXT ---------------------------
    set_app_context(
        car=car,
        camera=camera,
        led=led,
        buzzer=buzzer,
    )

    print(f"[MAIN_WEB] Web UI available at http://<robot-ip>:{HTTP_PORT}/")
    print("[MAIN_WEB] Press Ctrl+C to stop.")

    try:
        # This blocks in the main thread; Ctrl+C raises KeyboardInterrupt here
        start_http_server(port=HTTP_PORT)
    except KeyboardInterrupt:
        print("\n[MAIN_WEB] Caught Ctrl+C, shutting down...")
    finally:
        # Clean up hardware on exit
        try:
            camera.stop_stream()
            camera.close()
        except Exception:
            pass

        try:
            car.close()
        except Exception:
            pass

        try:
            led.colorBlink(0)
        except Exception:
            pass

        try:
            buzzer.set_state(0)
        except Exception:
            pass

        print("[MAIN_WEB] Shutdown complete.")
        sys.exit(0)


if __name__ == "__main__":
    main()
