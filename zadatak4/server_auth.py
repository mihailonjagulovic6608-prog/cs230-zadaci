import socket
import datetime

HOST = '0.0.0.0'
PORT = 9600
LOG_FILE = 'audit_log.txt'

KORISNICI = {
    'admin': 'admin123',
    'student': 'lozinka1',
}

def upisi_log(poruka):
    vreme = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f'[{vreme}] {poruka}\n')

def posalji(konekcija, tekst):
    konekcija.sendall((tekst + '\n').encode('utf-8'))

def procitaj_liniju(konekcija):
    bafer = b''
    while not bafer.endswith(b'\n'):
        deo = konekcija.recv(1024)
        if not deo:
            break
        bafer += deo
    return bafer.decode('utf-8').strip()

def opsluzi_klijenta(konekcija, adresa):
    korisnicko_ime = procitaj_liniju(konekcija)
    lozinka = procitaj_liniju(konekcija)

    if KORISNICI.get(korisnicko_ime) == lozinka:
        upisi_log(f"User '{korisnicko_ime}' successfully logged in.")
        posalji(konekcija, 'OK')
        while True:
            poruka = procitaj_liniju(konekcija)
            if not poruka or poruka == 'IZLAZ':
                break
            posalji(konekcija, f'Primljeno: {poruka}')
    else:
        upisi_log(f"User '{korisnicko_ime}' failed login attempt.")
        posalji(konekcija, 'ODBIJENO')

    konekcija.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_soket:
        server_soket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_soket.bind((HOST, PORT))
        server_soket.listen(5)
        print(f'Server aktivan na {HOST}:{PORT}')
        while True:
            konekcija, adresa = server_soket.accept()
            opsluzi_klijenta(konekcija, adresa)

if __name__ == '__main__':
    main()
