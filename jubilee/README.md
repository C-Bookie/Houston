

connecting to serial
ls /dev/cu.usbserial-*
screen /dev/cu.usbserial-0001 115200
screen /dev/cu.usbserial-A50285BI 115200

screen /dev/cu.usbserial-142100 115200


to disable hotspot
comment out last lines in dhcpcd.conf
sudo systemctl disable hostapd
sudo systemctl mask hostapd
sudo systemctl disable dnsmasq
sudo systemctl mask dnsmasq

reboot

hostapd

pio run --target upload --upload-port /dev/cu.usbserial-0001

/dev/cu.usbserial-0001
/dev/cu.usbserial-142100
/dev/cu.usbserial-142101

