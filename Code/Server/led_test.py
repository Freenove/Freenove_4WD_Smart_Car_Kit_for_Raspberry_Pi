# File: ~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server/led_test.py
# Simple test script to light up WS2812 LEDs using the installed rpi_ws281x Python wrapper

import time
import board
import neopixel

# 🛠️ Config — adjust to your setup:
NUM_LEDS = 8              # How many LEDs you're using
PIN = board.D18           # GPIO 18 (Physical Pin 12)

# 🎛️ Initialize LED strip
pixels = neopixel.NeoPixel(
    PIN, NUM_LEDS, brightness=0.4, auto_write=False, pixel_order=neopixel.GRB
)

# 🌈 Cycle through colors
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue

for color in colors:
    pixels.fill(color)
    pixels.show()
    time.sleep(1)

# 🚫 Turn off
pixels.fill((0, 0, 0))
pixels.show()
