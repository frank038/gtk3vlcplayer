# gtk3vlcplayer
A very simple vlc frontend made with python and gtk3.
Free to use and modify

Requirements:
- python
- gtk3
- vlc

How to play a video file:
gtk3vlcplayer.py video.file

Optionals: media:MEDIA_OPTIONS player:VIDEO_OPTIONS --fullscreen
where MEDIA_OPTIONS must be in the form: option1=value:option2=value (without "--" at the beginning)
and VIDEO_OPTIONS must be in the form: option1:option2 (without "--" at the beginning().

Features:
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
- accept (which ones?) options for the media and the player from the command line.

This program supports a very few custom settings. They can be found and changed at the beginning of the file.

![My image](https://github.com/frank038/gtk2vlcplayer/blob/main/screenshot.png)
