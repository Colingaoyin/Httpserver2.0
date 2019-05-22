"""

"""
from socket import *
s = socket()

ADDR = ("127.0.0.1",8080)
s.connect(ADDR)
while True:
    data = input("向服务端发送消息：")
    if not data:
        break
    s.send(data.encode())
    data = s.recv(1024)
    print(data.decode())



s.close()