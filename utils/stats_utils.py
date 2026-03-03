import math

from utils.threads_utils import threads_manager


def average(values: list[float]) -> float:
    '''Return the arithmetic mean of a list of numeric values.'''
    return sum(values) / len(values)


def standard_deviation(values: list[float]) -> float:
    '''Return the sample standard deviation of a list of numeric values.'''
    if len(values) < 2:
        return 0.0

    mean_value = average(values)
    squared_differences = 0.0
    for value in values:
        difference = value - mean_value
        squared_differences += difference * difference

    variance = squared_differences / (len(values) - 1)
    return math.sqrt(variance)


def statistics_calculator(worker, thread_count: int, duration_seconds: float) -> tuple[list[float], float, float]:
    '''Run one benchmark configuration 3 times and return runs, average, and standard deviation.'''
    ops_per_second_runs = []

    for _ in range(3):
        _, _, ops_per_second = threads_manager(worker, thread_count, duration_seconds)
        ops_per_second_runs.append(ops_per_second)

    avg_ops_per_second = average(ops_per_second_runs)
    sd_ops_per_second = standard_deviation(ops_per_second_runs)

    return ops_per_second_runs, avg_ops_per_second, sd_ops_per_second
