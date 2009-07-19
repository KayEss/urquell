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

    def get_result(self,frame):
        if frame.has_key('value'): return frame['value']
        if frame.has_key('error'): return frame['error']['message']
        return 'None'

class FrameDisplay(Display):
    def display(self):
        format = u'\n%s\nHash: %s     Name: %s     Result: %s\nArgs: %s\n'
        for h,f in self.session.frames.items():
            data = f['url'],f['hash'], f['name'], self.get_result(f), ', '.join(f['args'])
            self.doc.AppendText(format % data)
        self.doc.AppendText('\n%s' % 'hash')
