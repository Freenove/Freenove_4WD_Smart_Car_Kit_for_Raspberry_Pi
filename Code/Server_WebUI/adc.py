import smbus  # Import the smbus module for I2C communication
import time  # Import the time module for sleep functionality
from parameter import ParameterManager  # Import the ParameterManager class from the parameter module

class ADC:
    def __init__(self):
        """Initialize the ADC class."""
        self.I2C_ADDRESS = 0x48                                               # Set the I2C address of the ADC
        self.ADS7830_COMMAND = 0x84                                           # Set the command byte for ADS7830
        self.parameter_manager = ParameterManager()                           # Create an instance of ParameterManager
        self.pcb_version = self.parameter_manager.get_pcb_version()           # Get the PCB version
        self.adc_voltage_coefficient = 3.3 if self.pcb_version == 1 else 5.2  # Set the ADC voltage coefficient based on the PCB version
        self.i2c_bus = smbus.SMBus(1)                                         # Initialize the I2C bus

    def _read_stable_byte(self) -> int:
        """Read a stable byte from the ADC."""
        while True:
            value1 = self.i2c_bus.read_byte(self.I2C_ADDRESS)                 # Read the first byte from the ADC
            value2 = self.i2c_bus.read_byte(self.I2C_ADDRESS)                 # Read the second byte from the ADC
            if value1 == value2:
                return value1                                                 # Return the value if both reads are the same

    def read_adc(self, channel: int) -> float:
        """Read the ADC value for the specified channel using ADS7830."""
        command_set = self.ADS7830_COMMAND | ((((channel << 2) | (channel >> 1)) & 0x07) << 4)  # Calculate the command set for the specified channel
        self.i2c_bus.write_byte(self.I2C_ADDRESS, command_set)                # Write the command set to the ADC
        value = self._read_stable_byte()                                      # Read a stable byte from the ADC
        voltage = value / 255.0 * self.adc_voltage_coefficient                # Convert the ADC value to voltage
        return round(voltage, 2)                                              # Return the voltage rounded to 2 decimal places

    def scan_i2c_bus(self) -> None:
        """Scan the I2C bus for connected devices."""
        print("Scanning I2C bus...")                                          # Print a message indicating the start of I2C bus scanning
        for device in range(128):                                             # Iterate over possible I2C addresses (0 to 127)
            try:
                self.i2c_bus.read_byte_data(device, 0)                        # Try to read data from the current device address
                print(f"Device found at address: 0x{device:02X}")            # Print the address of the found device
            except OSError:
                pass                                                          # Ignore any OSError exceptions

    def close_i2c(self) -> None:
        """Close the I2C bus."""
        self.i2c_bus.close()                                                  # Close the I2C bus

if __name__ == '__main__':
    print('Program is starting ... ')                                        # Print a message indicating the start of the program
    adc = ADC()                                                             # Create an instance of the ADC class
    try:
        while True:
            left_idr = adc.read_adc(0)                                        # Read the left photoresistor value
            right_idr = adc.read_adc(1)                                       # Read the right photoresistor value
            power = adc.read_adc(2) * (3 if adc.pcb_version == 1 else 2)      # Calculate the power value based on the PCB version
            print(f"Left IDR: {left_idr}V, Right IDR: {right_idr}V, Power: {power}V")  # Print the values of left IDR, right IDR, and power
            time.sleep(1)                                                     # Wait for 1 second
    except KeyboardInterrupt:
        adc.close_i2c()                                                       # Close the I2C bus when the program is interrupted