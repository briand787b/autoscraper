#!/usr/bin/env bash

sudo cp carmax.service carmax.timer /etc/systemd/system
sudo systemctl enable carmax.timer
sudo systemctl start carmax.timer