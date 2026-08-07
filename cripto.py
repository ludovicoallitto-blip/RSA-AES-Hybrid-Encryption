from Crypto.Util.number import getStrongPrime, bytes_to_long, long_to_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import json
import base64
import hashlib
from factordb.factordb import FactorDB
import getpass
import socket
e=65537

def crack():
    n=int(input('N: '))
    try:
        f = FactorDB(n)
        f.connect()
        status = f.get_status()
        
        if status == "FF":
            print("Modulo N completamente fattorizzato trovato!")
            fattori = f.get_factor_list()
            print(f"I fattori sono: {fattori}")
            
            
        elif status == "C" or status == "U":
            print("Sicuro (per ora): FactorDB non ha i fattori per questo N.")
        
        elif status == "P" or status == "PRP":
            print("Il numero non è N, il numero è primo. dato che è un numero primo phi è facilmente calcolabile: ")
            print(n-1)
            
            
        else:
            print(f"Stato inaspettato da FactorDB: {status}")
            
    except:
        print('Problema inaspettato nella connesione\n')
def generate():
    e=65537
    p = getStrongPrime(1024, e=65537)
    q = getStrongPrime(1024, e=65537)
    print(f'Ecco p e q: \n')
    print(f'p: {p}\n')
    print(f'q: {q}\n')
    n=p*q
    phi=(p-1)*(q-1)
    d=pow(e, -1, phi)
    print(f'N: {n}\n')
    print(f'phi: {phi}\n')
    print(f'd: {d}\n')


    dati_public = {
    "N": n,
    "e": e
    }
    dati_private= {
    "N": n,
    "e": e,
    "p": p,
    "q": q,
    "phi":phi,
    "d": d
    }
    while True:
        print('Vuoi salvare i dati privati e pubblici in dei file?')
        print("y/n: ")
        a=input()
        if a=="y":
            pasw=getpass.getpass("scegli una password per rendere sicuri i tuoi dati, ricordatela! ")
            key = hashlib.sha256(pasw.encode('utf-8')).digest()
            cipher = AES.new(key, AES.MODE_EAX)
            dati_private = json.dumps(dati_private).encode('utf-8')
            
            ciphertext, tag = cipher.encrypt_and_digest(dati_private)
            pacchetto_privato = {
                "nonce": base64.b64encode(cipher.nonce).decode(),
                "ciphertext": base64.b64encode(ciphertext).decode(),
                "tag": base64.b64encode(tag).decode()
            }
            try:
                with open("dati_pubblici.json", "w", encoding="utf-8") as f:
                    json.dump(dati_public, f, indent=4)
                with open("dati_privati.json", "w", encoding="utf-8") as f:
                    json.dump(pacchetto_privato, f, indent=4)
                print("File salvato con successo!")
            except PermissionError:
                print("[-] Errore: Permesso negato! Non hai i diritti per scrivere in questa cartella.")

            except OSError as e:
                print(f"[-] Errore di Sistema (OS): {e}")

            except FileNotFoundError:
                print("[-] Errore: Il file richiesto non è stato trovato.")

            except IsADirectoryError:
                print("[-] Errore: Il percorso indicato è una cartella, non un file.")

            except json.JSONDecodeError:
                print("[-] Errore: Il file non è un JSON valido.")

            except Exception as e:
                print(f"[-] Si è verificato un errore generico: {e}")
            break
        elif a=="n":
            print("perfetto ")
            break
        else:
            print("Opzione non valida")

        
def cripta():
    e=65537
    sec = ""
    print('benvenuto nello strumento per criptare\n')
    with open("dati_privati.json", "r", encoding="utf-8") as f:
        dati = json.load(f)
    try:
        nonce = base64.b64decode(dati["nonce"])
        ciphertext = base64.b64decode(dati["ciphertext"])
        tag = base64.b64decode(dati["tag"])
        pasw=getpass.getpass("password per i dati privati:  ")
        key = hashlib.sha256(pasw.encode('utf-8')).digest()
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        dati = cipher.decrypt_and_verify(ciphertext, tag)   
        dati = json.loads(dati.decode('utf-8'))
    except:
        print("riscontrato un errore")
        return(0)
    N=dati["N"]
    p=dati["p"]
    q=dati["q"]
    phi=dati["phi"]
    d=dati["d"]
    while True:
        try:
            with open("contatti.json", "r", encoding="utf-8") as f:
                    rubrica = json.load(f)
            stringa = json.dumps(rubrica, sort_keys=True).encode("utf-8")
            hash = hashlib.sha256(stringa).hexdigest()
            try:
                with open("security.txt", "r", encoding="utf-8") as f:
                    sec = f.read()
            except FileNotFoundError:
                print("File di sicurezza non trovato")

            if sec != hash:
                print("I contatti sono stati manomessi, se non lo hai fatto tu potrei aver subito un attaco hacker, vuoi proseguire lo stesso? y/n:")
                b=input()
                if b=="n":
                    print("Arrivederci")
                    return(0)
            nome=input("Con chi stai parlando? ")
            if nome in rubrica:
                n=rubrica[nome]["N"]
                break
            else:
                print("Non hai questo contato in rubrica.")
        except FileNotFoundError:
            print("Non hai ancora contatti")
            return()
    c=input("c: ").encode("utf-8")
    key = get_random_bytes(32)
    hash_bytes = hashlib.sha256(c).digest()
    hash_bytes=bytes_to_long(hash_bytes)
    if hash_bytes<N:
        s=pow(hash_bytes, d, N)
    else:
        print("N troppo piccolo per il messaggio")
    s=long_to_bytes(s) #fine generazione firma
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(c)
    key_N=bytes_to_long(key)
    if key_N<n:
        final_key=long_to_bytes((pow(key_N, e, n)))
    else:
        print("n troppo piccolo per il messaggio")
    
    pacchetto = {
    "chiave_aes_cifrata": base64.b64encode(final_key).decode(),
    "nonce": base64.b64encode(nonce).decode(),
    "ciphertext": base64.b64encode(ciphertext).decode(),
    "tag": base64.b64encode(tag).decode(),
    "firma": base64.b64encode(s).decode()
}
    final = json.dumps(pacchetto).encode('utf-8')
    HOST = str(input("Inserisci l'indirizzo ip del destinatario xxx.xxx.xxx.xxx: "))
    PORT = int(input("Inserisci la porta dove comunicare"))
    try:
        co=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        co.connect((HOST, PORT))
        
        print(f"connesso con ip: {HOST}")
        co.sendall(final)
        co.close()
        print("messaggio inviato con successo.\n")
    except Exception as e:
        print(f"Si è verificato un errore, riprovare. {e}\n")
        return(0)


    
    
def decripta():
    e=65537
    sec = ""
    print('benvenuto nello strumento per decriptare\n')
    while True:
        nome=input("Con chi stai parlando? ")
        with open("dati_privati.json", "r", encoding="utf-8") as f:
            dati = json.load(f)
        try:
            nonce = base64.b64decode(dati["nonce"])
            ciphertext = base64.b64decode(dati["ciphertext"])
            tag = base64.b64decode(dati["tag"])
            pasw=getpass.getpass("password per i dati privati:  ")
            key = hashlib.sha256(pasw.encode('utf-8')).digest()
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            dati = cipher.decrypt_and_verify(ciphertext, tag)   
            dati = json.loads(dati.decode('utf-8'))
        except:
            print("riscontrato un errore")
            return(0)
        try:
            with open("contatti.json", "r", encoding="utf-8") as f:
                rubrica = json.load(f)
        except FileNotFoundError:
            print("Non hai ancora contatti")
            return()
        stringa = json.dumps(rubrica, sort_keys=True).encode("utf-8")
        hash = hashlib.sha256(stringa).hexdigest()
        try:
            with open("security.txt", "r", encoding="utf-8") as f:
                sec = f.read()
        except FileNotFoundError:
            print("file di sicurezza non trovato")
        if sec != hash:
            print("I contatti sono stati manomessi, se non lo hai fatto tu potrei aver subito un attaco hacker, vuoi proseguire lo stesso? y/n:")
            b=input()
            if b=="n":
                print("Arrivederci")
                return(0)
        N=dati["N"]
        d=dati["d"]
        if nome in rubrica:
            Na=rubrica[nome]['N']
            break
        else:
            print("Non hai questo contato in rubrica.")

    HOST = '0.0.0.0'
    PORT = int(input("Inserisci la porta dove comunicare"))
    try:
        co=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        co.bind((HOST, PORT))
        co.listen(1)
        conn, addr = co.accept()
        print(f"connesso con ip: {addr}")
        m=conn.recv(4096).decode('utf-8')
        conn.close()
        co.close()
        print("Messaggio ricevuto con successo\n")
    except Exception as e:
        print(f"Errore imprevisto riprovare.{e}\n")
        return(0)
    pacchetto=json.loads(m)
    #estrazione dati
    chiave_aes_cifrata = base64.b64decode(pacchetto["chiave_aes_cifrata"])
    nonce = base64.b64decode(pacchetto["nonce"])
    ciphertext = base64.b64decode(pacchetto["ciphertext"])
    tag = base64.b64decode(pacchetto["tag"])
    firma = base64.b64decode(pacchetto["firma"])
    chiave_aes_cifrata=bytes_to_long(chiave_aes_cifrata)
    key=(long_to_bytes(pow(chiave_aes_cifrata, d, N)))#decodifica chaive aes
    firma=bytes_to_long(firma)
    firma=pow(firma, e, Na)
    firma=long_to_bytes(firma) #decodifica firma

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        print('TAG valido, il messaggio non è stato modificato')
        hash_bytes = hashlib.sha256(plaintext).digest()
        if hash_bytes == firma:
            print("Firma VALIDA. Il messaggio è originale.")
            print("Messaggio in chiaro:", plaintext.decode('utf-8'))
        else:
            print("ALLARME: Firma NON valida! Messaggio corrotto o hackerato.")
    except ValueError:
        print("Chiave corrotta o non valida")

def creazione():
    nome=input("Nome del contatto: ")
    e=65537
    N=int(input("N del contatto: "))
    try:
        with open("contatti.json", "r", encoding="utf-8") as f:
            dati = json.load(f)
    except FileNotFoundError:
        dati={}
    dati[nome]= {
    "N": N,
    "e": e
    }
    stringa = json.dumps(dati, sort_keys=True).encode("utf-8")
    hash = hashlib.sha256(stringa).hexdigest()
    with open("security.txt", "w", encoding="utf-8") as f:
        f.write(hash)
    with open("contatti.json", "w", encoding="utf-8") as f:
        json.dump(dati, f, indent=4)
def get_N(nome):
    try:
        with open("contatti.json", "r", encoding="utf-8") as f:
                rubrica = json.load(f)
                if nome in rubrica:
                    n_trovato = rubrica[nome]["N"]
                    return n_trovato
                else:
                    print(f"[-] Errore: Il contatto '{nome}' non esiste nella rubrica.")
                    return None
    except FileNotFoundError:
        print("Non hai ancora contatti")

while True:
    e=65537
    print("BENVENUTO SU RSA CODER/DECODERE, COSA VUOI FARE?")
    print("1. criptare\n")
    print("2. decriptare\n")
    print("3. generare p e q\n")
    print("4. crakkare N\n")
    print("5. Aggiungere un contatto in rubrica\n")
    print("6. uscire\n")
    n=int(input("\n"))
    if(n==1):
        cripta()
    if(n==2):
        decripta()
    if(n==3):
        generate()
    if(n==4):
        crack()
    if n == 5:
        creazione()
    if(n==6):
        print("arrrivedrci")
        break   