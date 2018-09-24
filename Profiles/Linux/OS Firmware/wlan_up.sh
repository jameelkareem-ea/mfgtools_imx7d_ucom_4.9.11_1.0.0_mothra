#/bin/sh

if [ -z "$1" ]; then
	echo "Usage:"
	echo "   $0 <if name>"
	echo
	exit
fi
echo "Using $1"

ifconfig $1 up
wpa_supplicant -i $1 -D nl80211 -c /etc/wpa_supplicant.conf -B

read -p "Press y when connected to network? " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "No network, aborting"
	exit
fi
udhcpc -i $1
wl -i $1 frameburst 1
wl -i $1 PM 0
echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq
wl -i $1 scansuppress
wl -i $1 scansuppress 1

echo "Done with configuration"
echo "Run performance test with:"
echo
echo "iperf3 -c 192.168.1.128 -i 1 -P 4"
echo
