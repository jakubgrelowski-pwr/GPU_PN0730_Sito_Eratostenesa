import random
import threading

def miller_rabin_test(n, k=10):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    def is_probably_prime(n, k):
        if n in (2, 3):
            return True

        if n <= 1 or n % 2 == 0:
            return False

        s, d = 0, n - 1
        while d % 2 == 0:
            s += 1
            d //= 2

        def test_witness(a):
            print(a)
            x = pow(a, d, n)
            if x in(1, n - 1):
                return True
            for _ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    return True
            return False

        for _ in range(k):
            a = random.randint(2, n - 2)
            if not test_witness(a):
                return False

        return True

    results = [False] * k
    threads = []

    def test_thread(i):
        results[i] = is_probably_prime(n, 1)

    for i in range(k):
        thread = threading.Thread(target=test_thread, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return bool(all(results))

if __name__ == "__main__":
    n = int(input("Podaj liczbę do przetestowania: "))
    k = int(input("Liczba iteracji testu (zalecane minimum 10): "))

    is_prime = miller_rabin_test(n, k)

    if is_prime:
        print(f"{n} jest prawdopodobnie liczbą pierwszą.")
    else:
        print(f"{n} nie jest liczbą pierwszą.")
