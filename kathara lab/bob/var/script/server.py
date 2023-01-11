import socket, sys
from time import sleep
from random import randint
import subprocess
import time
import os
import signal
import sys


messaggi=['Regina Black', 'Tina Whitehead', ' sarah74@example.org', ' sara56@example.net', '4930300091182163', '4712917422022444487']
i=0

def covertSendMsg(c: socket.socket, msg: str, coverFile):
    try:
        covertMsg = coverFile.readline().strip('\n') + ' '
    except EOFError:
        print("Ran out of text in cover file")


    #trasforma in stringa binaria il messaggio
    #la funzione ord() ritorna il carattere unicode
    binaryStr = ''.join(format(ord(l), '07b') for l in msg) + '0000000'

    runs = randint(1,3)
    overtDex = 0

    #invia sul canale il messaggio coprente
    #il messaggio segreto inviato è binaryStr nascosto nei tempi di attesa tra un pacchetto e l'altro
    for i in range(runs):
        msgDex = 0
        for bit in binaryStr:
            if overtDex+1 >= len(covertMsg):
                covertMsg = coverFile.readline().strip('\n') + ' '    
                overtDex = 0

            c.send(covertMsg[overtDex].encode())
            if bit == '1':
                sleep(0.1)
            else:
                sleep(0.025)
            overtDex += 1

    #manda un EOF per far comprendere al client che il messaggio è terminato
    c.send("EOF".encode())
    

"""
==========
   MAIN
==========
"""
port = 1337
coverFile = "const.txt"
msg = None


#tipi = ['carta_credito' , 'email', 'nome_cognome', 'vuota']
tipi = ['vuota' ]

try:
    with open(coverFile, "r") as f:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #avvia il server e mettilo in attesa di una richiesta di connessione            
            s.bind(("", port))
            s.listen(0)

            while True:
                try:
                    #accetta la connessione del client
                    print("Awaiting Connections...")
                    c, addr = s.accept()
                    print(f"Connected to host {addr[0]}:{addr[1]}")

                    with c:
                        for tipo in tipi:
                            for i in range(6):
                                #genera un messaggio
                                msg = messaggi[i]
                                print('> '+msg)
                                #mandalo in covert timing channel
                                covertSendMsg(c, msg, f)
                except KeyboardInterrupt:
                    print("\rGoodbye")
                    break
                except (BrokenPipeError, TimeoutError, socket.timeout, ConnectionResetError) as e:
                    print(f'\rLost connection to client ({e})')
except OSError as e:
    if e.errno == 98:
        print(f"Port in use, trying again ({e})")
    else:
        raise e
