#!/usr/bin/python

import socket, select, Robot

robot = Robot.Robot()

response = b''

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8080))
serversocket.listen(10)
serversocket.setblocking(0)
serversocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)

try:
  connections = {}; requests = {}; responses = {}
  while True:
    events = epoll.poll(1)
    for fileno, event in events:
      if fileno == serversocket.fileno():
        connection, address = serversocket.accept() # Accept Connection

        connection.setblocking(0) # Set Client fd into non-blocking
        epoll.register(connection.fileno(), select.EPOLLIN)
        connections[connection.fileno()] = connection
        requests[connection.fileno()] = b''
        responses[connection.fileno()] = response
      elif event & select.EPOLLIN:
        requests[fileno] += connections[fileno].recv(1024)
        req = requests[fileno]
        if req == b'Move Right':
          print("Moving Robot Right")
	  robot.right(127)
        elif req == b'Move Left':
          print("Moving Robot Left")
          robot.left(127)
	elif req == b'Move Up':
          print("Moving Robot Up")
          robot.forward(127)
	elif req == b'Move Down':
          print("Moving Robot Down")
          robot.backward(127)
	elif req == b'Space':
	  print("Stoping Robot")
	  robot.stop()
	epoll.modify(fileno, select.EPOLLOUT)
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
