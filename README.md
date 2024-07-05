# Covert Timing Channel (CTC)

This repository contains a simple Covert Timing Channel Proof Of Concept - implemented in python3. <br>
Furthermore, there is a lab [kathará](https://www.kathara.org) - a tool for emulating computer networks - to verify its functioning. <br>
The project supported my thesis work for the Master's degree in Computer Engineering at the [Universita Degli Studi Roma Tre](https://www.uniroma3.it/).

### Covert Channel
A Covert Channel is any communication system that allows the transfer of information between two or more entities by exploiting characteristics of the system that are not used for this purpose. Given the nature of the channel itself, they are difficult to identify. In this scenario, Covert Channels (CC) are widely used both to send legitimate traffic that needs to be kept hidden and to share malicious information by attackers too.

CCs can be divided into two macro categories.

- _Covert Storage Channel_ <br>
These kind of channels are created by inserting information into storage which will subsequently be read by the receiver. <br>
An example of use is encoding information in TCP segment fields.
- _Covert Timing Channel_ <br>
These kind of channels are created by modulating information over time. <br>
An example of use is the variation of the interarrival time of the packets to encode the message to be sent.

An interesting read about it. <br>
> J. Millen, "20 years of covert channel modeling and analysis," Proceedings of the 1999 IEEE Symposium on Security and Privacy (Cat. No.99CB36344), Oakland, CA, USA, 1999, pp. 113-114, doi: 10.1109/SECPRI.1999.766906.


### Covert Timing Channel (CTC)
A simple implementation of Covert Timing Channel can be as follows. <br>
Imagine a scenario in which there are two interlocutors, Alice and Bob, who establish a TCP connection. <br>
Alice wants to send a message in CTC to Bob: to do so, she encodes the message in interarrival times between packets relating to a covering communication.

Let the covered message be the string "*addio*". <br>
Let the covering message be the string "*come stai?*". <br>
Alice divides the blanket message into multiple packets that she sends at different time intervals. <br>
Bob, by receiving the packets and analyzing the interarrival times, is able to reconstruct the covered message. <br>
This means that a malicious user, Cindy, present on the channel can only read the covert message and not become aware of a hidden communication.

<div align="center">
<img src="https://github.com/mariocuomo/covert-timing-channel/blob/main/imgs/ctc-schema.png">
</div>

The first operation that Alice performs is the 7-bit encoding of each character of the covered message. <br>
<div align="center">
<img src="https://github.com/mariocuomo/covert-timing-channel/blob/main/imgs/7bitascii.png">
</div>

At this point the covered message is represented by a string of bits - 1100001(a) 1100100(d) 1100100(d) 1101001(i) 1101111(o) - which Alice will have to transmit on the channel by encoding it in the interarrival times. <br>
The two interlocutors agree on the convention to use: if Alice wants to transmit a '0' she will wait _x_ time before sending the next packet; if she wants to send a '1' she will instead wait a time _y_. The contents of the packets sent are the characters of the covert message so as not to arouse suspicion. <br>

<div align="center">
<img src="https://github.com/mariocuomo/covert-timing-channel/blob/main/imgs/covertmessage.png">
</div>

### Kathará
In the folder [kathara lab](https://github.com/mariocuomo/covert-timing-channel/tree/main/kathara%20lab) a kathara lab composed of 3 machines on the address space 195.11.14.0/24 is created as illustrated in the figure.

<div align="center">
<img src="https://github.com/mariocuomo/covert-timing-channel/blob/main/imgs/lan-schema.png">
</div>

Alice is a server that listens for a connection. <br>
Bob is a client connecting on port 1337 of the server. <br>
Once a connection has been received, the server sends some messages in CTC to the client which reconstructs it. <br>
The python3 scripts are available in the ```*/var/script/```folder.

**SERVER OPERATION PSEUDOCODE**
``` Python
WHILE socketopen:
  #server waiting for a connection, and accept it when it arrives
  server.listen(...)

  while stillSomethingToSay:
     #generate a message
     msg = generaMessaggio()
     
     #encode the message for the CTC and send it to the client
     codificaEMandaMessaggio(msg)
```


**CLIENT OPERATION PSEUDOCODE**
``` Python
WHILE socketopen:
  #send connection request to the server and wait for acceptance
  client.connect(...)

  while serverHasNotCloseConnection:
     #retrieves packets related to the message
     pacchetti = recuperaPacchetti()
     
     #construct binary string considering the packet interarrival time
     stringa_binaria = analizzaInterarrivoDeiPacchetti(pacchetti)
     
     #retrieves the server message
     messaggio = conversioneInStringa(stringa_binaria) 
```

My thesis work focuses on the creation of Artificial Intelligence models (ML and DL) for the identification of CTCs.<br>
[Detecting CTC Attack in IoMT Communications using Deep Learning Approach](https://www.astesj.com/v08/i02/p15/)
