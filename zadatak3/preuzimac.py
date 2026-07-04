import threading
import os
import urllib.request
from urllib.parse import urlparse

def preuzmi_datoteku(url, odredisni_folder):
    naziv_datoteke = os.path.basename(urlparse(url).path) or "preuzeta_datoteka"
    putanja = os.path.join(odredisni_folder, naziv_datoteke)
    try:
        urllib.request.urlretrieve(url, putanja)
        print(f"[OK] Preuzeto: {url} -> {putanja}")
    except Exception as greska:
        print(f"[GRESKA] {url}: {greska}")

def preuzmi_sve(url_lista, odredisni_folder="preuzeto"):
    os.makedirs(odredisni_folder, exist_ok=True)
    niti = []
    for url in url_lista:
        nit = threading.Thread(target=preuzmi_datoteku, args=(url, odredisni_folder))
        niti.append(nit)
        nit.start()
    for nit in niti:
        nit.join()

if __name__ == "__main__":
    urlovi = [
        "https://www.python.org/static/img/python-logo.png",
        "https://www.w3.org/TR/PNG/iso_8859-1.txt",
        "https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore",
    ]
    preuzmi_sve(urlovi)
