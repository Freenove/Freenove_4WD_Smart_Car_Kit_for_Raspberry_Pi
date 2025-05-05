# SPDX-FileCopyrightText: 2023 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_platformdetect.revcodes`
================================================================================

Class to help with Raspberry Pi Rev Codes

* Author(s): Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Software and Dependencies:**

* Linux and Python 3.7 or Higher

Data values from https://github.com/raspberrypi/documentation/blob/develop/
documentation/asciidoc/computers/raspberry-pi/revision-codes.adoc#new-style-revision-codes

"""

NEW_OVERVOLTAGE = (
    "Overvoltage allowed",
    "Overvoltage disallowed",
)

NEW_OTP_PROGRAM = (
    "OTP programming is allowed",
    "OTP programming is disallowed",
)

NEW_OTP_READ = (
    "OTP reading is allowed",
    "OTP reading is disallowed",
)

NEW_WARRANTY_BIT = (
    "Warranty is intact",
    "Warranty has been voided by overclocking",
)

NEW_REV_STYLE = (
    "Old-style revision",
    "New-style revision",
)

NEW_MEMORY_SIZE = (
    "256MB",
    "512MB",
    "1GB",
    "2GB",
    "4GB",
    "8GB",
)

NEW_MANUFACTURER = (
    "Sony UK",
    "Egoman",
    "Embest",
    "Sony Japan",
    "Embest",
    "Stadium",
)

NEW_PROCESSOR = (
    "BCM2835",
    "BCM2836",
    "BCM2837",
    "BCM2711",
    "BCM2712",
)

PI_TYPE = {
    0x00: "A",
    0x01: "B",
    0x02: "A+",
    0x03: "B+",
    0x04: "2B",
    0x05: "Alpha (early prototype)",
    0x06: "CM1",
    0x08: "3B",
    0x09: "Zero",
    0x0A: "CM3",
    0x0B: "Custom",
    0x0C: "Zero W",
    0x0D: "3B+",
    0x0E: "3A+",
    0x0F: "Internal use only",
    0x10: "CM3+",
    0x11: "4B",
    0x12: "Zero 2 W",
    0x13: "400",
    0x14: "CM4",
    0x15: "CM4S",
    0x17: "5",
    0x18: "CM5",
    0x19: "500",
    0x1A: "CM5 Lite",
}

OLD_MANUFACTURER = (
    "Sony UK",
    "Egoman",
    "Embest",
    "Qisda",
)

OLD_MEMORY_SIZE = ("256MB", "512MB", "256MB/512MB")

NEW_REV_STRUCTURE = {
    "overvoltage": (31, 1, NEW_OVERVOLTAGE),
    "otp_program": (30, 1, NEW_OTP_PROGRAM),
    "otp_read": (29, 1, NEW_OTP_READ),
    "warranty": (25, 1, NEW_WARRANTY_BIT),
    "rev_style": (23, 1, NEW_REV_STYLE),
    "memory_size": (20, 3, NEW_MEMORY_SIZE),
    "manufacturer": (16, 4, NEW_MANUFACTURER),
    "processor": (12, 4, NEW_PROCESSOR),
    "type": (4, 8, PI_TYPE),
    "revision": (0, 4, int),
}

OLD_REV_STRUCTURE = {
    "type": (0, PI_TYPE),
    "revision": (1, float),
    "memory_size": (2, OLD_MEMORY_SIZE),
    "manufacturer": (3, OLD_MANUFACTURER),
}

OLD_REV_EXTRA_PROPS = {
    "warranty": (24, 1, NEW_WARRANTY_BIT),
}

OLD_REV_LUT = {
    0x02: (1, 1.0, 0, 1),
    0x03: (1, 1.0, 0, 1),
    0x04: (1, 2.0, 0, 0),
    0x05: (1, 2.0, 0, 3),
    0x06: (1, 2.0, 0, 1),
    0x07: (0, 2.0, 0, 1),
    0x08: (0, 2.0, 0, 0),
    0x09: (0, 2.0, 0, 3),
    0x0D: (1, 2.0, 1, 1),
    0x0E: (1, 2.0, 1, 0),
    0x0F: (1, 2.0, 1, 1),
    0x10: (3, 1.2, 1, 0),
    0x11: (6, 1.0, 1, 0),
    0x12: (2, 1.1, 0, 0),
    0x13: (3, 1.2, 1, 2),
    0x14: (6, 1.0, 1, 2),
    0x15: (2, 1.1, 2, 2),
}


class PiDecoder:
    """Raspberry Pi Revision Code Decoder"""

    def __init__(self, rev_code):
        try:
            self.rev_code = int(rev_code, 16) & 0xFFFFFFFF
        except ValueError:
            print("Invalid revision code. It should be a hexadecimal value.")

    def is_valid_code(self):
        """Quickly check the validity of a code"""
        if self.is_new_format():
            for code_format in NEW_REV_STRUCTURE.values():
                lower_bit, bit_size, values = code_format
                prop_value = (self.rev_code >> lower_bit) & ((1 << bit_size) - 1)
                if not self._valid_value(prop_value, values):
                    return False
        else:
            if (
                self.rev_code & 0xFFFF
            ) not in OLD_REV_LUT.keys():  # pylint: disable=consider-iterating-dictionary
                return False
            for code_format in OLD_REV_STRUCTURE.values():
                index, values = code_format
                code_format = OLD_REV_LUT[self.rev_code & 0xFFFF]
                if index >= len(code_format):
                    return False
                if not self._valid_value(code_format[index], values):
                    return False
        return True

    def _get_rev_prop_value(self, name, structure=None, raw=False):
        if structure is None:
            structure = NEW_REV_STRUCTURE
        if name not in structure.keys():
            raise ValueError(f"Unknown property {name}")
        lower_bit, bit_size, values = structure[name]
        prop_value = self._get_bits_value(lower_bit, bit_size)
        if not self._valid_value(prop_value, values):
            raise ValueError(f"Invalid value {prop_value} for property {name}")
        if raw:
            return prop_value
        return self._format_value(prop_value, values)

    def _get_bits_value(self, lower_bit, bit_size):
        return (self.rev_code >> lower_bit) & ((1 << bit_size) - 1)

    def _get_old_rev_prop_value(self, name, raw=False):
        if (
            name
            not in OLD_REV_STRUCTURE.keys()  # pylint: disable=consider-iterating-dictionary
        ):
            raise ValueError(f"Unknown property {name}")
        index, values = OLD_REV_STRUCTURE[name]
        data = OLD_REV_LUT[self.rev_code & 0xFFFF]
        if index >= len(data):
            raise IndexError(f"Index {index} out of range for property {name}")
        if not self._valid_value(data[index], values):
            raise ValueError(f"Invalid value {data[index]} for property {name}")
        if raw:
            return data[index]
        return self._format_value(data[index], values)

    @staticmethod
    def _format_value(value, valid_values):
        if valid_values is float or valid_values is int:
            return valid_values(value)
        return valid_values[value]

    @staticmethod
    def _valid_value(value, valid_values):
        if valid_values is float or valid_values is int:
            return isinstance(value, valid_values)
        if isinstance(valid_values, (tuple, list)) and 0 <= value < len(valid_values):
            return True
        if isinstance(valid_values, dict) and value in valid_values.keys():
            return True
        return False

    def _get_property(self, name, raw=False):
        if name not in NEW_REV_STRUCTURE:
            raise ValueError(f"Unknown property {name}")
        if self.is_new_format():
            return self._get_rev_prop_value(name, raw=raw)
        if name in OLD_REV_EXTRA_PROPS:
            return self._get_rev_prop_value(
                name, structure=OLD_REV_EXTRA_PROPS, raw=raw
            )
        return self._get_old_rev_prop_value(name, raw=raw)

    def is_new_format(self):
        """Check if the code is in the new format"""
        return self._get_rev_prop_value("rev_style", raw=True) == 1

    @property
    def overvoltage(self):
        """Overvoltage allowed/disallowed"""
        return self._get_property("overvoltage")

    @property
    def warranty_bit(self):
        """Warranty bit"""
        return self._get_property("warranty")

    @property
    def otp_program(self):
        """OTP programming allowed/disallowed"""
        return self._get_property("otp_program")

    @property
    def otp_read(self):
        """OTP reading allowed/disallowed"""
        return self._get_property("otp_read")

    @property
    def rev_style(self):
        """Revision Code style"""
        # Force new style for Rev Style
        return self._get_rev_prop_value("rev_style")

    @property
    def memory_size(self):
        """Memory size"""
        return self._get_property("memory_size")

    @property
    def manufacturer(self):
        """Manufacturer"""
        return self._get_property("manufacturer")

    @property
    def processor(self):
        """Processor"""
        return self._get_property("processor")

    @property
    def type(self):
        """Specific Model"""
        return self._get_property("type")

    @property
    def type_raw(self):
        """Raw Value of Specific Model"""
        return self._get_property("type", raw=True)

    @property
    def revision(self):
        """Revision Number"""
        return self._get_property("revision")
