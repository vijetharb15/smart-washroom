import RPi.GPIO as GPIO
import time
import atexit
import signal
import sys

# GPIO Pin Configuration
MQ135_DO_PIN = 24
PIR_PIN = 25
TRIG = 26
ECHO = 27

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Setup GPIO pins
GPIO.setup(MQ135_DO_PIN, GPIO.IN)
GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# Ensure trigger pin is low initially
GPIO.output(TRIG, False)
time.sleep(2)

def cleanup_gpio():
    print("Cleaning up GPIO pins...")
    GPIO.cleanup()

atexit.register(cleanup_gpio)

def signal_handler(sig, frame):
    print("Interrupted, exiting...")
    cleanup_gpio()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def detect_gas():
    try:
        return GPIO.input(MQ135_DO_PIN)
    except RuntimeError as e:
        print(f"Gas Sensor Error: {e}")
        return 1

def detect_motion():
    try:
        return GPIO.input(PIR_PIN)
    except RuntimeError as e:
        print(f"PIR Sensor Error: {e}")
        return 0

def get_soap_level():
    try:
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        start_time = time.time()
        stop_time = time.time()
        timeout = start_time + 0.1

        while GPIO.input(ECHO) == 0:
            start_time = time.time()
            if start_time > timeout:
                return -1

        while GPIO.input(ECHO) == 1:
            stop_time = time.time()
            if stop_time > timeout:
                return -1

        distance = (stop_time - start_time) * 34300 / 2
        return round(distance, 2)
    except RuntimeError as e:
        print(f"Ultrasonic Sensor Error: {e}")
        return -1

def read_sensors():
    return {
        "odorLevel": 100 if detect_gas() else 20,
        "soapLevel": get_soap_level(),
        "motionDetected": detect_motion()
    }

if __name__ == "__main__":
    print("Starting sensor readings...")
    try:
        while True:
            print(read_sensors())
            time.sleep(2)
    except KeyboardInterrupt:
        print("Stopped by user.")
        cleanup_gpio()