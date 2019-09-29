#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 20:44:16 2019

@author: whatevercamps
"""
import sys
import socket
import pickle
import hashlib
import time 
print("empezando client")

HEADERSIZE = 22
conectado = False

while not conectado: 
    try:
        ip = input('ingrese ip del servidor:')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        print(f"Intentado conectarse al servidor {ip}", end="\r")
        s.connect((ip, 5555))
        s.settimeout(300)
        conectado = True
    except:
        print(f"Error:", sys.exc_info()[0])

print(f"Conectado correctamente al servidor {ip}")

print("""
+------------------------------+
|           Opciones           |
+-----+------------------------+
| Num |         accion         |
+-----+------------------------+
|  1  |     Enviar "Listo"     |
+-----+------------------------+
|  2  | Enviar "No me esperes" |
+-----+------------------------+
|  3  |   terminar coneccion   |
+-----+------------------------+
""")
opcion = ""
opcion = input("Ingrese una opcion: ")
listo = False

if opcion == "1":
    s.sendall(bytes("LISTO",'utf-8'))
    print("pos listo we")
    listo = True
    

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