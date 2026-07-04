import socket
import struct
import io
from PIL import Image

HOST = '0.0.0.0'
PORT = 9500

def primi_podatke(konekcija, broj_bajtova):
    podaci = b''
    while len(podaci) < broj_bajtova:
        deo = konekcija.recv(broj_bajtova - len(podaci))
        if not deo:
            raise ConnectionError('Konekcija prekinuta.')
        podaci += deo
    return podaci

def posalji_podatke(konekcija, podaci):
    konekcija.sendall(struct.pack('>I', len(podaci)))
    konekcija.sendall(podaci)

def obradi_sliku(sirovi_bajtovi):
    slika = Image.open(io.BytesIO(sirovi_bajtovi))
    crno_bela = slika.convert('L')
    izlaz = io.BytesIO()
    crno_bela.save(izlaz, format=slika.format if slika.format else 'PNG')
    return izlaz.getvalue()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_soket:
        server_soket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_soket.bind((HOST, PORT))
        server_soket.listen(1)
        print(f'Server aktivan na {HOST}:{PORT}')
        while True:
            konekcija, adresa = server_soket.accept()
            with konekcija:
                print(f'Povezan klijent: {adresa}')
                duzina = struct.unpack('>I', primi_podatke(konekcija, 4))[0]
                slika_bajtovi = primi_podatke(konekcija, duzina)
                obradjena_slika = obradi_sliku(slika_bajtovi)
                posalji_podatke(konekcija, obradjena_slika)
                print('Slika obradjena i poslata nazad klijentu.')

if __name__ == '__main__':
    main()
