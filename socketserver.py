import socket
import sys

#  创建socket对象
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
print("socket server host name: %s" % host)
port = 9999
# 绑定端口号
serversocket.bind((host, port))
# 设置最大连接数，超过后排队
serversocket.listen(5)

while True:
    clientsocket, addr = serversocket.accept()
    print("链接地址：%s" % str(addr))
    msg = "欢迎访问lzh服务器！"
    clientsocket.send(msg.encode('utf-8'))
    reply = clientsocket.recv(1024)
    print("reply:%s" % reply.decode('utf-8'))
    clientsocket.close()
    break