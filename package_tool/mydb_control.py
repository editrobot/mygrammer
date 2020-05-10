#!/usr/bin/env python3
#encoding: utf-8
# -*- coding: utf-8 -*-

__author__ = 'editrobot'

import os
import platform
import logging
import random
import urllib
import json
from datetime import datetime
import subprocess
from collections import deque
import codecs
import time
import sys

import xlrd
import xlwt
import xlutils.copy

import mysql.connector

import package_tool.mysql_control
from package_tool import file

class mydb_control_class(object):

	def __getattr__(self):
		return None

	def __init__(self):
		self._tablename = ""


	@property
	def tablename(self):
		return self._tablename
	@tablename.setter
	def tablename(self,value):
		self._tablename = value

	def method_update_weather(self):
		tempmysql_control_var = package_tool.mysql_control.mysql_control_class()
		# tempmysql_control_var.method_insert(
			# "chinacityinfo",
			# ["F_Province", "F_CityName", "F_PostCode", "F_AreaCode", "F_AsKeyword", "weather"],
			# inputdata)

		# tempmysql_control_var.method_update("keywordlist", "id = '1'", "kw = '100'")
		# tempmysql_control_var.method_delete("keywordlist", "id = '2'")
		for x in tempmysql_control_var.method_select("chinacityinfo",""):
			print("http://op.juhe.cn/onebox/weather/query?key=d9682f2a2df8ec56041e8fb6ea6e54f8&cityname=%s" % x[2])
			with urllib.request.urlopen("http://op.juhe.cn/onebox/weather/query?key=d9682f2a2df8ec56041e8fb6ea6e54f8&cityname=%s" % urllib.parse.quote(x[2])) as f:
				data = f.read()
				print('Status:', f.status, f.reason)
				for k, v in f.getheaders():
					print('%s: %s' % (k, v))
				print('Data:', data.decode('utf-8'))
			
			tempmysql_control_var.method_update("chinacityinfo", "F_CityName = '%s'" % (x[2]), "weather = '%s'" % (data.decode('utf-8')))
		tempmysql_control_var.method_close()

	def method_update_news(self):
		pass

	def method_update_keyword(self):
		count = 0
		tempmysql_control_var = package_tool.mysql_control.mysql_control_class()
		with codecs.open("filetemp\\out.txt", 'r',"utf-8") as f:
			for line in f.readlines():
				count = count + 1
				if count%500 == 0:
					print(count)
				result = tempmysql_control_var.method_select("keywordlist","kw = '%s'"%(line.strip()))
				if len(result) == 0:
					# print("insert %s"%line.strip())
					tempmysql_control_var.method_insert(
						"keywordlist",
						["kw"],
						[line.strip()])

	def method_backup(self):
		tempmysql_control_var = package_tool.mysql_control.mysql_control_class()
		for x in tempmysql_control_var.method_select("chinacityinfo","",[0,3]):
			print(x)

	def method_search(self,kw):
		try:
			www_fmchl_comconn = mysql.connector.connect(
				user="root",
				password="",
				database="www_fmchl_com")
			www_fmchl_comcursor = www_fmchl_comconn.cursor()
			mydbconn = mysql.connector.connect(
				user="root",
				password="",
				database="mydb")
			mydbcursor = mydbconn.cursor()
		except:
			print("Error:数据库连接错误")

		www_fmchl_comcursor.execute('select * from wp_weixin_custom_replies WHERE keyword = %s', (kw,))
		print(www_fmchl_comcursor.fetchall())
		
		www_fmchl_comcursor.close()
		www_fmchl_comconn.close()
		mydbcursor.close()
		mydbconn.close()

	def __str__(self):
		# temp_Attributes_list = []
		# temp_Attributes_list.append("self._tablename:%s" % (self._tablename))
		# return "\n".join(temp_Attributes_list)
		return "class mydb_control"

def TestPlatform():
	print("i am module mydb_control")

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
	import package_tool.mydb_control
	tempmydb_control_var = package_tool.mydb_control.mydb_control_class()
	tempmydb_control_var.tablename = ""
	tempmydb_control_var.method_update_weather()
	tempmydb_control_var.method_update_news()
	tempmydb_control_var.method_backup()
	print(tempmydb_control_var)
'''
'''
# 用命令行简单调用这个脚本的示例代码
import subprocess
r = subprocess.call(['python', 'package_tool\\mydb_control.py', 'mydb_control_argv'])
print('Exit code:', r)

'''

'''
# 用多命令行多输入调用这个脚本的示例代码
import subprocess
p = subprocess.Popen(['python','package_tool\mydb_control.py','mydb_control_argv'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate(b'call\ntest\n')
print(output.decode('utf-8'))
print('Exit code:', p.returncode)
'''