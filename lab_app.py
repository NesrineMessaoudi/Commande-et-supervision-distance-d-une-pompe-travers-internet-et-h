import RPi.GPIO as GPIO
import time
import sqlite3
import sys
import datetime 
import plotly 
import numpy as np 
from plotly.graph_objs import Scatter, Layout
import plotly.graph_objects as go

from flask import Flask, render_template, request

app = Flask(__name__)
pin=3
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
GPIO.setwarnings(False)



@app.route("/button",methods=['GET'])
def button ():


	from_date_str = request.args.get('from',time.strftime("%Y-%m-%d")) #Get the from date value from the URL
	print from_date_str
 	to_date_str = request.args.get('to',time.strftime("%Y-%m-%d"))   #Get the to date value from the URL
	print to_date_str
	print validate_date(from_date_str)
	print validate_date(to_date_str)
	if not validate_date(from_date_str): # Validate date before sending it to the DB 
		from_date_str = time.strftime("%Y-%m-%d")
	if not validate_date(to_date_str):
		to_date_str = time.strftime("%Y-%m-%d")		# Validate date before sending it to the DB






	pin=3
	range=request.args.get('range_b','');
	range_b_int = "nan" 
	try:
		range_b_int= int( range)
	except:
		print "range not a number"

	if range_b_int == 1:
		reponse1 = "ON"
		GPIO.output(pin, GPIO.HIGH)
        	
	else :
		reponse1 = "OFF"
		GPIO.output(pin, GPIO.LOW)
        	




	import sqlite3 
	conn=sqlite3.connect('/var/www/lab_app2/lab_app.db')
	curs=conn.cursor()
	curs.execute("SELECT * FROM pompe2 WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str)) 
	etat_pom = curs.fetchall()
	conn.close()



#	import sqlite3 
#	conn=sqlite3.connect('/var/www/lab_app2/lab_app.db')
#	curs=conn.cursor()
#	curs.execute("SELECT * FROM pompe2") 
#	etat_pom = curs.fetchall()
#	conn.close()


	return render_template('pin.html',reponse = reponse1, etat=etat_pom, from_date = from_date_str, to_date=to_date_str)
#	return render_template('pin.html',reponse = reponse1, etat=etat_pom)	
	


@app.route("/to_plotly", methods=['GET'])
def to_plotly():
	

	from_date_str = request.args.get('from',time.strftime("%Y-%m-%d")) #Get the from date value from the URL
	print from_date_str
	to_date_str = request.args.get('to',time.strftime("%Y-%m-%d"))   #Get the to date value from the URL
	print to_date_str
	print validate_date(from_date_str)
	print validate_date(to_date_str)
	if not validate_date(from_date_str): # Validate date before sending it to the DB
		from_date_str = time.strftime("%Y-%m-%d")
	if not validate_date(to_date_str):
		to_date_str = time.strftime("%Y-%m-%d")         # Validate date before sending it to t






	import sqlite3
	conn=sqlite3.connect('/var/www/lab_app2/lab_app.db')
	curs=conn.cursor()
	curs.execute("SELECT * FROM pompe2 WHERE rDateTime BETWEEN ? AND ?", (from_date_str, to_date_str))
	etat_pom = curs.fetchall()
	conn.close()




	temps=()
	for x in etat_pom:
		temps += (x[0],)
	print temps

	etat_pom2=()
	for x in etat_pom:
		etat_pom2 +=(x[1],)
	print etat_pom2


	fig = go.Figure(data=[
	go.Scatter( 
	x=temps, 
	y=etat_pom2
	)
	])

	
	fig.write_html('./templates/first_figure.html',auto_open=True)
	return render_template ("first_figure.html")
#	return render_template('pin.html',reponse = reponse1, etat=etat_pom, from_date = from_date_str, to_date=to_date_str)



def validate_date(d): 
	try: 
		datetime.datetime.strptime(d, '%Y-%m-%d') 
		return True
	except ValueError:
		return False



if __name__ == "__main__":
	# 1- initiation de la l'interruption
	app.run(host='0.0.0.0', port=8080, debug=True)
