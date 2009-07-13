# -*- coding: utf-8 -*-
from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi import document

import re
from uri_validate import absolute_URI
URIregex = re.compile(absolute_URI, re.VERBOSE)

import urllib
from jsonrpc.json import dumps, loads
from google.appengine.api.urlfetch import fetch

from urquell.invocation import execute

def on_robot_added(properties, context):
  """Invoked when the robot has been added."""
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("Urquell calling")

def on_blip_submitted(properties, context):
  blipid = properties['blipId']
  blip = context.GetBlipById(blipid)
  content = blip.GetDocument().GetText()

  exec_pos = content.rfind('!x')
  desc_pos = content.rfind('!d')  	

  if exec_pos > -1:
    handle_exec(blip,content,exec_pos)	
  elif desc_pos > -1:
    handle_desc(blip,content,desc_pos)
	 
def handle_exec(blip, content, exec_pos):
  url_pos = content.rfind('http://')
  doc = blip.GetDocument()
  stack_frame = u''
  formatted_args = u''

  url = content[url_pos:exec_pos]
  result = execute(url)
  for a in result['args']:
    formatted_args += '%s ' % a

  stack_frame = u'Hash: %s\nName: %s\nArgs: %s\nResult: %s' % (result['hash'], result['name'], formatted_args, result['value'])
  doc.SetTextInRange(document.Range(url_pos,exec_pos + 2), ('%s\n\n%s' % (stack_frame,result['hash'])))

def handle_desc(blip, content, desc_pos):
  pass

def main():
  myRobot = robot.Robot(
      'urquell-fn',
      image_url='http://urquell-fn.appspot.com/assets/icon.jpg',
      version='4',
      profile_url='http://urquell-fn.appspot.com/'
  )
  myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, on_robot_added)
  myRobot.RegisterHandler(events.BLIP_SUBMITTED, on_blip_submitted)
  myRobot.Run()


if __name__ == '__main__':
    main()
