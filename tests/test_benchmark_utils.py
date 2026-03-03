import time
import unittest

from utils.cli_utils import normalize_output_file, parse_thread_counts
from utils.stats_utils import average, standard_deviation
from utils.threads_utils import float_worker, integer_worker, threads_manager


class TestBenchmarkUtils(unittest.TestCase):
    """Validate helper behavior in cli_utils, stats_utils, and threads_utils."""

    def test_average(self) -> None:
        """average returns the expected mean value."""
        self.assertAlmostEqual(average([1.0, 2.0, 3.0]), 2.0)

    def test_standard_deviation_sample(self) -> None:
        """standard_deviation returns sample SD for multi-value input."""
        self.assertAlmostEqual(standard_deviation([1.0, 2.0, 3.0]), 1.0)

    def test_standard_deviation_single_value(self) -> None:
        """standard_deviation handles single-value input."""
        self.assertEqual(standard_deviation([42.0]), 0.0)

    def test_parse_thread_counts(self) -> None:
        """parse_thread_counts parses comma-separated thread values."""
        self.assertEqual(parse_thread_counts("1, 2, 4, 8"), [1, 2, 4, 8])

    def test_normalize_output_file_simple_name(self) -> None:
        """normalize_output_file applies default directory and extension."""
        self.assertEqual(normalize_output_file("mygraph"), "benchmarks/mygraph.png")

    def test_normalize_output_file_with_directory(self) -> None:
        """normalize_output_file keeps directory and appends extension."""
        self.assertEqual(normalize_output_file("reports/graph"), "reports/graph.png")

    def test_normalize_output_file_png_kept(self) -> None:
        """normalize_output_file preserves already-normalized png paths."""
        self.assertEqual(normalize_output_file("benchmarks/plot.png"), "benchmarks/plot.png")

    def test_integer_worker_writes_totals_slot(self) -> None:
        """integer_worker stores operation count in totals at the given index."""
        totals = [0]
        stop_time = time.perf_counter() + 0.02

        integer_worker(stop_time, totals, 0)

        self.assertGreater(totals[0], 0)

    def test_float_worker_writes_totals_slot(self) -> None:
        """float_worker stores operation count in totals at the given index."""
        totals = [0]
        stop_time = time.perf_counter() + 0.02

        float_worker(stop_time, totals, 0)

        self.assertGreater(totals[0], 0)

    def test_threads_manager_aggregates_worker_results(self) -> None:
        """threads_manager aggregates per-thread totals and computes throughput."""
        def fixed_worker(_stop_time: float, totals: list[int], index: int) -> None:
            totals[index] = 10

        elapsed, total_operations, ops_per_second = threads_manager(
            worker=fixed_worker,
            thread_count=4,
            duration_seconds=0.01,
        )

        self.assertGreater(elapsed, 0.0)
        self.assertEqual(total_operations, 40)
        self.assertGreater(ops_per_second, 0.0)


if __name__ == "__main__":
    unittest.main()
