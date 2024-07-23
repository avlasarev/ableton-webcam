import Live
from ableton.v2.control_surface import ControlSurface, MIDI_NOTE_TYPE
from ableton.v2.control_surface.control import ButtonControl

class MyRemoteScript(ControlSurface):
    def __init__(self, c_instance):
        super(MyRemoteScript, self).__init__(c_instance)
        self.song().add_tempo_listener(self._on_tempo_changed)
        self.log_message("MyRemoteScript Loaded")

    def _on_tempo_changed(self):
        tempo = self.song().tempo
        self.show_message(f"Current Tempo: {tempo}")
