#encoding: utf-8
# -*- coding: utf-8 -*-

__author__ = 'editrobot'

from datetime import datetime
import random

class guid_class(object):
	def __init__(self):
		self._id = 0

	def get_guid(self):
		if self._id == 99999:
			self._id = 1
		self._id += 1
		return "%s%s%s" % ( str(random.randint(0,99999)),str(self._id),str(datetime.now().timestamp()) )
