# Covert Timing Channel (CTC)

Questo repository mostra come sia possibile implementare un semplice Covert Timing Channel in python3. <br>
Inoltre, è presente un lab [kathará](https://www.kathara.org) - un tool per l'emulazione di reti di calcolatori - per verificarne il funzionamento. <br>
Il progetto è di supporto al mio lavoro di tesi per la laurea Magistrale in Ingegneria Informatica all'[Universita Degli Studi Roma Tre](https://www.uniroma3.it/).

### Covert Channel
Un Canale Coperto è un qualsiasi sistema di comunicazione che permette il trasferimento di informazione tra due o più entità sfruttando caratteristiche del sistema che non sono utilizzate a tale scopo. Data la natura del canale stesso, essi risultano essere difficilmente identificabili. In questo scenario i Covert Channel (CC) sono largamente utilizzati sia per inviare traffico legittimo che si vuole tenere nascosto, sia per condividere informazioni malevoli da parte di attaccanti.

I CC possono essere divisi in due macrocategorie.

- _Covert Storage Channel_ <br>
Questi canali sono creati scrivendo informazioni su uno storage che successivamente sarà letto dal ricevente. <br>
Un esempio di utilizzo è la codifica delle informazioni nei campi dei segmenti TCP.
- _Covert Timing Channel_ <br>
Questi canali sono creati modulano le informazioni nel tempo. <br>
Un esempio di utilizzo è la variazione del tempo di interarrivo dei pacchetti per codificare il messaggio da inviare.

Una lettura interessante a riguardo. <br>
> J. Millen, "20 years of covert channel modeling and analysis," Proceedings of the 1999 IEEE Symposium on Security and Privacy (Cat. No.99CB36344), Oakland, CA, USA, 1999, pp. 113-114, doi: 10.1109/SECPRI.1999.766906.


### Covert Timing Channel (CTC)
Una semplice implementazione di Covert Timing Channel può essere la seguente. <br>
Si immagini uno scenario in cui sono presenti due interlocutori, Alice e Bob, che instaurano una connessione TCP. <br>
Alice vuole inviare un messaggio in CTC a Bob: per farlo, codifica il messaggio in dei tempi di interarrivo tra pacchetti relativi a una comunicazione coprente.

Sia il messaggio coperto la stringa "*addio*". <br>
Sia il messaggio coprente la stringa "*come stai?*". <br>
Alice divide il messaggio coprente in più pacchetti che invia a intervalli di tempo diversi. <br>
Bob ricevendo i pacchetti e analizzando i tempi di interarrivo riesce a ricostruire il messaggio coperto. <br>
Questo fa sì che un utente malevolo, Cindy, presente sul canale possa leggere solo il messaggio coprente e non venire a conoscenza di una comunicazione nascosta.  

<div align="center">
<img src="https://github.com/mariocuomo/covert-timing-channel/blob/main/imgs/ctc-schema.png">
</div>

La prima operazione che Alice effettua è la codifica in 7 bit di ogni carattere del messaggio coperto. <br>
<div align="center">
<img src="https://github.com/mariocuomo/covert-timing-channel/blob/main/imgs/7bitascii.png">
</div>

A questo punto il messaggio coperto è rappresentato da una stringa di bit - 1100001(a) 1100100(d) 1100100(d) 1101001(i) 1101111(o) - e che Alice dovrà trasmettere sul canale codificandola nei tempi di interarrivo. <br>
I due interlocutori sono d'accordo sulla convenzione da utilizzare: se Alice vuole trasmettere uno '0' attenderà un tempo _x_ prima di inviare il successivo pacchetto; se vuole trasmettere un '1' invece attenderà un tempo _y_. Il contenuto dei pacchetti inviati sono i caratteri del messaggio coprente per non destare sospetti. <br>

<div align="center">
<img src="https://github.com/mariocuomo/covert-timing-channel/blob/main/imgs/covertmessage.png">
</div>

### Kathará
Nella cartella [kathara lab](https://github.com/mariocuomo/covert-timing-channel/tree/main/kathara%20lab) è realizzato un lab kathara composto da 3 macchine sullo spazio di indirizzamento 195.11.14.0/24 come illustrato in figura.

<div align="center">
<img src="https://github.com/mariocuomo/covert-timing-channel/blob/main/imgs/lan-schema.png">
</div>

Alice è un server che si mette in ascolto in attesa di una connessione. <br>
Bob è un client che si connette sulla porta 1337 del server. <br>
Ricevuta una connessione, il server invia in CTC alcuni messaggi al client che ricostruisce. <br>
Gli script python3 sono presenti nelle cartelle ```*/var/script/```

**PSEUDOCODICE FUNZIONAMENTO SERVER**
``` Python
WHILE socketaperta:
  #metti in ascolto il server sulla in attesa di una connessione, e accettala all'arrivo
  server.listen(...)

  while ancoraQualcosaDaDire:
     #genera un messaggio
     msg = generaMessaggio()
     
     #codifica il messaggio per il CTC e mandalo al client
     codificaEMandaMessaggio(msg)
```


**PSEUDOCODICE FUNZIONAMENTO CLIENT**
``` Python
WHILE socketaperta:
  #invia richiesta di connessione al server e rimani in attesa dell'accettazione
  client.connect(...)

  while serverNonHaChiusoConnessione:
     #recupera i pacchetti relativi al messaggio
     pacchetti = recuperaPacchetti()
     
     #costruisci stringa binaria considerando il tempo di interarrivo dei pacchetti
     stringa_binaria = analizzaInterarrivoDeiPacchetti(pacchetti)
     
     #recupera il messaggio del server
     messaggio = conversioneInStringa(stringa_binaria) 
```

Il mio lavoro di tesi si concentra sulla realizzazione di modelli di Intelligenza Artificiale (ML e DL) per l'identificazione dei CTC.
