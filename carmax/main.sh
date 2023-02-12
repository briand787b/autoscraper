#!/usr/bin/env bash

source /home/brian/mambaforge/etc/profile.d/conda.sh
conda activate autoscraper

python -u /home/brian/autoscraper/carmax/carmax.py scrape \
	--password "${CARMAX_PW:-carmax}"

