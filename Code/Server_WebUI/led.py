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
        # Get the Connect version from the parameter file
        self.connect_version = self.param.get_connect_version()
        # Get the Raspberry Pi version from the parameter file
        self.pi_version = self.param.get_raspberry_pi_version()

        # Set up the LED strip based on PCB and Raspberry Pi versions
        if self.connect_version == 1 and self.pi_version == 1:
            self.strip = Freenove_RPI_WS281X(8, 255, 'RGB')
            self.is_support_led_function = True

        elif self.connect_version == 2 and (self.pi_version == 1 or self.pi_version == 2):
            self.strip = Freenove_SPI_LedPixel(8, 255, 'GRB')
            self.is_support_led_function = True

        elif self.connect_version == 1 and self.pi_version == 2:
            # Print an error message and disable LED function if unsupported combination
            print("Connect Version 1.0 is not supported on Raspberry PI 5.")
            self.is_support_led_function = False
                    
        self.start = time.time()
        self.next = 0
        self.color_wheel_value = 100
        self.color_chase_rainbow_index = 0
        self.color_wipe_index = 0
        self.rainbowbreathing_brightness = 0

    def colorBlink(self, state=1, wait_ms=300):
        """Wipe color across display a pixel at a time."""
        if self.is_support_led_function == False:
            return
        else:
            if state == 1:
                color = [[255, 0, 0],[0, 0, 0],[0, 255, 0],[0, 0, 0],[0, 0, 255],[0, 0, 0]]
                self.next = time.time()
                if (self.next - self.start) > wait_ms / 1000.0:
                    self.start = self.next
                    for i in range(self.strip.get_led_count()):
                        self.strip.set_led_rgb_data(i, color[self.color_wipe_index%4])
                        self.strip.show()
                    self.color_wipe_index += 1
            else:
                self.strip.set_all_led_color(0, 0, 0)
                self.strip.show()

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
        
    def rainbowbreathing(self, wait_ms=10):
        """Draw rainbowbreathing that fades across all pixels at once."""
        if self.is_support_led_function == False:
            return
        else:
            self.next = time.time()
            if (self.next - self.start) > wait_ms / 1000.0:
                self.start = self.next
                color1 = self.wheel((self.color_wheel_value%255) & 255)
                if (self.rainbowbreathing_brightness%200) > 100:
                    brightness = 200 - self.rainbowbreathing_brightness
                else:
                    brightness = self.rainbowbreathing_brightness
                color2 = [int(color1[0] * brightness / 100), int(color1[1] * brightness / 100), int(color1[2] * brightness / 100)]
                for i in range(self.strip.get_led_count()):
                    self.strip.set_led_rgb_data(i, color2)
                self.strip.show()

                self.rainbowbreathing_brightness += 1  
                if self.rainbowbreathing_brightness >= 200:
                    self.rainbowbreathing_brightness = 0
                    self.color_wheel_value += 32
                    if self.color_wheel_value >= 256:
                        self.color_wheel_value = 0



    def rainbowCycle(self, wait_ms = 20):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        if not self.is_support_led_function:
            return
        else:
            self.next = time.time()
            if (self.next - self.start > wait_ms / 1000.0):
                self.start = self.next
                for i in range(self.strip.get_led_count()):
                    self.strip.set_led_rgb_data(i, self.wheel((int(i * 256 / self.strip.get_led_count()) + self.color_wheel_value) & 255))
                self.strip.show()
                self.color_wheel_value += 1
                if self.color_wheel_value >= 256:
                    self.color_wheel_value = 0

    def following(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        if self.is_support_led_function == False:
            return
        else:
            self.next = time.time()
            if (self.next - self.start > wait_ms / 1000.0):
                self.start = self.next
                for i in range(self.strip.get_led_count()):
                    self.strip.set_led_rgb_data(i, [0, 0, 0])
                self.strip.set_led_rgb_data(self.color_chase_rainbow_index, self.wheel((self.color_wheel_value) & 255))
                self.strip.show()
                self.color_chase_rainbow_index += 1
                if self.color_chase_rainbow_index >= self.strip.get_led_count():
                    self.color_chase_rainbow_index = 0
                self.color_wheel_value += 5
                if self.color_wheel_value >= 256:
                    self.color_wheel_value = 0
               
                    
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
               
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    led = Led()       
    try:
        print ("colorBlink animation")
        start = time.time()
        while (time.time() - start) < 5:
            led.colorBlink(1)
        
        print ("following animation")
        start = time.time()
        while (time.time() - start) < 5:
            led.following(50)
        
        print ("rainbowbreathing animation")
        start = time.time()
        while (time.time() - start) < 5:
            led.rainbowbreathing(10)

        print ("rainbowCycle animation")
        start = time.time()
        while (time.time() - start) < 10:
            led.rainbowCycle(20)

        led.colorBlink(0)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        led.colorBlink(0)
    finally:
        print ("\nEnd of program")
            
        
                    




   
