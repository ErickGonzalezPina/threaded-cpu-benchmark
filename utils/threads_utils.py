import threading
import time


def integer_worker(stop_time: float, totals: list[int], index: int) -> None:
    '''Run integer operations until stop_time and store this thread's total operations.'''
    value = 1 + index
    iterations = 0

    while time.perf_counter() < stop_time:
        value = value * 3
        value = value + 7
        value = value - 5
        value = value // 3
        value = value * 2
        iterations += 1

    totals[index] = iterations * 5


def float_worker(stop_time: float, totals: list[int], index: int) -> None:
    '''Run floating-point operations until stop_time and store this thread's total operations.'''
    value = 1.0 + float(index)
    iterations = 0

    while time.perf_counter() < stop_time:
        value = value * 3.0
        value = value + 7.0
        value = value - 5.0
        value = value / 3.0
        value = value * 2.0
        iterations += 1

    totals[index] = iterations * 5


def threads_manager(worker, thread_count: int, duration_seconds: float) -> tuple[float, int, float]:
    '''Start worker threads, wait for completion, and return elapsed time and throughput.'''
    totals = [0] * thread_count
    threads = []

    start = time.perf_counter()
    stop_time = start + duration_seconds

    for index in range(thread_count):
        thread = threading.Thread(target=worker, args=(stop_time, totals, index))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    elapsed = time.perf_counter() - start
    total_operations = sum(totals)
    ops_per_second = total_operations / elapsed
    return elapsed, total_operations, ops_per_second
