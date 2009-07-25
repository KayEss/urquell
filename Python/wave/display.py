# -*- coding: utf-8 -*-
from waveapi import document
		
class Display(object):
	blip = None
	doc = None
	session = None
	style = None

	def __init__(self,blip,session):
		self.blip = blip
		self.doc = blip.GetDocument()
		self.session = session
		self.doc.Clear()
		self.style = self.Style()
		text = u''
		if not self.blip.IsRoot(): text += ' \n'
		text += 'Urquell Session'
		self.doc.AppendText('%s - %s\n' % (text,self.session.data.created.strftime('%Y.%m.%d - %H:%M')))
		self.doc.SetAnnotation(document.Range(1,len(text)),'style/fontWeight','bold')

	class Style(object):
		bold = ('style/fontWeight','bold')
		def color(self,values): return ('style/color',('rgb(%s)' % values))
		def bgcolor(self,values): return ('style/backgroundColor',('rgb(%s)' % values))
		def link(self,target): return ('link/auto',target)
		
class FrameDisplay(Display):
	def display(self):
		output = ''
		hr_ranges = []
		header_len = len(self.doc.GetText())
		hr = '---------------------------------------------------------------------------------------------------'
		format = u'%s\n%s\n  Hash: %s   Result: %s\n  Name: %s   Args: %s\n'
		for f in self.session.ordered_frames():
			pos = header_len + len(output)
			hr_ranges.append(document.Range(pos,(pos + len(hr))))
			data = hr,f['url'],f.get('hash','None'), self.session.get_result(f), f['name'], ', '.join(f.get('args',''))
			output += (format % data)
		self.doc.AppendText(output + hr + '\n')
		for r in hr_ranges[1:]: self.doc.SetAnnotation(r,'style/color','rgb(182, 182, 182)')

class ModuleDisplay(Display):
	def display(self,frame):
		s = self.style
		output = AnnotatedString(len(self.doc.GetText()))
		output.a(('\nModule: %s\n' % frame['path']),[s.color('102, 51, 51'),s.bold])
		if frame['value']['modules']:
			output.a(('\n%s\n    ' % 'Submodules:'),[s.color('0, 51, 0'),s.bold])
			names = map(lambda x: x['name'], frame['value']['modules'])
			output.a('    '.join(names),[s.color('92, 92, 92')])
		if frame['value']['functions']:
			output.a(('\n%s\n   ' % 'Functions:'),[s.color('0, 51, 0'),s.bold])
			names = map(lambda x: x['name'], frame['value']['functions'])
			output.a('    '.join(names),[s.color('92, 92, 92')])
		self.doc.AppendText(output.string)
		output.apply(self.doc)
		
class AnnotatedString(object):
	string = ''
	offset = 0
	notes = []

	def __init__(self,offset = 0):
		self.offset = offset
		
	def a(self,string,notes = None):
		if not notes: 
			self.string += string
			return			
		beg = len(self.string) + self.offset
		end = beg + len(string)
		self.string += string
		for n in notes: self.notes.append((document.Range(beg,end),n[0],n[1]))
		return self	
			
	def apply(self,doc):
		for n in self.notes: doc.SetAnnotation(n[0],n[1],n[2])