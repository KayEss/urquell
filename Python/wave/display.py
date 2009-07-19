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
        for h,f in self.session.frames.items():
            data = f['url'],f['hash'], f['name'], f['value'], ', '.join(f['args'])
            self.doc.AppendText(format % data)
        self.doc.AppendText('\n%s' % 'hash')
