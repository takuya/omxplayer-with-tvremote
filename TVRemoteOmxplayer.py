#!/usr/bin/env python

import re
import shlex
import subprocess

from CecClient import CecClient

class TVRemoteOmxplayer(CecClient):
  
  KEY_UP   = b'\[A'
  KEY_DOWN = b'\[B'
  KEY_RIGHT= b'\[C'
  KEY_LEFT = b'\[D'
  """
           1           decrease speed
           2           increase speed
           <           rewind
           >           fast forward
           z           show info
           j           previous audio stream
           k           next audio stream
           i           previous chapter
           o           next chapter
           n           previous subtitle stream
           m           next subtitle stream
           s           toggle subtitles
           w           show subtitles
           x           hide subtitles
           d           decrease subtitle delay (- 250 ms)
           f           increase subtitle delay (+ 250 ms)
           q           exit omxplayer
           p / space   pause/resume
           -           decrease volume
           + / =       increase volume
           left arrow  seek -30 seconds
           right arrow seek +30 seconds
           down arrow  seek -600 seconds
           up arrow    seek +600 seconds
  """
  
  keymap_of_omxplayer = {
    'decrease speed': b'1',
    'increase speed': b'2',
    'rewind': b'<',
    'fast forward': b'>',
    'show info': b'z',
    'previous audio stream': b'j',
    'next audio stream': b'k',
    'previous chapter': b'i',
    'next chapter': b'o',
    'previous subtitle stream': b'n',
    'next subtitle stream': b'm',
    'toggle subtitles': b's',
    'show subtitles': b'w',
    'hide subtitles': b'x',
    'decrease subtitle delay (- 250 ms)': b'd',
    'increase subtitle delay (+ 250 ms)': b'f',
    'exit omxplayer': b'q',
    'pause/resume': b'p',
    'decrease volume': b'-',
    'increase volume': b'+',
    'seek -30 seconds': KEY_LEFT,
    'seek +30 seconds': KEY_RIGHT,
    'seek -600 seconds': KEY_DOWN,
    'seek +600 seconds': KEY_UP,
    }
  keymap_tvremote_to_omxplayer_action ={
    
    'select':'pause/resume',
    'right':'seek +30 seconds',
    'left':'seek -30 seconds',
    'down':'seek -600 seconds',
    'up':'seek +600 seconds',
    'F1':'decrease speed',
    'F2':'increase speed',
    'F3':'rewind',
    'F4':'fast forward',
    'exit':'exit omxplayer',
    'channel_down':'decrease volume',
    'channel_up':'increase volume',
    'rewind':'rewind',
    'Fast_forward':'fast forward',
    
    }
  
  def __init__(self):
    super().__init__()
  def play(self, url, *options):
    cmd = f"omxplayer '{url}' "
    if len(options) > 0 :
      cmd = cmd + ' '.join(options)
    print(cmd)
    cmd = shlex.split(cmd)
    self.p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    self.start()
  def send_key_to_omxplayer(self,name_of_command):
    key = self.keymap_of_omxplayer[name_of_command]
    self.p.stdin.write(key)
    self.p.stdin.flush()

  def exit(self):
    self.on_exit()

  def on_exit(self):
    if hasattr(self,'p') :
      self.p.terminate()
    if hasattr(self,'cec_proc') :
      self.cec_proc.terminate()
      
  
  def dispatch(self,key):
    
    match = re.search( "[^\(]+", key )
    key =  match[0]
    key = re.sub('\s+$', "", key)
    key = re.sub('\s', "_", key)
    
    
    if key in self.keymap_tvremote_to_omxplayer_action:
      omxplayer_key = self.keymap_tvremote_to_omxplayer_action[key]
      self.send_key_to_omxplayer(omxplayer_key)
      if key == 'exit':
        self.on_exit()
        exit()
    else:
      print(f"{key} pressed, but no action defined")




