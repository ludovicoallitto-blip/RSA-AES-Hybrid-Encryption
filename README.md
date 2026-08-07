# RSA-AES-Hybrid-Encryption
Hybrid RSA-AES Encryption and Signature Tool

RSA-AES Hybrid Encrypted Messaging and Network Tool un applicazione in Python da riga di comando che implementa un sistema avanzato di messaggistica cifrata end-to-end con comunicazione di rete basata su socket TCP Il progetto unisce la sicurezza della crittografia asimmetrica RSA alla velocita della crittografia simmetrica AES integrando firme digitali protezione dei dati a riposo controllo di integrita della rubrica e un modulo di analisi FactorDB.

Caratteristiche Principali.
La comunicazione di rete tramite socket TCP permette di inviare e ricevere pacchetti JSON cifrati direttamente tra due terminali gestendo autonomamente la connessione Client e Server.
La cifratura ibrida efficiente utilizza AES in modalita EAX per cifrare messaggi di qualsiasi lunghezza proteggendo la chiave di sessione AES tramite cifratura RSA asimmetrica.
Le firme digitali autenticate garantiscono l integrita del messaggio e l identita del mittente tramite hashing SHA-256 e firme digitali RSA.
La protezione dati a riposo assicura che i dati privati e le chiavi locali siano cifrati con AES-256 utilizzando una password protetta da hash SHA-256 e inserita in modo sicuro tramite la libreria getpass.
L integrita della rubrica contatti e verificata automaticamente tramite hash SHA-256 salvato in un file di controllo per rilevare tempestivamente qualsiasi tentativo di manomissione.
L integrazione con FactorDB include uno strumento per interrogare il database pubblico FactorDB e testare lo stato di fattorizzazione di un modulo N.
L interfaccia CLI interattiva offre un menu a terminale strutturato per gestire chiavi contatti cifratura decifratura e test di rete.

Requisiti e Installazione.
Il progetto richiede Python 3 e le librerie crittografiche necessarie. Dopo aver clonato o scaricato la repository e possibile installare le dipendenze eseguendo da terminale pip install pycryptodome factordb-python.

Come Utilizzare il Programma.
Avvia lo script principale dal terminale digitando python3 cripto.py.
Il menu principale offre sei opzioni operative.
La prima opzione permette di criptare e inviare un messaggio sbloccando i dati privati selezionando un contatto cifrando il testo con AES e firma digitale e inviando il pacchetto via socket inserendo l indirizzo IP e la porta.
La seconda opzione consente di ricevere e decriptare un messaggio mettendo il computer in ascolto su una porta di rete per ricevere il pacchetto decodificare la chiave AES verificare il tag di integrita e autenticare la firma.
La terza opzione genera nuove chiavi p e q creando numeri primi forti e calcolando i parametri RSA con salvataggio sicuro protetto da password.
La quarta opzione interroga FactorDB per verificare se un modulo N e fattorizzato o vulnerabile.
La quinta opzione aggiunge un contatto in rubrica inserendo nome e modulo N pubblico aggiornando l hash di sicurezza.
La sesta opzione termina l esecuzione del programma.

Informazioni di Sicurezza.
Le chiavi RSA utilizzano numeri primi forti generati tramite getStrongPrime a 1024 bit per singolo fattore con modulo N totale di 2048 bit.
La cifratura simmetrica sfrutta lo standard AES in modalita EAX assicurando riservatezza e autenticazione dei dati.
L utilizzo di getpass previene la visualizzazione accidentale delle password sullo schermo durante la digitazione.

Autore.
Creato da Ludovico come progetto di approfondimento sulla crittografia moderna e la programmazione di rete in Python.
