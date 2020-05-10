#!/usr/bin/env python3
#encoding: utf-8
# -*- coding: utf-8 -*-

__author__ = 'editrobot'

import sys
import platform

import functools

def log(text):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			print('begin %s call %s():' % (text, func.__name__))
			f = func(*args, **kw)
			print('end %s call %s():' % (text, func.__name__))
			return f
		return wrapper
	return decorator

def TestPlatform():
	print ("----------Operation System--------------------------")
	#Windows will be : (32bit, WindowsPE)
	#Linux will be : (32bit, ELF)
	print(platform.architecture())

	#Windows will be : Windows-XP-5.1.2600-SP3 or Windows-post2008Server-6.1.7600
	#Linux will be : Linux-2.6.18-128.el5-i686-with-redhat-5.3-Final
	print(platform.platform())

	#Windows will be : Windows
	#Linux will be : Linux
	print(platform.system())

	print ("--------------Python Version-------------------------")
	#Windows and Linux will be : 3.1.1 or 3.1.3
	print(platform.python_version())

def init_def():
	args = sys.argv
	if len(args)==1:
		print('Hello, world!')
	elif len(args)==2:
		print('Hello, %s!' % args[1])
	else:
		print('Too many arguments!')

#命令行运行时才执行
if __name__=='__main__':
    init_def()