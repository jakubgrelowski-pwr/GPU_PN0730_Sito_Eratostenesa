import random
import pyopencl as cl
import numpy as np
import time

# Pobieranie informacji o platformie i urządzeniu OpenCL
platform = cl.get_platforms()[0]
device = platform.get_devices()[0]
context = cl.Context([device])
queue = cl.CommandQueue(context, properties=cl.command_queue_properties.PROFILING_ENABLE)

# Kernel wykonujący test pierwszości Millera-Rabina na GPU.
program_source = """
__kernel void test_witness(__global const ulong* a, ulong s, ulong d, ulong n, __global int* result) {
    ulong gid = get_global_id(0);
    ulong x = a[gid];
    for (ulong i = 1; i < d; i++) {
        x = (x * a[gid]) % n;
    }
    if (x == 1 || x == n - 1) {
        result[gid] = 1;
    } else {
        for (ulong i = 0; i < s - 1; i++) {
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
        a_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=a_gpu.astype(np.uint64))
        result_buf = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, result_gpu.nbytes)

        # Wywołanie kernela OpenCL do wykonania testu Millera-Rabina na GPU
        global_size = (k,)
        local_size = None
        event = program.test_witness(queue, global_size, local_size, a_buf, np.uint64(s), np.uint64(d), np.uint64(n), result_buf)
        event.wait()

        start_time = event.profile.start
        end_time = event.profile.end
        execution_time = (end_time - start_time) * 1e-9
        #print("Kernel execution time: {:.10f} seconds".format(execution_time))

        # Kopiowanie wyników z urządzenia do pamięci CPU
        cl.enqueue_copy(queue, result_gpu, result_buf).wait()

        # Sprawdzenie wyników testów
        results = [int(result) for result in result_gpu]
        return all(results)

    return is_probably_prime(n, k)

# Główna funkcja programu
if __name__ == "__main__":

    carmichael_numbers = [633267, 414154, 622188, 269938, 788018, 676447, 858479, 201674, 996040, 1000037]

    number_ranges = {
        "1001-9999": (1001, 9999),
        "10001-99999": (10001, 99999),
        "100001-999999": (100001, 999999),
        "Carmichael": carmichael_numbers
    }


    k = 10000
    num_repeats = 100

    for range_name, number_range in number_ranges.items():
        total_execution_time = 0.0

        for _ in range(num_repeats):
            n = random.randint(*number_range) if range_name != "Carmichael" else random.choice(carmichael_numbers)

            start_time = time.time()
            is_prime = miller_rabin_test_gpu(n, k)
            end_time = time.time()

            execution_time = end_time - start_time
            total_execution_time += execution_time

            print(f"Algorytm Millera-Rabina GPU, test {_ + 1}/{num_repeats}, czas: {execution_time:.4f}s, rezultat: {n} is prime: {is_prime}")

        average_execution_time = total_execution_time / num_repeats

        print(f"Range: {range_name}, Number of Repeats: {num_repeats}, Average Execution Time: {average_execution_time:.10f} seconds\n")