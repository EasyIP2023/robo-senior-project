require 'socket'

$sock = TCPSocket.open Socket.gethostname, 8080
$sock.send("WebApp",0) # Send the type of device
