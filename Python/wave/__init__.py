# -*- coding: utf-8 -*-
from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi import document
from google.appengine.api.urlfetch import fetch
from urquell.invocation import execute
from wave import session

# import re
# from uri_validate import absolute_URI
# URIregex = re.compile(absolute_URI, re.VERBOSE)
# 
# import urllib
# from jsonrpc.json import dumps, loads

class WaveHandler(object):
  content = None
  blip = None
  wavelet = None
  wave = None

  def on_robot_added(self,properties, context):
    """Invoked when the robot has been added."""
    root_wavelet = context.GetRootWavelet()
    root_wavelet.CreateBlip().GetDocument().SetText("Urquell calling - !x to execute, !d to describe")

  def on_document_changed(self,properties, context):
    blipid = properties['blipId']
    self.blip = context.GetBlipById(blipid)
    self.content = self.blip.GetDocument().GetText()
    self.wavelet = context.GetWaveletById(self.blip.GetWaveletId())
    self.wave = context.GetWaveById(self.blip.GetWaveId())
	
    exec_pos = self.content.rfind('!x')
    desc_pos = self.content.rfind('!d')

    if exec_pos > -1:
      self.handle_exec(exec_pos)
    elif desc_pos > -1:
      self.handle_desc(desc_pos)

  def handle_exec(self,exec_pos):
    doc = self.blip.GetDocument()
    expr_pos = self.content.find('http',self.content.rpartition('!x')[0].rfind('\n'))
    stack_frame = u''
    formatted_args = u''

    try:
      expr = self.content[expr_pos:exec_pos]
      result = execute(expr)
      if result:
        format = u'%s\nHash: %s     Name: %s     Result: %s\nArgs: %s'
        data = (expr,result['hash'], result['name'], result['value'], ', '.join(result['args']))
        stack_frame =  format % data
        doc.SetTextInRange(document.Range(expr_pos,exec_pos + 2), ('%s\n\n%s' % (stack_frame,result['hash'])))
    except Exception, e:
      doc.DeleteRange(document.Range(exec_pos,exec_pos + 2))
      self.wavelet.CreateBlip().GetDocument().SetText('\n\nException thrown:\n%s' % unicode(e))

  def handle_desc(self,desc_pos):
    pass

def main():
  myRobot = robot.Robot(
      'lurquell',
      image_url='http://urquell-fn.appspot.com/assets/icon.jpg',
      version='5',
      profile_url='http://urquell-fn.appspot.com/'
  )
  handler = WaveHandler()
  myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, handler.on_robot_added)
  myRobot.RegisterHandler(events.DOCUMENT_CHANGED, handler.on_document_changed)
  myRobot.Run()


if __name__ == '__main__':
    main()
