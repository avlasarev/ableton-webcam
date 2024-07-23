from __future__ import with_statement
import Live
from ableton.v2.control_surface import ControlSurface, MIDI_NOTE_TYPE
from ableton.v2.control_surface.control import ButtonControl

class MyRemoteScript(ControlSurface):
    def __init__(self, c_instance):
        super(MyRemoteScript, self).__init__(c_instance)
        self._c_instance = c_instance
        self.log_message("MyRemoteScript loaded")
        with self.component_guard():
            self._setup_controls()
            self._setup_listeners()

    def _setup_controls(self):
        self._play_button = ButtonControl()

    def _setup_listeners(self):
        self._c_instance.song().add_is_playing_listener(self._on_play)

    def _on_play(self):
        self.log_message("Playing: %s" % self._c_instance.song().is_playing)
