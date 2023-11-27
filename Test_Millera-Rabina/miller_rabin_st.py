import random
import math
import sys

def is_probably_prime(number, test_count):
    if number <= 2 or number % 2 == 0:
        return "Bledny argument. (n <= 2 or n % 2 == 0)"

    if number == 3:
        return f"{number} jest l. pierwsza"

    s, d = 0, number - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    def witness(a, x, n):
        for _ in range(s):
            x = (x ** 2) % n
            if x == 1 and a != 1 and a != n - 1:
                return False
        return x != 1

    for _ in range(test_count):
        a = random.randint(2, number - 2)
        x = pow(a, d, number)
        if x == 1 or x == number - 1:
            continue

        if witness(a, x, number):
            return False

    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uzycie: python miller_rabin_st.py <liczba_do_przetestowania> <liczba_iteracji>")
        sys.exit(1)
    
    n = int(sys.argv[1])
    k = int(sys.argv[2])

    is_prime = is_probably_prime(n, k)
    result_text = f"{n} jest prawdopodobnie liczba pierwsza." if is_prime else f"{n} nie jest liczba pierwsza."
    print(result_text)