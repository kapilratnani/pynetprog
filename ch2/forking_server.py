import SocketServer
import os
import argparse


class ForkingServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass


class ServerRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        response = "Process %s: %s" % (os.getpid(), data)
        self.request.send(response)
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', action="store",
                        dest="port", type=int, default=8080)
    parser.add_argument('--host', action="store",
                        dest="host", type=str,
                        default="localhost")
    args = parser.parse_args()
    port = args.port
    host = args.host

    server = ForkingServer((host, port), ServerRequestHandler)
    print("main server process:%s" % os.getpid())
    server.serve_forever()
