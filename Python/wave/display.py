# -*- coding: utf-8 -*-
from waveapi import document

class Display(object):
    doc = None
    session = None

    def __init__(self,doc,session):
        self.doc = doc
        self.session = session

class FrameDisplay(Display):
    def display(self):
        self.doc.Clear()
        format = u'\n%s\nHash: %s     Name: %s     Result: %s\nArgs: %s\n'
        for h,f in self.session.frames.items():
            data = f['url'],f['hash'], f['name'], f['value'], ', '.join(f['args'])
            self.doc.AppendText(format % data)
        self.doc.AppendText('\n%s' % 'hash')
