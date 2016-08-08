#!/usr/bin/env python
import socket
import argparse


def echo_client(host, port):
    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM)
    server_addr = (host, port)

    sock.connect(server_addr)

    message = "Test Message"
    sock.sendall(message)
    data = sock.recv(1024)
    print("Received: %s" % data)
    sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", action="store",
                        type=str, dest="host",
                        default="localhost")
    parser.add_argument("--port", action="store",
                        type=int, dest="port",
                        default=8080)

    args = parser.parse_args()
    echo_client(args.host, args.port)
