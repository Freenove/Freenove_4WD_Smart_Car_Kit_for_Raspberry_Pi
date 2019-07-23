# -*-coding: utf-8 -*-
import time
from rpi_ws281x import *
# LED strip configuration:
LED_COUNT      = 8      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
# Define functions which animate LEDs in various ways.
class Led:
    def __init__(self):
        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()
        self.number='0'
    def colorWipe(self,strip, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def theaterChase(self,strip, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0,self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, color)
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    def wheel(self,pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(self,strip, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                 self.strip.setPixelColor(i, self.wheel((i+j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def rainbowCycle(self,strip, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def theaterChaseRainbow(self,strip, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i+q, 0)
    def ledIndex(self,index,R,G,B):
        self.strip.setPixelColor(index, Color(R,G,B))
        self.strip.show()
    def ledMode(self,n):
        self.mode=n
        while True:
            if self.mode=='one':
                self.colorWipe(self.strip, Color(255, 0, 0))  # Red wipe
                self.colorWipe(self.strip, Color(0, 255, 0))  # Green wipe
                self.colorWipe(self.strip, Color(0, 0, 255))  # Blue wipe
                self.colorWipe(self.strip, Color(0,0,0),10)
            elif self.mode=='two':
                self.theaterChaseRainbow(self.strip)
                self.colorWipe(self.strip, Color(0,0,0),10)
            elif self.mode=='three':
                self.rainbow(self.strip)
                self.colorWipe(self.strip, Color(0,0,0),10)
            elif self.mode=='four':
                self.rainbowCycle(self.strip)
                self.colorWipe(self.strip, Color(0,0,0),10)
            else:
                self.colorWipe(self.strip, Color(0,0,0),10)
                break
led=Led()                 
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        while True:
            print "Chaser animation"
            led.colorWipe(led.strip, Color(255, 0, 0))  # Red wipe
            led.colorWipe(led.strip, Color(0, 255, 0))  # Green wipe
            led.colorWipe(led.strip, Color(0, 0, 255))  # Blue wipe
            led.theaterChaseRainbow(led.strip)
            print "Rainbow animation"
            led.rainbow(led.strip)
            led.rainbowCycle(led.strip)
            led.colorWipe(led.strip, Color(0,0,0),10)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        led.colorWipe(led.strip, Color(0,0,0),10)

        
            
        
                    




   
