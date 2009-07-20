# -*- coding: utf-8 -*-
from waveapi import document

class Display(object):
    blip = None
    doc = None
    session = None

    def __init__(self,blip,session):
        self.blip = blip
        self.doc = blip.GetDocument()
        self.session = session
        self.doc.Clear()
        if not self.blip.IsRoot(): self.doc.AppendText('\n')
        self.doc.AppendText('Urquell Session - %s\n' % self.session.data.created.strftime('%Y.%m.%d - %H:%M'))


class FrameDisplay(Display):
    def display(self):
        format = u'\n%s\nHash: %s     Name: %s     Result: %s\nArgs: %s\n'
        for h,f in reversed(self.session.frames.items()):
            data = f['url'],f.get('hash','None'), f['name'], self.session.get_result(f), ', '.join(f['args'])
            self.doc.AppendText(format % data)
        self.doc.AppendText('\n%s' % self.session.frames.keys()[0] if self.session.frames.keys() else '')

class ModuleDisplay(Display):
	def display(self,frame):
		output = ('\nModule: %s\n' % frame['path'])
		if frame['value']['modules']:
			output += '\n%s\n' % 'Submodules:'
			for f in frame['value']['modules']: output += (' %s\n' % f['name'])
		if frame['value']['functions']:
			output += '\n%s\n' % 'Functions:'
			for f in frame['value']['functions']: output += (' %s\n' % f['name'])
		self.doc.AppendText(output)