#!/usr/bin/env python

import RPi.GPIO as GPIO
import sqlite3
import sys
import time

def log_values(etat_pom):
	conn=sqlite3.connect('/var/www/lab_app2/lab_app.db') #it is important to provide an absolute path to database file , otherwise cron win't be able to find it!

	curs=conn.cursor()
	curs.execute("""INSERT INTO pompe2 values(datetime('now'), (?))""", (etat_pom,))
	conn.commit()
	conn.close()


GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.IN)
GPIO.setwarnings(False)


def my_callback(channel):
	if GPIO.input(5):
		etat_pom = 1
	else :
		etat_pom = 0

	log_values(etat_pom)
GPIO.add_event_detect(5, GPIO.BOTH, callback=my_callback, bouncetime=1000)

while(True):
	try:
		time.sleep(1)
	except:
		time.sleep(1)

