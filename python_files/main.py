#!/usr/bin/python

from RoboThreadPool import RoboThreadPool
import RPi.GPIO as GPIO
import Robot
import socket
import select
import time

# For encoders
RIGHT_WHEEL_PIN = 12
LEFT_WHEEL_PIN  = 13

EOL = b'\n' # Used to close client socket file descriptor
response = b''
robot = Robot.Robot()

# Instantiate a thread pool with 4 worker threads
pool = RoboThreadPool(4)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8080))
serversocket.listen(10)
serversocket.setblocking(0)
#serversocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN | select.EPOLLET)

GPIO.setmode(GPIO.BCM)

GPIO.setup(RIGHT_WHEEL_PIN, GPIO.IN, GPIO.PUD_UP) # right wheel
GPIO.setup(LEFT_WHEEL_PIN, GPIO.IN, GPIO.PUD_UP) # left wheel

time.sleep(2)

# optimized for 5 inches; moving more or less than that will
# result in a larger margin of error
def goDistanceLeft(distance):
    distSoFar = 0
    initPosition = GPIO.input(LEFT_WHEEL_PIN)
    while (distSoFar < distance):
        while(GPIO.input(LEFT_WHEEL_PIN) == 1):
            pass
        distSoFar += 0.35  # distance (in inches) with each slot rotation of encoder
        while(GPIO.input(LEFT_WHEEL_PIN) == 0):
            pass
    return 1

def goDistanceRight(distance):
    distSoFar = 0
    initPosition = GPIO.input(RIGHT_WHEEL_PIN)
    while (distSoFar < distance):
        while(GPIO.input(RIGHT_WHEEL_PIN) == initPosition):
            pass
        distSoFar += 0.35 # distance (in inches) with each slot rotation of encoder
        while(GPIO.input(RIGHT_WHEEL_PIN) != initPosition):
            pass
    return 1


def receive_web_request(req):
    if req == 'Move Right':
        robot.right(127)
    elif req == 'Move Left':
        robot.left(127)
    elif req == 'Move Up':
        robot.forward(127)
    elif req == 'Move Down':
        robot.backward(127)
    elif req == 'Space':
        robot.stop()

def receive_sensor_request(sensor_name,req):
    if (sensor_name == 'sensor_one' or sensor_name == 'sensor_two' or sensor_name == 'sensor_three') and req == 'MoveBotBack':
        robot.backward(127)
        #goDistanceRight(5.00)
        time.sleep(0.5)
        robot.stop()
    if (sensor_name == 'sensor_four' or sensor_name == 'sensor_five') and req == 'MoveBotForward':
        robot.forward(127)
        #goDistanceLeft(5.00)
        time.sleep(0.5)
        robot.stop()

def receive_pi_cam_request(move_cmd,midpoint):
    mid = float(midpoint) * 2.0

    if move_cmd == b'TurnLeft':
        robot.left(127)
        time.sleep(0.2 * mid)
        robot.stop()
    elif move_cmd == b'TurnRight':
        robot.right(127)
        time.sleep(0.2 * mid)
        robot.stop()
    elif move_cmd == b'Robot Ready':
        robot.right(127)
        time.sleep(0.4)
        robot.left(127)
        time.sleep(0.4)
        robot.stop()
    elif move_cmd == b'RoboInFront':
        robot.stop()

def main():
    try:
        connections = {}; requests = {}; responses = {}; devices = {}
        while True:
            events = epoll.poll(1)
            for fileno, event in events:
                if fileno == serversocket.fileno():
                    try:
                        while True:
                            connection, address = serversocket.accept() # Accept Connection

                            connection.setblocking(0) # Set Client fd into non-blocking
                            epoll.register(connection.fileno(), select.EPOLLIN | select.EPOLLET)
                            connections[connection.fileno()] = connection
                            requests[connection.fileno()] = b''
                            responses[connection.fileno()] = response
                            #devices[connection.fileno()] = connections[connection.fileno()].recv(16) # Receive initial response
                    except socket.error:
                        pass
                elif event & select.EPOLLIN:
                    try:
                        while True:
                            requests[fileno] = connections[fileno].recv(1024)
                    except socket.error:
                        pass

                    req = requests[fileno]
                    loaded_data = req.split(",")
                    if EOL in loaded_data[0]:
                        epoll.modify(fileno, select.EPOLLOUT)
                    else:
                        if loaded_data[0] == 'WebApp':
                            pool.add_task(receive_web_request, loaded_data[1])
                        elif loaded_data[0] == 'Sensor':
                            pool.add_task(receive_sensor_request,loaded_data[1],loaded_data[2])
                        elif loaded_data[0] == 'PiCam':
                            pool.add_task(receive_pi_cam_request, loaded_data[1],loaded_data[2])
                        pool.wait_completion()
                elif event & select.EPOLLOUT:
                    try:
                        while len(responses[fileno]) > 0:
                            byteswritten = connections[fileno].send(responses[fileno])
                            responses[fileno] = responses[fileno][byteswritten:]
                    except socket.error:
                        pass
                    if len(responses[fileno]) == 0:
                        epoll.modify(fileno, 0)
                        connections[fileno].shutdown(socket.SHUT_RDWR)
                elif event & select.EPOLLHUP:
                    epoll.unregister(fileno)
                    connections[fileno].close()
                    del connections[fileno]
    finally:
        epoll.unregister(serversocket.fileno())
        epoll.close()
        serversocket.close()

main()
