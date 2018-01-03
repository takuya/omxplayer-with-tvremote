#!/usr/bin/env python



import atexit
import time
import subprocess
import re
from threading import Thread

class CecClient(object):
  
  regex_pattern = "(?<=key released: )\w+\s(((\w+)?\s?(\w+)?)?\s?\(\w+\))"
 
  
  def __init__(self):
    self.pattern = re.compile( CecClient.regex_pattern )
  
  def watch(self):
    self.cec_proc = subprocess.Popen(["cec-client"], stdout=subprocess.PIPE)
  
    while True:
      line = self.cec_proc.stdout.readline()
      line = line.decode("utf-8")
    
      match = re.search( self.regex_pattern ,line )
      if match :
        key =  match[0]
        self.dispatch(key)

  def run(self):
    self.cec_th = Thread( target=self.watch, daemon=True )
    self.cec_th.start()
    return self.cec_th
    
  
  def dispatch(self,key):
    
    match = re.search( "[^\(]+", key )
    key =  match[0]
    key = re.sub('\s+$', "", key)
    key = re.sub('\s', "_", key)
    
    name = f"on_{key}"
    if hasattr(self,name) :
      method = getattr(self,name)
      method()
    else:
      print(f"{key} pressed, but no action defined")
  
  
  def on_right(self):
    print(" right button.")
  
  def on_down(self):
    print(" down button.")
  
  def on_left(self):
    print(" left button.")
  
  def on_up(self):
    print(" up button.")
  
  def on_play(self):
    print(" play button.")
  
  def on_select(self):
    print(" select  button.")
  
  def on_pause(self):
    print(" pause button.")
  
  def on_forward(self):
    print(" forward button.")
  
  def on_backward(self):
    print(" backward button.")
  
  def on_exit(self):
    print(" exit button.")
  
  def on_clear(self):
    print(" clear button.")


def on_exit():
  print("Good-Bye\n")


if __name__ == "__main__" :
  
  atexit.register( on_exit )
  try:
    cec = CecClient()
    cec.start()
  
  except KeyboardInterrupt:
    pass
  
