import socket
import struct
import sys
import os

HOST = '127.0.0.1'
PORT = 9500

def primi_podatke(soket, broj_bajtova):
    podaci = b''
    while len(podaci) < broj_bajtova:
        deo = soket.recv(broj_bajtova - len(podaci))
        if not deo:
            raise ConnectionError('Konekcija prekinuta.')
        podaci += deo
    return podaci

def posalji_podatke(soket, podaci):
    soket.sendall(struct.pack('>I', len(podaci)))
    soket.sendall(podaci)

def main(putanja_do_slike):
    with open(putanja_do_slike, 'rb') as f:
        sirovi_bajtovi = f.read()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as klijent_soket:
        klijent_soket.connect((HOST, PORT))
        posalji_podatke(klijent_soket, sirovi_bajtovi)
        duzina = struct.unpack('>I', primi_podatke(klijent_soket, 4))[0]
        obradjena_slika = primi_podatke(klijent_soket, duzina)

    naziv, ekstenzija = os.path.splitext(putanja_do_slike)
    izlazna_putanja = f'{naziv}_crno_belo{ekstenzija}'
    with open(izlazna_putanja, 'wb') as f:
        f.write(obradjena_slika)
    print(f'Sacuvano: {izlazna_putanja}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Upotreba: python klijent_slika.py putanja_do_slike')
        sys.exit(1)
    main(sys.argv[1])
