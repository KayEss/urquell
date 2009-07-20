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
        frames = self.session.frames.items()
        frames.reverse
        format = u'\n%s\nHash: %s     Name: %s     Result: %s\nArgs: %s\n'
        for h,f in frames:
            data = f['url'],f.get('hash','None'), f['name'], self.session.get_result(f), ', '.join(f['args'])
            self.doc.AppendText(format % data)
        self.doc.AppendText('\n%s' % self.session.frames.keys()[0] if self.session.frames.keys() else '')