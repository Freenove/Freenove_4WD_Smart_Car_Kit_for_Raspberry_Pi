#!/usr/bin/env python3
"""
Keyboard Input Test Script for Raspberry Pi
Tests if Apple Bluetooth keyboard input is being captured
Press arrow keys to test, ESC to exit
"""

import evdev
import sys
import time

def find_keyboard_device():
    """Find the connected Apple keyboard device"""
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    
    print("Available input devices:")
    for device in devices:
        print(f"  {device.path}: {device.name}")
        
    # Look for keyboard devices (they typically have key capabilities)
    keyboard_devices = []
    for device in devices:
        capabilities = device.capabilities()
        # Check if device has key event capability
        if evdev.ecodes.EV_KEY in capabilities:
            keyboard_devices.append(device)
    
    if not keyboard_devices:
        print("No keyboard devices found!")
        return None
        
    # If multiple keyboards, try to find the Apple one
    for device in keyboard_devices:
        if 'keyboard' in device.name.lower() or 'magic' in device.name.lower():
            print(f"\nUsing device: {device.name}")
            return device
    
    # If no Apple keyboard found, use the first keyboard device
    print(f"\nUsing first keyboard device: {keyboard_devices[0].name}")
    return keyboard_devices[0]

def test_keyboard_input():
    """Test keyboard input and print feedback"""
    
    try:
        keyboard = find_keyboard_device()
        if not keyboard:
            return
            
        print("\n" + "="*50)
        print("KEYBOARD INPUT TEST")
        print("="*50)
        print("Press arrow keys to test keyboard input")
        print("Press ESC key to exit")
        print("Any key presses will be shown below:")
        print("-" * 30)
        
        # Key code mappings for arrow keys
        key_map = {
            evdev.ecodes.KEY_UP: "UP ARROW",
            evdev.ecodes.KEY_DOWN: "DOWN ARROW", 
            evdev.ecodes.KEY_LEFT: "LEFT ARROW",
            evdev.ecodes.KEY_RIGHT: "RIGHT ARROW",
            evdev.ecodes.KEY_ESC: "ESCAPE",
            evdev.ecodes.KEY_SPACE: "SPACE",
            evdev.ecodes.KEY_ENTER: "ENTER"
        }
        
        # Listen for keyboard events
        for event in keyboard.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                key_event = evdev.categorize(event)
                
                # Only show key press events (not release)
                if key_event.keystate == evdev.KeyEvent.key_down:
                    key_name = key_map.get(event.code, f"KEY_CODE_{event.code}")
                    print(f"Key pressed: {key_name}")
                    
                    # Exit on ESC key
                    if event.code == evdev.ecodes.KEY_ESC:
                        print("ESC pressed - exiting...")
                        break
                        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by Ctrl+C")
    except PermissionError:
        print("\nPermission denied! Try running with sudo:")
        print("sudo python3 keyboard_test.py")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure your keyboard is connected via Bluetooth")
        print("2. Try running with sudo permissions")
        print("3. Install evdev if missing: pip3 install evdev")

if __name__ == "__main__":
    print("Starting keyboard input test...")
    test_keyboard_input()
    print("\nKeyboard test completed!")
