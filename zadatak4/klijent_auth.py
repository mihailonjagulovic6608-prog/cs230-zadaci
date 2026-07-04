import socket

HOST = '127.0.0.1'
PORT = 9600

def procitaj_liniju(soket):
    bafer = b''
    while not bafer.endswith(b'\n'):
        deo = soket.recv(1024)
        if not deo:
            break
        bafer += deo
    return bafer.decode('utf-8').strip()

def main():
    korisnicko_ime = input('Korisnicko ime: ')
    lozinka = input('Lozinka: ')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as klijent_soket:
        klijent_soket.connect((HOST, PORT))
        klijent_soket.sendall((korisnicko_ime + '\n').encode('utf-8'))
        klijent_soket.sendall((lozinka + '\n').encode('utf-8'))

        odgovor = procitaj_liniju(klijent_soket)
        if odgovor != 'OK':
            print('Prijava neuspesna.')
            return

        print('Prijava uspesna. Ukucaj IZLAZ za kraj.')
        while True:
            poruka = input('>> ')
            klijent_soket.sendall((poruka + '\n').encode('utf-8'))
            if poruka == 'IZLAZ':
                break
            print(procitaj_liniju(klijent_soket))

if __name__ == '__main__':
    main()
