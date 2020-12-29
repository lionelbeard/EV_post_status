#!/bin/bash


SOC=`python /home/pi/EV_post_status/ioniq_soc.py`

# Sync RTC time
sudo hwclock -s

DATE=`date`

PIJUICE_BATT=`python3 /home/pi/EV_post_status/pijuice_getchargelevel.py | sed "s/'/\"/g" | jq '.data'`

curl -X POST -H "Content-Type: application/json" -d '{"soc":"'"$SOC"'", "date":"'"$DATE"'", "pijuice_batt":"'"$PIJUICE_BATT"'"}' http://domobeyou.beard.fr:1980/ioniq-status

autohalt=`curl -X GET http://domobeyou.beard.fr:1980/auto-halt`
if [ $autohalt == "on" ]
then
  python3 /home/pi/EV_post_status/shutdown.py
else
  echo "Not halting..."
  sudo systemctl start pioniq.timer
fi
