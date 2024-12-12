# AOC Stats
Private leaderboard data visualizer for AdventOfCode

## Environment Setup
From the top of the repo do the following:
* Initialize python virtual environment: `python3 -m venv .venv`
* Activate venv: `source .venv/bin/activate`
* Setup venv: `pip3 install -r requirements.txt`

## Configure
Edit `config.py` with the following configuration:
* `AOC_URL`: JSON endpoint for the private leaderboard
* `AOC_SESSION`: session key for AdventOfCode (pull from your browser cookie)

## How To Run
Run locally with `bin/aoc_stats.`  Access `localhost:8000` in your browser.
