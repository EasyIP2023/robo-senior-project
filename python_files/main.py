#!/usr/bin/python

from RoboThreadPool import RoboThreadPool
#import RPi.GPIO as GPIO
#import Robot
import socket
import subprocess
import select
import time

# For encoders
RIGHT_WHEEL_PIN = 12
LEFT_WHEEL_PIN  = 13

EOL = b'\n' # Used to close client socket file descriptor
response = b''
#robot = Robot.Robot()
#cmdline = ['vlc','--demux','h264','-']
#player = subprocess.Popen(cmdline,stdin=subprocess.PIPE)
# Instantiate a thread pool with 4 worker threads
pool = RoboThreadPool(4)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8080))
serversocket.listen(10)
serversocket.setblocking(0)
serversocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)

# GPIO.setmode(GPIO.BCM)
#
# GPIO.setup(RIGHT_WHEEL_PIN, GPIO.IN, GPIO.PUD_UP) # right wheel
# GPIO.setup(LEFT_WHEEL_PIN, GPIO.IN, GPIO.PUD_UP) # left wheel
#
# time.sleep(2)
#
# # optimized for 5 inches; moving more or less than that will
# # result in a larger margin of error
# def goDistanceLeft(distance):
#     distSoFar = 0
#     initPosition = GPIO.input(LEFT_WHEEL_PIN)
#     while (distSoFar < distance):
#         while(GPIO.input(LEFT_WHEEL_PIN) == 1):
#             pass
#         distSoFar += 0.35  # distance (in inches) with each slot rotation of encoder
#         while(GPIO.input(LEFT_WHEEL_PIN) == 0):
#             pass
#     return 1
#
# def goDistanceRight(distance):
#     distSoFar = 0
#     initPosition = GPIO.input(RIGHT_WHEEL_PIN)
#     while (distSoFar < distance):
#         while(GPIO.input(RIGHT_WHEEL_PIN) == initPosition):
#             pass
#         distSoFar += 0.35 # distance (in inches) with each slot rotation of encoder
#         while(GPIO.input(RIGHT_WHEEL_PIN) != initPosition):
#             pass
#     return 1


def receive_web_request(req):
    # if req == b'Move Right':
    #     robot.right(127)
    # elif req == b'Move Left':
    #     robot.left(127)
    # elif req == b'Move Up':
    #     robot.forward(127)
    # elif req == b'Move Down':
    #     robot.backward(127)
    # elif req == b'Space':
    #     robot.stop()
    print("web request")

def receive_sensor_request(sensor_name,req):
    # if (sensor_name == 'sensor_one' or sensor_name == 'sensor_two' or sensor_name == 'sensor_three') and req == 'MoveBotBack':
    #     robot.backward(127)
    #     goDistanceRight(5.00)
    #     robot.stop()
    # if (sensor_name == 'sensor_four' or sensor_name == 'sensor_five') and req == 'MoveBotForward':
    #     robot.forward(127)
    #     goDistanceLeft(5.00)
    #     robot.stop()
    print("in sensor code")

def receive_pi_cam_request(req):
    print(req)

def main():
    try:
        connections = {}; requests = {}; responses = {}; devices = {}
        while True:
            events = epoll.poll(1)
            for fileno, event in events:
                if fileno == serversocket.fileno():
                    connection, address = serversocket.accept() # Accept Connection, Make file-like object out of it

                    connection.setblocking(0) # Set Client fd into non-blocking
                    epoll.register(connection.fileno(), select.EPOLLIN)
                    connections[connection.fileno()] = connection
                    requests[connection.fileno()] = b''
                    responses[connection.fileno()] = response
                    devices[connection.fileno()] = connections[connection.fileno()].recv(16) # Receive initial response
                elif event & select.EPOLLIN:
                    requests[fileno] = connections[fileno].recv(4096)
                    req = requests[fileno]
                    if EOL in req:
                        epoll.modify(fileno, select.EPOLLOUT)
                    else:
                        if devices[fileno] == b'WebApp':
                            pool.add_task(receive_web_request, req)
                        elif devices[fileno] == b'Sensor':
                            loaded_data = req.split(",")
                            pool.add_task(receive_sensor_request,loaded_data[0],loaded_data[1])
                        elif devices[fileno] == b'PiCam':
                            pool.add_task(receive_pi_cam_request, req)
                        pool.wait_completion()
                elif event & select.EPOLLOUT:
                    byteswritten = connections[fileno].send(responses[fileno])
                    responses[fileno] = responses[fileno][byteswritten:]
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
        #player.terminate()
        #GPIO.cleanup()
main()
