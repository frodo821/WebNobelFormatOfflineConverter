#-*- coding:utf-8 -*-
import __main__ as mn
import functools

def tagAdder_ruby(func):
	@functools.wraps(func)
	def wrapper(*args,**kwargs):
		ret = "<ruby><rp>(</rp>"
		ret = ret + func(args[0],args[1],**kwargs)
		ret = ret + "<rp>)</rp></ruby>"
		return ret
	return wrapper

def tagAdder(tag,attr):
	if not attr == "":
		attr = " " + attr
	def _tagAdder(func):
		@functools.wraps(func)
		def wrapper(*args,**kwargs):
			ret = "<" + tag + attr + ">"
			ret = ret + func(args[0],**kwargs)
			ret = ret + "</" + tag + ">"
			return ret
		return wrapper
	return _tagAdder
