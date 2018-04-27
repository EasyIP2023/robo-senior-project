require 'socket'

$sock = TCPSocket.open Socket.gethostname, 8080
