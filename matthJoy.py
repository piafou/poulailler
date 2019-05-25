#!/usr/bin/python
#--------------------------------------
# This script reads data from a
# MCP3008 ADC device using the SPI bus.
#
# Analogue joystick version!
#
# Author : Matt Hawkins
# Date   : 17/04/2014
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------
 
import spidev
import time
import os
from scriptexit import ScriptExit
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Define sensor channels
# (channels 3 to 7 unused)
swt_channel = 0
vrx_channel = 1
vry_channel = 2
 
# Define delay between readings (s)
delay = 2
readoldsw=0
readoldx=0
readoldy=0
tolerance=100
mod=101
 
while True:
 
  # Read the joystick position data
  vrx_pos = ReadChannel(vrx_channel)
  vry_pos = ReadChannel(vry_channel)
 
  # Read switch state
  swt_val = ReadChannel(swt_channel)
  mod=abs(vrx_pos-readoldx)+abs(readoldy-vry_pos)
  # Print out results
  if (vrx_pos>600):
   print "--------------------------------------------"
   print("X : {}  Y : {}  Switch : {}".format(vrx_pos,vry_pos,swt_val))
   readoldx=vrx_pos
   readoldy=vry_pos
   readoldsw=swt_val
   try:
    execfile('montePorte.py')
   except SystemExit:
    print "sys.exit was called but I'm proceeding anyway (so there!-)."
  if (vrx_pos<400):
   print "--------------------------------------------"
   print("X : {}  Y : {}  Switch : {}".format(vrx_pos,vry_pos,swt_val))
   readoldx=vrx_pos
   readoldy=vry_pos
   readoldsw=swt_val
   try:
    execfile('descendrePorte.py')
   except SystemExit:
    print "sys.exit was called but I'm proceeding anyway (so there!-)."
  # Wait before repeating loop
  time.sleep(delay)
