#!/usr/bin/env bash

source /home/brian/mambaforge/etc/profile.d/conda.sh
conda activate autoscraper

python -u /home/brian/autoscraper/carvana/carvana.py scrape \
	--password "${CARVANA_PW:-carvana}"

