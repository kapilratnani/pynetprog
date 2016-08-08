#!/usr/bin/env python
import select
import socket
import argparse
import os
import cPickle
import struct
import signal
import sys


def receive(client_soc):
    pass


def send(client_soc, data):
    pass


class ChatServer(object):

    def __init__(self, host, port, backlog=5):
        self.clients = 0
        self.client_map = {}
        self.outputs = []
        self.server = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(backlog)
        print("Server Listening at (%s,%s)" % (host, port))
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        print("Shutdown")
        for o in self.outputs:
            o.close()
        self.server.close()

    def get_client_name(self, client_soc):
        info = self.client_map[client_soc]
        return '@'.join(info)

    def run(self):
        inputs = [self.server, sys.stdin]
        self.outputs = []

        running = True

        while running:
            readable, writable, _ = select.select(
                inputs, self.outputs, []
            )

            for sock in readable:
                if sock == self.server:
                    # this means someone connected
                    client, addr = self.server.accept()
                    print("New connection from '%s:%s'" % addr)
                    # read name
                    cname = receive(client).split(":")[1]
                    self.clients += 1
                    # send address to client
                    send(client, "ADDR:%s:%s" % addr)
                    self.client_map[client] = (cname, addr)

                    # notify all other clients of new connection
                    msg = "(New client %s)" % self.get_client_name(client)
                    for o in self.outputs:
                        send(o, msg)
                    self.outputs.append(client)
                elif sock == sys.stdin:
                    inp = sys.stdin.readline()
                    if inp == "q" or inp == "Q":
                        running = False
                else:
