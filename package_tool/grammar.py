#!/usr/bin/env python3
#encoding: utf-8
# -*- coding: utf-8 -*-

__author__ = 'editrobot'

import os
import platform
import logging
import random
from datetime import datetime
import subprocess
from collections import deque
import copy
from package_tool import file
import time
import sys

class grammar_class(object):

	def __getattr__(self):
		return None

	def __init__(self):
		self._dict_list = []
		self._src_list = []
		self._split_list = []


	@property
	def dict_list(self):
		return self._dict_list
	@dict_list.setter
	def dict_list(self,value):
		if isinstance(value,list) :
			self._dict_list = deque(copy.deepcopy(value))
		else:
			self._dict_list.append(value)


	@property
	def src_list(self):
		return self._src_list
	@src_list.setter
	def src_list(self,value):
		if isinstance(value,list) :
			self._src_list = deque(copy.deepcopy(value))
		else:
			self._src_list.append(value)


	@property
	def split_list(self):
		return self._split_list
	@split_list.setter
	def split_list(self,value):
		if isinstance(value,list) :
			self._split_list = deque(copy.deepcopy(value))
		else:
			self._split_list.append(value)

	def method_getstr(self,str,begin,end):
		temp = []
		while not end < begin:
			temp.append(str[begin])
			begin+=1
		return "".join(temp)

	def method_elementindict(self,dict,parameter):
		split_list = []
		parameter_length = len(parameter)
		point = 0

		while parameter_length > point :
			lock = False
			temp = 1
			for y in range(len(dict)):
				for x in range(len(dict[y])):
					index = parameter.find(dict[y][x],point)
					keylength = len(dict[y][x])
					if not index == -1 and \
						index == point and \
						not keylength < temp:
						temp = keylength
						type = dict[y][x]
						if not lock:
							lock = True
			if lock:
				split_list.append([type,point,point+temp-1])
			point+=temp
		return split_list

	def method_split_element(self,str,split_list):
		temp = []
		str_point = 0
		split_list_point = 0
		while len(split_list) > split_list_point:
			if split_list[split_list_point][1] > str_point:
				temp.append(self.method_getstr(str,str_point,split_list[split_list_point][1]-1))
				str_point = split_list[split_list_point][1]
				step = 0
			elif split_list[split_list_point][1] == str_point:
				temp.append(self.method_getstr(str,split_list[split_list_point][1],split_list[split_list_point][2]))
				str_point = split_list[split_list_point][2]+1
				step = 1
			split_list_point += step
		if not str_point > len(str):
			temp.append(self.method_getstr(str,str_point,len(str)-1))
		return temp

	def method_out_put(self,dict_path,src_path):
		dict = file.read_json_file(dict_path)
		str = "".join(file.read_file_to_str(src_path))

		split_list = self.method_elementindict(dict,str)
		return {
			"str": str,
			"index": self.method_split_element(str,split_list)
		}

	def __str__(self):
		# temp_Attributes_list = []
		# temp_Attributes_list.append("self._dict_list:%s" % (self._dict_list))
		# temp_Attributes_list.append("self._src_list:%s" % (self._src_list))
		# temp_Attributes_list.append("self._split_list:%s" % (self._split_list))
		# return "\n".join(temp_Attributes_list)
		return "class grammar"

def TestPlatform():
	print("i am module grammar")

def test():
	args = sys.argv
	if len(args)==1:
		print('Hello, world!')
	elif len(args)==2:
		print('Hello, %s!' % args[1])
	else:
		print('Too many arguments!')
if __name__=='__main__':
	test()
	startCall = input()
	CallTestPlatform = input()
	if(startCall == "call") and (CallTestPlatform == "test"):
		TestPlatform()

'''
#类的调用方式
	import package_tool.grammar
	tempgrammar_var = package_tool.grammar.grammar_class()
	tempgrammar_var.dict_list = []
	tempgrammar_var.src_list = []
	tempgrammar_var.split_list = []
	tempgrammar_var.method_elementindict()
	tempgrammar_var.method_split_element()
	tempgrammar_var.method_out_put()
	print(tempgrammar_var)
'''
'''
# 用命令行简单调用这个脚本的示例代码
import subprocess
r = subprocess.call(['python', 'package_tool\\grammar.py', 'grammar_argv'])
print('Exit code:', r)
'''

'''
# 用多命令行多输入调用这个脚本的示例代码
import subprocess
p = subprocess.Popen(['python','package_tool\grammar.py','grammar_argv'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate(b'call\ntest\n')
print(output.decode('utf-8'))
print('Exit code:', p.returncode)
'''