from waveapi import events
from waveapi import model
from waveapi import robot


def OnRobotAdded(properties, context):
  """Invoked when the robot has been added."""
  root_wavelet = context.GetRootWavelet()
  Notify(context, "Urquell calling")

def OnBlipSubmitted(properties, context):
  root_wavelet = context.GetRootWavelet()
  Notify(context, "Blip submitted")


def Notify(context, text):
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText(text)


if __name__ == '__main__':
  myRobot = robot.Robot('urquell-fn', 
      image_url='http://urquell-fn.appspot.com/icon.png',
      version='2',
      profile_url='http://urquell-fn.appspot.com/')
  myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
  myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
  myRobot.Run()
