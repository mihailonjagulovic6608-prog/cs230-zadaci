class ServerA:
    naziv = 'server_a'

    def obradi_podatke(self, podaci):
        return podaci.upper()


class ServerB:
    naziv = 'server_b'

    def obradi_podatke(self, podaci):
        return podaci[::-1]


class CentralniImenik:
    def __init__(self):
        self._mapa_usluga = {}

    def registruj_uslugu(self, naziv_usluge, server):
        self._mapa_usluga[naziv_usluge] = server

    def pronadji_server(self, naziv_usluge):
        return self._mapa_usluga.get(naziv_usluge)


class Middleware:
    def __init__(self, imenik):
        self.imenik = imenik

    def obradi_zahtev(self, naziv_usluge, podaci):
        server = self.imenik.pronadji_server(naziv_usluge)
        if server is None:
            return False, f"Usluga '{naziv_usluge}' nije registrovana ni na jednom serveru."
        rezultat = server.obradi_podatke(podaci)
        return True, rezultat


class Klijent:
    def __init__(self, middleware):
        self.middleware = middleware

    def posalji_zahtev(self, naziv_usluge, podaci):
        uspeh, rezultat = self.middleware.obradi_zahtev(naziv_usluge, podaci)
        if uspeh:
            print(f"[OK] Rezultat: {rezultat}")
        else:
            print(f"[GRESKA] {rezultat}")
        return rezultat


def main():
    imenik = CentralniImenik()
    imenik.registruj_uslugu('veliko_slovo', ServerA())
    imenik.registruj_uslugu('obrnuti_redosled', ServerB())

    middleware = Middleware(imenik)
    klijent = Klijent(middleware)

    print('Dostupne usluge: veliko_slovo, obrnuti_redosled')
    naziv_usluge = input('Izaberite uslugu: ').strip()
    podaci = input('Unesite tekst za obradu: ').strip()

    klijent.posalji_zahtev(naziv_usluge, podaci)

if __name__ == '__main__':
    main()
