#!/usr/bin/env bash

# todo rename to setup

echo "Setting up project jubliee..."

crontab -e
crontab -l

# https://bc-robotics.com/tutorials/setting-cron-job-raspberry-pi/
@reboot sleep 20; sudo systemctl restart hostapd
@reboot sleep 30; cd /home/pi/Houston/jubilee && sudo -u pi tmux new-session -d -s "jubliee" "python3 ./jubliee.py && bash"

echo "Set up project jubliee"
