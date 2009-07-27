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
		self.doc.AppendText('Frames: %s    Errors: %s    Display: frames\n' % (len(session.frames),len(session.errors())))
		self.doc.SetAnnotation(document.Range(1,len(text)),'style/fontWeight','bold')
		
class FrameDisplay(Display):
	def display(self):
		s = Style()
		output = AnnotatedString(len(self.doc.GetText()))
		for f in self.session.ordered_frames():
			color = (s.red if self.session.is_error(f) else s.gray)
			output.a('%s\n%s\n' % (self.hr,f['url']),[s.lightGray])
			output.a('Hash: ',[color,s.bold])
			output.a('%s   ' % f.get('hash','None'),[s.gray])
			output.a('Result: ',[color,s.bold])
			output.a('%s\n' % self.session.get_result(f),[s.gray])
			output.a('Name: ',[color,s.bold])
			output.a('%s   ' % f['name'],[s.gray])
			output.a('Args: ',[color,s.bold])
			output.a('%s\n' % ', '.join(f.get('args','')),[s.gray])
		output.a(self.hr + '\n',[s.lightGray])
		self.doc.AppendText(output.string)
		output.apply(self.doc)

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

class HelpDisplay(Display):
	def display(self):
		s = Style()
		output = AnnotatedString(len(self.doc.GetText()))
		output.a('\nLurquell, an Urquell assistant\n\n',[s.red,s.bold])
		output.a("Lurquell aims to make writing programs in Urquell a reasonable endeavor. It does so by managing a collection of Urquell expressions in a session, and facilitating their perusal, manipulation, and composition. Lurquell evaluates the last line of a blip upon submission, and redisplays the modified session data. Interacting with Lurquell falls in the following pattern: ctrl-e to begin editing a blip, type,copy, paste input on the last line of the blip, shift-enter to submit the blip. rinse, repeat. Three types of input are understood:\n\n",[s.gray])
		output.a('Urquell expressions\n\n',[s.green,s.bold])
		output.a("All expressions in an Urquell program are URL's which return a JSON string representing the result of their evaluation. for example: http://urquell-fn.appspot.com/lib/echo/hello%20world. Lurquell collects the result of each evaluated URL in a Session attached to the blip in which it was submitted. An Urquell URL has been placed on the last line of this blip to get you started.\n\n",[s.gray])
		output.a('Urquell invocation hashes\n\n',[s.green,s.bold])
		output.a("The result of evaluating each Urquell expression contains an invocation hash. This hash can be used to reference the return value of the URL. These hashes are composed of 8 characters preceeded by a '*'. eg. *B5_YIEPO. If provided as input to Lurquell, the hash well be derefernced, and its associated Urquell expression displayed.\n\n",[s.gray])
		output.a('Lurquell commands\n\n',[s.green,s.bold])		
		output.a("Currently two commands are implemented: !reset clears the current session data. !help displays this help text\n\n",[s.gray])
		self.doc.AppendText(output.string + 'http://urquell-fn.appspot.com/lib')
		output.apply(self.doc)

class AnnotatedString(object):
	string = ''
	offset = 0
	notes = None

	def __init__(self,offset = 0):
		self.offset,self.notes = offset,[]

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
	gray = ('style/color','rgb(82, 82, 82)')
	lightGray = ('style/color','rgb(192, 192, 192)')
	green = ('style/color','rgb(0, 51, 0)')
	red = ('style/color','rgb(152, 51, 51)')

	def color(self,values): return ('style/color',('rgb(%s)' % values))
