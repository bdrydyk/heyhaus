from flask import Flask
from webpower import WebPowerSwitch

app = Flask(__name__)

@app.route("/webpower/")
@app.route("/webpower/<outlet>/")
@app.route("/webpower/<outlet>/<state>")
def webpower(outlet=None,state=None):
	w = WebPowerSwitch()
	states = w.get_states()

	if outlet ==None and state==None:
		return(str(states))

	if outlet != None and state == None:
		return(str(w.outlet[int(outlet)]))

	if outlet != None and state != None:
		if state == "ON":
			state=True
		elif state == "OFF":
			state=False
		return(str(w.set_outlet(str(outlet),state)))


if __name__ == "__main__":
	app.run(host="0.0.0.0",debug=True)