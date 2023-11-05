import random
import math

def is_probably_prime(number, testCount):
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

    for _ in range(testCount):
        a = random.randint(2, number - 2)
        x = pow(a, d, number)
        if x == 1 or x == number - 1:
            continue

        if witness(a, x, number):
            return f"{number} jest l. zlozona"

    return f"{number} jest prawdopodobnie l. pierwsza"

print(is_probably_prime(number = 3, testCount = 523))





