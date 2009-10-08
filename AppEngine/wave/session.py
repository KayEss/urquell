# -*- coding: utf-8 -*-
from google.appengine.ext import db

from waveapi.simplejson import dumps, loads


"""
Example record

{
sid: 'b+KMIw2XGM%Dwavesandbox.com!w+Ix_odYwF%A',
frames: '{'*hygt3td6': {value:{},.. },'*uh1i9d65': {error:.. },.. }'
}
"""

class Session(db.Model):
	# a globally unique identifier composed of a wave id, and a blip id
	sid = db.StringProperty(required=True)
	# a JSON object whose properties are Urquell invocation hash's, and
	# values are call frames.
	frames = db.TextProperty(required=True)
	# created timestamp, so we can give a user friendly sid in the blip
	created = db.DateTimeProperty(auto_now_add=True)
	# last modified timestamp, so we can cull stale sessions periodically
	modified = db.DateTimeProperty(auto_now=True)

class SessionWrapper(object):
	sid = None
	frames = None
	data = None

	def __init__(self,sid):
		self.data = Session.gql("WHERE sid = :1", sid).fetch(1)
		if len(self.data):
			self.data = self.data[0]
			self.sid, self.frames = self.data.sid,loads(self.data.frames)
		else:
			self.sid, self.frames, self.data = sid,{},Session(sid=sid,frames="{}")

	def save(self):
		self.data.frames = dumps(self.frames)
		db.put(self.data)

	def get_result(self,frame):
		if frame.has_key('value'): return frame['value']
		if frame.has_key('error'): return frame['error']['message']
		return 'None'

	def is_error(self,frame):
		if frame.has_key('error'): return True
		return False

	def errors(self):
		def error_filter(f): return (True if f.has_key('error') else False) 
		return filter(error_filter,self.frames.values())

	def ordered_frames(self):
		frames = self.frames.items()
		frames.sort(lambda x,y: cmp(x[1]['fnum'],y[1]['fnum']))
		return [value for key, value in frames]

	def last_fnum(self):
		if not len(self.frames): return 0
		return self.ordered_frames()[-1].get('fnum',0)
