from flask import Flask, abort, render_template, jsonify
from webpower import WebPowerSwitch
import smbus
import RPi.GPIO as GPIO
from BMP180 import BMP085
import grovepi
import math

DHT_SENSOR = 4
DHT_BLUE = 0    # The Blue colored sensor.
DHT_WHITE = 1   # The White colored sensor.

app = Flask(__name__)

@app.route("/")
def index():
	"""sets all outlet states based on the byte sent, i.e. EE, FE, 1E etc"""

	return(render_template('index.html'))


@app.route("/webpower/set/{hexstr}")
def webpower_set(hexstr):
	"""sets all outlet states based on the byte sent, i.e. EE, FE, 1E etc"""

	w = WebPowerSwitch()
	w.set_outlet_states(hexstr)
	res = w.get_hex_states()
	return(str(res))


@app.route("/webpower/")
@app.route("/webpower/<outlet>/")
@app.route("/webpower/<outlet>/<state>")
def webpower(outlet=None,state=None):
	w = WebPowerSwitch()
	states = w.get_outlet_states()

	if outlet ==None and state==None:
		return(jsonify(states))

	if outlet != None:
		if outlet == "set":
			res = w.set_outlet_states(state)
			return(jsonify(res))
		elif outlet == "cycle":
			res = w.cycle_outlet_states(state)
			return(jsonify(res))
		else:
			try:
				assert 1 <= int(outlet) <= 8, "outlet number not valid"
			except:
				abort(401)

			outlet = int(outlet)
			outlet_index = outlet-1

			if state == None:
				res = w.outlets[outlet_index]
				return(jsonify(res))
			else:
				if state == "ON":
					state=True
				elif state == "OFF":
					state=False
				else:
					abort(401)
				res = w.set_outlet(str(outlet),state)
				return(jsonify(res))

@app.route("/temp/")
def temp():
	# bmp = BMP085(0x77, 1)
	# bus = smbus.SMBus(1)
	# temp = bmp.readTemperature()

	[temp,humidity] = grovepi.dht(DHT_SENSOR,DHT_BLUE)
	temp_c = temp
	temp_f = temp_c*1.8+32
	return(str(temp_f))

@app.route("/humidity/")
def humidity():
	[temp,humidity] = grovepi.dht(DHT_SENSOR,DHT_BLUE)

	return(jsonify(humidity))

@app.route("/pressure/")
def pressure():
	bmp = BMP085(0x77, 1)
	bus = smbus.SMBus(1)
	pressure = int(round(bmp.readPressure()))
	return(jsonify(pressure))


@app.route("/altitude/")
def altitude():
	bmp = BMP085(0x77, 1)
	bus = smbus.SMBus(1)
	altitude = bmp.readAltitude(101560)
	return(jsonify(altitude))

if __name__ == "__main__":
	app.run(host="0.0.0.0",debug=True)