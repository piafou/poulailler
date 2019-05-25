#!/usr/bin/python
from crontab import CronTab


cron=CronTab(user='root')
cron.remove_all(command='python /home/pi/script/SunsetSunrise.py')
job  = cron.new(command='python /home/pi/script/SunsetSunrise.py')
job.minute.on(0)
job.hour.on(0)
cron.write()
execfile("/home/pi/script/SunsetSunrise.py")
