#!/usr/bin/python

import RPi.GPIO as GPIO
import Robot
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1',8080))
sock.send(b"Sensor") # Send initial connection device name
time.sleep(1)

GPIO.setmode(GPIO.BCM)

# First element in array is the echo pin and the second is trig pin
echo_trig_pins = {}
echo_trig_pins['sensor_one']   = [22, 23]
echo_trig_pins['sensor_two']   = [17, 24]
echo_trig_pins['sensor_three'] = [27, 25]
echo_trig_pins['sensor_four']  = [18,  5]
echo_trig_pins['sensor_five']  = [4,  19]

# GPIO Pin setup for sensor one
GPIO.setup(echo_trig_pins['sensor_one'][1],GPIO.OUT)
GPIO.setup(echo_trig_pins['sensor_one'][0], GPIO.IN)

# GPIO Pin setup for sensor two
GPIO.setup(echo_trig_pins['sensor_two'][1],GPIO.OUT)
GPIO.setup(echo_trig_pins['sensor_two'][0], GPIO.IN)

# GPIO Pin setup for sensor three
GPIO.setup(echo_trig_pins['sensor_three'][1],GPIO.OUT)
GPIO.setup(echo_trig_pins['sensor_three'][0], GPIO.IN)

# GPIO Pin setup for sensor four
GPIO.setup(echo_trig_pins['sensor_four'][1],GPIO.OUT)
GPIO.setup(echo_trig_pins['sensor_four'][0], GPIO.IN)

# GPIO Pin setup for sensor three
GPIO.setup(echo_trig_pins['sensor_five'][1],GPIO.OUT)
GPIO.setup(echo_trig_pins['sensor_five'][0], GPIO.IN)

time.sleep(2) # needed to make sure sonar settles to one value

def get_sensor_data(sensor_name):
    global echo_trig_pins, sock
    pulse_end,pulse_start = 0,0

    GPIO.output(echo_trig_pins[sensor_name][1], True)
    time.sleep(0.00001)
    GPIO.output(echo_trig_pins[sensor_name][1], False)

    while GPIO.input(echo_trig_pins[sensor_name][0]) == 0:
        pulse_start = time.time()

    while GPIO.input(echo_trig_pins[sensor_name][0]) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    if distance < 10.00000 and (sensor_name == 'sensor_one' or sensor_name == 'sensor_two' or sensor_name == 'sensor_three'):
        data = sensor_name + ",MoveBotBack"
        sock.send(data)
        time.sleep(1)
    if distance < 10.00000 and (sensor_name == 'sensor_four' or sensor_name == 'sensor_five'):
        data = sensor_name + ",MoveBotForward"
        sock.send(data)
        time.sleep(1)

while True:
    get_sensor_data('sensor_one')
    get_sensor_data('sensor_two')
    get_sensor_data('sensor_three')
    get_sensor_data('sensor_four')
    get_sensor_data('sensor_five')

GPIO.cleanup()
sock.send(b"\n") # Send end character
sock.close()
