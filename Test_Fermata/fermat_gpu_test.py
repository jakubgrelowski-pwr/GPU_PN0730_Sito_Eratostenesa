import pyopencl as cl
import numpy as np
import sys
import time

def fermat_test_gpu(n, k, ctx, queue):
    kernel_code = """
    __kernel void fermat_test(__global ulong* results, ulong n, __global ulong* a_values) {
        int gid = get_global_id(0);
        ulong x = 1;
        for (ulong i = 0; i < n - 1; i++) {
            x = (x * a_values[gid]) % n;
        }
        results[gid] = (x == 1) ? 1 : 0;
    }
    """

    prg = cl.Program(ctx, kernel_code).build()

    a_values = np.random.randint(2, n, size=k, dtype=np.uint64)
    results = np.zeros(k, dtype=np.uint64)
    a_values_buffer = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=a_values)
    results_buffer = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, results.nbytes)

    prg.fermat_test(queue, (k,), None, results_buffer, np.uint64(n), a_values_buffer)

    cl.enqueue_copy(queue, results, results_buffer).wait()

    return all(result == 1 for result in results)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uzycie: python fermat_gpu_test.py <liczba_do_przetestowania> <liczba_iteracji>")
        sys.exit(1)

    n = int(sys.argv[1])
    k = int(sys.argv[2])

    platform = cl.get_platforms()[0]
    device = platform.get_devices()[0]
    ctx = cl.Context([device])
    queue = cl.CommandQueue(ctx)

    is_prime = fermat_test_gpu(n, k, ctx, queue)

    result_text = f"{n} jest prawdopodobnie liczba pierwsza." if is_prime else f"{n} nie jest liczba pierwsza."
    print(result_text)
