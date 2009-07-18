from google.appengine.ext import db
from jsonrpc.json import dumps, loads

"""
Example record

{
sid: 'b+KMIw2XGM%Dwavesandbox.com!w+Ix_odYwF%A',
frames: '[{value:{},.. },{error:.. },.. ]'
}
"""

class Session(db.Model):
	# a globally unique identifier composed of a wave id, and a blip id
	sid = db.StringProperty(required=True)
	# a JSON array. each element of the array is an urquell frame
	frames = db.StringProperty(required=True)

class SessionWrapper(object):
	sid = None
	frames = None
	data = None
	
	def __init__(self,sid):	
		self.data = Session.gql("WHERE sid = :1", sid).fetch(1)
		if len(self.data): 
			self.sid, self.frames = data.sid,loads(self.data.frames)
		else:
			self.sid, self.frames, self.data = sid,{},Session(sid=sid,frames="{}")
			
	def save(self):
		self.data.frames = dumps(self.frames)
		db.put(self.data)