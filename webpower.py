#!/usr/bin/python3
import requests
import csv
import os
import logging
import sched, time
import re, binascii

#ON OFF CCL
BASE_URL = "http://admin:seebeck10@10.0.1.67/"
STATE_STR= "<!-- state=ef lock=e6 -->"

logger = logging.getLogger(__name__)
logger.handlers = []
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel(logging.INFO)


def byte_to_binary(n):
	return ''.join(str((n & (1 << i)) and 1) for i in (range(8)))

def hex_to_binary(h):
	return ''.join(byte_to_binary(ord(b)) for b in binascii.unhexlify(h))

class WebPowerSwitch(object):
	"""docstring for WebPowerSwitch"""
	def __init__(self):
		super(WebPowerSwitch, self).__init__()
		self.base_url = BASE_URL

		self.outlet1 = False
		self.outlet2 = False
		self.outlet3 = False
		self.outlet4 = False
		self.outlet5 = False
		self.outlet6 = False
		self.outlet7 = False
		self.outlet8 = False

		self.getOutletStates()

	def getOutletStates(self):
		r = requests.get(self.base_url + 'index.htm')
		m = re.search("<!-- state=(\S\S) lock=(\S\S) -->",r.text)
		on_states = hex_to_binary(m.group(1))
		lock_states = hex_to_binary(m.group(2))

		self.outlet1 = bool(int(on_states[0]))
		self.outlet2 = bool(int(on_states[1]))
		self.outlet3 = bool(int(on_states[2]))
		self.outlet4 = bool(int(on_states[3]))
		self.outlet5 = bool(int(on_states[4]))
		self.outlet6 = bool(int(on_states[5]))
		self.outlet7 = bool(int(on_states[6]))
		self.outlet8 = bool(int(on_states[7]))
		return on_states


	def outlet(self,outlet,state):
		if state == True:
			state="ON"
		elif state == False:
			state="OFF"
		requests.get(self.base_url + "outlet", params={str(outlet):state})
		return self.getOutletStates()

