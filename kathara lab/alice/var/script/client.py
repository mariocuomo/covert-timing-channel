#!/usr/bin/env python
import socket, sys
from time import perf_counter
from statistics import mode
import getopt
import os

def interpretBinary(binStr: str):
    passes = ['']
    currPass = 0

    # dividi il messaggio in parole - ognuna di 7 bit
    if ' ' in binStr:
        words = binStr.split(' ')
    else:
        words = [binStr[i:i+7] for i in range(0, len(binStr), 7)]


    # trasforma le parole in bit in parole in caratteri
    for word in words:
        if word == '':
            continue
        char = chr(int(word, 2))

        if char.isprintable():
            passes[currPass] += char
        elif char == '\000':
            passes.append('')
            currPass += 1
        else:
            passes[currPass] += '\000'

    if len(passes) == 1:
        return passes[0]

    # costruisci il messaggio
    finalStr = ''
    for i in range(max(len(p) for p in passes)):
        poss = []
        for p in passes:
            if i < len(p) and p[i] != '\000':
                poss.append(p[i])

        if len(poss) == 0:
            finalStr += '*'
        else:
            finalStr += mode(poss)

    return finalStr



"""
==========
   MAIN
==========
"""
ip = "195.11.14.2"
port = 1337


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #avvia il client e connettilo al server
        s.connect((ip, port))

        lst = []
        tipo = 'vuota'
        #rimani in attesa di dati ricevuti dal server
        data = s.recv(4096).decode()
        i=0

        #fino a che il server non chiude la comunicazione
        while data != "":
            covert_bin = ""
            _lst = []

            #fino a che il server non invia un EOF, ovvero mi fa capire che il messaggio non è terminato
            while(data.rstrip("\n")) not in ["EOF", ""]:
                
                #analizza il tempo di interarrivo dei pacchetti per capire se mi ha trasmesso un 1 o uno 0
                t0 = perf_counter()
                data = s.recv(4096).decode()
                t1 = perf_counter()
                _lst.append(t1)

                delta = round(t1 - t0, 3)

                if delta >= 0.1:
                    covert_bin += "1"
                else:
                    covert_bin += "0"

                if data == "":
                    print("Connection closed unexpectedly", file=sys.stderr)
                    break

            #stampa messaggio decifrato
            msg = interpretBinary(covert_bin)
            print(msg)

            data = s.recv(4096).decode()

