import socket
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999
s.connect((host, port))
msg = s.recv(1024)
# s.close()
print(msg.decode('utf-8'))

s.send("你好，我是lzh".encode('utf-8'))
s.close()

