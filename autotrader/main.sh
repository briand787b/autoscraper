#!/usr/bin/env bash

source "${MAMBA_PATH:-'/home/brian/mambaforge'}/bin/activate autoscraper"

## diagnostic stuff
# mamba info
# echo the script ran!!!
# exit 0

python -u /home/brian/autoscraper/autotrader/main.py scrape \
	--password "${AUTOTRADER_PW:-autotrader}"

