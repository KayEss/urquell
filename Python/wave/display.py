# -*- coding: utf-8 -*-
from waveapi import document
		
class Display(object):
	blip = None
	doc = None
	session = None
	hr = '---------------------------------------------------------------------------------------------------'

	def __init__(self,blip,session):
		self.blip = blip
		self.doc = blip.GetDocument()
		self.session = session
		self.doc.Clear()
		text = u''
		if not self.blip.IsRoot(): text += ' \n'
		text += 'Urquell Session'
		self.doc.AppendText('%s - %s\n' % (text,self.session.data.created.strftime('%Y.%m.%d - %H:%M')))
		self.doc.SetAnnotation(document.Range(1,len(text)),'style/fontWeight','bold')
		
class FrameDisplay(Display):
	def display(self):
		output = ''
		hr_ranges = []
		header_len = len(self.doc.GetText())
		format = u'%s\n%s\n  Hash: %s   Result: %s\n  Name: %s   Args: %s\n'
		for f in self.session.ordered_frames():
			pos = header_len + len(output)
			hr_ranges.append(document.Range(pos,(pos + len(self.hr))))
			data = self.hr,f['url'],f.get('hash','None'), self.session.get_result(f), f['name'], ', '.join(f.get('args',''))
			output += (format % data)
		self.doc.AppendText(output + self.hr + '\n')
		for r in hr_ranges[1:]: self.doc.SetAnnotation(r,'style/color','rgb(182, 182, 182)')

class ModuleDisplay(Display):
	def display(self,frame):
		s = Style()
		output = AnnotatedString(len(self.doc.GetText()))
		output.a(self.hr,[s.lightGray])
		output.a(('\nModule: %s\n' % frame['path']),[s.red,s.bold,s.underline])
		if frame['value']['modules']:
			names = map(lambda x: x['name'], frame['value']['modules'])
			output.a(('\n%s\n' % 'Submodules:'),[s.green,s.bold])
			output.a('    '.join(names),[s.gray])
		if frame['value']['functions']:
			names = map(lambda x: x['name'], frame['value']['functions'])
			output.a(('\n%s\n' % 'Functions:'),[s.green,s.bold])
			output.a('    '.join(names) + '\n',[s.gray])
		output.a(self.hr + '\n',[s.lightGray])
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
		
class Style(object):
	bold = ('style/fontWeight','bold')
	underline = ('style/fontDecoration','underline')
	gray = ('style/color','rgb(92, 92, 92)')
	lightGray = ('style/color','rgb(192, 192, 192)')
	green = ('style/color','rgb(0, 51, 0)')
	red = ('style/color','rgb(102, 51, 51)')

	def color(self,values): return ('style/color',('rgb(%s)' % values))
