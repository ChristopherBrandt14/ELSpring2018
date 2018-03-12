#!/usr/bin/python
import os
import time
import sqlite3 as mydb
import sys

#""" Log Current Time, Temperature in Celsius and Fahrenheit
 #To an Sqlite3 database """

def readTemp():
  tempfile = open("/sys/bus/w1/devices/28-000006974ebe/w1_slave")
  tempfile_text = tempfile.read()
  currentTime = time.strftime('%x %X %Z')
  tempfile.close()
  tempC=float(tempfile_text.split("\n")[1].split("t=")[1])/1000
  tempF=tempC*9.0/5.0+32.0
  return [currentTime, tempC, tempF]

# readTemp and stores in temperature.db database
def logTemp():
  con = mydb.connect('/home/pi/temperature.db')
  with con:
      try:
        [t,C,F]=readTemp()
        print "Current temperature is: %s F" %F
        cur = con.cursor()
        cur.execute('insert into TempData values(?,?,?)',(t,C,F))
        print "Temperature logged"
      except:
        print "Error!!"
logTemp()
