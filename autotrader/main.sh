#!/usr/bin/env bash

source /home/brian/mambaforge/etc/profile.d/conda.sh
conda activate autoscraper

python -u /home/brian/autoscraper/autotrader/main.py scrape \
	--password "${AUTOTRADER_PW:-autotrader}"

