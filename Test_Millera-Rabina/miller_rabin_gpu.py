import random
import pyopencl as cl
import numpy as np

# Pobieranie informacji o platformie i urządzeniu OpenCL
platform = cl.get_platforms()[0]
device = platform.get_devices()[0]
context = cl.Context([device])
queue = cl.CommandQueue(context)

# Kernel wykonujący test pierwszości Millera-Rabina na GPU.
program_source = """
    __kernel void test_witness(__global const int* a, int s, int d, int n, __global int* result) {
    int gid = get_global_id(0);
    int x = a[gid];
    for (int i = 1; i < d; i++) {
        x = (x * a[gid]) % n;
    }
    if (x == 1 || x == n - 1) {
        result[gid] = 1;
    } else {
        for (int i = 0; i < s - 1; i++) {
            x = (x * x) % n;
            if (x == n - 1) {
                result[gid] = 1;
                return;
            }
        }
        result[gid] = 0;
    }
}
"""

# Kompilacja programu OpenCL
program = cl.Program(context, program_source).build()

# Funkcja wykonująca test pierwszości Millera-Rabina na GPU
def miller_rabin_test_gpu(n, k):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Funkcja pomocnicza sprawdzająca, czy liczba jest prawdopodobnie pierwsza
    def is_probably_prime(n, k):
        if n in (2, 3):
            return True

        if n <= 1 or n % 2 == 0:
            return False

        s, d = 0, n - 1
        while d % 2 == 0:
            s += 1
            d //= 2

        # Generowanie losowych liczb 'a' dla testów
        a_values = [random.randint(2, n - 2) for _ in range(k)]

        # Przygotowanie danych dla GPU
        a_gpu = np.array(a_values, dtype=np.int32)
        result_gpu = np.zeros(k, dtype=np.int32)

        # Przygotowanie buforów na urządzenie OpenCL
        a_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=a_gpu)
        result_buf = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, result_gpu.nbytes)

        # Wywołanie kernela OpenCL do wykonania testu Millera-Rabina na GPU
        program.test_witness(queue, a_gpu.shape, None, a_buf, np.int32(s), np.int32(d), np.int32(n), result_buf)

        # Kopiowanie wyników z urządzenia do pamięci CPU
        cl.enqueue_copy(queue, result_gpu, result_buf).wait()

        # Sprawdzenie wyników testów
        results = [bool(result) for result in result_gpu]

        return all(results)

    return is_probably_prime(n, k)


# Główna funkcja programu
if __name__ == "__main__":
    n = int(input("Podaj liczbę do przetestowania: "))
    k = int(input("Liczba iteracji testu (zalecane minimum 10): "))

    is_prime = miller_rabin_test_gpu(n, k)

    if is_prime:
        print(f"{n} jest prawdopodobnie liczbą pierwszą.")
    else:
        print(f"{n} nie jest liczbą pierwszą.")
