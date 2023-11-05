import random


def miller_rabin_test(n, k):
    if n <= 1 or n == 4:
        return "jest l. zlozona"
    if n <= 3:
        return "jest prawdopodobnie l. pierwsza"

    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)

        for _ in range(s):
            y = pow(x, 2, n)

            if y == 1 and x != 1 and x != n - 1:
                return "jest wielokrotnoscia", gcd(x - 1, n)

            x = y

        if x != 1:
            return "jest l. zlozona"

    return "jest prawdopodobnie l. pierwsza"


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# Example usage
n = 123908479253851
k = 100
result = miller_rabin_test(n, k)
print(result)