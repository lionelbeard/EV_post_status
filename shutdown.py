#!/usr/bin/python3

import pijuice, os
import datetime, time
import subprocess

while not os.path.exists('/dev/i2c-1'):
    time.sleep(0.1)

# access to pijuice and wait for valid data
PiJuice_OK = False
pj = pijuice.PiJuice(1, 0x14)
while PiJuice_OK == False:
    try:
        current = float(pj.status.GetIoCurrent()['data'])/1000
        PiJuice_OK = True
    except KeyError:
        pass
        
# Rely on RTC to keep the time
cmd = "sudo hwclock --hctosys"
os.system(cmd)

DELTA_MIN = 10
d_wake = dict()
d_wake['year'] = 'EVERY_YEAR'
d_wake['month'] = 'EVERY_MONTH'
d_wake['day'] = 'EVERY_DAY'
d_wake['hour'] = 'EVERY_HOUR'
t = datetime.datetime.utcnow()
d_wake['minute'] = (t.minute + DELTA_MIN) % 60
d_wake['second'] = 0

status = pj.rtcAlarm.SetAlarm(d_wake)
if status['error'] != 'NO_ERROR':
    print('Cannot set alarm\n')
    sys.exit()
else:
    print('Alarm set for ' + str(pj.rtcAlarm.GetAlarm()) + '\n')
    
#time.sleep(180)

# Enable wakeup, otherwise power to the RPi will not be
# applied when the RTC alarm goes off
pj.rtcAlarm.SetWakeupEnabled(True)

# clear alarm flag
pj.rtcAlarm.ClearAlarmFlag()

# PiJuice shuts down power to Rpi after 30 sec from now
# This leaves sufficient time to execute the shutdown sequence

pj.power.SetPowerOff(30)
subprocess.call(["sudo", "poweroff"])
