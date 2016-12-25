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


class WebPowerSwitch(object):
	"""docstring for WebPowerSwitch"""
	def __init__(self):
		super(WebPowerSwitch, self).__init__()
		self.base_url = "http://admin:seebeck10@10.0.1.67/"
		self.outlet = [False,False,False,False,False,False,False,False,False]
		self.get_states()

	def byte_to_binary(self,n):
		return ''.join(str((n & (1 << i)) and 1) for i in (range(8)))

	def hex_to_binary(self,h):
		return ''.join(self.byte_to_binary(ord(b)) for b in binascii.unhexlify(h))

	def get_states(self):
		r = requests.get(self.base_url + 'index.htm')
		m = re.search("<!-- state=(\S\S) lock=(\S\S) -->",r.text)
		on_states = self.hex_to_binary(m.group(1))
		lock_states = self.hex_to_binary(m.group(2))

		self.outlet[0] = on_states
		self.outlet[1] = bool(int(on_states[0]))
		self.outlet[2] = bool(int(on_states[1]))
		self.outlet[3] = bool(int(on_states[2]))
		self.outlet[4] = bool(int(on_states[3]))
		self.outlet[5] = bool(int(on_states[4]))
		self.outlet[6] = bool(int(on_states[5]))
		self.outlet[7] = bool(int(on_states[6]))
		self.outlet[8] = bool(int(on_states[7]))
		return on_states

	def set_outlet(self,outlet,state):
		if state == True:
			state="ON"
		elif state == False:
			state="OFF"
		requests.get(self.base_url + "outlet", params={str(outlet):state})
		return self.get_states()

