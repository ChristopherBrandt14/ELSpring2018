#!/usr/bin/python

# The following script sets the Pi up as a web server
#   If a remote machine accesses the Pi's web address
#   it is set up to handle the route request by displaying
#   "Hello!" and the current date and time.

from flask import Flask, render_template, request, g
import access
import datetime
import sqlite3 as mydb
DATABASE = '/home/pi/temperature.db'

app = Flask(__name__)

@app.route("/")
def hello():
  now = datetime.datetime.now()
  timeString = now.strftime("%Y-%m-%d %H:%M")
  templateData = {
    'title' : 'HELLO!',
    'time' : timeString
  }
  return render_template('main.html',**templateData)

@app.route("/getTemp")
def getTemp():
  templateData = {
    'title' : 'Temperature Data'
  }
  return render_template('getTemp.html',**templateData)

@app.route('/result', methods = ['POST', 'GET'])
def result():
  if request.method == 'POST':
    dates = request.form.getlist('date[]')
    print dates
    _dates = []
    for date in dates:
      _dates.append(date)

    out_date1 = _dates[0].split("-")
    _dates[0] = out_date1[1] + "/" + out_date1[2] + "/" + out_date1[0][-2:] + " 00:00:00 EDT"

    out_date2 = _dates[1].split("-")
    _dates[1] = out_date2[1] + "/" + out_date2[2] + "/" + out_date2[0][-2:] + " 23:59:59 EDT"
    print _dates[1]

    cur = get_db().cursor()
    cur.execute("select * from temperature where date_time>=:start and " \
        "date_time<=:end",{"start":_dates[0], "end":_dates[1]})
    records = cur.fetchall()
    date = []
    tempC = []
    tempF = []
    for record in records:
      date.append(record[0])
      tempC.append(record[1])
      tempF.append(record[2])
    templateData = {
      'date' : date,
      'tempC' : tempC,
      'tempF' : tempF
    }
    return render_template("TempResult.html", **templateData)

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = mydb.connect(DATABASE)
  return db

if __name__ == "__main__":
  app.run(host='0.0.0.0', port = 8081, debug = True)
