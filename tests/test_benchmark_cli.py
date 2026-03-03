import os
import pathlib
import subprocess
import sys
import tempfile
import unittest
import importlib.util


HAS_MATPLOTLIB = importlib.util.find_spec("matplotlib") is not None


@unittest.skipUnless(HAS_MATPLOTLIB, "matplotlib is required to run benchmark CLI")
class TestBenchmarkCLI(unittest.TestCase):
    """Validate benchmark CLI runs successfully and writes the graph output file."""

    def test_cli_smoke_run(self) -> None:
        """Run the benchmark CLI with minimal settings and verify output artifacts."""
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
                    "--thread-counts",
                    "1",
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


if __name__ == "__main__":
    unittest.main()
