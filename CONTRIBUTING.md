# Contributing

Thanks for your interest in improving this project.

## Development setup

1. Create and activate a virtual environment:
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
2. Install dependencies:
   - `pip install -r requirements.txt`

## Run benchmark

- `python benchmark.py --duration-seconds 3 --thread-counts 1,2,4,8`

## Pull request guidelines

- Keep changes small and focused.
- Prefer clear function names and comments for benchmark logic.
- Preserve command-line compatibility unless necessary.
- Update `README.md` when behavior or usage changes.
