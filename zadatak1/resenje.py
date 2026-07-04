import time
from functools import wraps

def merilac_vremena(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pocetak = time.perf_counter()
        rezultat = func(*args, **kwargs)
        kraj = time.perf_counter()
        print(f"Funkcija '{func.__name__}' izvrsena za {kraj - pocetak:.6f} sekundi.")
        return rezultat
    return wrapper

@merilac_vremena
def calculate_sum(n):
    return sum(range(n + 1))

if __name__ == "__main__":
    print(calculate_sum(1000000))
