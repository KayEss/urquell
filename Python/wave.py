from waveapi import events
from waveapi import model
from waveapi import robot

import re
from uri_validate import absolute_URI
URIregex = re.compile(absolute_URI, re.VERBOSE)

from jsonrpc.json import dumps, loads
from google.appengine.api.urlfetch import fetch


def OnRobotAdded(properties, context):
  """Invoked when the robot has been added."""
  Notify(context, "Urquell calling")

def OnBlipSubmitted(properties, context):
  root_wavelet = context.GetRootWavelet()
  blipid = properties['blipId']
  blip = context.GetBlipById(blipid)

  content = blip.GetDocument().GetText()
  feedback = u''

  for url in URIregex.findall(content):
    if url.startswith('http://urquell-fn.appspot.com/'):
      feedback = url.replace('_', '__').replace('/','_s').replace(':', '_c')
      feedback = u'=%s\nResult: %s' % (feedback, loads(fetch(url).content)['value'])
  if feedback:
    notify = blip.CreateChild()
    notify.GetDocument().SetText(feedback)

def Notify(context, text):
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText(text)


if __name__ == '__main__':
  myRobot = robot.Robot(
      'urquell-fn', 
      image_url='http://urquell-fn.appspot.com/assets/icon.jpg',
      version='4',
      profile_url='http://urquell-fn.appspot.com/'
  )
  myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
  myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
  myRobot.Run()
