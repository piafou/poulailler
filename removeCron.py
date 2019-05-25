#!/usr/bin/python
from crontab import CronTab


#cron = CronTab(tabfile='filename.tab') #windows
cron=CronTab(user='root')

cron.remove_all()


cron.write()
