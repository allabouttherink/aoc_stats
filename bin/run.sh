#! /usr/bin/env bash
#
# Assume activated vEnv and working directory is aoc_stats
#

gunicorn aoc_stats:app --log-file=gunicorn.log
