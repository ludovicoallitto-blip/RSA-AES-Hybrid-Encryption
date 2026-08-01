from Crypto.Util.number import getStrongPrime, bytes_to_long, long_to_bytes
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import json
import base64
import hashlib
from factordb.factordb import FactorDB
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
            try:
                with open("dati_pubblici.json", "w", encoding="utf-8") as f:
                    json.dump(dati_public, f, indent=4)
                with open("dati_privati.json", "w", encoding="utf-8") as f:
                    json.dump(dati_private, f, indent=4)
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
    print('benvenuto nello strumento per criptare\n')
    while True:
        print("Hai i dati salvati nei file creati dal sistema?")
        print("y/n")
        a=input()
        if a=="y":
            try:
                with open("dati_privati.json", "r", encoding="utf-8") as f:
                    dati = json.load(f)
                N = dati["N"]
                d = dati["d"]
                print("dati caricati con sucesso")
                n=int(input("N pubblico ricevente: "))
                break
            except FileNotFoundError:
                print(f"[-] Errore: Il file dati_privati non esiste! Controlla il nome o il percorso.")

            except json.JSONDecodeError:
                print("[-] Errore: Il file esiste ma non è un JSON valido (è corrotto o vuoto).")
            except Exception as e:
                print(f"[-] Si è verificato un errore generico: {e}")

            
        elif a=="n":
            n=int(input("N pubblico ricevente: "))
            N=int(input("N pubblico mandante: "))
            d=int(input("d privato: "))
            break
        else:
            print("Valore non valido")
    c=input("c: ").encode("utf-8")
    key = get_random_bytes(32)
    hash_bytes = hashlib.sha256(c).digest()
    hash_bytes=bytes_to_long(hash_bytes)
    if hash_bytes<N:
        s=pow(hash_bytes, d, N)
    else:
        print("N troppo picollo per il messaggio")
    s=long_to_bytes(s) #fine generazione firma
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(c)
    key_N=bytes_to_long(key)
    if key_N<n:
        final_key=long_to_bytes((pow(key_N, e, n)))
    else:
        print("N troppo picollo per il messaggio")
    
    pacchetto = {
    "chiave_aes_cifrata": base64.b64encode(final_key).decode(),
    "nonce": base64.b64encode(nonce).decode(),
    "ciphertext": base64.b64encode(ciphertext).decode(),
    "tag": base64.b64encode(tag).decode(),
    "firma": base64.b64encode(s).decode()
}
    final = json.dumps(pacchetto)
    #final=bytes_to_long(final.encode("utf-8"))
    
    print(final)
def decripta():
    e=65537
    print('benvenuto nello strumento per decriptare\n')
    while True:
        
                print("Hai i dati salvati nei file creati dal sistema?")
                print("y/n")
                a=input()
                if a=="y":
                    try:
                        with open("dati_privati.json", "r", encoding="utf-8") as f:
                            dati = json.load(f)
                        n = dati["N"]
                        phi = dati["phi"]
                        print("dati caricati con sucesso")
                        Na=int(input("N del mandante del messaggio: "))
                        break
                    except FileNotFoundError:
                        print(f"[-] Errore: Il file dati_privati non esiste! Controlla il nome o il percorso.")

                    except json.JSONDecodeError:
                        print("[-] Errore: Il file esiste ma non è un JSON valido (è corrotto o vuoto).")
                    except Exception as e:
                        print(f"[-] Si è verificato un errore generico: {e}")   
                elif a=="n":
                        Na=int(input("N del mandante del messaggio: "))
                        print('Possiedi p e q?')
                        a=input('y/n: ')
                        if a=="y":
                            p=int(input("p: "))
                            q=int(input("q: "))
                            n=p*q
                            phi=(p-1)*(q-1)
                            break
                        elif a=="n":
                            while True:
                                print('possiedi n e phi?')
                                a=input('y/n: ')
                                if a=="y":
                                    n=int(input('N: '))
                                    phi=int(input('phi: '))
                                    break
                                if a=="n":
                                    print("operazione non possibile:")
                                    exit(0)
                                else:
                                    print("Scelta non valida")
                            break
                        else:
                            print("Scelta non valida")
                else:
                    print("Valore non valido")          
    d=pow(e, -1, phi)
    m=(input("m: "))
    pacchetto=json.loads(m)
    #estrazione dati
    chiave_aes_cifrata = base64.b64decode(pacchetto["chiave_aes_cifrata"])
    nonce = base64.b64decode(pacchetto["nonce"])
    ciphertext = base64.b64decode(pacchetto["ciphertext"])
    tag = base64.b64decode(pacchetto["tag"])
    firma = base64.b64decode(pacchetto["firma"])
    chiave_aes_cifrata=bytes_to_long(chiave_aes_cifrata)
    key=(long_to_bytes(pow(chiave_aes_cifrata, d, n)))#decodifica chaive aes
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



while True:
    e=65537
    print("BENVENUTO SU RSA CODER/DECODERE, COSA VUOI FARE?")
    print("1. criptare\n")
    print("2. decriptare\n")
    print("3. generare p e q\n")
    print("4. crakkare N\n")
    print("5. uscire\n")
    n=int(input("\n"))
    if(n==1):
        cripta()
    if(n==2):
        decripta()
    if(n==3):
        generate()
    if(n==4):
        crack()
    if(n==5):
        print("arrrivedrci")
        break   