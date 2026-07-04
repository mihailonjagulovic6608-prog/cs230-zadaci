import socket

HOST = '0.0.0.0'
PORT = 9700
DATOTEKA = 'server2_data.txt'

def procitaj_liniju(konekcija):
    bafer = b''
    while not bafer.endswith(b'\n'):
        deo = konekcija.recv(1024)
        if not deo:
            break
        bafer += deo
    return bafer.decode('utf-8').strip()

def posalji_sadrzaj_datoteke(konekcija):
    with open(DATOTEKA, 'r', encoding='utf-8') as f:
        redovi = f.readlines()
    for red in redovi:
        konekcija.sendall((red.rstrip('\n') + '\n').encode('utf-8'))
    konekcija.sendall(b'<<KRAJ>>\n')

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_soket:
        server_soket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_soket.bind((HOST, PORT))
        server_soket.listen(1)
        print(f'Server2 ceka konekciju na {HOST}:{PORT}')
        konekcija, adresa = server_soket.accept()
        with konekcija:
            print(f'Povezan Server1: {adresa}')
            konekcija.sendall(b'SPREMNO\n')
            zahtev = procitaj_liniju(konekcija)
            if zahtev == 'POSALJI_SADRZAJ':
                posalji_sadrzaj_datoteke(konekcija)
                print('Sadrzaj datoteke poslat Server1 radi poredjenja.')

if __name__ == '__main__':
    main()
