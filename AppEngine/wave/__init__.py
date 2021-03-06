# -*- coding: utf-8 -*-
from waveapi import events
from waveapi import robot
from wave.handler import WaveHandler

def main():
  myRobot = robot.Robot(
      'lurquell',
      image_url='http://urquell-fn.appspot.com/assets/icon.jpg',
      version='7',
      profile_url='http://urquell-fn.appspot.com/'
  )
  handler = WaveHandler()
  myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, handler.on_robot_added)
  myRobot.RegisterHandler(events.BLIP_SUBMITTED, handler.on_blip_submitted)
  myRobot.Run()


if __name__ == '__main__':
    main()
