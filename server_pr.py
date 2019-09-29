import socket, threading
import pickle
import hashlib
import sys
import time

HEADERSIZE = 22
usrs = []

class Client(threading.Thread):
    def __init__(self, clientAddress, clientsocket, pos):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.index = pos
        print ("Nuevo cliente vinculado: ", clientAddress[0])
    def run(self):
        while True:
            msg = self.csocket.recv(1024)
            msg_dcd = msg.decode("utf-8")
            if "LISTO" in msg_dcd:
                usrs[self.index][2] = True
    def enviar(self, msg, hasher):
        print("llega al menos")
        print(f"enviando archivo con tamanio: {len(msg)} y hash: {hasher.hexdigest()}")
        msg_pr = bytes(f"{len(msg):<{HEADERSIZE}}", "utf-8") + msg
        self.csocket.send(msg_pr)

        

class Admin(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print ("""
+-------------------------------------+
|               Opciones              |
+-----+-------------------------------+
| Num |             Accion            |
+-----+-------------------------------+
|  1  | Mostrar clientes conectados   |
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
                        for a in usrs:
                            estado = "ESPERANDO"
                            if a[2] == True:
                                estado = "LISTO"
                            print(f"{a[0][0]:^20}" + f"{a[0][1]:^20}" + f"{estado:^20}")

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
|  1  | Mostrar clientes conectados   |
+-----+-------------------------------+
|  2  | Enviar archivo                |
+-----+-------------------------------+
|  9  | Terminar                      |
+-----+-------------------------------+
                    """)
                else:
                    listos = 0
                    for i in usrs:
                        if i[2]:
                            listos += 1
                    if listos >= 0:
                        file = open(f'file{opcion}.mp4', 'rb')
                        msg_enviar = file.read()
                        hasher = hashlib.md5()
                        hasher.update(msg_enviar)
                        print("estamos listos")
                        for i in usrs:
                            if i[2]:
                                i[3].enviar(msg_enviar, hasher)
                    else:
                        print("Los clientes aun no estan listos")
                        nivel = 0
                        print("""
+-------------------------------------+
|               Opciones              |
+-----+-------------------------------+
| Num |             Accion            |
+-----+-------------------------------+
|  1  | Mostrar clientes conectados   |
+-----+-------------------------------+
|  2  | Enviar archivo                |
+-----+-------------------------------+
|  9  | Terminar                      |
+-----+-------------------------------+
                    """)
            time.sleep(0.5)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(),5555))
newthread = Admin()
newthread.start()
posNewClient = 0
while True:
    s.listen(25)
    clientsocket, address = s.accept()
    clientThread = Client(address, clientsocket, posNewClient)
    clientThread.start()
    usrs.append([address, clientsocket, False, clientThread])
    posNewClient += 1

