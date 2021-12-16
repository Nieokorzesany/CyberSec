from SocketServer import BaseRequestHandler, TCPServer
from socket import socket, AF_INET, SOCK_STREAM
import sys
class SockHandler(BaseRequestHandler):
def handle(self):
  self.data = self.request.recv(1024)
  print("Passing data from: "+ str(self.client_address[0]) + " to " + external_LAN_IP)
  print(self.data)
socket = socket(AF_INET, SOCK_STREAM)
try:
  socket.connect((external_LAN_IP, external_LAN_PORT))
  socket.sendall(self.data)
  while 1:
    command = socket.recv(1024)
    if not command:
      break
    self.request.sendall(command)
finally:
  socket.close()
if __name__ == '__main__':
  private_LAN_IP, private_LAN_PORT, external_LAN_IP, external_LAN_PORT= sys.argv[1:]
  myserver = TCPServer((private_LAN_IP, private_LAN_PORT), SockHandler)
  myserver.serve_forever()
