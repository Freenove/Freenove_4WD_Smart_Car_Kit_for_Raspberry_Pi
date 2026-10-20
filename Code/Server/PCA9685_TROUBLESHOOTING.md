# Troubleshooting: motor test reports an I2C error

If `sudo python test.py Motor` fails with `OSError: [Errno 5] Input/output error` while initializing `PCA9685(0x40)`, the Raspberry Pi has not successfully communicated with the PWM controller. This happens before the motor test commands any wheel movement.

## Check the controller connection first

1. Check the kit's power and battery setup against the Freenove assembly tutorial. Confirm the board is switched on and its connectors are seated correctly.
2. Confirm I2C is enabled in Raspberry Pi configuration.
3. Check that the expected bus is present: `ls /dev/i2c-*`.
4. Scan bus 1: `sudo i2cdetect -y 1`. The default PCA9685 address used by `Code/Server/pca9685.py` is `0x40`.
5. If `0x40` does not appear, investigate the controller's power, connection, and I2C bus before changing motor speeds or PWM code. If it does appear but the test still fails, record the exact traceback and contact Freenove support.

A blank I2C scan does **not** establish a motor software bug. It means the expected I2C device did not acknowledge the scan; the specific hardware cause still needs diagnosis.

## Why this check matters

`Code/Server/pca9685.py` writes to the PCA9685 MODE1 register during initialization. An I2C failure at that point prevents `test.py Motor` from reaching the commands that drive the motors.

Related report: [issue #77](https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/issues/77).

This troubleshooting guidance is based on code inspection and the public issue report. It has **not** been verified on physical Freenove hardware.
