import socket

HOST = '127.0.0.1'
PORT = 9700
DATOTEKA = 'server1_data.txt'

def procitaj_liniju(soket):
    bafer = b''
    while not bafer.endswith(b'\n'):
        deo = soket.recv(1024)
        if not deo:
            break
        bafer += deo
    return bafer.decode('utf-8').strip()

def primi_sadrzaj_datoteke(soket):
    redovi = []
    while True:
        red = procitaj_liniju(soket)
        if red == '<<KRAJ>>':
            break
        redovi.append(red)
    return redovi

def ucitaj_lokalne_redove():
    with open(DATOTEKA, 'r', encoding='utf-8') as f:
        return [red.rstrip('\n') for red in f.readlines()]

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as klijent_soket:
        klijent_soket.connect((HOST, PORT))
        potvrda = procitaj_liniju(klijent_soket)
        if potvrda != 'SPREMNO':
            print('Server2 nije spreman za replikaciju.')
            return

        print('Server2 potvrdio da je spreman za replikaciju.')
        klijent_soket.sendall(b'POSALJI_SADRZAJ\n')

        redovi_server2 = primi_sadrzaj_datoteke(klijent_soket)
        redovi_server1 = ucitaj_lokalne_redove()

        nedostajuci_redovi = [red for red in redovi_server1 if red not in redovi_server2]

        if nedostajuci_redovi:
            print('Redovi koje Server2 nema, a treba ih poslati:')
            for red in nedostajuci_redovi:
                print(f'  - {red}')
        else:
            print('Server2 vec ima sve redove iz data.txt.')

if __name__ == '__main__':
    main()
