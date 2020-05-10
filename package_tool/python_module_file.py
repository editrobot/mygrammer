#!/usr/bin/env python3
#encoding: utf-8
# -*- coding: utf-8 -*-

__author__ = 'editrobot'

import sys
import os
import platform
from package_tool import file

class python_module_file_class(object):
	def __init__(self,
		name,
		inherit="object",
		path = "script",
		Attributes_list = ["name"],
		methods_list = ["test"],
		load_module = [],
		mode = ["process",2] ):
		
		self.module_list = []
		self.exp_code = []
		self.class_code = []
		self.system_info_code = []
		self.run_mode_code = []
		
		self.name = name
		self.inherit = "object" if inherit == "" else inherit
		self.path = path
		self.Attributes_list = Attributes_list
		self.methods_list = methods_list

		self.mode = mode

		self.result = [
			"#!/usr/bin/env python3",
			"#encoding: utf-8",
			"# -*- coding: utf-8 -*-",
			"",
			"__author__ = 'editrobot'",
			""
		]
		
		self.load_module("import os")
		self.load_module("import platform")
		self.load_module("import logging")
		self.load_module("import random")
		self.load_module("from datetime import datetime")
		self.load_module("import subprocess")
		self.load_module("from collections import deque")
		self.load_module("import copy")
		for module_count in load_module:
			self.load_module(module_count)
		
		self.creat_class_code()

		self.print_system_info()
		self.run_mode()
		
		self.result.append("\n".join(self.module_list))
		self.result.append("\n".join(self.class_code))
		self.result.append("\n".join(self.system_info_code))
		self.result.append("\n".join(self.run_mode_code))
		self.result.append("\n".join(self.exp_code))
		if os.path.isfile("%s/%s.py" % (self.path,name)) :
			print("\n".join(self.result))
			file.write_str_file("%s/%s.py" % (self.path,name),"\n".join(self.result))
		else:
			print("the %s/%s.py is exists, add python module erro!!!" % (self.path,name))

	def load_module(self,module_name):
		lock = True
		for n in self.module_list:
			if(n == module_name):
				lock = lock and False
				break
		if(lock):
			self.module_list.append(module_name)

	# 打印示例代码
	def print_exp_code(self,the_code):
		self.exp_code.append(the_code)

	def creat_class_code(self):
		self.print_exp_code("")
		self.print_exp_code("'''")
		self.print_exp_code("#类的调用方式")
		self.print_exp_code("	import %s.%s" % (self.path,self.name))
		self.print_exp_code("	temp%s_var = %s.%s.%s_class()" % (self.name,self.path,self.name,self.name))
		self.class_code.append("")
		self.class_code.append("class %s_class(%s):" % (self.name,self.inherit))
		self.class_code.append("")
		self.class_code.append("	def __getattr__(self):")
		self.class_code.append("		return None")
		self.class_code.append("")
		self.class_code.append("	def __init__(self):")
		for n in self.Attributes_list:
			try:
				init_data = n["init"]
			except KeyError:
				if n["format"] == "list" or n["format"] == "on_repeat_list":
					init_data = "deque([])"
				elif n["format"] == "str":
					init_data = "\"\""
			finally:
				pass
			if n["format"] == "list" or n["format"] == "on_repeat_list":
				self.class_code.append("		self._%s = %s" % (n["name"],init_data))
			elif n["format"] == "str":
				self.class_code.append("		self._%s = %s" % (n["name"],init_data))
		for n in self.Attributes_list:
			self.add_class_Attributes(n)
			if n["format"] == "list" or n["format"] == "on_repeat_list":
				self.print_exp_code("	temp%s_var.%s = []" % (self.name,n["name"]))
			elif n["format"] == "str":
				self.print_exp_code("	temp%s_var.%s = \"\"" % (self.name,n["name"]))
		for n in self.methods_list:
			self.add_class_methods(n)
			self.print_exp_code("	temp%s_var.method_%s()" % (self.name,n["name"]))
		self.print_exp_code("	print(temp%s_var)" % (self.name))
		self.print_exp_code("'''")
		self.class_code.append("")
		self.class_code.append("	def __str__(self):")
		self.class_code.append("		# temp_Attributes_list = []")
		for n in self.Attributes_list:
			self.class_code.append("		# temp_Attributes_list.append(\"self._%s:%%s\" %% (self._%s))" %(n["name"],n["name"]))
		self.class_code.append("		# return \"\\n\".join(temp_Attributes_list)")
		self.class_code.append("		return \"class %s\"" %(self.name))


	def add_class_Attributes(self,Attribute):
		self.class_code.append("")
		self.class_code.append("")
		self.class_code.append("	@property")
		self.class_code.append("	def %s(self):" % (Attribute["name"]))
		self.class_code.append("		return self._%s" % (Attribute["name"]))
		self.class_code.append("	@%s.setter" % (Attribute["name"]))
		self.class_code.append("	def %s(self,value):" % (Attribute["name"]))
		if Attribute["format"] == "on_repeat_list":
			self.class_code.append("		lock = False")
			self.class_code.append("		if isinstance(value,list) :")
			self.class_code.append("			self._%s = deque(copy.deepcopy(value))" % (Attribute["name"]))
			self.class_code.append("		else:")
			self.class_code.append("			for x in self._%s:" % (Attribute["name"]))
			self.class_code.append("				if x == value:")
			self.class_code.append("					lock = True")
			self.class_code.append("					break")
			self.class_code.append("			if not lock == True:")
			self.class_code.append("				self._%s.append(value)" % (Attribute["name"]))
		elif Attribute["format"] == "list":
			self.class_code.append("		if isinstance(value,list) :")
			self.class_code.append("			self._%s = deque(copy.deepcopy(value))" % (Attribute["name"]))
			self.class_code.append("		else:")
			self.class_code.append("			self._%s.append(value)" % (Attribute["name"]))
		elif Attribute["format"] == "str":
			self.class_code.append("		self._%s = value" % (Attribute["name"]))

	def add_class_methods(self,method):
		try:
			if not method["init"] == "":
				init_data = "%s" % (method["init"])
			else:
				init_data = "		pass"
		except KeyError:
			init_data = "		pass"
		finally:
			pass
		Attributes = ""
		if len(method["Attributes"]) > 0:
			Attributes = ",%s" % (",".join(method["Attributes"]))
		self.class_code.append("")
		self.class_code.append("	def method_%s(self%s):" % (method["name"],Attributes))
		self.class_code.append("%s" % init_data)


	def print_system_info(self):
		self.load_module("import time")
		self.system_info_code.append("")
		self.system_info_code.append("def TestPlatform():")
		self.system_info_code.append("	print(\"i am module %s\")" % (self.name))

	def run_mode(self):
		self.print_exp_code("'''")
		self.print_exp_code("# 用命令行简单调用这个脚本的示例代码")
		self.print_exp_code("import subprocess")
		self.print_exp_code("r = subprocess.call(['python', '%s\\\\%s.py', '%s_argv'])" % (self.path,self.name,self.name))
		self.print_exp_code("print('Exit code:', r)")
		self.print_exp_code("")
		self.print_exp_code("'''")
		if(self.mode[0] == "cmd"):
			self.print_exp_code("")
			self.print_exp_code("'''")
			self.print_exp_code("# 用多命令行多输入调用这个脚本的示例代码")
			self.print_exp_code("import subprocess")
			self.print_exp_code("p = subprocess.Popen(['python','%s\\%s.py','%s_argv'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)" % (self.path,self.name,self.name))
			self.print_exp_code("output, err = p.communicate(b'call\\ntest\\n')")
			self.print_exp_code("print(output.decode('utf-8'))")
			self.print_exp_code("print('Exit code:', p.returncode)")
			self.print_exp_code("'''")
			self.load_module("import sys")
			self.run_mode_code.append("")
			self.run_mode_code.append("def test():")
			self.run_mode_code.append("	args = sys.argv")
			self.run_mode_code.append("	if len(args)==1:")
			self.run_mode_code.append("		print('Hello, world!')")
			self.run_mode_code.append("	elif len(args)==2:")
			self.run_mode_code.append("		print('Hello, %s!' % args[1])")
			self.run_mode_code.append("	else:")
			self.run_mode_code.append("		print('Too many arguments!')")
			self.run_mode_code.append("if __name__=='__main__':")
			self.run_mode_code.append("	test()")
			self.run_mode_code.append("	startCall = input()")
			self.run_mode_code.append("	CallTestPlatform = input()")
			self.run_mode_code.append("	if(startCall == \"call\") and (CallTestPlatform == \"test\"):")
			self.run_mode_code.append("		TestPlatform()")
		elif(self.mode[0] == "process") and ( self.mode[1] > 1 ) and (platform.system() == "Windows"):
			self.load_module("import time")
			self.load_module("from multiprocessing import Pool")
			self.run_mode_code.append("")
			self.run_mode_code.append("# 如果要启动大量的子进程，可以用进程池的方式批量创建子进程：")
			self.run_mode_code.append("def long_time_task(name):")
			self.run_mode_code.append("	print('Run task %s (%s)...' % (name, os.getpid()))")
			self.run_mode_code.append("	start = time.time()")
			self.run_mode_code.append("	time.sleep(random.random() * 3)")
			self.run_mode_code.append("	end = time.time()")
			self.run_mode_code.append("	print('Task %s runs %0.2f seconds.' % (name, (end - start)))")
			self.run_mode_code.append("")
			self.run_mode_code.append("if __name__=='__main__':")
			self.run_mode_code.append("	print('Parent process %s.' % os.getpid())")
			self.run_mode_code.append("	p = Pool(%s)" % (self.mode[1]))
			self.run_mode_code.append("	for i in range(%s):" % (self.mode[1]))
			self.run_mode_code.append("		p.apply_async(long_time_task, args=(i,))")
			self.run_mode_code.append("	print('Waiting for all subprocesses done...')")
			self.run_mode_code.append("	p.close()")
			self.run_mode_code.append("	p.join()")
			self.run_mode_code.append("	print('All subprocesses done.')")
		elif(self.mode[0] == "process") and ( self.mode[1] == 1 ) and (platform.system() == "Windows"):
			self.load_module("import os")
			self.load_module("import sys")
			self.load_module("from multiprocessing import Process")
			self.load_module("from multiprocessing import Queue")
			self.run_mode_code.append("")
			self.run_mode_code.append("# 跨平台创建子进程示例代码")
			self.run_mode_code.append("def run_proc(name):")
			self.run_mode_code.append("	args = sys.argv")
			self.run_mode_code.append("	if len(args)==1:")
			self.run_mode_code.append("		print('%s%s say: Hello, world!' % (name, os.getpid() ))")
			self.run_mode_code.append("	elif len(args)==2:")
			self.run_mode_code.append("		print('%s%s say: Hello, %s!' % (name, os.getpid(), args[1] ))")
			self.run_mode_code.append("	else:")
			self.run_mode_code.append("		print('Too many arguments!')")
			self.run_mode_code.append("")
			self.run_mode_code.append("# 写数据进程执行的代码:")
			self.run_mode_code.append("def write(name,q):")
			self.run_mode_code.append("	for value in ['A', 'B', 'C']:")
			self.run_mode_code.append("		print('Process %s (%s) to write: Put %s to queue...' % (name, os.getpid(), value))")
			self.run_mode_code.append("		q.put(value)")
			self.run_mode_code.append("		time.sleep(random.random())")
			self.run_mode_code.append("")
			self.run_mode_code.append("# 读数据进程执行的代码:")
			self.run_mode_code.append("def read(name,q):")
			self.run_mode_code.append("	while True:")
			self.run_mode_code.append("		value = q.get(True)")
			self.run_mode_code.append("		print('Process %s (%s) to read: Get %s from queue.' % (name, os.getpid(), value))")
			self.run_mode_code.append("")
			self.run_mode_code.append("")
			self.run_mode_code.append("")
			self.run_mode_code.append("if __name__=='__main__':")
			self.run_mode_code.append("	q = Queue()")
			self.run_mode_code.append("	print('Parent process %s.' % os.getppid())")
			self.run_mode_code.append("	pp = Process(target=run_proc, args=('pp',))")
			self.run_mode_code.append("	pw = Process(target=write, args=('pw',q))")
			self.run_mode_code.append("	pr = Process(target=read, args=('pr',q))")
			self.run_mode_code.append("	print('Child process will start.')")
			self.run_mode_code.append("	pp.start()")
			self.run_mode_code.append("	pw.start()")
			self.run_mode_code.append("	pr.start()")
			self.run_mode_code.append("	pp.join()")
			self.run_mode_code.append("	pw.join()")
			self.run_mode_code.append("	pr.terminate()")
			self.run_mode_code.append("	print('Child process end.')")
			self.run_mode_code.append("")
		elif(self.mode[0] == "process") and (platform.system() != "Windows"):
			self.load_module("import os")
			self.run_mode_code.append("")
			self.run_mode_code.append("# Unix/Linux/Mac以下是多线程示例代码")
			self.run_mode_code.append("print('Process (%s) start...' % os.getpid())")
			self.run_mode_code.append("# Only works on Unix/Linux/Mac:")
			self.run_mode_code.append("pid = os.fork()")
			self.run_mode_code.append("if pid == 0:")
			self.run_mode_code.append("	print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))")
			self.run_mode_code.append("else:")
			self.run_mode_code.append("	print('I (%s) just created a child process (%s).' % (os.getpid(), pid))")
		elif(self.mode[0] == "threading") and ( self.mode[1] == 1 ):
			self.load_module("import time")
			self.load_module("import threading")
			self.run_mode_code.append("")
			self.run_mode_code.append("# 示例全局变量")
			self.run_mode_code.append("globalValue = 0")
			self.run_mode_code.append("")
			self.run_mode_code.append("# 初始化一个全局变量锁")
			self.run_mode_code.append("lock = threading.Lock()")
			self.run_mode_code.append("")
			self.run_mode_code.append("# 创建全局ThreadLocal对象,让线程有自己的变量池:")
			self.run_mode_code.append("local_dict = threading.local()")
			self.run_mode_code.append("")
			self.run_mode_code.append("# 新线程执行的代码:")
			self.run_mode_code.append("def loop(count,nickname):")
			self.run_mode_code.append("	global globalValue")
			self.run_mode_code.append("	print('thread %s is running...' % threading.current_thread().name)")
			self.run_mode_code.append("	n = 0")
			self.run_mode_code.append("	while n < count:")
			self.run_mode_code.append("		# 如果有进行全局变量修改，就要先要获取锁:")
			self.run_mode_code.append("		local_dict.nickname = nickname")
			self.run_mode_code.append("		lock.acquire()")
			self.run_mode_code.append("		try:")
			self.run_mode_code.append("			n = n + 1")
			self.run_mode_code.append("			globalValue = globalValue + n")
			self.run_mode_code.append("			globalValue = globalValue - n")
			self.run_mode_code.append("			print('thread %s (%s) >>> count=%s' % (local_dict.nickname,threading.current_thread().name, n))")
			self.run_mode_code.append("			time.sleep(1)")
			self.run_mode_code.append("		finally:")
			self.run_mode_code.append("			# 改完了一定要释放锁:")
			self.run_mode_code.append("			lock.release()")
			self.run_mode_code.append("	print(\"globalValue is : %s\" % globalValue)")
			self.run_mode_code.append("	print('thread %s ended.' % threading.current_thread().name)")
			self.run_mode_code.append("")
			self.run_mode_code.append("if __name__=='__main__':")
			self.run_mode_code.append("	print('thread %s is running...' % threading.current_thread().name)")
			self.run_mode_code.append("	t1 = threading.Thread(target=loop, name='LoopThread_t1', args=(5,\"Alice\"))")
			self.run_mode_code.append("	t2 = threading.Thread(target=loop, name='LoopThread_t2', args=(5,\"Bob\"))")
			self.run_mode_code.append("	t1.start()")
			self.run_mode_code.append("	t2.start()")
			self.run_mode_code.append("	t1.join()")
			self.run_mode_code.append("	t2.join()")
			self.run_mode_code.append("	print('thread %s ended.' % threading.current_thread().name)")
			self.run_mode_code.append("")
		elif(self.mode[0] == "managers") and ( self.mode[1] == 1 ):
			self.load_module("import random")
			self.load_module("import time")
			self.load_module("import queue")
			self.load_module("from multiprocessing.managers import BaseManager")