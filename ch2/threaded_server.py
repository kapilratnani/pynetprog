#!/usr/bin/env python

import SocketServer
import os
import argparse
import threading


class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class ServerRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        response = "Thread %s: %s" % (threading.current_thread(), data)
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

    server = ThreadedServer((host, port), ServerRequestHandler)
    print("main server process:%s" % os.getpid())
    server.serve_forever()
