import gi, os, vlc
from modules import dialog
from vlc import callbackmethod
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('GdkX11', '3.0')

MRL = ""

@callbackmethod
def clip_finished(self, player):
    print("Hello")
    player.is_player_active = False
    player.playback_button.set_image(player.play_image)
    return



class Player(Gtk.Window):

    is_player_active = False
    player_paused = False


    play_image = None
    pause_image = None
    stop_image = None

    def __init__(self, file = ''):
        global MRL

        MRL = file

        if not os.path.isfile(MRL):
            dialog.ErrorMsg('This file does not exist.')

        else:
            Gtk.Settings.get_default().set_property("gtk-icon-theme-name", "HighContrast")
            Gtk.Settings.get_default().set_property("gtk-theme-name", "HighContrast")

            Gtk.Window.__init__(self, title="Media Player")
            self.connect("destroy", Gtk.main_quit)

            self.playback_button = Gtk.Button()
            self.stop_button = Gtk.Button()
            self.draw_area = Gtk.DrawingArea()
            self.hbox = Gtk.Box(spacing=6)
            self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

            self.setup_objects_and_events()
            self.show()

            Gtk.main()
            self.player.stop()
            self.vlcInstance.release()

    def show(self):
        self.show_all()
        
    def setup_objects_and_events(self):
        
        self.play_image = Gtk.Image.new_from_icon_name(
                "media-playback-start",
                Gtk.IconSize.MENU
            )
        self.pause_image = Gtk.Image.new_from_icon_name(
                "media-playback-pause",
                Gtk.IconSize.MENU
            )
        self.stop_image = Gtk.Image.new_from_icon_name(
                "media-playback-stop",
                Gtk.IconSize.MENU
            )
        self.playback_button.set_image(self.play_image)
        self.stop_button.set_image(self.stop_image)
        
        self.playback_button.connect("clicked", self.toggle_player_playback)
        self.stop_button.connect("clicked", self.stop_player)

        self.draw_area.set_size_request(1200,800)
        
        self.draw_area.connect("realize",self._realized)

        self.hbox.pack_start(self.playback_button, True, True, 0)
        self.hbox.pack_start(self.stop_button, True, True, 0)

        self.add(self.vbox)
        self.vbox.pack_start(self.draw_area, True, True, 0)
        self.vbox.pack_start(self.hbox, False, False, 0)

    def stop_player(self, widget, data=None):
        if self.player_paused:
            self.player.stop()
        else:
            self.player.stop()
            self.is_player_active = False
            self.playback_button.set_image(self.play_image)

        
    def toggle_player_playback(self, widget, data=None):

        if self.is_player_active == False and self.player_paused == False:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.is_player_active = True

        elif self.is_player_active == True and self.player_paused == True:
            self.player.play()
            self.playback_button.set_image(self.pause_image)
            self.player_paused = False

        elif self.is_player_active == True and self.player_paused == False:
            self.player.pause()
            self.playback_button.set_image(self.play_image)
            self.player_paused = True
        else:
            pass
        
    def _realized(self, widget, data=None):
        self.vlcInstance = vlc.Instance("--input-repeat=-1", "--fullscreen", "--no-xlib", "mouse-hide-timeout=5")
        self.player = self.vlcInstance.media_player_new()
        self.player.event = self.player.event_manager()
        self.player.event.event_attach(vlc.EventType.MediaPlayerEndReached, clip_finished, self)
        win_id = widget.get_window().get_xid()
        self.player.set_xwindow(win_id)
        self.player.set_mrl(MRL)
        self.playback_button.set_image(self.play_image)