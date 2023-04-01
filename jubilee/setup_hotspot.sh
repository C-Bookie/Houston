#!/usr/bin/env bash

echo "Setting-up hotspot..."

# https://thepi.io/how-to-use-your-raspberry-pi-as-a-wireless-access-point/
# https://hawksites.newpaltz.edu/myerse/2018/06/08/hostapd-on-raspberry-pi/comment-page-1/

#sudo apt-get install hostapd
#sudo apt-get install dnsmasq

sudo systemctl disable hostapd
sudo systemctl mask hostapd
sudo systemctl disable dnsmasq
sudo systemctl mask dnsmasq

sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl unmask dnsmasq
sudo systemctl enable dnsmasq

#sudo systemctl unmask hostapd
#sudo systemctl enable hostapd
#sudo systemctl disable hostapd
#sudo systemctl stop hostapd
#sudo systemctl start hostapd
#sudo systemctl restart hostapd

#sudo /usr/sbin/hostapd /etc/hostapd/hostapd.conf

# may just need to restart on a delay
# https://raspberrypi.stackexchange.com/questions/87759/hostapd-dont-start-at-boot

echo "setup hotspot"
