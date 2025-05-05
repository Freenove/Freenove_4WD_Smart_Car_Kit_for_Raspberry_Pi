# File: ~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server/led_test_raw.py
# Direct use of rpi_ws281x to light up LEDs (no Blinka or neopixel module required)

import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT      = 8        # Number of LED pixels.
LED_PIN        = 18       # GPIO pin connected to the pixels (18 uses PWM).
LED_FREQ_HZ    = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10       # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 128      # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0        # Set to 1 for GPIOs 13, 19, 41, 45 or 53

# Initialize the strip
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Test: cycle red, green, blue
def color_wipe(strip, color, wait_ms=500):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(wait_ms / 1000.0)

# Run the test
color_wipe(strip, Color(255, 0, 0))  # Red
color_wipe(strip, Color(0, 255, 0))  # Green
color_wipe(strip, Color(0, 0, 255))  # Blue
color_wipe(strip, Color(0, 0, 0))    # Off

