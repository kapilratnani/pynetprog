#!/usr/bin/env python
import socket
import argparse

data_payload = 2048
backlog = 5


def echo_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_addr = (host, port)

    sock.bind(server_addr)

    sock.listen(backlog)

    while True:
        client, addr = sock.accept()
        print("connection from %s:%s" % addr)
        data = client.recv(data_payload)
        print("Data received:%s" % data)
        if data:
            client.send(data)
        client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', action="store",
                        dest="port", type=int,
                        default=8080)
    parser.add_argument('--host', action='store',
                        dest="host", type=str,
                        default="localhost")
    args = parser.parse_args()
    port = args.port
    host = args.host
    echo_server(host, port)
