import os
import matplotlib.pyplot as plt


def create_performance_graph(
    thread_counts: list[int],
    integer_avg_giops: list[float],
    integer_sd_giops: list[float],
    float_avg_gflops: list[float],
    float_sd_gflops: list[float],
    output_file: str,
) -> None:
    '''Create and save a throughput graph with error bars for integer and float benchmarks.'''
    output_directory = os.path.dirname(output_file)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    plt.figure(figsize=(9, 6))

    plt.errorbar(
        thread_counts,
        integer_avg_giops,
        yerr=integer_sd_giops,
        marker="o",
        capsize=5,
        linewidth=2,
        label="Integer (GIOPS)",
    )

    plt.errorbar(
        thread_counts,
        float_avg_gflops,
        yerr=float_sd_gflops,
        marker="s",
        capsize=5,
        linewidth=2,
        label="Float (GFLOPS)",
    )

    plt.title("CPU Throughput vs Thread Count")
    plt.xlabel("Thread Count")
    plt.ylabel("Throughput (Giga Operations per Second)")
    plt.xticks(thread_counts)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()
