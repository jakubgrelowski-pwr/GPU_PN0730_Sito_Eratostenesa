import pyopencl as cl
import numpy as np

def fermat_test(n, a_values, ctx, queue):
    kernel_code = """
    __kernel void fermat_test(__global ulong* results, ulong n, __global ulong* a_values, int num_tests) {
        int gid = get_global_id(0);
        ulong x = 1;
        for (ulong i = 0; i < n - 1; i++) {
            x = (x * a_values[gid]) % n;
        }
        results[gid] = (x == 1) ? 1 : 0;
    }
    """

    prg = cl.Program(ctx, kernel_code).build()

    results = np.zeros(len(a_values), dtype=np.uint64)
    a_values_buffer = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=a_values)
    results_buffer = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, results.nbytes)

    prg.fermat_test(queue, (len(a_values),), None, results_buffer, np.uint64(n), a_values_buffer, np.uint32(len(a_values)))

    # Czytanie wynikow z bufora
    cl.enqueue_copy(queue, results, results_buffer).wait()

    return results

def main():
    # Liczba do testowania (n)
    n = 561

    # Liczba testow i generowanie losowych wartosci
    num_tests = 5
    a_values = np.random.randint(2, n, size=num_tests, dtype=np.uint64)

    platform = cl.get_platforms()[0]
    device = platform.get_devices()[0]
    ctx = cl.Context([device])
    queue = cl.CommandQueue(ctx)

    results = fermat_test(n, a_values, ctx, queue)

    # Wyniki
    for i, result in enumerate(results):
        if result == 1:
            print(f"Dla a = {a_values[i]}, {n} jest liczba prawdopodobnie pierwsza.")
        else:
            print(f"For a = {a_values[i]}, {n} jest liczba zlozona.")

if __name__ == "__main__":
    main()
