#!/usr/bin/env bash

source /home/brian/mambaforge/etc/profile.d/conda.sh
conda activate autoscraper

mkdir -p /var/opt/autoscraper/carvana

python -u /home/brian/autoscraper/carvana/carvana.py scrape \
	--password "${CARVANA_PW:-carvana}"

