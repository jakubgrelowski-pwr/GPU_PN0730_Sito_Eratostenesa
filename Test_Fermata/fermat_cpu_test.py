import sys
import threading
import random
import time
def power_mod(base, exponent, mod):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exponent //= 2
    return result

def gcd(number1, number2):
    while number2 != 0:
        number1, number2 = number2, number1 % number2
    return number1

def is_coprime(number1, number2):
    return gcd(number1, number2) == 1

def fermat_test_cpu(n, k):
    results = []
    base_a = []

    while len(base_a) != k:
        probably_a = random.randint(2, n - 1)
        if is_coprime(probably_a, n):
            base_a.append(probably_a)

    def test(i):
        return power_mod(base_a[i], n - 1, n) == 1

    threads = []
    for i in range(k):
        thread = threading.Thread(target=lambda i=i: results.append(test(i)))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return all(results)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uzycie: python fermat_cpu_test.py <liczba_do_przetestowania> <liczba_iteracji>")
        sys.exit(1)

    n = int(sys.argv[1])
    k = int(sys.argv[2])

    is_prime = fermat_test_cpu(n, k)
    result_text = f"{n} jest prawdopodobnie liczba pierwsza." if is_prime else f"{n} nie jest liczba pierwsza."
    print(result_text)
