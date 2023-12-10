import pyopencl as cl
import numpy as np
import random
import time

platform = cl.get_platforms()[0]
device = platform.get_devices()[0]
context = cl.Context([device])
queue = cl.CommandQueue(context, properties=cl.command_queue_properties.PROFILING_ENABLE)

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

prg = cl.Program(context, kernel_code).build()



def fermat_test_gpu(n, k, ctx, queue):

    results = np.zeros(k, dtype=np.uint64)
    a_values = np.random.randint(2, n, size=k, dtype=np.uint64)

    a_values_buffer = cl.Buffer(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=a_values)
    results_buffer = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, results.nbytes)

    prg.fermat_test(queue, (k,), None, results_buffer, np.uint64(n), a_values_buffer, np.uint32(k))

    # Read the results from the buffer
    cl.enqueue_copy(queue, results, results_buffer).wait()

    return all(result == 1 for result in results)

def main():

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
            is_prime = fermat_test_gpu(n, k, context, queue)
            end_time = time.time()

            execution_time = end_time - start_time
            total_execution_time += execution_time

            print(f"Test fermata gpu, test {_ + 1}/{num_repeats}, czas: {execution_time:.4f}s, rezultat: {n} is prime: {is_prime}")

        average_execution_time = total_execution_time / num_repeats

        print(f"Range: {range_name}, Number of Repeats: {num_repeats}, Average Execution Time: {average_execution_time:.10f} seconds\n")

if __name__ == "__main__":
    main()
