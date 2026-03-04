import os
import pathlib
import subprocess
import sys
import tempfile
import unittest


class TestBenchmarkCLI(unittest.TestCase):
    """Validate benchmark CLI runs successfully and writes the graph output file."""

    def test_cli_threaded_mode(self) -> None:
        """Run benchmark CLI in threaded mode and verify output artifacts."""

        project_root = pathlib.Path(__file__).resolve().parents[1]
        script_path = project_root / "benchmark.py"
        graph_output_path = "benchmarks/benchmark_performance.png"

        env = os.environ.copy()
        env.setdefault("MPLBACKEND", "Agg")

        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [
                    sys.executable,
                    str(script_path),
                    "--duration-seconds",
                    "0.1",
                    "--worker-counts",
                    "1",
                    "--mode",
                    "threaded",
                    "--output-file",
                    graph_output_path,
                ],
                cwd=temp_dir,
                env=env,
                capture_output=True, 
                text=True,
                timeout=120,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("Integer benchmark (threaded)", result.stdout)
            self.assertIn("Float benchmark (threaded)", result.stdout)

            output_graph = pathlib.Path(temp_dir) / graph_output_path
            self.assertTrue(output_graph.exists(), "Expected benchmark graph file to be created")

    def test_cli_process_mode(self) -> None:
        """Run benchmark CLI in process mode and verify output artifacts."""

        project_root = pathlib.Path(__file__).resolve().parents[1]
        script_path = project_root / "benchmark.py"
        graph_output_path = "benchmarks/benchmark_performance_process.png"

        env = os.environ.copy()
        env.setdefault("MPLBACKEND", "Agg")

        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [
                    sys.executable,
                    str(script_path),
                    "--duration-seconds",
                    "0.1",
                    "--worker-counts",
                    "1",
                    "--mode",
                    "process",
                    "--output-file",
                    graph_output_path,
                ],
                cwd=temp_dir,
                env=env,
                capture_output=True,
                text=True,
                timeout=120,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("Integer benchmark (process)", result.stdout)
            self.assertIn("Float benchmark (process)", result.stdout)

            output_graph = pathlib.Path(temp_dir) / graph_output_path
            self.assertTrue(output_graph.exists(), "Expected benchmark graph file to be created")

    def test_cli_both_mode(self) -> None:
        """Run benchmark CLI in both mode and verify comparison output artifacts."""

        project_root = pathlib.Path(__file__).resolve().parents[1]
        script_path = project_root / "benchmark.py"
        graph_output_path = "benchmarks/benchmark_performance_both.png"

        env = os.environ.copy()
        env.setdefault("MPLBACKEND", "Agg")

        with tempfile.TemporaryDirectory() as temp_dir:
            result = subprocess.run(
                [
                    sys.executable,
                    str(script_path),
                    "--duration-seconds",
                    "0.1",
                    "--worker-counts",
                    "1",
                    "--mode",
                    "both",
                    "--output-file",
                    graph_output_path,
                ],
                cwd=temp_dir,
                env=env,
                capture_output=True,
                text=True,
                timeout=120,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("Integer benchmark (threaded)", result.stdout)
            self.assertIn("Integer benchmark (process)", result.stdout)
            self.assertIn("IOPS gain at 1 workers", result.stdout)

            output_graph = pathlib.Path(temp_dir) / graph_output_path
            self.assertTrue(output_graph.exists(), "Expected benchmark graph file to be created")


if __name__ == "__main__":
    unittest.main()
