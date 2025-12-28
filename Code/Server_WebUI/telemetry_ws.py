#!/usr/bin/env python3
# telemetry_ws.py
#
# WebSocket server for telemetry, using the `websockets` library.
#
# Requires:
#   pip3 install websockets
#
# Listens on TELEMETRY_WS_PORT (default 8090) and serves telemetry on:
#   ws://<robot-ip>:8090/    (path is ignored, port is dedicated to telemetry)
#
# It periodically reads sensor values from the shared `car` object
# and pushes JSON messages to all connected clients.

import asyncio
import json
import threading
import time

import websockets  # pip3 install websockets

TELEMETRY_WS_PORT = 8090

# ---------------------------------------------------------------------------
# CONFIG: set this to True to test with dummy data instead of real sensors.
# If the WS becomes stable with dummy data, the issue is in the sensor read
# path (Car/ADC/Sonic/etc). If it's still unstable, it's WS/network-level.
# ---------------------------------------------------------------------------
USE_DUMMY_SNAPSHOT = True

# Global references set from main.py
_car = None
_started = False

TELEMETRY_INTERVAL = 0.5  # seconds between telemetry updates (slightly slower)


def set_car(car):
    """Set the car object used for telemetry snapshots."""
    global _car
    _car = car


def _get_dummy_snapshot():
    """Return a simple, safe snapshot for debugging the WebSocket itself."""
    now = time.time()
    return {
        "power": 42,
        "voltage": 11.1,
        "sonic": 123.4,
        "light_left": 1.23,
        "light_right": 4.56,
        "status": "DUMMY",
        "t": round(now, 2),
    }


def _get_real_snapshot():
    """
    Build a telemetry snapshot from the global `_car`.

    Returns a dict with keys:
      power, voltage, sonic, light_left, light_right, status
    """
    if _car is None:
        raise RuntimeError("Car object not set in telemetry_ws")

    car = _car

    try:
        adc = car.adc
        sonic = car.sonic
    except AttributeError:
        # Car object exists but doesn't have the expected attributes
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

    # Crude power percentage estimate (12V nominal)
    power_pct = max(0, min(100, int((voltage / 12.0) * 100)))

    return {
        "power": power_pct,
        "voltage": round(voltage, 2),
        "sonic": round(distance, 2),
        "light_left": round(light_left, 2),
        "light_right": round(light_right, 2),
        "status": "OK",
    }


def _get_telemetry_snapshot():
    """Select dummy or real snapshot depending on USE_DUMMY_SNAPSHOT."""
    if USE_DUMMY_SNAPSHOT:
        return _get_dummy_snapshot()
    return _get_real_snapshot()


# IMPORTANT: your websockets version calls handler(websocket), not (websocket, path).
# We ignore the path entirely and just treat any connection to this port as telemetry.
async def _telemetry_handler(websocket):
    """
    WebSocket handler for telemetry.

    Sends periodic JSON telemetry snapshots until the
    client disconnects.
    """
    path = getattr(websocket, "path", "/")
    print(f"[WS] Telemetry client connected (path reported as: {path})")

    try:
        while True:
            # Be very defensive about sensor errors
            try:
                snapshot = _get_telemetry_snapshot()
            except Exception as e:
                # Don't kill the WS connection if hardware glitches
                print(f"[WS] Telemetry snapshot error: {e}")
                snapshot = {"error": str(e), "status": "ERROR"}

            try:
                await websocket.send(json.dumps(snapshot))
            except websockets.ConnectionClosed as e:
                # LOG CLOSE CODE + REASON
                code = getattr(e, "code", None)
                reason = getattr(e, "reason", "")
                print(f"[WS] Telemetry client disconnected (code={code}, reason={reason})")
                break
            except Exception as e:
                print(f"[WS] Error sending telemetry: {e}")
                break

            await asyncio.sleep(TELEMETRY_INTERVAL)

    except Exception as e:
        # This should be rare now
        print(f"[WS] Telemetry error (outer): {e}")


async def _run_ws_server(host: str, port: int):
    """Async entrypoint for the telemetry WebSocket server."""
    print(f"[WS] Starting telemetry WebSocket on ws://{host}:{port}/ (path ignored)")
    # Your websockets version calls handler(websocket), so we pass _telemetry_handler
    async with websockets.serve(_telemetry_handler, host, port):
        await asyncio.Future()  # run forever


def _ws_thread_entry(host: str, port: int):
    """Thread entry: creates and runs its own asyncio loop."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(_run_ws_server(host, port))
    finally:
        loop.close()


def start_telemetry_ws_server(car, host: str = "0.0.0.0", port: int = TELEMETRY_WS_PORT):
    """
    Start the telemetry WebSocket server in a background thread.

    Safe to call multiple times; it will only start once.
    """
    global _started
    if _started:
        print("[WS] Telemetry WS server already started, skipping")
        return

    set_car(car)
    t = threading.Thread(target=_ws_thread_entry, args=(host, port), daemon=True)
    t.start()
    _started = True
    print(f"[WS] Telemetry WS server thread started on port {port}")
