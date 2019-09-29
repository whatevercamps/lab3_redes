#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import pickle
import hashlib
import sys
import time

print("empezando server")

HEADERSIZE = 22

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(),5555))
s.listen(5)

print('{:^30}'.format('Usuarios conectados') + '{:^30}'.format('Estado'))
while True:
    i = 1
    while True:
        table = f"""{f"192.168.0.{i}":^30}"""
        print(f"""{table} {table}""", end="\r")
        i += 1
        time.sleep(1)

    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    file = open('file2.mp4', 'rb')
    msg = file.read()

    hasher = hashlib.md5()
    hasher.update(msg)

    print(f"send file with len: {len(msg)} and hash: {hasher.hexdigest()}")
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", "utf-8") + msg

    clientsocket.send(msg)
