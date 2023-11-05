import threading
import random

# Losowa liczba i wykonanie obliczenia:
def power_mod(base, exponent, mod):
    result = 1

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exponent //= 2
    
    return result

# 561 - liczba Carmichaela dla ktorej wychodzi roznie
p = 3

# Liczba powtórzeń:
num_threads = 4

# Lista na wyniki
results = []
base_a = []

for i in range(num_threads):
    base_a.append(random.randint(2, 1000))

print(base_a)

# Tworzenie wątków
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=lambda i=i: results.append(power_mod(base_a[i], p-1,p)))
    threads.append(thread)
    thread.start()

# Oczekiwanie na zakończenie wątków
for thread in threads:
    thread.join()

# Sprawdzenie wynikow ze wszyskich powtórzeń:
print("Wyniki z wszystkich wątków:", results)
is_prime = True

for i in results:
    if i!=1:
        is_prime = False

if is_prime:
    print(p, " jest prawdopodobnie l. pierwsza")
else:
    print(p, " jest prawdopodobnie l. zlozona")
