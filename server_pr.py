import socket, threading
import pickle
import hashlib
import sys
import time
HEADERSIZE = 22
usrs = []

class Client(threading.Thread):
    def __init__(self, clientAddress, clientsocket, msg):
        threading.Thread.__init__(self)
        self.msg = msg
        self.csocket = clientsocket
        print ("Nuevo cliente creado: ", clientAddress[0])
    def run(self):
        self.csocket.send(self.msg)

class Admin(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global usrs
        print ("""
+-------------------------------------+
|               Opciones              |
+-----+-------------------------------+
| Num |             Accion            |
+-----+-------------------------------+
|  1  | Mostrar servidores conectados |
+-----+-------------------------------+
|  2  | Enviar archivo                |
+-----+-------------------------------+
|  9  | Terminar                      |
+-----+-------------------------------+
        """)
        nivel = 0
        while True:
            opcion = input("Ingrese una opcion: ")
            if nivel == 0:
                if opcion == "1":
                    if len(usrs) == 0:
                        print("NO HAY CLIENTES CONECTADOS")
                    else:
                        print(f"{'IP':^20}" + f"{'PUERTO':^20}" + f"{'ESTADO':^20}")
                        for a in range(len(usrs)):
                            print(f"{usrs[a][0][0]:^20}" + f"{usrs[a][0][1]:^20}" + f"{'ESTADO':^20}")

                elif opcion == "2":
                    nivel = 1
                    print("""
+---------------------------+
|   Seleccione el archivo   |
+-----+-----------+---------+
| Num |   Nombre  | Tamanio |
+-----+-----------+---------+
|  1  | file1.mp4 |  272MB  |
+-----+-----------+---------+
|  2  | file2.mp4 |  107MB  |
+-----+-----------+---------+
|  9  |       regresar      |
+-----+---------------------+
                    """)
            elif nivel == 1:
                if opcion != "1" and opcion != "2" and opcion != "9":
                    print("ingrese una opcion valida")
                elif opcion == "9":
                    nivel = 0
                    print("""
+-------------------------------------+
|               Opciones              |
+-----+-------------------------------+
| Num |             Accion            |
+-----+-------------------------------+
|  1  | Mostrar servidores conectados |
+-----+-------------------------------+
|  2  | Enviar archivo                |
+-----+-------------------------------+
|  9  | Terminar                      |
+-----+-------------------------------+
                    """)
                else:
                    nivel = 0
                    file = open(f'file{opcion}.mp4', 'rb')
                    msg = file.read()
                    hasher = hashlib.md5()
                    hasher.update(msg)

                    print(f"sending file with len: {len(msg)} and hash: {hasher.hexdigest()}")
                    msg = bytes(f"{len(msg):<{HEADERSIZE}}", "utf-8") + msg

                    for a in range(len(usrs)):
                        clientThread = Client(usrs[a][0], usrs[a][1], msg)
                        clientThread.start()
            time.sleep(0.5)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(),5555))
newthread = Admin()
newthread.start()
while True:
    s.listen(25)
    clientsocket, address = s.accept()
    usrs.append([address, clientsocket])


