import argparse
from typing import Callable

from utils.processes_utils import float_process_worker, integer_process_worker, processes_manager
from utils.threads_utils import float_worker, integer_worker, threads_manager
from utils.plot_utils import create_performance_graph
from utils.cli_utils import normalize_output_file, parse_thread_counts
from utils.stats_utils import statistics_calculator


def run_benchmark_series(
    worker,
    manager: Callable,
    worker_counts: list[int],
    duration_seconds: float,
    benchmark_title: str,
    worker_label: str,
    ops_label: str,
    giga_label: str,
) -> tuple[list[float], list[float]]:
    '''Run one benchmark type across all worker counts, print results to CLI and return giga avg/sd lists.'''
    avg_giga_values = []
    sd_giga_values = []

    print(benchmark_title)
    for worker_count in worker_counts:
        runs, avg_ops, sd_ops = statistics_calculator(
            worker=worker,
            worker_count=worker_count,
            duration_seconds=duration_seconds,
            manager=manager,
        )

        # Calculate GIOPS/GFLOPS
        avg_giga = avg_ops / 1e9
        sd_giga = sd_ops / 1e9

        print(
            f"{worker_label}: {worker_count} | "
            f"Run {ops_label}: {[round(value, 2) for value in runs]} | "
            f"Avg {ops_label}: {avg_ops:,.2f} ({avg_giga:.6f} {giga_label}) | "
            f"SD: {sd_ops:,.2f} ({sd_giga:.6f} {giga_label})"
        )

        avg_giga_values.append(avg_giga)
        sd_giga_values.append(sd_giga)

    return avg_giga_values, sd_giga_values


def threaded_benchmark(duration_seconds: float, thread_counts: list[int], output_file: str) -> None:
    '''Run threaded benchmark configurations, print statistics, and generate the comparison graph.'''

    # Integer Benchmark
    integer_avg_giops, integer_sd_giops = run_benchmark_series(
        worker=integer_worker,
        manager=threads_manager,
        worker_counts=thread_counts,
        duration_seconds=duration_seconds,
        benchmark_title="Integer benchmark (threaded)",
        worker_label="Threads",
        ops_label="IOPS",
        giga_label="GIOPS",
    )

    print()

    # Float Benchmark
    float_avg_gflops, float_sd_gflops = run_benchmark_series(
        worker=float_worker,
        manager=threads_manager,
        worker_counts=thread_counts,
        duration_seconds=duration_seconds,
        benchmark_title="Float benchmark (threaded)",
        worker_label="Threads",
        ops_label="FLOPS",
        giga_label="GFLOPS",
    )

    # Create Graph
    create_performance_graph(
        thread_counts=thread_counts,
        integer_avg_giops=integer_avg_giops,
        integer_sd_giops=integer_sd_giops,
        float_avg_gflops=float_avg_gflops,
        float_sd_gflops=float_sd_gflops,
        output_file=output_file,
        mode_label= "threaded",
    )
    print(f"\nComparison graph has been saved to {output_file}")


def processes_benchmark(duration_seconds: float, process_counts: list[int], output_file: str) -> None:
    '''Run process benchmark configurations, print statistics, and generate the comparison graph.'''

    # Integer Benchmark
    integer_avg_giops, integer_sd_giops = run_benchmark_series(
        worker=integer_process_worker,
        manager=processes_manager,
        worker_counts=process_counts,
        duration_seconds=duration_seconds,
        benchmark_title="Integer benchmark (process)",
        worker_label="Processes",
        ops_label="IOPS",
        giga_label="GIOPS",
    )

    print()

    # Float Benchmark
    float_avg_gflops, float_sd_gflops = run_benchmark_series(
        worker=float_process_worker,
        manager=processes_manager,
        worker_counts=process_counts,
        duration_seconds=duration_seconds,
        benchmark_title="Float benchmark (process)",
        worker_label="Processes",
        ops_label="FLOPS",
        giga_label="GFLOPS",
    )

    # Create Graph
    create_performance_graph(
        thread_counts=process_counts,
        integer_avg_giops=integer_avg_giops,
        integer_sd_giops=integer_sd_giops,
        float_avg_gflops=float_avg_gflops,
        float_sd_gflops=float_sd_gflops,
        output_file=output_file,
        mode_label="process",
    )
    print(f"\nComparison graph has been saved to {output_file}")


def threaded_vs_processes_benchmark(duration_seconds: float, worker_counts: list[int], output_file: str):
    '''Run threaded and process benchmarks side-by-side, print comparative stats, and save a graph comparing results.'''

    mode_config = {
        "threaded": {
            "integer_worker": integer_worker,
            "float_worker": float_worker,
            "manager": threads_manager,
            "worker_label": "Threads",
            "name": "threaded",
        },
        "process": {
            "integer_worker": integer_process_worker,
            "float_worker": float_process_worker,
            "manager": processes_manager,
            "worker_label": "Processes",
            "name": "process",
        },
    }
    threaded_config = mode_config["threaded"]
    process_config = mode_config["process"]

    # Threaded Integer Benchmark
    threaded_integer_avg, threaded_integer_sd = run_benchmark_series(
        worker=threaded_config["integer_worker"],
        manager=threaded_config["manager"],
        worker_counts= worker_counts,
        duration_seconds=duration_seconds,
        benchmark_title="Integer benchmark (threaded)",
        worker_label=threaded_config["worker_label"],
        ops_label="IOPS",
        giga_label="GIOPS",
    )

    print()

    # Threaded Float Benchmark
    threaded_float_avg, threaded_float_sd = run_benchmark_series(
        worker=threaded_config["float_worker"],
        manager=threaded_config["manager"],
        worker_counts= worker_counts,
        duration_seconds=duration_seconds,
        benchmark_title="Float benchmark (threaded)",
        worker_label=threaded_config["worker_label"],
        ops_label="FLOPS",
        giga_label="GFLOPS",
    )

    print()

    # Processes Integer Benchmark
    process_integer_avg, process_integer_sd = run_benchmark_series(
        worker=process_config["integer_worker"],
        manager=process_config["manager"],
        worker_counts= worker_counts,
        duration_seconds=duration_seconds,
        benchmark_title="Integer benchmark (process)",
        worker_label=process_config["worker_label"],
        ops_label="IOPS",
        giga_label="GIOPS",
    )

    print()
    
    # Processes Float Benchmark
    process_float_avg, process_float_sd = run_benchmark_series(
        worker=process_config["float_worker"],
        manager=process_config["manager"],
        worker_counts= worker_counts,
        duration_seconds=duration_seconds,
        benchmark_title="Float benchmark (process)",
        worker_label=process_config["worker_label"],
        ops_label="FLOPS",
        giga_label="GFLOPS",
    )

    # Create Comparison Graph
    create_performance_graph(
        thread_counts= worker_counts,
        integer_avg_giops=threaded_integer_avg,
        integer_sd_giops=threaded_integer_sd,
        float_avg_gflops=threaded_float_avg,
        float_sd_gflops=threaded_float_sd,
        output_file=output_file,
        process_integer_avg_giops=process_integer_avg,
        process_integer_sd_giops=process_integer_sd,
        process_float_avg_gflops=process_float_avg,
        process_float_sd_gflops=process_float_sd,
    )

    # Integer throughput Gains
    threaded_integer_last = threaded_integer_avg[-1]
    process_integer_last = process_integer_avg[-1]
    # Percent gain formula: ((process - threaded) / threaded) * 100
    iops_gain_pct = ((process_integer_last - threaded_integer_last) / threaded_integer_last) * 100
    iops_scale = process_integer_last / threaded_integer_last

    # Floating-point throughput Gains
    threaded_float_last = threaded_float_avg[-1]
    process_float_last = process_float_avg[-1]
    # Percent gain formula: ((process - threaded) / threaded) * 100
    flops_gain_pct = ((process_float_last - threaded_float_last) / threaded_float_last) * 100
    flops_scale = process_float_last / threaded_float_last

    worker_count = worker_counts[-1]

    print()

    # Print Performance Gains 
    print(
        f"IOPS gain at {worker_count} workers (process vs threaded): "
        f"{iops_gain_pct:.2f}% ({iops_scale:.2f}x)"
    )
    print(
        f"FLOPS gain at {worker_count} workers (process vs threaded): "
        f"{flops_gain_pct:.2f}% ({flops_scale:.2f}x)"
    )
    print(f"\nComparison graph has been saved to {output_file}")
    return


def main(duration_seconds: float, worker_counts: list[int], output_file: str, mode: str) -> None:
    '''Run benchmark in threaded, process, or both modes.'''

    if mode == "threaded":
        threaded_benchmark(duration_seconds=duration_seconds, thread_counts=worker_counts, output_file=output_file)
        return
    if mode == "process":
        processes_benchmark(duration_seconds=duration_seconds, process_counts=worker_counts, output_file=output_file)
        return
    if mode == "both":
        threaded_vs_processes_benchmark(duration_seconds=duration_seconds, worker_counts=worker_counts, output_file=output_file)
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Threaded integer/float benchmarking")
    parser.add_argument(
        "--duration-seconds",
        type=float,
        default=3.0,
        help="Duration of each benchmark run in seconds (default: 3.0)",
    )
    parser.add_argument(
        "--worker-counts",
        type=str,
        default="1,2,4,8",
        help="Comma-separated worker counts (default: 1,2,4,8)",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default="benchmarks/benchmark_performance.png",
        help="Output graph filename (default: benchmarks/benchmark_performance.png)",
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["threaded", "process", "both"],
        default="threaded",
        help="Execution mode: threaded, process, or both (default: threaded)",
    )
    args = parser.parse_args()

    main(
        duration_seconds=args.duration_seconds,
        worker_counts=parse_thread_counts(args.worker_counts),
        output_file=normalize_output_file(args.output_file),
        mode=args.mode,
    )

