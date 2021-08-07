#! /usr/bin/python3
# 20210807
##################

### image size in each button
# 1: MENU (16px); 2: DND (32px); 3: DIALOG (48px); 4: LARGE_TOOLBAR (24px); 5: BUTTON (16px); 6: SMALL_TOOLBAR (16px);
BUTTON_ICON_SIZE = 4

### width and height of the starting window
WWIDTH = 640
HHEIGHT = 640

### use the headbar instead of let the wm to decorate this window
USE_HEADBAR = 0

### needed for getting file to be loaded properly in seconds
TIME_TO_WAIT = 1

##################

import sys,os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from gi.repository import Gdk
gi.require_version('GdkX11', '3.0')
from gi.repository import GdkX11
import time
import vlc

if BUTTON_ICON_SIZE == 1:
    BUTTON_ICON_SIZE = Gtk.IconSize.MENU
elif BUTTON_ICON_SIZE == 2:
    BUTTON_ICON_SIZE = Gtk.IconSize.DND
elif BUTTON_ICON_SIZE == 3:
    BUTTON_ICON_SIZE = Gtk.IconSize.DIALOG
elif BUTTON_ICON_SIZE == 4:
    BUTTON_ICON_SIZE = Gtk.IconSize.LARGE_TOOLBAR
elif BUTTON_ICON_SIZE == 5:
    BUTTON_ICON_SIZE = Gtk.IconSize.BUTTON
elif BUTTON_ICON_SIZE == 6:
    BUTTON_ICON_SIZE = Gtk.IconSize.SMALL_TOOLBAR

MRL = ""

IS_FULLSCREEN = ""


# info dialog
class DialogBox(Gtk.Dialog):
 
    def __init__(self, parent, info):
        Gtk.Dialog.__init__(self, title="Info", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
 
        self.set_default_size(150, 100)
        
        label = Gtk.Label(label=info)
 
        box = self.get_content_area()
        box.add(label)
        self.show_all()

###################################

class ApplicationWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="PyVlc")
        self.player_paused=False
        self.is_player_active = False
        self.connect("destroy",Gtk.main_quit)
        self.connect("delete-event",Gtk.main_quit)
        self.connect("key-press-event", self.on_key_press)
        #
        if USE_HEADBAR:
            self.header = Gtk.HeaderBar(title="PyVlc")
            self.header.props.show_close_button = True
            self.set_titlebar(self.header)
    
    def show(self):
        self.show_all()
    
    def on_key_press(self, w, e):
        # press esc to close this window
        if e.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()
        
        # press o to open the file dialos
        elif e.keyval == Gdk.KEY_o:
            if self.player.get_state() == 3:
                self.player.pause()
                # 
                self.playback_button.set_image(self.play_image)
            self.on_file_clicked()
        
        # press f to set/unset fullscreen
        elif e.keyval == Gdk.KEY_f:
            isVisible = self.hbox.get_property("visible")
            if (isVisible):
                self.hbox.hide()
            else:
                self.hbox.show()

            self.player.toggle_fullscreen()
        
        # press space to toggle play/pause
        elif e.keyval == Gdk.KEY_space:
            self.on_toggle_player_playback()

    
    #
    def _otherStatus(self, n):
        if n == 1:
            msg = "Skipped"
        elif n == 2:
            msg = "Failed"
        elif n == 3:
            msg = "Timeout"
        dialog = DialogY(self, "Info", "Error: {}.".format(msg))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            Gtk.main_quit()
            sys.exit()
    
    
    def setup_objects_and_events(self):
        ###### player
        self.vlcInstance = vlc.Instance('--no-xlib')
        self.player = self.vlcInstance.media_player_new()
        m = self.vlcInstance.media_new(str(MRL))
        self.player.set_media(m)
        #
        self.player.video_set_key_input(False)
        self.player.video_set_mouse_input(False)
        #
        # Start the parser
        m.parse_with_options(0,1000)
        mTray = 0
        time.sleep(1)
        while True:
            # done
            if m.get_parsed_status() == 4:
                break
            # skipped
            elif m.get_parsed_status() == 1:
                self._otherStatus(1)
                break
            # failed
            elif m.get_parsed_status() == 2:
                self._otherStatus(2)
                break
            # timeout
            elif m.get_parsed_status() == 3:
                self._otherStatus(3)
                break
            else:
                mTray += 1
                if mTray == 5:
                    dialog = DialogY(self, "Info", "The media is taking too long.")
                    response = dialog.run()
                    if response == Gtk.ResponseType.OK:
                        Gtk.main_quit()
                        sys.exit()
                time.sleep(1)
        # video duration
        media_duration = m.get_duration()
        # video dimentions
        self.vw, self.vh = self.player.video_get_size()
        #
        self.movie_lenght = media_duration/1000
        # set the correct ratio
        video_ratio = round(self.vw/self.vh,2)
        NEW_WIDTH = int(HHEIGHT*video_ratio)
        self.resize(NEW_WIDTH, HHEIGHT)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # set the title of the window
        if USE_HEADBAR:
            self.header.set_title(os.path.basename(str(MRL)))
        else:
            self.set_title(os.path.basename(str(MRL)))
        
                
        # set fullscreen
        if IS_FULLSCREEN == "--fullscreen":
            self.player.set_fullscreen(True)
            
        #####################
        ###### the widgets
        ### the box
        self.hbox = Gtk.Box(spacing=6)
        #
        ### play/pause and stop buttons
        self.playback_button = Gtk.Button()
        self.stop_button = Gtk.Button()

        self.play_image = Gtk.Image.new_from_icon_name(
                "gtk-media-play",
                BUTTON_ICON_SIZE
            )
        self.pause_image = Gtk.Image.new_from_icon_name(
                "gtk-media-pause",
                BUTTON_ICON_SIZE
            )
        self.stop_image = Gtk.Image.new_from_icon_name(
                "gtk-media-stop",
                BUTTON_ICON_SIZE
            )

        self.playback_button.set_image(self.play_image)
        self.stop_button.set_image(self.stop_image)
        
        self.hbox.pack_start(self.playback_button, True, True, 0)
        self.hbox.pack_start(self.stop_button, True, True, 0)
        
        self.playback_button.connect("clicked", self.toggle_player_playback)
        self.stop_button.connect("clicked", self.stop_player)
        #
        ### mute/unmute button
        self.unmute_image = Gtk.Image.new_from_icon_name(
                "audio-volume-high",
                BUTTON_ICON_SIZE
            )
        self.mute_image = Gtk.Image.new_from_icon_name(
                "audio-volume-muted",
                BUTTON_ICON_SIZE
            )
        self.toggle_mute_btn = Gtk.Button(image=self.unmute_image)
        self.toggle_mute_btn.connect("clicked", self.toggle_audio_mute)
        self.hbox.pack_start(self.toggle_mute_btn, False, False, 0)
        #
        ### the drawing area
        self.draw_area = Gtk.DrawingArea()
        self.draw_area.set_size_request(WWIDTH,HHEIGHT)
        #
        self.draw_area.connect("realize",self._realized)
        self.draw_area.connect('draw', self.onExposeEvent)

        ### scale
        min_val = 0.0
        max_val = 1.0
        step_val = 0.001
        self.scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, min_val, max_val, step_val)
        self.scale.set_draw_value(False)
        self.scale.connect("button-release-event", self.on_scale_changed)
        self.scale.connect("key-release-event", self.on_scale_changed)
        #
        box_scale = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        box_scale.pack_start(self.scale, True, True, 0)
        #
        ### the label and its event box
        self.label_scale = Gtk.Label(label="0:00:00")
        #
        label_eventbox = Gtk.EventBox()
        label_eventbox.set_events(Gdk.EventMask.BUTTON_PRESS_MASK| Gdk.EventMask.POINTER_MOTION_MASK)
        label_eventbox.connect("button-press-event", self.on_pb_click)
        label_eventbox.add(self.label_scale)
        box_scale.pack_start(label_eventbox, False, False, 0)
        # label state: 0 normal - 1 reversed
        self.label_state = False
        
        ### main box
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        self.vbox.pack_start(self.draw_area, True, True, 0)
        self.vbox.pack_start(box_scale, False, False, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)
    
    
    def toggle_player_playback(self, widget, data=None):
        self.on_toggle_player_playback()
        
    
    def on_toggle_player_playback(self):
        player_state = self.player.get_state()
        # playing
        if player_state == 3 and self.player.can_pause():
            self.player.pause()
            self.playback_button.set_image(self.play_image)
        # paused
        elif player_state == 4:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
        # error
        if player_state == 7:
            self.playback_button.set_image(self.play_image)
            self.player.stop()
        
    
    def stop_player(self, widget, data=None):
        if self.player.is_playing():
            self.player.stop()
            self.playback_button.set_image(self.play_image)
    
        
    def toggle_audio_mute(self, w):
        #self.player.audio_toggle_mute()
        a_bool = self.player.audio_get_mute()
        if a_bool == 1:
            self.toggle_mute_btn.set_image(self.unmute_image)
            self.player.audio_set_mute(False)
        elif a_bool == 0:
            self.toggle_mute_btn.set_image(self.mute_image)
            self.player.audio_set_mute(True)
        # elif a_bool == -1:
            # pass
    
    
    # scrolling the scale widget by mouse
    def on_scale_changed(self, scale, data):
        # the media is seekable
        if self.player.is_seekable():
            new_value = self.scale.get_value()
            self.player.set_position(new_value)
            
    
    # label mouse button clicked
    def on_pb_click(self, w, e, d=None):
        self.label_state = not self.label_state

    
    def newMedia(self):
        pret = self._play()
        #
        m = self.player.get_media()
        media_duration = m.get_duration()
        self.movie_lenght = media_duration/1000
        self.label_state = False
        #
        self.vw, self.vh = self.player.video_get_size()
        video_ratio = round(self.vw/self.vh,2)
        NEW_WIDTH = int(HHEIGHT*video_ratio)
        self.resize(NEW_WIDTH, HHEIGHT)
        self.set_position(Gtk.WindowPosition.CENTER)
    
    
    def oldMedia(self):
        self.on_toggle_player_playback()
        
    
    def _realized(self, widget, data=None):
        win_id = widget.get_window().get_xid()
        self.player.set_xwindow(win_id)
        #
        pret = self._play()
        if pret:
            GLib.timeout_add(1000,self.update_pb)
    
    #
    def _play(self):
        self.player.play()
        time.sleep(TIME_TO_WAIT)
        CAN_PLAY = self.player.will_play()
        if CAN_PLAY == 0 or CAN_PLAY == False:
            dialog = DialogY(self, "Error", "Cannot play this media.")
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                Gtk.main_quit()
                sys.exit()
        self.player.audio_set_mute(False)
        
        # set the pause image
        if self.player.is_playing():
            self.playback_button.set_image(self.pause_image)
            return 1

    
    # update the scale widget position and label every second
    def update_pb(self):
        # media is ended
        if self.player.get_state() == 6:
            self.playback_button.set_image(self.play_image)
            self.player.stop()
        #
        new_pos = self.player.get_position()
        self.scale.set_value(new_pos)
        
        if self.label_state:
            to_play_time = self.movie_lenght - self.player.get_time()/1000
            m, s = divmod(to_play_time, 60)
            h, m = divmod(m, 60)
            self.label_scale.set_text('{:d}:{:02d}:{:02d}'.format(int(h), int(m), int(s)))
        # 
        else:
            play_time = self.player.get_time()/1000
            m, s = divmod(play_time, 60)
            h, m = divmod(m, 60)
            self.label_scale.set_text('{:d}:{:02d}:{:02d}'.format(int(h), int(m), int(s)))
        # stopped
        if self.player.get_state() == 5:
            self.label_scale.set_text("-:--:--")
        
        return True
        
    
    def onExposeEvent(self, area, context):
        context.scale(area.get_allocated_width(), area.get_allocated_height())    
        context.set_source_rgb(0.5, 0.5, 0.7)
        context.fill() 
        context.paint()
    
    
    def on_file_clicked(self):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            selected_file = dialog.get_filename()
            m = self.vlcInstance.media_new(str(selected_file))
            self.player.set_media(m)
            self.set_title(os.path.basename(str(selected_file)))
            self.newMedia()
        elif response == Gtk.ResponseType.CANCEL:
            self.oldMedia()

        dialog.destroy()


###################################

class DialogY(Gtk.Dialog):
    def __init__(self, parent, title, info):
        Gtk.Dialog.__init__(self, title=title, transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label=info)

        box = self.get_content_area()
        box.add(label)
        self.show_all()


#### dialog YES/NO
class DialogYN(Gtk.Dialog):
    def __init__(self, parent, title, info):
        Gtk.Dialog.__init__(self, title=title, transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label=info)

        box = self.get_content_area()
        box.add(label)
        self.show_all()


if __name__ == '__main__':
    if not sys.argv[1:]:
        dialog = DialogBox(None, "Exiting \nMust provide one file.")
        dialog.run()
        dialog.destroy()
        sys.exit(1)
    if len(sys.argv[1:]) == 1:
        MRL = sys.argv[1]
        window = ApplicationWindow()
        window.setup_objects_and_events()
        window.show()
        Gtk.main()
        window.player.stop()
        window.vlcInstance.release()
    elif len(sys.argv[1:]) == 2:
        MRL = sys.argv[1]
        IS_FULLSCREEN = sys.argv[2]
        window = ApplicationWindow()
        window.setup_objects_and_events()
        window.show()
        Gtk.main()
        window.player.stop()
        window.vlcInstance.release()
