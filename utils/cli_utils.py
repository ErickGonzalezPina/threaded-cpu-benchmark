import os


def parse_thread_counts(thread_counts_text: str) -> list[int]:
    '''Parse a comma-separated thread-count string into a list of integers.'''
    return [int(value.strip()) for value in thread_counts_text.split(",") if value.strip()]


def normalize_output_file(output_file: str) -> str:
    '''Normalize output path: default to benchmarks/ and ensure .png extension.'''
    cleaned = output_file.strip()
    if not cleaned:
        return "benchmarks/benchmark_performance.png"

    directory = os.path.dirname(cleaned)
    filename = os.path.basename(cleaned)

    if not filename.lower().endswith(".png"):
        filename = f"{filename}.png"

    if directory:
        return os.path.join(directory, filename)
    return os.path.join("benchmarks", filename)
