import time
from Motor import *
import RPi.GPIO as GPIO
from servo import *
from PCA9685 import PCA9685

class Ultrasonic:
    def __init__(self):
        GPIO.setwarnings(False)
        self.trigger_pin = 27
        self.echo_pin = 22
        self.MAX_DISTANCE = 300  # maximum measuring distance in cm
        self.timeOut = self.MAX_DISTANCE * 60
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
       
        # Initialize motor and servo
        self.PWM = Motor()
        self.pwm_S = Servo()
        self.distance_threshold = 30  # Distance in cm to trigger obstacle avoidance

    def pulseIn(self, pin, level, timeOut):  # obtain pulse time of a pin under timeOut
        t0 = time.time()
        while GPIO.input(pin) != level:
            if (time.time() - t0) > timeOut * 0.000001:
                return 0
        t0 = time.time()
        while GPIO.input(pin) == level:
            if (time.time() - t0) > timeOut * 0.000001:
                return 0
        pulseTime = (time.time() - t0) * 1000000
        return pulseTime

    def get_distance(self):  # get the measurement results of ultrasonic module, with unit: cm
        GPIO.output(self.trigger_pin, GPIO.HIGH)  # make trigger_pin output 10us HIGH level
        time.sleep(0.00001)  # 10us
        GPIO.output(self.trigger_pin, GPIO.LOW)  # make trigger_pin output LOW level
        pingTime = self.pulseIn(self.echo_pin, GPIO.HIGH, self.timeOut)  # read pulse time of echo_pin
        distance = pingTime * 340.0 / 2.0 / 10000.0  # calculate distance in cm
        return int(distance)

    def move_forward(self):
        self.PWM.setMotorModel(500, 500, 500, 500)

    def stop(self):
        self.PWM.setMotorModel(0, 0, 0, 0)

    def turn_left(self):
        self.PWM.setMotorModel(-3000, -3000, 3000, 3000)  # Adjust speed as necessary

    def turn_right(self):
        self.PWM.setMotorModel(3000, 3000, -3000, -3000)  # Adjust speed as necessary

    def reverse(self):
        self.PWM.setMotorModel(-1000, -1000, -1000, -1000)
        time.sleep(0.5)
        self.stop()

    def avoid_obstacle(self):
        # Scan distances to the left, middle, and right
        self.pwm_S.setServoPwm("0", 90)  # Center position
        time.sleep(0.2)
        middle_distance = self.get_distance()

        if middle_distance < self.distance_threshold:  # Obstacle detected ahead
            self.pwm_S.setServoPwm("0", 30)  # Turn to left
            time.sleep(0.2)
            left_distance = self.get_distance()

            self.pwm_S.setServoPwm("0", 150)  # Turn to right
            time.sleep(0.2)
            right_distance = self.get_distance()

            # Decide which direction to turn based on obstacle detection
            if left_distance > self.distance_threshold:
                self.turn_left()
                time.sleep(0.5)  # Adjust as necessary
            elif right_distance > self.distance_threshold:
                self.turn_right()
                time.sleep(0.5)  # Adjust as necessary
            else:
                # If both sides are blocked, reverse and stop
                self.reverse()
                time.sleep(0.5)

        else:
            # Move forward if no obstacles ahead
            self.move_forward()

    def run(self):
        while True:
            self.avoid_obstacle()  # Continuously check for obstacles

# Main program logic
if __name__ == '__main__':
    print('Program is starting...')
    ultrasonic = Ultrasonic()
    try:
        ultrasonic.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, stop the car
        ultrasonic.stop()
        GPIO.cleanup()
        print("Program stopped by user.")
