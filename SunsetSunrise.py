#!/usr/bin/python
from math import cos, acos, sin, asin, degrees, radians
import datetime
import time
from crontab import CronTab

# Source:
# http://pagesperso-orange.fr/jean-paul.cornec/heures_lc.htm
class sunriseClass:
 def __init__(self):
  self.theDay=0
  self.theDate=[]
  self.solarDeclination=0
  self.equationOfTime=0
  self.latitude=0
  self.longitude=0
  self.sunrise=0
  self.sunset=0
  self.meridian=0
  self.duration=0
  self.sunriseTime=0
  self.sunsetTime=0
  self.meridianTime=0
  self.durationTime=0
 def getDay(self,d,m,y):
  d=float(d)
  m=float(m)
  y=float(y)
  n1 = int( (m* 275.0)/9.0 )
  n2 = int( (m+9.0)/12.0 )
  k = 1.0 + int( (y-4.0*int(y/4.0)+2.0)/3.0 )
  n=n1-n2*k+d-30.0
  return int(n)
 def getEoT(self,j):
  j=float(j)
  m = 357.0+(0.9856*j) 
  c = (1.914*sin(radians(m))) + (0.02*sin(radians(2.0*m)))
  l = 280.0 + c + (0.9856*j)
  r=(-2.465*sin(radians(2.0*l))) + (0.053*sin(radians(4.0*l)))
  Equ=(c+r)*4.0
  return Equ/60.0
 def getDec(self,j):
  j=float(j)
  m = 357.0+(0.9856*j) 
  c = (1.914*sin(radians(m))) + (0.02*sin(radians(2.0*m)))
  l = 280.0 + c + (0.9856*j)
  sinDec= 0.3978*sin(radians(l))
  return degrees(asin(sinDec))
 def getHo(self,Dec,Lat,Lon):
  cosHo=( -0.01454-sin(radians(self.solarDeclination))*sin(radians(self.latitude)) ) / ( cos(radians(self.solarDeclination))*cos(radians(self.latitude)) )
  return (degrees(acos(cosHo))/15.0)
 def setNumericalDate(self,d,m,y):
  self.theDate=[d,m,y]
  self.theDay=self.getDay(d,m,y)
  self.solarDeclination=self.getDec(self.theDay)
  self.equationOfTime=self.getEoT(self.theDay)
  return None
 def setLocation(self,Lat,Lon):
  self.latitude=Lat
  self.longitude=Lon
  return None
 def getHM(self,nH):
  h=int(nH)
  m=int(((nH*60.0)%60)+0.5)
  return '%d:%02d' % (h,m)
 def calculateWithUTC(self,UTC):
  mLon=(self.longitude*4.0)/60.0
  Ho=self.getHo(self.solarDeclination,self.latitude,self.longitude)
  self.meridian=12.0+self.equationOfTime-mLon+UTC
  self.sunrise=self.meridian-Ho
  self.sunset=self.meridian+Ho
  self.duration=2.0*Ho
  self.meridianTime=self.getHM(self.meridian)
  self.sunriseTime=self.getHM(self.sunrise)
  self.sunsetTime=self.getHM(self.sunset)
  self.durationTime=self.getHM(self.duration)
  return None


thisDay=datetime.date.today()#+datetime.timedelta(days=1)
mySunrise=sunriseClass()
mySunrise.setNumericalDate(thisDay.day,thisDay.month,thisDay.year)
#mySunrise.setLocation(34.052222,-118.243611) # Los Angeles, UTC -8
#mySunrise.setLocation(41.012222,28.975833) # Istanbul, UTC +2
mySunrise.setLocation(48.361155, 7.579854) # HUTTENHEIM
#mySunrise.setLocation(48.856667,2.350833) # Paris, UTC +1
#Heure ete +2 hiver +1
cur = time.localtime()
if cur.tm_isdst:
    mySunrise.calculateWithUTC(+2)
else:
    mySunrise.calculateWithUTC(+1)
print 'Date:',mySunrise.theDate[0],'/',mySunrise.theDate[1],'/',mySunrise.theDate[2]
print 'Lever du soleil:',mySunrise.sunriseTime
print 'Passage au meridien:',mySunrise.meridianTime
print 'Coucher du soleil:',mySunrise.sunsetTime
print 'Duree du jour',mySunrise.durationTime


#cron = CronTab(tabfile='filename.tab') #windows
cron=CronTab(user='root')

cron.remove_all(command='python /home/pi/script/montePorte.py')
cron.remove_all(command='python /home/pi/script/descendrePorte.py')

job  = cron.new(command='python /home/pi/script/montePorte.py')
lev=mySunrise.sunrise
job.minute.on(int(((lev*60.0)%60)))
job.hour.on(int(lev))
job.day.on(mySunrise.theDate[0])
job.month.on(mySunrise.theDate[1])
job  = cron.new(command='python /home/pi/script/descendrePorte.py')
sunsetDelta=  mySunrise.sunset+0.5
job.minute.on(int(((sunsetDelta*60.0)%60)))
job.hour.on(int(sunsetDelta))
job.day.on(mySunrise.theDate[0])
job.month.on(mySunrise.theDate[1])

cron.write()
