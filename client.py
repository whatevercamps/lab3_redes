#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 20:44:16 2019

@author: whatevercamps
"""

import socket
import pickle
import hashlib
print("empezando client")

HEADERSIZE = 22

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 5555))

while True:
    full_msg = b''
    new_msg = True

    while True:
        msg = s.recv(1048576)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
            print(f"new msg len: {msglen}") 

        full_msg += msg

        print(f"actual msg len: {len(full_msg)}")

        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg recvd")
            hasher = hashlib.md5()
            hasher.update(full_msg[HEADERSIZE:])

            print(f"recvd file with len: {len(full_msg[HEADERSIZE:])} and hash: {hasher.hexdigest()}")
            new_msg = True
            full_msg = b''