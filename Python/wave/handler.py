# -*- coding: utf-8 -*-
from waveapi import model
from waveapi import document
from urquell.invocation import execute
from wave.session import SessionWrapper
from wave.display import FrameDisplay
from wave.display import ModuleDisplay
import traceback

class WaveHandler(object):
  content = None
  blip = None
  wavelet = None
  wave = None

  def on_robot_added(self,properties, context):
    """Invoked when the robot has been added."""
    doc = context.GetRootWavelet().CreateBlip().GetDocument()
    welcome = "Urquell calling - !x to execute !reset to reset session."
    doc.SetText(welcome)
    doc.InsertElement(len(welcome),document.Gadget('http://urquell-fn.appspot.com/assets/wave-gadget.xml'))
	
  def on_blip_submitted(self,properties, context):
    blipid = properties['blipId']
    self.blip = context.GetBlipById(blipid)
    self.content = self.blip.GetDocument().GetText()
    self.wavelet = context.GetWaveletById(self.blip.GetWaveletId())
    self.wave = context.GetWaveById(self.blip.GetWaveId())
	
    last_line = self.content.strip().split('\n')[-1].strip()
    
    if last_line.find('http') > -1:
      self.handle_expr(last_line)
    if last_line.find('*') > -1:
      self.handle_hash(last_line)	
    elif last_line.find('!') > -1:
      self.handle_cmnd(last_line)

  def handle_expr(self,expr):
    doc = self.blip.GetDocument()
    stack_frame = u''
    formatted_args = u''

    try:
      sess = SessionWrapper(self.blip.GetId() + self.wave.GetId())
      result = execute(expr)
      if result and result.has_key('hash'):
        result['url'] = expr
        sess.frames[result['hash']] = result
        sess.save()
        FrameDisplay(self.blip,sess).display()
        doc.AppendText('\n%s' % result['hash'])
      elif result and result.has_key('value'):
        ModuleDisplay(self.blip,sess).display(result)
        doc.AppendText('\n%s' % expr)
      elif result and result.has_key('error'):
        data = result['headers']['Host'],result['path'],result['error']['message']
        self.wavelet.CreateBlip().GetDocument().SetText('\n\nExecution error:\nHost: %s\nPath: %s\nError: %s' % data)
        FrameDisplay(self.blip,sess).display()
    except Exception, e:
      self.wavelet.CreateBlip().GetDocument().SetText('\n\nException thrown:\n%s' % traceback.format_exc())

  def handle_hash(self,hash):
    pass

  def handle_cmnd(self,cmnd):
    sess = SessionWrapper(self.blip.GetId() + self.wave.GetId())
    sess.frames = {}
    sess.save()
    FrameDisplay(self.blip,sess).display()
    