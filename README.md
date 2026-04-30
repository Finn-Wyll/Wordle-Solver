<!-- prettier-ignore -->
# 🎯 Wordle-Solver

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A compact, research-friendly Wordle solver and automation toolkit — fast, reproducible, and ready for experiments. This repository contains the solver core, sample data, and an optional browser automation example.

✨ Highlights
- Small, readable solver logic in `wordle.py` with interactive and programmatic APIs
- Precomputed frequency and entropy maps in `data/`
- Optional browser automation example (`Wordle-Solver.py`) using Selenium
- Included `cache.json` to speed repeated runs (see caching section)

Contents
- `wordle.py` — solver functions (interactive and auto modes)
- `Wordle-Solver.py` — example Selenium automation (optional)
- `data/freq_map.json` — frequency-ranked candidate words
- `data/entropy_map.json` — precomputed entropy values
- `cache.json` — runtime cache (included)
- `requirements.txt` — Python dependencies
- `LICENSE` — MIT license

Getting started
----------------

1. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Try the interactive solver:

```bash
python -c "import wordle; wordle.start()"
```

Automated example (optional)
---------------------------

`Wordle-Solver.py` demonstrates driving the NYT Wordle UI with Selenium. This is an example only — verify you comply with the NYT terms before using automation. Requires Chrome + chromedriver on `PATH`.

```bash
python Wordle-Solver.py
```

Caching (notes)
---------------

- `cache.json` is included in this repository to speed metric computations during demonstrations and offline experiments.
- If you want a fresh run with no cache interaction (for CI or reproducibility), set the environment variable:

```bash
export WORDLE_DISABLE_CACHE=1
python -c "import wordle; wordle.start()"
```

Or override the cache path with:

```bash
export WORDLE_CACHE_FILE=my_cache.json
```

Developer notes
---------------

- Core algorithm: the solver evaluates candidate guesses by expected remaining-word count (see `calc_feedback` / `calc_entropy`).
- The included `freq_map.json` contains ~13k candidate words used for scoring; tests and smaller sample lists are recommended for fast iteration.
- Consider adding a small `tests/` suite (pytest) and a GitHub Actions workflow that runs tests and linting.

Recommended next steps
----------------------

- Add a `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` if you plan to welcome external contributors.
- Add unit tests for `wordle.py` to validate core functions (`green_letter`, `yellow_letter`, `handle_black`, and `calc_feedback`).
- Add a lightweight CI job to run tests on push and PRs.

Contact & support
-----------------

Open an issue or submit a PR on GitHub: https://github.com/Finn-Wyll/Wordle-Solver

License
-------

This project is distributed under the MIT License — see `LICENSE`.
