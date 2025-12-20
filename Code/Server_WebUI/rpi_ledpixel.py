import time
from rpi_ws281x import Adafruit_NeoPixel, Color

class Freenove_RPI_WS281X:
    def __init__(self, led_count: int = 4, brightness: int = 255, sequence: str = "RGB"):
        """Initialize the LED strip with default parameters."""
        self.set_led_type(sequence)
        self.set_led_count(led_count)
        self.set_led_brightness(brightness)
        self.led_begin()
        self.set_all_led_color(0, 0, 0)

    def led_begin(self) -> None:
        """Initialize the NeoPixel strip."""
        self.strip = Adafruit_NeoPixel(
            self.get_led_count(), 18, 800000, 10, False, self.led_brightness, 0
        )
        self.led_init_state = 0 if self.strip.begin() else 1

    def check_rpi_ws281x_state(self) -> int:
        """Check the initialization state of the NeoPixel strip."""
        return self.led_init_state

    def led_close(self) -> None:
        """Turn off all LEDs."""
        self.set_all_led_rgb([0, 0, 0])

    def set_led_count(self, count: int) -> None:
        """Set the number of LEDs in the strip."""
        self.led_count = count
        self.led_color = [0, 0, 0] * self.led_count
        self.led_original_color = [0, 0, 0] * self.led_count

    def get_led_count(self) -> int:
        """Get the number of LEDs in the strip."""
        return self.led_count

    def set_led_type(self, rgb_type: str) -> int:
        """Set the RGB sequence type for the LEDs."""
        try:
            led_type = ['RGB', 'RBG', 'GRB', 'GBR', 'BRG', 'BGR']
            led_type_offset = [0x06, 0x09, 0x12, 0x21, 0x18, 0x24]
            index = led_type.index(rgb_type)
            self.led_red_offset = (led_type_offset[index] >> 4) & 0x03
            self.led_green_offset = (led_type_offset[index] >> 2) & 0x03
            self.led_blue_offset = (led_type_offset[index] >> 0) & 0x03
            return index
        except ValueError:
            self.led_red_offset = 1
            self.led_green_offset = 0
            self.led_blue_offset = 2
            return -1

    def set_led_brightness(self, brightness: int) -> None:
        """Set the brightness of the LEDs."""
        self.led_brightness = brightness
        for i in range(self.get_led_count()):
            self.set_led_rgb_data(i, self.led_original_color)

    def set_led_pixel(self, index: int, r: int, g: int, b: int) -> None:
        """Set the color of a specific LED."""
        p = [0, 0, 0]
        p[self.led_red_offset] = round(r * self.led_brightness / 255)
        p[self.led_green_offset] = round(g * self.led_brightness / 255)
        p[self.led_blue_offset] = round(b * self.led_brightness / 255)
        self.led_original_color[index * 3 + self.led_red_offset] = r
        self.led_original_color[index * 3 + self.led_green_offset] = g
        self.led_original_color[index * 3 + self.led_blue_offset] = b
        for i in range(3):
            self.led_color[index * 3 + i] = p[i]

    def set_led_color_data(self, index: int, r: int, g: int, b: int) -> None:
        """Set the color data of a specific LED."""
        self.set_led_pixel(index, r, g, b)

    def set_led_rgb_data(self, index: int, color: list) -> None:
        """Set the RGB data of a specific LED."""
        self.set_led_pixel(index, color[0], color[1], color[2])

    def set_led_color(self, index: int, r: int, g: int, b: int) -> None:
        """Set the color of a specific LED and update the display."""
        self.set_led_pixel(index, r, g, b)
        self.show()

    def set_led_rgb(self, index: int, color: list) -> None:
        """Set the RGB color of a specific LED and update the display."""
        self.set_led_rgb_data(index, color)
        self.show()

    def set_all_led_color_data(self, r: int, g: int, b: int) -> None:
        """Set the color data of all LEDs."""
        for i in range(self.get_led_count()):
            self.set_led_color_data(i, r, g, b)

    def set_all_led_rgb_data(self, color: list) -> None:
        """Set the RGB data of all LEDs."""
        for i in range(self.get_led_count()):
            self.set_led_rgb_data(i, color)

    def set_all_led_color(self, r: int, g: int, b: int) -> None:
        """Set the color of all LEDs and update the display."""
        for i in range(self.get_led_count()):
            self.set_led_color_data(i, r, g, b)
        self.show()

    def set_all_led_rgb(self, color: list) -> None:
        """Set the RGB color of all LEDs and update the display."""
        for i in range(self.get_led_count()):
            self.set_led_rgb_data(i, color)
        self.show()

    def show(self) -> None:
        """Update the LED strip with the current color data."""
        for i in range(self.get_led_count()):
            self.strip.setPixelColor(
                i, Color(self.led_color[i * 3], self.led_color[i * 3 + 1], self.led_color[i * 3 + 2])
            )
        self.strip.show()

    def wheel(self, pos: int) -> list:
        """Generate a color wheel value based on the position."""
        if pos < 85:
            return [255 - pos * 3, pos * 3, 0]
        elif pos < 170:
            pos -= 85
            return [0, 255 - pos * 3, pos * 3]
        else:
            pos -= 170
            return [pos * 3, 0, 255 - pos * 3]

    def hsv2rgb(self, h: int, s: int, v: int) -> list:
        """Convert HSV to RGB."""
        h = h % 360
        rgb_max = round(v * 2.55)
        rgb_min = round(rgb_max * (100 - s) / 100)
        i = round(h / 60)
        diff = round(h % 60)
        rgb_adj = round((rgb_max - rgb_min) * diff / 60)
        if i == 0:
            r = rgb_max
            g = rgb_min + rgb_adj
            b = rgb_min
        elif i == 1:
            r = rgb_max - rgb_adj
            g = rgb_max
            b = rgb_min
        elif i == 2:
            r = rgb_min
            g = rgb_max
            b = rgb_min + rgb_adj
        elif i == 3:
            r = rgb_min
            g = rgb_max - rgb_adj
            b = rgb_max
        elif i == 4:
            r = rgb_min + rgb_adj
            g = rgb_min
            b = rgb_max
        else:
            r = rgb_max
            g = rgb_min
            b = rgb_max - rgb_adj
        return [r, g, b]

if __name__ == '__main__':
    led = FreenoveRPIWS281X(4, 255, "RGB")
    try:
        if led.check_rpi_ws281x_state() != 0:
            led.set_led_count(4)
            led.set_all_led_color_data(255, 0, 0)
            led.show()
            time.sleep(0.5)
            led.set_all_led_rgb_data([0, 255, 0])
            led.show()
            time.sleep(0.5)
            led.set_all_led_color(0, 0, 255)
            time.sleep(0.5)
            led.set_all_led_rgb([255, 255, 255])
            time.sleep(0.5)
            led.set_all_led_rgb([0, 0, 0])
            time.sleep(0.5)

            led.set_led_brightness(20)
            while True:
                for j in range(255):
                    for i in range(led.get_led_count()):
                        led.set_led_rgb_data(i, led.wheel((round(i * 255 / led.get_led_count()) + j) % 256))
                    led.show()
                    time.sleep(0.002)
        else:
            led.led_close()
    except KeyboardInterrupt:
        led.led_close()