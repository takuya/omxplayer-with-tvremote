#!/usr/bin/env python3
# coding: utf8

import argparse
import os
import sys
import atexit
import signal
import time

path = os.path.dirname(os.path.abspath(__file__+'/../'))
sys.path.append(path)

import TVRemoteOmxplayer



def main(args):
  
  player = TVRemoteOmxplayer.TVRemoteOmxplayer()
  def on_exit():
    player.on_exit()

  atexit.register( on_exit )

  def func(num,frame):
    player.on_exit()
    sys.exit()
  
  signal.signal(signal.SIGINT,  func)
  signal.signal(signal.SIGTERM, func)
  
  args = vars(args)
  url = args['URL'][0]
  options = args['omxplayer_options']
  player.play( url , *options )




if __name__ == "__main__" :
  

  parser = argparse.ArgumentParser(description='omxplayer をTVリモコンと連動させて起動します。')
  parser.add_argument('URL', metavar='URL', type=str, nargs=1,help='movie path or url')
  parser.add_argument('omxplayer_options', metavar='options',nargs=argparse.REMAINDER,help='options pass to omxplayer')
  
  args = parser.parse_args()
  main(args)
  

