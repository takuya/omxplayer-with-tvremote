## Raspberry Pi omxplayer を TV リモコンで操作する


raspi の omxplayer で動画再生中に、テレビのリモコンで操作できるようにする。

## 準備
```
sudo apt install cec-client
git clone https://github.com/takuya/omxplayer-with-tvremote
```

## 使い方

```
./bin/omxplayer-with-tvremote.py URL
```

## プロセス管理

omxplayer を複数起動しないように管理するサンプル
```
bin/omxplayer-daemon.rb restart -- URL
```

## Reference 

http://takuya-1st.hatenablog.jp/entry/2017/12/27/175608
