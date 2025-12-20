# Import the LineSensor class from gpiozero for reading infrared sensors
from gpiozero import LineSensor
import time

# Define the Infrared class to manage infrared sensors
class Infrared:
    def __init__(self):
        # Define the GPIO pins for each infrared sensor
        self.IR_PINS = {
            1: 14,
            2: 15,
            3: 23
        }
        # Initialize LineSensor objects for each infrared sensor
        self.sensors = {channel: LineSensor(pin) for channel, pin in self.IR_PINS.items()}

    def read_one_infrared(self, channel: int) -> int:
        """Read the value of a single infrared sensor."""
        if channel in self.sensors:
            return 1 if self.sensors[channel].value else 0
        else:
            raise ValueError(f"Invalid channel: {channel}. Valid channels are {list(self.IR_PINS.keys())}.")

    def read_all_infrared(self) -> int:
        """Combine the values of all three infrared sensors into a single integer."""
        return (self.read_one_infrared(1) << 2) | (self.read_one_infrared(2) << 1) | self.read_one_infrared(3)

    def close(self) -> None:
        """Close each LineSensor object to release GPIO resources."""
        for sensor in self.sensors.values():
            sensor.close()

# Main entry point for testing the Infrared class
if __name__ == '__main__':
    # Create an Infrared object
    infrared = Infrared()
    try:
        # Continuously read and print the combined value of all infrared sensors
        while True:
            infrared_value = infrared.read_all_infrared()
            print(f"Infrared value: {infrared_value}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        # Close the Infrared object and print a message when interrupted
        infrared.close()
        print("\nEnd of program")