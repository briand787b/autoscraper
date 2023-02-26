#!/usr/bin/env bash

sudo cp carvana.service carvana.timer /etc/systemd/system
sudo systemctl enable carvana.timer
sudo systemctl start carvana.timer