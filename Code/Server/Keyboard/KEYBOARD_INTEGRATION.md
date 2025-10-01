# Keyboard Integration for Freenove 4WD Smart Car

This project extends the original [Freenove 4WD Smart Car Kit](https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi) with Bluetooth keyboard control capabilities.

## Project Goal
Enable real-time car control using Apple Bluetooth keyboard arrow keys:
- ⬆️ **UP Arrow** → Move Forward
- ⬇️ **DOWN Arrow** → Move Backward  
- ⬅️ **LEFT Arrow** → Turn Left
- ➡️ **RIGHT Arrow** → Turn Right
- **No Key Pressed** → Stop Car

## Hardware Requirements
- Freenove 4WD Smart Car Kit
- Raspberry Pi 5 (or compatible model with built-in Bluetooth)
- Apple Bluetooth Keyboard (Magic Keyboard tested)
- SSH access to Raspberry Pi

## Setup Instructions

### 1. Bluetooth Keyboard Pairing
Connect your Apple keyboard to the Raspberry Pi via SSH:

```bash
sudo bluetoothctl
```

Inside bluetoothctl:
```bash
power on
agent on
default-agent
discoverable on
pairable on
scan on
```

Put your Apple keyboard in pairing mode, then:
```bash
pair XX:XX:XX:XX:XX:XX  # Replace with your keyboard's MAC address
connect XX:XX:XX:XX:XX:XX
trust XX:XX:XX:XX:XX:XX
exit
```

### 2. Install Dependencies
```bash
sudo apt update
sudo apt install python3-evdev
```

### 3. Test Keyboard Input
```bash
cd Code/Server
sudo python3 keyboard_test.py
```

## 🔧 Custom Files Added

### `Code/Server/keyboard_test.py`
- Tests Bluetooth keyboard connectivity
- Captures and displays real-time key presses
- Validates arrow key detection for car control
- Provides feedback through SSH terminal

## Usage

### Testing Keyboard Connection
```bash
sudo python3 keyboard_test.py
```
Press arrow keys on your Bluetooth keyboard to verify connectivity.

### Car Control (Coming Soon)
Integration with existing Freenove motor control functions for real-time car control.

## Technical Details

### Input Capture Method
- Uses Linux `evdev` (event device) subsystem
- Reads keyboard events directly from hardware level
- Bypasses terminal input limitations in SSH environments
- Provides real-time key detection suitable for vehicle control

### Communication Chain
```
Apple Keyboard → Bluetooth → Pi Hardware → Linux Kernel → 
evdev → Python Script → SSH Terminal → User Feedback
```

## Next Steps
1. Integrate keyboard input with existing car motor functions
2. Implement real-time car control mapping
3. Add safety features (emergency stop, speed control)
4. Create enhanced keyboard mapping for additional features

## Credits
- **Original Hardware & Software:** [Freenove 4WD Smart Car Kit](https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi)
- **Keyboard Integration & Bluetooth Setup:** Custom implementation
- **Documentation:** Project-specific additions

