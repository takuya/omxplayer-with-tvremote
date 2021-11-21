#!/usr/bin/env ruby

## ssh 経由で制御するサンプル


require 'daemons'
require 'pp'

system('mkdir -p /usr/local/var/run') unless Dir.exists? '/usr/local/var/run'
# PLAYER_CMD = File.expand_path('sleep.py', File.realpath( File.dirname(__FILE__)))
PYTHON = "/home/takuya/.pyenv/shims/python3.6"
PLAYER_CMD = File.expand_path('omxplayer-with-tvremote.py', File.realpath( File.dirname(__FILE__)))



options = {
  :dir_mode   => :normal,
  :multiple   => false,
  :ontop      => false,
  :mode       => :exec,
  :backtrace  => true,
  :monitor    => false,
}





def main_proc(argv)

  player_cmd = PLAYER_CMD
  pid = nil

  Signal.trap(:TERM){
    puts "TERMを貰ったので送信する"
    Process.kill :TERM, pid if pid
    exit
  }


  raise 'too short arguments' unless argv.rindex('--')
  argv = argv[(argv.rindex('--')+1)..-1]
  urls = argv

  s = Thread.new {
    system("echo 'as 0 ' | cec-client -s --log-level 1 ")
    system("echo 'as 0 ' | cec-client -s --log-level 1 ")
  }
  s.join


  urls.each{|url|
    puts '--' * 10
    puts url
    pid = spawn(PYTHON, player_cmd, *url )
    Process.wait pid
  }
  
  s = Thread.new {
    system("echo 'standby 0 ' | cec-client -s --log-level 1 ")
  }
  s.join
end

if __FILE__ == $0 then
  Daemons.run_proc("omxplayer-with-tvremote-daemon" , options ){
    cmd =  main_proc(ARGV)
  }
end
