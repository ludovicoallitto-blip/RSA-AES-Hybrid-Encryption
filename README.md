# RSA-AES-Hybrid-Encryption
Hybrid RSA-AES Encryption and Signature Tool

Un sistema di cifratura ibrida sicuro sviluppato in Python, che unisce la velocità della crittografia simmetrica (AES-256) alla sicurezza della crittografia asimmetrica (RSA), integrando firme digitali e un modulo di analisi per testare la robustezza dei moduli N tramite FactorDB.

Caratteristiche Principali

* Cifratura Ibrida Efficiente: Usa l'AES (modalità EAX) per cifrare messaggi di qualsiasi lunghezza in modo istantaneo, proteggendo la chiave AES tramite RSA.
* Firme Digitali Autenticate: Garantisce l'integrità e l'identità del mittente tramite hashing SHA-256 e firme RSA.
* Gestione delle Chiavi su File: Permette di salvare e ricaricare in modo sicuro le chiavi pubbliche e private tramite file JSON locali.
* Integrazione con FactorDB: Include uno strumento integrato per verificare lo stato di fattorizzazione di un modulo N tramite il database pubblico FactorDB.
* Interfaccia CLI Interattiva: Un menu a terminale semplice e intuitivo per gestire tutte le operazioni.

Requisiti e Installazione

Il progetto richiede Python 3 e le librerie crittografiche standard del settore.

1. Clona o scarica questa repository.
2. Installa le dipendenze necessarie eseguendo da terminale:
pip install pycryptodome factordb-python

Come Utilizzare il Programma

Avvia lo script principale dal tuo terminale:
python3 cripto.py

Dal menu principale potrai scegliere tra 5 opzioni:

1. Cifrare un messaggio: Cifra un testo in chiaro generando una chiave AES protetta da RSA e firmando digitalmente il contenuto.
2. Decifrare un messaggio: Legge il pacchetto JSON cifrato, sblocca la chiave AES, verifica l'integrità del Tag e autentica la firma del mittente.
3. Generare chiavi RSA: Crea una nuova coppia di chiavi a 1024 bit e offre la possibilità di salvarle in formato JSON (dati_pubblici.json e dati_privati.json).
4. Analizzare N (FactorDB): Interroga il database pubblico FactorDB per verificare se un modulo N è stato fattorizzato o se è sicuro.
5. Uscire dal programma.

Informazioni di Sicurezza

* Le chiavi RSA sono generate usando numeri primi forti a 1024 bit per un modulo N totale di 2048 bit.
* La cifratura simmetrica sfrutta lo standard AES in modalità EAX, garantendo sia la riservatezza che la protezione contro la manomissione dei dati.

Autore
Creato da Ludovico come progetto di approfondimento sulla crittografia moderna.
