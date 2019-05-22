"""
 http server v2.0
 *IO并发处理
 *基本的request解析
 *使用类的封装
"""
from select import *
from socket import *


# 将具体http ser功能封装
class HTTPServer:
    def __init__(self, server_addr, static_dir):
        self.server_addr = server_addr
        self.static_dir = static_dir
        self.rlist = self.wlist = self.xlist = []
        self.creat_socket()
        self.bind()

    def creat_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def bind(self):
        self.sockfd.bind(self.server_addr)
        self.ip = self.server_addr[0]
        self.port = self.server_addr[1]

    # 启动服务
    def serve_forever(self):
        self.sockfd.listen(5)
        print("Listen the port %d" % self.port)
        self.rlist.append(self.sockfd)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r is self.sockfd:
                    c, addr = r.accept()
                    print("Connect from:", addr)
                    self.rlist.append(c)
                else:
                    # 处理浏览器请求
                    self.handle(r)
    #处理客户端请求
    def handle(self, connfd):
        # 接受http请求
        request = connfd.recv(4096)
        # 防止浏览断开
        if not request:
            self.rlist.remove(connfd)
            connfd.close()
            return
        request_line = request.splitlines()[0]
        info = request_line.decode().split(" ")[1]
        print(connfd.getpeername(),":",info)

        #info  分为访问网页和其他
        if info == "/" or info[-5:] == '.html':
            self.get_html(connfd,info)

        else:
            self.get_data(connfd,)

        self.rlist.remove(connfd)
        connfd.close()

    # 处理网页
    def get_html(self,connfd,info):
        if info == "/":
            filename = self.static_dir + '/index.html'

        else:
            filename = self.static_dir + info
        try:
            fd = open(filename)
        except Exception:
            responseHeaders = "HTTP/1.1 404 NOT Found\r\n"
            # responseHeaders += "Content-Type: Text/html\r\n"
            responseHeaders += '\r\n'
            responseHeadersBody = "<h1 align=center>Sorry,Not Found the page </h1>"

        else:
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            responseHeaders += "Content-Type: Text/html\r\n"
            responseHeaders += '\r\n'
            responseHeadersBody = fd.read()


        response = responseHeaders +responseHeadersBody
        connfd.send(response.encode())


    #其他情况
    def get_data(self,connfd):
        responseHeaders = "HTTP/1.1 200 OK\r\n"
        responseHeaders += "Content-Type: Text/html\r\n"
        responseHeaders += '\r\n'
        responseHeadersBody = "<h1 align=center>Waitting httpserver3.0</h1>"
        response = responseHeaders + responseHeadersBody
        connfd.send(response.encode())


# 如何使用HTTPServer类
if __name__ == '__main__':
    # 用户自己决定：地址和内容
    server_addr = ('0.0.0.0', 8080)
    static_dir = "./static"  # 网页存放位置

    httpd = HTTPServer(server_addr, static_dir)  # 生成实例对象
    httpd.serve_forever()  # 启动服务
