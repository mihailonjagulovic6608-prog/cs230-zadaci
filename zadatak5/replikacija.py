import os

class CentralniImenik:
    def __init__(self):
        self._lokacije = {}

    def registruj(self, naziv_datoteke, server):
        self._lokacije.setdefault(naziv_datoteke, set()).add(server)

    def pronadji(self, naziv_datoteke):
        return self._lokacije.get(naziv_datoteke, set())


class Server:
    def __init__(self, naziv, koren_direktorijum):
        self.naziv = naziv
        self.koren = koren_direktorijum
        os.makedirs(self.koren, exist_ok=True)

    def putanja(self, naziv_datoteke):
        return os.path.join(self.koren, naziv_datoteke)

    def sadrzi(self, naziv_datoteke):
        return os.path.exists(self.putanja(naziv_datoteke))

    def procitaj(self, naziv_datoteke):
        with open(self.putanja(naziv_datoteke), 'rb') as f:
            return f.read()

    def sacuvaj(self, naziv_datoteke, sadrzaj):
        with open(self.putanja(naziv_datoteke), 'wb') as f:
            f.write(sadrzaj)


class Middleware:
    def __init__(self, imenik, serveri):
        self.imenik = imenik
        self.serveri = serveri

    def repliciraj(self, naziv_datoteke, izvorni_server, ciljni_server):
        lokacije = self.imenik.pronadji(naziv_datoteke)
        if izvorni_server not in lokacije:
            return False, f"Datoteka '{naziv_datoteke}' ne postoji na serveru '{izvorni_server}'."

        izvor = self.serveri[izvorni_server]
        cilj = self.serveri[ciljni_server]

        sadrzaj = izvor.procitaj(naziv_datoteke)
        cilj.sacuvaj(naziv_datoteke, sadrzaj)
        self.imenik.registruj(naziv_datoteke, ciljni_server)

        return True, f"Datoteka '{naziv_datoteke}' uspesno replicirana sa '{izvorni_server}' na '{ciljni_server}'."


class Klijent:
    def __init__(self, middleware):
        self.middleware = middleware

    def zatrazi_replikaciju(self, naziv_datoteke, izvorni_server, ciljni_server):
        uspeh, poruka = self.middleware.repliciraj(naziv_datoteke, izvorni_server, ciljni_server)
        print(f"[{'OK' if uspeh else 'GRESKA'}] {poruka}")
        return uspeh


def main():
    imenik = CentralniImenik()
    server1 = Server('server1', 'skladiste_server1')
    server2 = Server('server2', 'skladiste_server2')

    with open(server1.putanja('data.txt'), 'w', encoding='utf-8') as f:
        f.write('Sadrzaj originalne datoteke data.txt')
    imenik.registruj('data.txt', 'server1')

    middleware = Middleware(imenik, {'server1': server1, 'server2': server2})
    klijent = Klijent(middleware)

    klijent.zatrazi_replikaciju('data.txt', 'server1', 'server2')

if __name__ == '__main__':
    main()
