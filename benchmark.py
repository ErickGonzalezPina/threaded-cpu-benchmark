import argparse
from utils.threads_utils import float_worker, integer_worker
from utils.plot_utils import create_performance_graph
from utils.cli_utils import normalize_output_file, parse_thread_counts
from utils.stats_utils import statistics_calculator


def run_benchmark_series(
    worker,
    thread_counts: list[int],
    duration_seconds: float,
    benchmark_title: str,
    ops_label: str,
    giga_label: str,
) -> tuple[list[float], list[float]]:
    '''Run one benchmark type across all thread counts, print results to CLI and return giga avg/sd lists.'''
    avg_giga_values = []
    sd_giga_values = []

    print(benchmark_title)
    for thread_count in thread_counts:
        runs, avg_ops, sd_ops = statistics_calculator(
            worker=worker,
            thread_count=thread_count,
            duration_seconds=duration_seconds,
        )

        # Calculate GIOPS/GFLOPS
        avg_giga = avg_ops / 1e9
        sd_giga = sd_ops / 1e9

        print(
            f"Threads: {thread_count} | "
            f"Run {ops_label}: {[round(value, 2) for value in runs]} | "
            f"Avg {ops_label}: {avg_ops:,.2f} ({avg_giga:.6f} {giga_label}) | "
            f"SD: {sd_ops:,.2f} ({sd_giga:.6f} {giga_label})"
        )

        avg_giga_values.append(avg_giga)
        sd_giga_values.append(sd_giga)

    return avg_giga_values, sd_giga_values


def main(duration_seconds: float, thread_counts: list[int], output_file: str) -> None:
    '''Run all benchmark configurations, print statistics, and generate the comparison graph.'''
    # Integer Benchmark
    integer_avg_giops, integer_sd_giops = run_benchmark_series(
        worker=integer_worker,
        thread_counts=thread_counts,
        duration_seconds=duration_seconds,
        benchmark_title="Integer benchmark (threaded)",
        ops_label="IOPS",
        giga_label="GIOPS",
    )

    print()

    # Float Benchmark
    float_avg_gflops, float_sd_gflops = run_benchmark_series(
        worker=float_worker,
        thread_counts=thread_counts,
        duration_seconds=duration_seconds,
        benchmark_title="Float benchmark (threaded)",
        ops_label="FLOPS",
        giga_label="GFLOPS",
    )

    # Creates the comparison graph
    create_performance_graph(
        thread_counts=thread_counts,
        integer_avg_giops=integer_avg_giops,
        integer_sd_giops=integer_sd_giops,
        float_avg_gflops=float_avg_gflops,
        float_sd_gflops=float_sd_gflops,
        output_file=output_file,
    )
    print(f"\nComparison graph has been saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Threaded integer/float benchmarking")
    parser.add_argument(
        "--duration-seconds",
        type=float,
        default=3.0,
        help="Duration of each benchmark run in seconds (default: 3.0)",
    )
    parser.add_argument(
        "--thread-counts",
        type=str,
        default="1,2,4,8",
        help="Comma-separated thread counts (default: 1,2,4,8)",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default="benchmarks/benchmark_performance.png",
        help="Output graph filename (default: benchmarks/benchmark_performance.png)",
    )
    args = parser.parse_args()

    main(
        duration_seconds=args.duration_seconds,
        thread_counts=parse_thread_counts(args.thread_counts),
        output_file=normalize_output_file(args.output_file),
    )

