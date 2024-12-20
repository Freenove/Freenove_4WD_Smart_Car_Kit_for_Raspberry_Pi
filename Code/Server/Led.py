# -*-coding: utf-8 -*-
import time
from parameter import ParameterManager
from rpi_ledpixel import Freenove_RPI_WS281X
from spi_ledpixel import Freenove_SPI_LedPixel

class Led:
    def __init__(self):
        """Initialize the Led class and set up LED strip based on PCB and Raspberry Pi versions."""
        # Initialize the ParameterManager instance
        self.param = ParameterManager()
        # Get the PCB version from the parameter file
        self.pcb_version = self.param.get_pcb_version()
        # Get the Raspberry Pi version from the parameter file
        self.pi_version = self.param.get_raspberry_pi_version()

        # Set up the LED strip based on PCB and Raspberry Pi versions
        if self.pcb_version == 1 and self.pi_version == 1:
            self.strip = Freenove_RPI_WS281X(8, 255, 'RGB')
            self.is_support_led_function = True

        elif self.pcb_version == 2 and (self.pi_version == 1 or self.pi_version == 2):
            self.strip = Freenove_SPI_LedPixel(8, 255, 'GRB')
            self.is_support_led_function = True

        elif self.pcb_version == 1 and self.pi_version == 2:
            # Print an error message and disable LED function if unsupported combination
            print("PCB Version 1.0 is not supported on Raspberry PI 5.")
            self.is_support_led_function = False

    def colorWipe(self, change_color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        if self.is_support_led_function == False:
            return
        else:
            # Iterate through each LED and set its color
            for i in range(self.strip.get_led_count()):
                self.strip.set_led_rgb_data(i, change_color)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if self.is_support_led_function == False:
            return
        else:
            if pos < 0 or pos > 255:
                r = g = b = 0
            elif pos < 85:
                r = pos * 3
                g = 255 - pos * 3
                b = 0
            elif pos < 170:
                pos -= 85
                r = 255 - pos * 3
                g = 0
                b = pos * 3
            else:
                pos -= 170
                r = 0
                g = pos * 3
                b = 255 - pos * 3
            return (r, g, b)
        
    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        if self.is_support_led_function == False:
            return
        else:
            # Generate and display rainbow colors
            for j in range(256 * iterations):
                for i in range(self.strip.get_led_count()):
                    self.strip.set_led_rgb_data(i, self.wheel((i + j) & 255))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)

    def rainbowCycle(self, wait_ms = 20, iterations = 5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        if self.is_support_led_function == False:
            return
        else:
            for j in range(256*iterations):
                for i in range(self.strip.get_led_count()):
                    self.strip.set_led_rgb_data(i, self.wheel((int(i * 256 / self.strip.get_led_count()) + j) & 255))
                self.strip.show()
                time.sleep(wait_ms/1000.0)

    def theaterChaseRainbow(self, wait_ms = 50):
        """Rainbow movie theater light style chaser animation."""
        if self.is_support_led_function == False:
            return
        else:
            led_count = self.strip.get_led_count()
            for j in range(0, 256, 5):
                for q in range(3):
                    for i in range(0, led_count, 3):
                        self.strip.set_led_rgb_data((i+q)%led_count, self.wheel((i+j) % 255))
                    self.strip.show()
                    time.sleep(wait_ms/1000.0)
                    for i in range(0, led_count, 3):
                        self.strip.set_led_rgb_data((i+q)%led_count, [0,0,0])
                    
    def ledIndex(self, index, R, G, B):
        """Set the color of specific LEDs based on the index."""
        if self.is_support_led_function == False:
            return
        else:
            color = (R, G, B)
            for i in range(8):
                if index & 0x01 == 1:
                    self.strip.set_led_rgb_data(i, color)
                    self.strip.show()
                index = index >> 1
            
    def ledMode(self, n):
        self.mode = n
        while True:
            if self.mode == '1':
                self.colorWipe([255, 0, 0])  # Red wipe
                self.colorWipe([0, 255, 0])  # Green wipe
                self.colorWipe([0, 0, 255])  # Blue wipe
                self.colorWipe([0, 0, 0], 10)
            elif self.mode == '2':
                self.theaterChaseRainbow()
            elif self.mode == '3':
                self.rainbow()
            elif self.mode == '4':
                self.rainbowCycle()
            else:
                self.colorWipe([0, 0, 0], 10)
                break
               
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    led = Led()       
    try:
        print ("colorWipe animation")
        led.colorWipe([255, 0, 0])  # Red wipe
        led.colorWipe([0, 255, 0])  # Green wipe
        led.colorWipe([0, 0, 255])  # Blue wipe
        print ("theaterChaseRainbow animation")
        led.theaterChaseRainbow(1)
        print ("rainbow animation")
        led.rainbow(10)
        print ("rainbowCycle animation")
        led.rainbowCycle(10)
        led.colorWipe([0, 0, 0], 10)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        led.colorWipe([0, 0, 0], 10)
    finally:
        print ("\nEnd of program")
            
        
                    




   
