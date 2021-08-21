# gtk3vlcplayer
A very simple vlc frontend made with python and gtk3.
Free to use and modify

Requirements:
- python3
- gtk3
- vlc

How to play a video file:
gtk3vlcplayer.py video.file

To get help press the h key.

Optionals: media:MEDIA_OPTIONS player:VIDEO_OPTIONS --fullscreen
where MEDIA_OPTIONS must be in the form: option1=value:option2=value (without "--" at the beginning)
and VIDEO_OPTIONS must be in the form: option1:option2 (without "--" at the beginning().

Features:
- play local media files
- play (direct) urls (initial or limited support), e.g.: gtk3vlcplayer.py "http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_1080p_30fps_normal.mp4"
- play dvb programs (initial or limited support), e.g.: gtk3vlcplayer.py dvb-t:// media:dvb-adapter=0:dvb-frequency=xxxxxxxxx:dvb-bandwidth=x:program=xxxx
- headbar support, if enabled
- file name in the titlebar
- play, pause, stop commands
- mute/unmute command
- seeking
- video duration and remaining (by clicking on the label)
- fullscreen, by pressing the f key or in the form: gtk3vlcplayer.py video.file --fullscreen
- pause/play by pressing the space key
- quit by pressing the esc key
- play a new file by pressing the o key
- play a new url by pressing the u key
- select a different audio track, if supported, by pressing the a key
- select a (different) subtitle track, if supported, by pressing the s key
- get some media infos by pressing the i key
- accept (which ones?) options for the media and the player from the command line.

This program supports a very few custom settings. They can be found and changed at the beginning of the file.

Known issues:
- the fullscreen by option or by pressing the f key could not work at all.

![My image](https://github.com/frank038/gtk2vlcplayer/blob/main/screenshot.png)
