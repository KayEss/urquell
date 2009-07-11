# -*- coding: utf-8 -*-
from waveapi import events
from waveapi import model
from waveapi import robot

import re
from uri_validate import absolute_URI
URIregex = re.compile(absolute_URI, re.VERBOSE)

import urllib
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
      bitly_hash = bitly(url)
      result = loads(fetch(url).content)
      feedback = u'\n\nHash: =%s\nName: %s\nArgs: %s\nResult: %s' % (bitly_hash, result['name'], result['args'], result['value'])
  if feedback:
    notify = blip.CreateChild()
    notify.GetDocument().SetText(feedback)

def Notify(context, text):
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText(text)

def bitly(url):
  quoted = urllib.quote(url)
  request = "http://api.bit.ly/shorten?version=2.0.1&longUrl="
  request += quoted
  request += "&login=rburns&apiKey=R_1ece1bb73288d02b25f7613d25ac63ce"
  return loads(fetch(request).content)['results'][url]['userHash']

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
