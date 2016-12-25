#!/usr/bin/python3
import requests
import csv
import os
import logging
import sched, time
from threading import Timer

try:
    from queue import Queue
except ImportError:
    from Queue import Queue
from collections import namedtuple
import threading


TICK_TIME = 1

options ={}
options['access_token'] = '121a6946461321fd48f813e8cda6ce07'
options['csv_file'] = "/Users/drydyk/src/homedata/homedata.csv"

#ON OFF CCL

logger = logging.getLogger(__name__)
logger.handlers = []
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel(logging.INFO)

def debounce(wait):
    """ Decorator that will postpone a functions
        execution until after wait seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)
            try:
                debounced.t.cancel()
            except(AttributeError):
                pass
            debounced.t = Timer(wait, call_it)
            debounced.t.start()
        return debounced
    return decorator

class WebPowerSwitch(object):
	"""docstring for WebPowerSwitch"""
	def __init__(self):
		super(WebPowerSwitch, self).__init__()
		self.base_url = "http://admin:seebeck10@10.0.1.67/"
		requests.get(self.base_url + 'login.tgi', params={'Username':'admin', 'Password':'seebeck10'})

	def outlet(self,outlet,state):
		requests.get(self.base_url + "outlet", params={outlet:state})
# r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
# r.status_code
# r.headers['content-type']
# r.encoding
# r.text
# r.json
