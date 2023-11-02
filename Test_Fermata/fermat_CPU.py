import random

# wykonanie obliczenia:
def power_mod(base, exponent, mod):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exponent //= 2

    print("wybrano a=", base, ", wynik: ", result)
    return result

# Glowna funkcja generujaca losowe liczby 'a' i powtarzajaca obliczenia:
def is_prime(p, repetiton):
    if p <= 1:
        return False

    for _ in range(repetition):
        a = random.randint(2, 1000)
        if power_mod(a, p - 1, p) != 1:
            return False

    return True

# 561 - liczba Carmichaela dla ktorej wychodzi roznie
p = 561
repetition = 4

if is_prime(p, repetition):
    print(p, " jest prawdopodobnie l. pierwsza")
else:
    print(p, " jest prawdopodobnie l. zlozona")
