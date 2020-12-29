#!/bin/bash


SOC=`python /home/pi/EV_post_status/ioniq_soc.py`

# Sync RTC time
hwclock -s

DATE=`date`

PIJUICE_BATT=`python3 /home/pi/EV_post_status/pijuice_getchargelevel.py | sed "s/'/\"/g" | jq '.data'`

curl -X POST -H "Content-Type: application/json" -d '{"soc":"'"$SOC"'", "date":"'"$DATE"'", "pijuice_batt":"'"$PIJUICE_BATT"'"}' http://domobeyou.beard.fr:1980/ioniq-status

donthalt=`curl -X GET http://domobeyou.beard.fr:1980/dont-halt`
if [ $donthalt == "FALSE" ]
then
  python3 /home/pi/EV_post_status/shutdown.py
else
  echo "Not halting..."
  sudo systemctl start pioniq.timer
fi
