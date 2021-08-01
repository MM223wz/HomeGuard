# Runs at boot
import machine
import uos as os
import _keys as keys
import utime as time
from network import WLAN

uart = machine.UART(0, baudrate=115200)
os.dupterm(uart)

# Connect to Wifi
wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
    if net.ssid == keys.WIFI_SSID:
        print('Wifi network found.')
        wlan.connect(net.ssid, auth=(net.sec, keys.WIFI_PASS), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('Wifi connection succeeded.')
        break

# Sync RTC - Real Time Clock
rtc = machine.RTC()
rtc.ntp_sync("pool.ntp.org")
while not rtc.synced():
    machine.idle()
# Adjust your local timezone, by default, NTP time will be GMT
time.timezone(1*60**2) # GMT+1: 1*60*60
print('RTC synced with NTP time: {}'.format(time.localtime()))

machine.main('main.py')
