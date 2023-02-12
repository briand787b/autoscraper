#!/usr/bin/env bash

sudo cp autotrader.service autotrader.timer /etc/systemd/system
sudo systemctl enable autotrader.timer
sudo systemctl start autotrader.timer