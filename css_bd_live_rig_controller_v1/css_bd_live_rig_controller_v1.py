from __future__ import division
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.Layer import Layer
from _Framework.DeviceComponent import DeviceComponent
from _Framework.MixerComponent import MixerComponent
from _Framework.SliderElement import SliderElement
from _Framework.TransportComponent import TransportComponent
from _Framework.InputControlElement import *
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.SessionComponent import SessionComponent
from _Framework.EncoderElement import *
from Launchpad.ConfigurableButtonElement import ConfigurableButtonElement
import time
from itertools import imap, chain
from _Framework.Util import find_if
import collections
try:
	from user import *
except ImportError:
	from user import *

class css_bd_live_rig_controller_v1(ControlSurface):
	def __init__(self, c_instance):
		super(css_bd_live_rig_controller_v1, self).__init__(c_instance)
		with self.component_guard():
			global _map_modes
			_map_modes = Live.MidiMap.MapMode
			self.current_track_offset = 0
			self.current_scene_offset = 0
			# mixer
			global mixer
			num_tracks = 128
			num_returns = 24
			self._settings()
			self._inputs()
			self.turn_inputs_off()
			self.mixer = MixerComponent(num_tracks, num_returns)
			global active_mode
			self.debug_on = False
			self.device_parameter_banks()
			self.mode_list()
			self.set_active_mode(self.modes[0])
			self.listening_to_tracks()
			self.song().add_tracks_listener(self.listening_to_tracks)

	def _settings(self):
		self.global_feedback = "default"
		self.global_feedback_active = True
		self.global_LED_on = 127
		self.global_LED_off = 0
		self.controller_LED_on = 127
		self.controller_LED_off = 0
		self.led_on = self.controller_LED_on
		self.led_off = self.controller_LED_off

	def mode_list(self):
		global modes
		self.modes = {}
		self.modes[0] = "1"

	def _inputs(self):
		self.input_map = [
			"midi_note_ch_0_val_5",
			"midi_note_ch_1_val_5",
			"midi_note_ch_2_val_5",
			"midi_note_ch_3_val_5",
			"midi_note_ch_4_val_5",
			"midi_note_ch_5_val_5",
			"midi_cc_ch_0_val_7",
			"midi_note_ch_0_val_0",
			"midi_note_ch_0_val_1",
			"midi_note_ch_0_val_2",
			"midi_note_ch_0_val_3",
			"midi_note_ch_0_val_4",
			"midi_cc_ch_1_val_7",
			"midi_note_ch_1_val_0",
			"midi_note_ch_1_val_1",
			"midi_note_ch_1_val_2",
			"midi_note_ch_1_val_3",
			"midi_note_ch_1_val_4",
			"midi_cc_ch_2_val_7",
			"midi_cc_ch_3_val_7",
			"midi_cc_ch_4_val_7",
			"midi_cc_ch_5_val_7",
			"midi_cc_ch_6_val_7",
			"midi_note_ch_2_val_0",
			"midi_note_ch_2_val_1",
			"midi_note_ch_2_val_2",
			"midi_note_ch_2_val_3",
			"midi_note_ch_2_val_4",
			"midi_note_ch_3_val_0",
			"midi_note_ch_3_val_1",
			"midi_note_ch_3_val_2",
			"midi_note_ch_3_val_3",
			"midi_note_ch_3_val_4",
			"midi_note_ch_4_val_0",
			"midi_note_ch_4_val_1",
			"midi_note_ch_4_val_2",
			"midi_note_ch_4_val_3",
			"midi_note_ch_4_val_4",
			"midi_note_ch_5_val_0",
			"midi_note_ch_5_val_1",
			"midi_note_ch_5_val_2",
			"midi_note_ch_5_val_3",
			"midi_note_ch_5_val_4",
			"midi_note_ch_6_val_0",
			"midi_note_ch_6_val_1",
			"midi_note_ch_6_val_2",
			"midi_note_ch_6_val_3",
			"midi_note_ch_6_val_4",
			"midi_cc_ch_15_val_7",
			"midi_cc_ch_0_val_56",
			"midi_cc_ch_0_val_57",
			"midi_cc_ch_0_val_16",
			"midi_cc_ch_0_val_17",
			"midi_cc_ch_0_val_18",
			"midi_cc_ch_0_val_19",
			"midi_cc_ch_0_val_20",
			"midi_cc_ch_0_val_21",
			"midi_cc_ch_0_val_22",
			"midi_cc_ch_0_val_23",
			"midi_cc_ch_0_val_81",
			"midi_cc_ch_0_val_82",
			"midi_cc_ch_0_val_83",
			"midi_cc_ch_0_val_84",
			"midi_cc_ch_0_val_85",
			"midi_cc_ch_0_val_86",
			"midi_cc_ch_0_val_87"]
		self.midi_note_ch_0_val_5 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 0, 5)
		self.midi_note_ch_0_val_5.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_0_val_5.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_1_val_5 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 1, 5)
		self.midi_note_ch_1_val_5.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_1_val_5.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_2_val_5 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 2, 5)
		self.midi_note_ch_2_val_5.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_2_val_5.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_3_val_5 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 3, 5)
		self.midi_note_ch_3_val_5.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_3_val_5.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_4_val_5 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 4, 5)
		self.midi_note_ch_4_val_5.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_4_val_5.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_5_val_5 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 5, 5)
		self.midi_note_ch_5_val_5.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_5_val_5.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_7 = EncoderElement(MIDI_CC_TYPE, 0, 7, _map_modes.absolute)
		self.midi_cc_ch_0_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_0_val_0 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 0, 0)
		self.midi_note_ch_0_val_0.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_0_val_0.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_0_val_1 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 0, 1)
		self.midi_note_ch_0_val_1.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_0_val_1.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_0_val_2 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 0, 2)
		self.midi_note_ch_0_val_2.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_0_val_2.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_0_val_3 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 0, 3)
		self.midi_note_ch_0_val_3.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_0_val_3.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_0_val_4 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 0, 4)
		self.midi_note_ch_0_val_4.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_0_val_4.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_1_val_7 = EncoderElement(MIDI_CC_TYPE, 1, 7, _map_modes.absolute)
		self.midi_cc_ch_1_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_1_val_0 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 1, 0)
		self.midi_note_ch_1_val_0.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_1_val_0.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_1_val_1 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 1, 1)
		self.midi_note_ch_1_val_1.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_1_val_1.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_1_val_2 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 1, 2)
		self.midi_note_ch_1_val_2.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_1_val_2.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_1_val_3 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 1, 3)
		self.midi_note_ch_1_val_3.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_1_val_3.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_1_val_4 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 1, 4)
		self.midi_note_ch_1_val_4.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_1_val_4.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_2_val_7 = EncoderElement(MIDI_CC_TYPE, 2, 7, _map_modes.absolute)
		self.midi_cc_ch_2_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_3_val_7 = EncoderElement(MIDI_CC_TYPE, 3, 7, _map_modes.absolute)
		self.midi_cc_ch_3_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_4_val_7 = EncoderElement(MIDI_CC_TYPE, 4, 7, _map_modes.absolute)
		self.midi_cc_ch_4_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_5_val_7 = EncoderElement(MIDI_CC_TYPE, 5, 7, _map_modes.absolute)
		self.midi_cc_ch_5_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_6_val_7 = EncoderElement(MIDI_CC_TYPE, 6, 7, _map_modes.absolute)
		self.midi_cc_ch_6_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_2_val_0 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 2, 0)
		self.midi_note_ch_2_val_0.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_2_val_0.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_2_val_1 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 2, 1)
		self.midi_note_ch_2_val_1.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_2_val_1.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_2_val_2 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 2, 2)
		self.midi_note_ch_2_val_2.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_2_val_2.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_2_val_3 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 2, 3)
		self.midi_note_ch_2_val_3.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_2_val_3.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_2_val_4 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 2, 4)
		self.midi_note_ch_2_val_4.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_2_val_4.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_3_val_0 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 3, 0)
		self.midi_note_ch_3_val_0.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_3_val_0.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_3_val_1 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 3, 1)
		self.midi_note_ch_3_val_1.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_3_val_1.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_3_val_2 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 3, 2)
		self.midi_note_ch_3_val_2.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_3_val_2.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_3_val_3 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 3, 3)
		self.midi_note_ch_3_val_3.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_3_val_3.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_3_val_4 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 3, 4)
		self.midi_note_ch_3_val_4.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_3_val_4.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_4_val_0 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 4, 0)
		self.midi_note_ch_4_val_0.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_4_val_0.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_4_val_1 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 4, 1)
		self.midi_note_ch_4_val_1.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_4_val_1.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_4_val_2 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 4, 2)
		self.midi_note_ch_4_val_2.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_4_val_2.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_4_val_3 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 4, 3)
		self.midi_note_ch_4_val_3.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_4_val_3.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_4_val_4 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 4, 4)
		self.midi_note_ch_4_val_4.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_4_val_4.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_5_val_0 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 5, 0)
		self.midi_note_ch_5_val_0.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_5_val_0.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_5_val_1 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 5, 1)
		self.midi_note_ch_5_val_1.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_5_val_1.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_5_val_2 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 5, 2)
		self.midi_note_ch_5_val_2.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_5_val_2.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_5_val_3 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 5, 3)
		self.midi_note_ch_5_val_3.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_5_val_3.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_5_val_4 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 5, 4)
		self.midi_note_ch_5_val_4.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_5_val_4.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_6_val_0 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 6, 0)
		self.midi_note_ch_6_val_0.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_6_val_0.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_6_val_1 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 6, 1)
		self.midi_note_ch_6_val_1.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_6_val_1.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_6_val_2 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 6, 2)
		self.midi_note_ch_6_val_2.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_6_val_2.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_6_val_3 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 6, 3)
		self.midi_note_ch_6_val_3.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_6_val_3.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_note_ch_6_val_4 = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, 6, 4)
		self.midi_note_ch_6_val_4.set_on_off_values(self.led_on, self.led_off)
		self.midi_note_ch_6_val_4.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_15_val_7 = EncoderElement(MIDI_CC_TYPE, 15, 7, _map_modes.absolute)
		self.midi_cc_ch_15_val_7.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_56 = EncoderElement(MIDI_CC_TYPE, 0, 56, _map_modes.absolute)
		self.midi_cc_ch_0_val_56.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_57 = EncoderElement(MIDI_CC_TYPE, 0, 57, _map_modes.absolute)
		self.midi_cc_ch_0_val_57.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_16 = EncoderElement(MIDI_CC_TYPE, 0, 16, _map_modes.absolute)
		self.midi_cc_ch_0_val_16.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_17 = EncoderElement(MIDI_CC_TYPE, 0, 17, _map_modes.absolute)
		self.midi_cc_ch_0_val_17.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_18 = EncoderElement(MIDI_CC_TYPE, 0, 18, _map_modes.absolute)
		self.midi_cc_ch_0_val_18.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_19 = EncoderElement(MIDI_CC_TYPE, 0, 19, _map_modes.absolute)
		self.midi_cc_ch_0_val_19.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_20 = EncoderElement(MIDI_CC_TYPE, 0, 20, _map_modes.absolute)
		self.midi_cc_ch_0_val_20.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_21 = EncoderElement(MIDI_CC_TYPE, 0, 21, _map_modes.absolute)
		self.midi_cc_ch_0_val_21.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_22 = EncoderElement(MIDI_CC_TYPE, 0, 22, _map_modes.absolute)
		self.midi_cc_ch_0_val_22.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_23 = EncoderElement(MIDI_CC_TYPE, 0, 23, _map_modes.absolute)
		self.midi_cc_ch_0_val_23.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_81 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 0, 81)
		self.midi_cc_ch_0_val_81.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_0_val_81.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_82 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 0, 82)
		self.midi_cc_ch_0_val_82.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_0_val_82.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_83 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 0, 83)
		self.midi_cc_ch_0_val_83.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_0_val_83.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_84 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 0, 84)
		self.midi_cc_ch_0_val_84.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_0_val_84.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_85 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 0, 85)
		self.midi_cc_ch_0_val_85.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_0_val_85.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_86 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 0, 86)
		self.midi_cc_ch_0_val_86.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_0_val_86.add_value_listener(self.placehold_listener,identify_sender= False)
		self.midi_cc_ch_0_val_87 = ConfigurableButtonElement(True, MIDI_CC_TYPE, 0, 87)
		self.midi_cc_ch_0_val_87.set_on_off_values(self.led_on, self.led_off)
		self.midi_cc_ch_0_val_87.add_value_listener(self.placehold_listener,identify_sender= False)

	def _mode1(self):
		self.show_message("Main is active")
		# Session Box
		num_tracks = 7
		num_scenes = 5
		track_offset = self.current_track_offset
		scene_offset = self.current_scene_offset
		combination_mode = "off"
		feedbackArr = {}
		feedbackArr["ClipRecording"] = None
		feedbackArr["ClipStarted"] = 127
		feedbackArr["ClipStopped"] = None
		feedbackArr["ClipTriggeredPlay"] = None
		feedbackArr["ClipTriggeredRecord"] = None
		feedbackArr["NoScene"] = None
		feedbackArr["RecordButton"] = None
		feedbackArr["Scene"] = None
		feedbackArr["SceneTriggered"] = None
		feedbackArr["StopAllOff"] = None
		feedbackArr["StopAllOn"] = None
		feedbackArr["StopClip"] = None
		feedbackArr["StopClipTriggered"] = None
		feedbackArr["StopTrackPlaying"] = None
		feedbackArr["StopTrackStopped"] = None
		clips = [self.midi_note_ch_0_val_0, self.midi_note_ch_1_val_0, self.midi_note_ch_2_val_0, self.midi_note_ch_3_val_0, self.midi_note_ch_4_val_0, self.midi_note_ch_5_val_0, self.midi_note_ch_6_val_0, self.midi_note_ch_0_val_1, self.midi_note_ch_1_val_1, self.midi_note_ch_2_val_1, self.midi_note_ch_3_val_1, self.midi_note_ch_4_val_1, self.midi_note_ch_5_val_1, self.midi_note_ch_6_val_1, self.midi_note_ch_0_val_2, self.midi_note_ch_1_val_2, self.midi_note_ch_2_val_2, self.midi_note_ch_3_val_2, self.midi_note_ch_4_val_2, self.midi_note_ch_5_val_2, self.midi_note_ch_6_val_2, self.midi_note_ch_0_val_3, self.midi_note_ch_1_val_3, self.midi_note_ch_2_val_3, self.midi_note_ch_3_val_3, self.midi_note_ch_4_val_3, self.midi_note_ch_5_val_3, self.midi_note_ch_6_val_3, self.midi_note_ch_0_val_4, self.midi_note_ch_1_val_4, self.midi_note_ch_2_val_4, self.midi_note_ch_3_val_4, self.midi_note_ch_4_val_4, self.midi_note_ch_5_val_4, self.midi_note_ch_6_val_4]
		stop_all = []
		stop_tracks = []
		scene_launch = []
		self.session_box(num_tracks, num_scenes, track_offset, scene_offset, clips, stop_all, stop_tracks, scene_launch, feedbackArr, combination_mode)
		# /Session Box end
		self.midi_cc_ch_0_val_7.add_value_listener(self.midi_cc_ch_0_val_7_mode1_listener,identify_sender= False)
		self.midi_note_ch_0_val_5.add_value_listener(self.midi_note_ch_0_val_5_mode1_listener,identify_sender= False)
		self.midi_note_ch_0_val_0.add_value_listener(self.midi_note_ch_0_val_0_mode1_listener,identify_sender= False)
		self.midi_note_ch_0_val_1.add_value_listener(self.midi_note_ch_0_val_1_mode1_listener,identify_sender= False)
		self.midi_note_ch_0_val_2.add_value_listener(self.midi_note_ch_0_val_2_mode1_listener,identify_sender= False)
		self.midi_note_ch_0_val_3.add_value_listener(self.midi_note_ch_0_val_3_mode1_listener,identify_sender= False)
		self.midi_note_ch_0_val_4.add_value_listener(self.midi_note_ch_0_val_4_mode1_listener,identify_sender= False)
		self.midi_note_ch_1_val_5.add_value_listener(self.midi_note_ch_1_val_5_mode1_listener,identify_sender= False)
		self.midi_note_ch_1_val_0.add_value_listener(self.midi_note_ch_1_val_0_mode1_listener,identify_sender= False)
		self.midi_note_ch_1_val_1.add_value_listener(self.midi_note_ch_1_val_1_mode1_listener,identify_sender= False)
		self.midi_note_ch_1_val_2.add_value_listener(self.midi_note_ch_1_val_2_mode1_listener,identify_sender= False)
		self.midi_note_ch_1_val_3.add_value_listener(self.midi_note_ch_1_val_3_mode1_listener,identify_sender= False)
		self.midi_note_ch_1_val_4.add_value_listener(self.midi_note_ch_1_val_4_mode1_listener,identify_sender= False)
		self.midi_cc_ch_1_val_7.add_value_listener(self.midi_cc_ch_1_val_7_mode1_listener,identify_sender= False)
		self.midi_note_ch_2_val_5.add_value_listener(self.midi_note_ch_2_val_5_mode1_listener,identify_sender= False)
		self.midi_note_ch_2_val_0.add_value_listener(self.midi_note_ch_2_val_0_mode1_listener,identify_sender= False)
		self.midi_note_ch_2_val_1.add_value_listener(self.midi_note_ch_2_val_1_mode1_listener,identify_sender= False)
		self.midi_note_ch_2_val_2.add_value_listener(self.midi_note_ch_2_val_2_mode1_listener,identify_sender= False)
		self.midi_note_ch_2_val_3.add_value_listener(self.midi_note_ch_2_val_3_mode1_listener,identify_sender= False)
		self.midi_note_ch_2_val_4.add_value_listener(self.midi_note_ch_2_val_4_mode1_listener,identify_sender= False)
		self.midi_cc_ch_2_val_7.add_value_listener(self.midi_cc_ch_2_val_7_mode1_listener,identify_sender= False)
		self.midi_note_ch_3_val_5.add_value_listener(self.midi_note_ch_3_val_5_mode1_listener,identify_sender= False)
		self.midi_note_ch_3_val_0.add_value_listener(self.midi_note_ch_3_val_0_mode1_listener,identify_sender= False)
		self.midi_note_ch_3_val_1.add_value_listener(self.midi_note_ch_3_val_1_mode1_listener,identify_sender= False)
		self.midi_note_ch_3_val_2.add_value_listener(self.midi_note_ch_3_val_2_mode1_listener,identify_sender= False)
		self.midi_note_ch_3_val_3.add_value_listener(self.midi_note_ch_3_val_3_mode1_listener,identify_sender= False)
		self.midi_note_ch_3_val_4.add_value_listener(self.midi_note_ch_3_val_4_mode1_listener,identify_sender= False)
		self.midi_cc_ch_3_val_7.add_value_listener(self.midi_cc_ch_3_val_7_mode1_listener,identify_sender= False)
		self.midi_note_ch_4_val_5.add_value_listener(self.midi_note_ch_4_val_5_mode1_listener,identify_sender= False)
		self.midi_note_ch_4_val_0.add_value_listener(self.midi_note_ch_4_val_0_mode1_listener,identify_sender= False)
		self.midi_note_ch_4_val_1.add_value_listener(self.midi_note_ch_4_val_1_mode1_listener,identify_sender= False)
		self.midi_note_ch_4_val_2.add_value_listener(self.midi_note_ch_4_val_2_mode1_listener,identify_sender= False)
		self.midi_note_ch_4_val_3.add_value_listener(self.midi_note_ch_4_val_3_mode1_listener,identify_sender= False)
		self.midi_note_ch_4_val_4.add_value_listener(self.midi_note_ch_4_val_4_mode1_listener,identify_sender= False)
		self.midi_cc_ch_4_val_7.add_value_listener(self.midi_cc_ch_4_val_7_mode1_listener,identify_sender= False)
		self.midi_note_ch_5_val_5.add_value_listener(self.midi_note_ch_5_val_5_mode1_listener,identify_sender= False)
		self.midi_note_ch_5_val_0.add_value_listener(self.midi_note_ch_5_val_0_mode1_listener,identify_sender= False)
		self.midi_note_ch_5_val_1.add_value_listener(self.midi_note_ch_5_val_1_mode1_listener,identify_sender= False)
		self.midi_note_ch_5_val_2.add_value_listener(self.midi_note_ch_5_val_2_mode1_listener,identify_sender= False)
		self.midi_note_ch_5_val_3.add_value_listener(self.midi_note_ch_5_val_3_mode1_listener,identify_sender= False)
		self.midi_note_ch_5_val_4.add_value_listener(self.midi_note_ch_5_val_4_mode1_listener,identify_sender= False)
		self.midi_cc_ch_5_val_7.add_value_listener(self.midi_cc_ch_5_val_7_mode1_listener,identify_sender= False)
		self.midi_note_ch_6_val_0.add_value_listener(self.midi_note_ch_6_val_0_mode1_listener,identify_sender= False)
		self.midi_note_ch_6_val_1.add_value_listener(self.midi_note_ch_6_val_1_mode1_listener,identify_sender= False)
		self.midi_note_ch_6_val_2.add_value_listener(self.midi_note_ch_6_val_2_mode1_listener,identify_sender= False)
		self.midi_note_ch_6_val_3.add_value_listener(self.midi_note_ch_6_val_3_mode1_listener,identify_sender= False)
		self.midi_note_ch_6_val_4.add_value_listener(self.midi_note_ch_6_val_4_mode1_listener,identify_sender= False)
		self.midi_cc_ch_6_val_7.add_value_listener(self.midi_cc_ch_6_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_15_val_7.add_value_listener(self.midi_cc_ch_15_val_7_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_16.add_value_listener(self.midi_cc_ch_0_val_16_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_17.add_value_listener(self.midi_cc_ch_0_val_17_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_18.add_value_listener(self.midi_cc_ch_0_val_18_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_19.add_value_listener(self.midi_cc_ch_0_val_19_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_20.add_value_listener(self.midi_cc_ch_0_val_20_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_21.add_value_listener(self.midi_cc_ch_0_val_21_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_22.add_value_listener(self.midi_cc_ch_0_val_22_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_23.add_value_listener(self.midi_cc_ch_0_val_23_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_56.add_value_listener(self.midi_cc_ch_0_val_56_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_57.add_value_listener(self.midi_cc_ch_0_val_57_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_81.add_value_listener(self.midi_cc_ch_0_val_81_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_82.add_value_listener(self.midi_cc_ch_0_val_82_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_83.add_value_listener(self.midi_cc_ch_0_val_83_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_84.add_value_listener(self.midi_cc_ch_0_val_84_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_85.add_value_listener(self.midi_cc_ch_0_val_85_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_86.add_value_listener(self.midi_cc_ch_0_val_86_mode1_listener,identify_sender= False)
		self.midi_cc_ch_0_val_87.add_value_listener(self.midi_cc_ch_0_val_87_mode1_listener,identify_sender= False)
		self._mode1_configs()
		self._mode1_led_listeners()

	def _remove_mode1(self):
		combination_mode = "off"
		self.remove_session_box(combination_mode)
		self.midi_cc_ch_0_val_7.remove_value_listener(self.midi_cc_ch_0_val_7_mode1_listener)
		self.midi_note_ch_0_val_5.remove_value_listener(self.midi_note_ch_0_val_5_mode1_listener)
		self.midi_note_ch_0_val_0.remove_value_listener(self.midi_note_ch_0_val_0_mode1_listener)
		self.midi_note_ch_0_val_1.remove_value_listener(self.midi_note_ch_0_val_1_mode1_listener)
		self.midi_note_ch_0_val_2.remove_value_listener(self.midi_note_ch_0_val_2_mode1_listener)
		self.midi_note_ch_0_val_3.remove_value_listener(self.midi_note_ch_0_val_3_mode1_listener)
		self.midi_note_ch_0_val_4.remove_value_listener(self.midi_note_ch_0_val_4_mode1_listener)
		self.midi_note_ch_1_val_5.remove_value_listener(self.midi_note_ch_1_val_5_mode1_listener)
		self.midi_note_ch_1_val_0.remove_value_listener(self.midi_note_ch_1_val_0_mode1_listener)
		self.midi_note_ch_1_val_1.remove_value_listener(self.midi_note_ch_1_val_1_mode1_listener)
		self.midi_note_ch_1_val_2.remove_value_listener(self.midi_note_ch_1_val_2_mode1_listener)
		self.midi_note_ch_1_val_3.remove_value_listener(self.midi_note_ch_1_val_3_mode1_listener)
		self.midi_note_ch_1_val_4.remove_value_listener(self.midi_note_ch_1_val_4_mode1_listener)
		self.midi_cc_ch_1_val_7.remove_value_listener(self.midi_cc_ch_1_val_7_mode1_listener)
		self.midi_note_ch_2_val_5.remove_value_listener(self.midi_note_ch_2_val_5_mode1_listener)
		self.midi_note_ch_2_val_0.remove_value_listener(self.midi_note_ch_2_val_0_mode1_listener)
		self.midi_note_ch_2_val_1.remove_value_listener(self.midi_note_ch_2_val_1_mode1_listener)
		self.midi_note_ch_2_val_2.remove_value_listener(self.midi_note_ch_2_val_2_mode1_listener)
		self.midi_note_ch_2_val_3.remove_value_listener(self.midi_note_ch_2_val_3_mode1_listener)
		self.midi_note_ch_2_val_4.remove_value_listener(self.midi_note_ch_2_val_4_mode1_listener)
		self.midi_cc_ch_2_val_7.remove_value_listener(self.midi_cc_ch_2_val_7_mode1_listener)
		self.midi_note_ch_3_val_5.remove_value_listener(self.midi_note_ch_3_val_5_mode1_listener)
		self.midi_note_ch_3_val_0.remove_value_listener(self.midi_note_ch_3_val_0_mode1_listener)
		self.midi_note_ch_3_val_1.remove_value_listener(self.midi_note_ch_3_val_1_mode1_listener)
		self.midi_note_ch_3_val_2.remove_value_listener(self.midi_note_ch_3_val_2_mode1_listener)
		self.midi_note_ch_3_val_3.remove_value_listener(self.midi_note_ch_3_val_3_mode1_listener)
		self.midi_note_ch_3_val_4.remove_value_listener(self.midi_note_ch_3_val_4_mode1_listener)
		self.midi_cc_ch_3_val_7.remove_value_listener(self.midi_cc_ch_3_val_7_mode1_listener)
		self.midi_note_ch_4_val_5.remove_value_listener(self.midi_note_ch_4_val_5_mode1_listener)
		self.midi_note_ch_4_val_0.remove_value_listener(self.midi_note_ch_4_val_0_mode1_listener)
		self.midi_note_ch_4_val_1.remove_value_listener(self.midi_note_ch_4_val_1_mode1_listener)
		self.midi_note_ch_4_val_2.remove_value_listener(self.midi_note_ch_4_val_2_mode1_listener)
		self.midi_note_ch_4_val_3.remove_value_listener(self.midi_note_ch_4_val_3_mode1_listener)
		self.midi_note_ch_4_val_4.remove_value_listener(self.midi_note_ch_4_val_4_mode1_listener)
		self.midi_cc_ch_4_val_7.remove_value_listener(self.midi_cc_ch_4_val_7_mode1_listener)
		self.midi_note_ch_5_val_5.remove_value_listener(self.midi_note_ch_5_val_5_mode1_listener)
		self.midi_note_ch_5_val_0.remove_value_listener(self.midi_note_ch_5_val_0_mode1_listener)
		self.midi_note_ch_5_val_1.remove_value_listener(self.midi_note_ch_5_val_1_mode1_listener)
		self.midi_note_ch_5_val_2.remove_value_listener(self.midi_note_ch_5_val_2_mode1_listener)
		self.midi_note_ch_5_val_3.remove_value_listener(self.midi_note_ch_5_val_3_mode1_listener)
		self.midi_note_ch_5_val_4.remove_value_listener(self.midi_note_ch_5_val_4_mode1_listener)
		self.midi_cc_ch_5_val_7.remove_value_listener(self.midi_cc_ch_5_val_7_mode1_listener)
		self.midi_note_ch_6_val_0.remove_value_listener(self.midi_note_ch_6_val_0_mode1_listener)
		self.midi_note_ch_6_val_1.remove_value_listener(self.midi_note_ch_6_val_1_mode1_listener)
		self.midi_note_ch_6_val_2.remove_value_listener(self.midi_note_ch_6_val_2_mode1_listener)
		self.midi_note_ch_6_val_3.remove_value_listener(self.midi_note_ch_6_val_3_mode1_listener)
		self.midi_note_ch_6_val_4.remove_value_listener(self.midi_note_ch_6_val_4_mode1_listener)
		self.midi_cc_ch_6_val_7.remove_value_listener(self.midi_cc_ch_6_val_7_mode1_listener)
		self.midi_cc_ch_15_val_7.remove_value_listener(self.midi_cc_ch_15_val_7_mode1_listener)
		self.midi_cc_ch_0_val_16.remove_value_listener(self.midi_cc_ch_0_val_16_mode1_listener)
		self.midi_cc_ch_0_val_17.remove_value_listener(self.midi_cc_ch_0_val_17_mode1_listener)
		self.midi_cc_ch_0_val_18.remove_value_listener(self.midi_cc_ch_0_val_18_mode1_listener)
		self.midi_cc_ch_0_val_19.remove_value_listener(self.midi_cc_ch_0_val_19_mode1_listener)
		self.midi_cc_ch_0_val_20.remove_value_listener(self.midi_cc_ch_0_val_20_mode1_listener)
		self.midi_cc_ch_0_val_21.remove_value_listener(self.midi_cc_ch_0_val_21_mode1_listener)
		self.midi_cc_ch_0_val_22.remove_value_listener(self.midi_cc_ch_0_val_22_mode1_listener)
		self.midi_cc_ch_0_val_23.remove_value_listener(self.midi_cc_ch_0_val_23_mode1_listener)
		self.midi_cc_ch_0_val_56.remove_value_listener(self.midi_cc_ch_0_val_56_mode1_listener)
		self.midi_cc_ch_0_val_57.remove_value_listener(self.midi_cc_ch_0_val_57_mode1_listener)
		self.midi_cc_ch_0_val_81.remove_value_listener(self.midi_cc_ch_0_val_81_mode1_listener)
		self.midi_cc_ch_0_val_82.remove_value_listener(self.midi_cc_ch_0_val_82_mode1_listener)
		self.midi_cc_ch_0_val_83.remove_value_listener(self.midi_cc_ch_0_val_83_mode1_listener)
		self.midi_cc_ch_0_val_84.remove_value_listener(self.midi_cc_ch_0_val_84_mode1_listener)
		self.midi_cc_ch_0_val_85.remove_value_listener(self.midi_cc_ch_0_val_85_mode1_listener)
		self.midi_cc_ch_0_val_86.remove_value_listener(self.midi_cc_ch_0_val_86_mode1_listener)
		self.midi_cc_ch_0_val_87.remove_value_listener(self.midi_cc_ch_0_val_87_mode1_listener)
		self._remove_mode1_led_listeners()

	def device_parameter_banks(self):
		self.device_id_118_banks = ["parameter_bank_1_id_119"]
		self.device_id_118_bank_names = ["Parameter Bank 1"]
		self.device_id_118_active_bank = 0
		self.device_id_118_bank_parameters_0 = [
			"parameter_1_id_120",
			"parameter_2_id_121",
			"parameter_3_id_122",
			"parameter_4_id_123",
			"parameter_5_id_124",
			"parameter_6_id_125",
			"parameter_7_id_126",
			"parameter_8_id_127"]

	def midi_cc_ch_0_val_7_mode1_listener(self, value):
		self.midi_cc_ch_0_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_7, "pre_val"):
			self.midi_cc_ch_0_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_7, "prev_press_time"):
			self.midi_cc_ch_0_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_id_7)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_7.pre_val = value
		self.midi_cc_ch_0_val_7.prev_press_time = time.time()

	def midi_note_ch_0_val_5_mode1_listener(self, value):
		self.midi_note_ch_0_val_5.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_0_val_5, "pre_val"):
			self.midi_note_ch_0_val_5.pre_val = None
		if not hasattr(self.midi_note_ch_0_val_5, "prev_press_time"):
			self.midi_note_ch_0_val_5.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.power_id_19)
		######################################
		### After running everything #####
		self.midi_note_ch_0_val_5.pre_val = value
		self.midi_note_ch_0_val_5.prev_press_time = time.time()

	def midi_note_ch_0_val_0_mode1_listener(self, value):
		self.midi_note_ch_0_val_0.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_0_val_0, "pre_val"):
			self.midi_note_ch_0_val_0.pre_val = None
		if not hasattr(self.midi_note_ch_0_val_0, "prev_press_time"):
			self.midi_note_ch_0_val_0.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_22)
		######################################
		### After running everything #####
		self.midi_note_ch_0_val_0.pre_val = value
		self.midi_note_ch_0_val_0.prev_press_time = time.time()

	def midi_note_ch_0_val_1_mode1_listener(self, value):
		self.midi_note_ch_0_val_1.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_0_val_1, "pre_val"):
			self.midi_note_ch_0_val_1.pre_val = None
		if not hasattr(self.midi_note_ch_0_val_1, "prev_press_time"):
			self.midi_note_ch_0_val_1.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_24)
		######################################
		### After running everything #####
		self.midi_note_ch_0_val_1.pre_val = value
		self.midi_note_ch_0_val_1.prev_press_time = time.time()

	def midi_note_ch_0_val_2_mode1_listener(self, value):
		self.midi_note_ch_0_val_2.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_0_val_2, "pre_val"):
			self.midi_note_ch_0_val_2.pre_val = None
		if not hasattr(self.midi_note_ch_0_val_2, "prev_press_time"):
			self.midi_note_ch_0_val_2.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_26)
		######################################
		### After running everything #####
		self.midi_note_ch_0_val_2.pre_val = value
		self.midi_note_ch_0_val_2.prev_press_time = time.time()

	def midi_note_ch_0_val_3_mode1_listener(self, value):
		self.midi_note_ch_0_val_3.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_0_val_3, "pre_val"):
			self.midi_note_ch_0_val_3.pre_val = None
		if not hasattr(self.midi_note_ch_0_val_3, "prev_press_time"):
			self.midi_note_ch_0_val_3.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_28)
		######################################
		### After running everything #####
		self.midi_note_ch_0_val_3.pre_val = value
		self.midi_note_ch_0_val_3.prev_press_time = time.time()

	def midi_note_ch_0_val_4_mode1_listener(self, value):
		self.midi_note_ch_0_val_4.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_0_val_4, "pre_val"):
			self.midi_note_ch_0_val_4.pre_val = None
		if not hasattr(self.midi_note_ch_0_val_4, "prev_press_time"):
			self.midi_note_ch_0_val_4.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_30)
		######################################
		### After running everything #####
		self.midi_note_ch_0_val_4.pre_val = value
		self.midi_note_ch_0_val_4.prev_press_time = time.time()

	def midi_note_ch_1_val_5_mode1_listener(self, value):
		self.midi_note_ch_1_val_5.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_1_val_5, "pre_val"):
			self.midi_note_ch_1_val_5.pre_val = None
		if not hasattr(self.midi_note_ch_1_val_5, "prev_press_time"):
			self.midi_note_ch_1_val_5.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.power_id_32)
		######################################
		### After running everything #####
		self.midi_note_ch_1_val_5.pre_val = value
		self.midi_note_ch_1_val_5.prev_press_time = time.time()

	def midi_note_ch_1_val_0_mode1_listener(self, value):
		self.midi_note_ch_1_val_0.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_1_val_0, "pre_val"):
			self.midi_note_ch_1_val_0.pre_val = None
		if not hasattr(self.midi_note_ch_1_val_0, "prev_press_time"):
			self.midi_note_ch_1_val_0.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_33)
		######################################
		### After running everything #####
		self.midi_note_ch_1_val_0.pre_val = value
		self.midi_note_ch_1_val_0.prev_press_time = time.time()

	def midi_note_ch_1_val_1_mode1_listener(self, value):
		self.midi_note_ch_1_val_1.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_1_val_1, "pre_val"):
			self.midi_note_ch_1_val_1.pre_val = None
		if not hasattr(self.midi_note_ch_1_val_1, "prev_press_time"):
			self.midi_note_ch_1_val_1.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_34)
		######################################
		### After running everything #####
		self.midi_note_ch_1_val_1.pre_val = value
		self.midi_note_ch_1_val_1.prev_press_time = time.time()

	def midi_note_ch_1_val_2_mode1_listener(self, value):
		self.midi_note_ch_1_val_2.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_1_val_2, "pre_val"):
			self.midi_note_ch_1_val_2.pre_val = None
		if not hasattr(self.midi_note_ch_1_val_2, "prev_press_time"):
			self.midi_note_ch_1_val_2.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_35)
		######################################
		### After running everything #####
		self.midi_note_ch_1_val_2.pre_val = value
		self.midi_note_ch_1_val_2.prev_press_time = time.time()

	def midi_note_ch_1_val_3_mode1_listener(self, value):
		self.midi_note_ch_1_val_3.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_1_val_3, "pre_val"):
			self.midi_note_ch_1_val_3.pre_val = None
		if not hasattr(self.midi_note_ch_1_val_3, "prev_press_time"):
			self.midi_note_ch_1_val_3.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_36)
		######################################
		### After running everything #####
		self.midi_note_ch_1_val_3.pre_val = value
		self.midi_note_ch_1_val_3.prev_press_time = time.time()

	def midi_note_ch_1_val_4_mode1_listener(self, value):
		self.midi_note_ch_1_val_4.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_1_val_4, "pre_val"):
			self.midi_note_ch_1_val_4.pre_val = None
		if not hasattr(self.midi_note_ch_1_val_4, "prev_press_time"):
			self.midi_note_ch_1_val_4.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_37)
		######################################
		### After running everything #####
		self.midi_note_ch_1_val_4.pre_val = value
		self.midi_note_ch_1_val_4.prev_press_time = time.time()

	def midi_cc_ch_1_val_7_mode1_listener(self, value):
		self.midi_cc_ch_1_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_1_val_7, "pre_val"):
			self.midi_cc_ch_1_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_1_val_7, "prev_press_time"):
			self.midi_cc_ch_1_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_id_38)
		######################################
		### After running everything #####
		self.midi_cc_ch_1_val_7.pre_val = value
		self.midi_cc_ch_1_val_7.prev_press_time = time.time()

	def midi_note_ch_2_val_5_mode1_listener(self, value):
		self.midi_note_ch_2_val_5.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_2_val_5, "pre_val"):
			self.midi_note_ch_2_val_5.pre_val = None
		if not hasattr(self.midi_note_ch_2_val_5, "prev_press_time"):
			self.midi_note_ch_2_val_5.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.power_id_46)
		######################################
		### After running everything #####
		self.midi_note_ch_2_val_5.pre_val = value
		self.midi_note_ch_2_val_5.prev_press_time = time.time()

	def midi_note_ch_2_val_0_mode1_listener(self, value):
		self.midi_note_ch_2_val_0.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_2_val_0, "pre_val"):
			self.midi_note_ch_2_val_0.pre_val = None
		if not hasattr(self.midi_note_ch_2_val_0, "prev_press_time"):
			self.midi_note_ch_2_val_0.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_47)
		######################################
		### After running everything #####
		self.midi_note_ch_2_val_0.pre_val = value
		self.midi_note_ch_2_val_0.prev_press_time = time.time()

	def midi_note_ch_2_val_1_mode1_listener(self, value):
		self.midi_note_ch_2_val_1.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_2_val_1, "pre_val"):
			self.midi_note_ch_2_val_1.pre_val = None
		if not hasattr(self.midi_note_ch_2_val_1, "prev_press_time"):
			self.midi_note_ch_2_val_1.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_48)
		######################################
		### After running everything #####
		self.midi_note_ch_2_val_1.pre_val = value
		self.midi_note_ch_2_val_1.prev_press_time = time.time()

	def midi_note_ch_2_val_2_mode1_listener(self, value):
		self.midi_note_ch_2_val_2.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_2_val_2, "pre_val"):
			self.midi_note_ch_2_val_2.pre_val = None
		if not hasattr(self.midi_note_ch_2_val_2, "prev_press_time"):
			self.midi_note_ch_2_val_2.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_49)
		######################################
		### After running everything #####
		self.midi_note_ch_2_val_2.pre_val = value
		self.midi_note_ch_2_val_2.prev_press_time = time.time()

	def midi_note_ch_2_val_3_mode1_listener(self, value):
		self.midi_note_ch_2_val_3.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_2_val_3, "pre_val"):
			self.midi_note_ch_2_val_3.pre_val = None
		if not hasattr(self.midi_note_ch_2_val_3, "prev_press_time"):
			self.midi_note_ch_2_val_3.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_50)
		######################################
		### After running everything #####
		self.midi_note_ch_2_val_3.pre_val = value
		self.midi_note_ch_2_val_3.prev_press_time = time.time()

	def midi_note_ch_2_val_4_mode1_listener(self, value):
		self.midi_note_ch_2_val_4.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_2_val_4, "pre_val"):
			self.midi_note_ch_2_val_4.pre_val = None
		if not hasattr(self.midi_note_ch_2_val_4, "prev_press_time"):
			self.midi_note_ch_2_val_4.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_51)
		######################################
		### After running everything #####
		self.midi_note_ch_2_val_4.pre_val = value
		self.midi_note_ch_2_val_4.prev_press_time = time.time()

	def midi_cc_ch_2_val_7_mode1_listener(self, value):
		self.midi_cc_ch_2_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_2_val_7, "pre_val"):
			self.midi_cc_ch_2_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_2_val_7, "prev_press_time"):
			self.midi_cc_ch_2_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_id_52)
		######################################
		### After running everything #####
		self.midi_cc_ch_2_val_7.pre_val = value
		self.midi_cc_ch_2_val_7.prev_press_time = time.time()

	def midi_note_ch_3_val_5_mode1_listener(self, value):
		self.midi_note_ch_3_val_5.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_3_val_5, "pre_val"):
			self.midi_note_ch_3_val_5.pre_val = None
		if not hasattr(self.midi_note_ch_3_val_5, "prev_press_time"):
			self.midi_note_ch_3_val_5.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.power_id_60)
		######################################
		### After running everything #####
		self.midi_note_ch_3_val_5.pre_val = value
		self.midi_note_ch_3_val_5.prev_press_time = time.time()

	def midi_note_ch_3_val_0_mode1_listener(self, value):
		self.midi_note_ch_3_val_0.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_3_val_0, "pre_val"):
			self.midi_note_ch_3_val_0.pre_val = None
		if not hasattr(self.midi_note_ch_3_val_0, "prev_press_time"):
			self.midi_note_ch_3_val_0.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_61)
		######################################
		### After running everything #####
		self.midi_note_ch_3_val_0.pre_val = value
		self.midi_note_ch_3_val_0.prev_press_time = time.time()

	def midi_note_ch_3_val_1_mode1_listener(self, value):
		self.midi_note_ch_3_val_1.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_3_val_1, "pre_val"):
			self.midi_note_ch_3_val_1.pre_val = None
		if not hasattr(self.midi_note_ch_3_val_1, "prev_press_time"):
			self.midi_note_ch_3_val_1.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_62)
		######################################
		### After running everything #####
		self.midi_note_ch_3_val_1.pre_val = value
		self.midi_note_ch_3_val_1.prev_press_time = time.time()

	def midi_note_ch_3_val_2_mode1_listener(self, value):
		self.midi_note_ch_3_val_2.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_3_val_2, "pre_val"):
			self.midi_note_ch_3_val_2.pre_val = None
		if not hasattr(self.midi_note_ch_3_val_2, "prev_press_time"):
			self.midi_note_ch_3_val_2.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_63)
		######################################
		### After running everything #####
		self.midi_note_ch_3_val_2.pre_val = value
		self.midi_note_ch_3_val_2.prev_press_time = time.time()

	def midi_note_ch_3_val_3_mode1_listener(self, value):
		self.midi_note_ch_3_val_3.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_3_val_3, "pre_val"):
			self.midi_note_ch_3_val_3.pre_val = None
		if not hasattr(self.midi_note_ch_3_val_3, "prev_press_time"):
			self.midi_note_ch_3_val_3.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_64)
		######################################
		### After running everything #####
		self.midi_note_ch_3_val_3.pre_val = value
		self.midi_note_ch_3_val_3.prev_press_time = time.time()

	def midi_note_ch_3_val_4_mode1_listener(self, value):
		self.midi_note_ch_3_val_4.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_3_val_4, "pre_val"):
			self.midi_note_ch_3_val_4.pre_val = None
		if not hasattr(self.midi_note_ch_3_val_4, "prev_press_time"):
			self.midi_note_ch_3_val_4.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_65)
		######################################
		### After running everything #####
		self.midi_note_ch_3_val_4.pre_val = value
		self.midi_note_ch_3_val_4.prev_press_time = time.time()

	def midi_cc_ch_3_val_7_mode1_listener(self, value):
		self.midi_cc_ch_3_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_3_val_7, "pre_val"):
			self.midi_cc_ch_3_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_3_val_7, "prev_press_time"):
			self.midi_cc_ch_3_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_id_66)
		######################################
		### After running everything #####
		self.midi_cc_ch_3_val_7.pre_val = value
		self.midi_cc_ch_3_val_7.prev_press_time = time.time()

	def midi_note_ch_4_val_5_mode1_listener(self, value):
		self.midi_note_ch_4_val_5.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_4_val_5, "pre_val"):
			self.midi_note_ch_4_val_5.pre_val = None
		if not hasattr(self.midi_note_ch_4_val_5, "prev_press_time"):
			self.midi_note_ch_4_val_5.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.power_id_74)
		######################################
		### After running everything #####
		self.midi_note_ch_4_val_5.pre_val = value
		self.midi_note_ch_4_val_5.prev_press_time = time.time()

	def midi_note_ch_4_val_0_mode1_listener(self, value):
		self.midi_note_ch_4_val_0.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_4_val_0, "pre_val"):
			self.midi_note_ch_4_val_0.pre_val = None
		if not hasattr(self.midi_note_ch_4_val_0, "prev_press_time"):
			self.midi_note_ch_4_val_0.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_75)
		######################################
		### After running everything #####
		self.midi_note_ch_4_val_0.pre_val = value
		self.midi_note_ch_4_val_0.prev_press_time = time.time()

	def midi_note_ch_4_val_1_mode1_listener(self, value):
		self.midi_note_ch_4_val_1.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_4_val_1, "pre_val"):
			self.midi_note_ch_4_val_1.pre_val = None
		if not hasattr(self.midi_note_ch_4_val_1, "prev_press_time"):
			self.midi_note_ch_4_val_1.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_76)
		######################################
		### After running everything #####
		self.midi_note_ch_4_val_1.pre_val = value
		self.midi_note_ch_4_val_1.prev_press_time = time.time()

	def midi_note_ch_4_val_2_mode1_listener(self, value):
		self.midi_note_ch_4_val_2.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_4_val_2, "pre_val"):
			self.midi_note_ch_4_val_2.pre_val = None
		if not hasattr(self.midi_note_ch_4_val_2, "prev_press_time"):
			self.midi_note_ch_4_val_2.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_77)
		######################################
		### After running everything #####
		self.midi_note_ch_4_val_2.pre_val = value
		self.midi_note_ch_4_val_2.prev_press_time = time.time()

	def midi_note_ch_4_val_3_mode1_listener(self, value):
		self.midi_note_ch_4_val_3.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_4_val_3, "pre_val"):
			self.midi_note_ch_4_val_3.pre_val = None
		if not hasattr(self.midi_note_ch_4_val_3, "prev_press_time"):
			self.midi_note_ch_4_val_3.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_78)
		######################################
		### After running everything #####
		self.midi_note_ch_4_val_3.pre_val = value
		self.midi_note_ch_4_val_3.prev_press_time = time.time()

	def midi_note_ch_4_val_4_mode1_listener(self, value):
		self.midi_note_ch_4_val_4.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_4_val_4, "pre_val"):
			self.midi_note_ch_4_val_4.pre_val = None
		if not hasattr(self.midi_note_ch_4_val_4, "prev_press_time"):
			self.midi_note_ch_4_val_4.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_79)
		######################################
		### After running everything #####
		self.midi_note_ch_4_val_4.pre_val = value
		self.midi_note_ch_4_val_4.prev_press_time = time.time()

	def midi_cc_ch_4_val_7_mode1_listener(self, value):
		self.midi_cc_ch_4_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_4_val_7, "pre_val"):
			self.midi_cc_ch_4_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_4_val_7, "prev_press_time"):
			self.midi_cc_ch_4_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_id_80)
		######################################
		### After running everything #####
		self.midi_cc_ch_4_val_7.pre_val = value
		self.midi_cc_ch_4_val_7.prev_press_time = time.time()

	def midi_note_ch_5_val_5_mode1_listener(self, value):
		self.midi_note_ch_5_val_5.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_5_val_5, "pre_val"):
			self.midi_note_ch_5_val_5.pre_val = None
		if not hasattr(self.midi_note_ch_5_val_5, "prev_press_time"):
			self.midi_note_ch_5_val_5.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.power_id_88)
		######################################
		### After running everything #####
		self.midi_note_ch_5_val_5.pre_val = value
		self.midi_note_ch_5_val_5.prev_press_time = time.time()

	def midi_note_ch_5_val_0_mode1_listener(self, value):
		self.midi_note_ch_5_val_0.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_5_val_0, "pre_val"):
			self.midi_note_ch_5_val_0.pre_val = None
		if not hasattr(self.midi_note_ch_5_val_0, "prev_press_time"):
			self.midi_note_ch_5_val_0.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_89)
		######################################
		### After running everything #####
		self.midi_note_ch_5_val_0.pre_val = value
		self.midi_note_ch_5_val_0.prev_press_time = time.time()

	def midi_note_ch_5_val_1_mode1_listener(self, value):
		self.midi_note_ch_5_val_1.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_5_val_1, "pre_val"):
			self.midi_note_ch_5_val_1.pre_val = None
		if not hasattr(self.midi_note_ch_5_val_1, "prev_press_time"):
			self.midi_note_ch_5_val_1.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_90)
		######################################
		### After running everything #####
		self.midi_note_ch_5_val_1.pre_val = value
		self.midi_note_ch_5_val_1.prev_press_time = time.time()

	def midi_note_ch_5_val_2_mode1_listener(self, value):
		self.midi_note_ch_5_val_2.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_5_val_2, "pre_val"):
			self.midi_note_ch_5_val_2.pre_val = None
		if not hasattr(self.midi_note_ch_5_val_2, "prev_press_time"):
			self.midi_note_ch_5_val_2.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_91)
		######################################
		### After running everything #####
		self.midi_note_ch_5_val_2.pre_val = value
		self.midi_note_ch_5_val_2.prev_press_time = time.time()

	def midi_note_ch_5_val_3_mode1_listener(self, value):
		self.midi_note_ch_5_val_3.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_5_val_3, "pre_val"):
			self.midi_note_ch_5_val_3.pre_val = None
		if not hasattr(self.midi_note_ch_5_val_3, "prev_press_time"):
			self.midi_note_ch_5_val_3.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_92)
		######################################
		### After running everything #####
		self.midi_note_ch_5_val_3.pre_val = value
		self.midi_note_ch_5_val_3.prev_press_time = time.time()

	def midi_note_ch_5_val_4_mode1_listener(self, value):
		self.midi_note_ch_5_val_4.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_5_val_4, "pre_val"):
			self.midi_note_ch_5_val_4.pre_val = None
		if not hasattr(self.midi_note_ch_5_val_4, "prev_press_time"):
			self.midi_note_ch_5_val_4.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_93)
		######################################
		### After running everything #####
		self.midi_note_ch_5_val_4.pre_val = value
		self.midi_note_ch_5_val_4.prev_press_time = time.time()

	def midi_cc_ch_5_val_7_mode1_listener(self, value):
		self.midi_cc_ch_5_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_5_val_7, "pre_val"):
			self.midi_cc_ch_5_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_5_val_7, "prev_press_time"):
			self.midi_cc_ch_5_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_id_94)
		######################################
		### After running everything #####
		self.midi_cc_ch_5_val_7.pre_val = value
		self.midi_cc_ch_5_val_7.prev_press_time = time.time()

	def midi_note_ch_6_val_0_mode1_listener(self, value):
		self.midi_note_ch_6_val_0.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_6_val_0, "pre_val"):
			self.midi_note_ch_6_val_0.pre_val = None
		if not hasattr(self.midi_note_ch_6_val_0, "prev_press_time"):
			self.midi_note_ch_6_val_0.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_103)
		######################################
		### After running everything #####
		self.midi_note_ch_6_val_0.pre_val = value
		self.midi_note_ch_6_val_0.prev_press_time = time.time()

	def midi_note_ch_6_val_1_mode1_listener(self, value):
		self.midi_note_ch_6_val_1.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_6_val_1, "pre_val"):
			self.midi_note_ch_6_val_1.pre_val = None
		if not hasattr(self.midi_note_ch_6_val_1, "prev_press_time"):
			self.midi_note_ch_6_val_1.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_104)
		######################################
		### After running everything #####
		self.midi_note_ch_6_val_1.pre_val = value
		self.midi_note_ch_6_val_1.prev_press_time = time.time()

	def midi_note_ch_6_val_2_mode1_listener(self, value):
		self.midi_note_ch_6_val_2.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_6_val_2, "pre_val"):
			self.midi_note_ch_6_val_2.pre_val = None
		if not hasattr(self.midi_note_ch_6_val_2, "prev_press_time"):
			self.midi_note_ch_6_val_2.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_105)
		######################################
		### After running everything #####
		self.midi_note_ch_6_val_2.pre_val = value
		self.midi_note_ch_6_val_2.prev_press_time = time.time()

	def midi_note_ch_6_val_3_mode1_listener(self, value):
		self.midi_note_ch_6_val_3.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_6_val_3, "pre_val"):
			self.midi_note_ch_6_val_3.pre_val = None
		if not hasattr(self.midi_note_ch_6_val_3, "prev_press_time"):
			self.midi_note_ch_6_val_3.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_106)
		######################################
		### After running everything #####
		self.midi_note_ch_6_val_3.pre_val = value
		self.midi_note_ch_6_val_3.prev_press_time = time.time()

	def midi_note_ch_6_val_4_mode1_listener(self, value):
		self.midi_note_ch_6_val_4.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_note_ch_6_val_4, "pre_val"):
			self.midi_note_ch_6_val_4.pre_val = None
		if not hasattr(self.midi_note_ch_6_val_4, "prev_press_time"):
			self.midi_note_ch_6_val_4.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.select_device_id_107)
		######################################
		### After running everything #####
		self.midi_note_ch_6_val_4.pre_val = value
		self.midi_note_ch_6_val_4.prev_press_time = time.time()

	def midi_cc_ch_6_val_7_mode1_listener(self, value):
		self.midi_cc_ch_6_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_6_val_7, "pre_val"):
			self.midi_cc_ch_6_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_6_val_7, "prev_press_time"):
			self.midi_cc_ch_6_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_id_108)
		######################################
		### After running everything #####
		self.midi_cc_ch_6_val_7.pre_val = value
		self.midi_cc_ch_6_val_7.prev_press_time = time.time()

	def midi_cc_ch_15_val_7_mode1_listener(self, value):
		self.midi_cc_ch_15_val_7.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_15_val_7, "pre_val"):
			self.midi_cc_ch_15_val_7.pre_val = None
		if not hasattr(self.midi_cc_ch_15_val_7, "prev_press_time"):
			self.midi_cc_ch_15_val_7.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.volume_8_id_116)
		######################################
		### After running everything #####
		self.midi_cc_ch_15_val_7.pre_val = value
		self.midi_cc_ch_15_val_7.prev_press_time = time.time()

	def midi_cc_ch_0_val_16_mode1_listener(self, value):
		self.midi_cc_ch_0_val_16.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_16, "pre_val"):
			self.midi_cc_ch_0_val_16.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_16, "prev_press_time"):
			self.midi_cc_ch_0_val_16.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_118_active_bank == 0):
			self.pick_brain(self.parameter_1_id_120)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_16.pre_val = value
		self.midi_cc_ch_0_val_16.prev_press_time = time.time()

	def midi_cc_ch_0_val_17_mode1_listener(self, value):
		self.midi_cc_ch_0_val_17.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_17, "pre_val"):
			self.midi_cc_ch_0_val_17.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_17, "prev_press_time"):
			self.midi_cc_ch_0_val_17.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_118_active_bank == 0):
			self.pick_brain(self.parameter_2_id_121)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_17.pre_val = value
		self.midi_cc_ch_0_val_17.prev_press_time = time.time()

	def midi_cc_ch_0_val_18_mode1_listener(self, value):
		self.midi_cc_ch_0_val_18.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_18, "pre_val"):
			self.midi_cc_ch_0_val_18.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_18, "prev_press_time"):
			self.midi_cc_ch_0_val_18.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_118_active_bank == 0):
			self.pick_brain(self.parameter_3_id_122)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_18.pre_val = value
		self.midi_cc_ch_0_val_18.prev_press_time = time.time()

	def midi_cc_ch_0_val_19_mode1_listener(self, value):
		self.midi_cc_ch_0_val_19.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_19, "pre_val"):
			self.midi_cc_ch_0_val_19.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_19, "prev_press_time"):
			self.midi_cc_ch_0_val_19.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_118_active_bank == 0):
			self.pick_brain(self.parameter_4_id_123)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_19.pre_val = value
		self.midi_cc_ch_0_val_19.prev_press_time = time.time()

	def midi_cc_ch_0_val_20_mode1_listener(self, value):
		self.midi_cc_ch_0_val_20.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_20, "pre_val"):
			self.midi_cc_ch_0_val_20.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_20, "prev_press_time"):
			self.midi_cc_ch_0_val_20.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_118_active_bank == 0):
			self.pick_brain(self.parameter_5_id_124)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_20.pre_val = value
		self.midi_cc_ch_0_val_20.prev_press_time = time.time()

	def midi_cc_ch_0_val_21_mode1_listener(self, value):
		self.midi_cc_ch_0_val_21.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_21, "pre_val"):
			self.midi_cc_ch_0_val_21.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_21, "prev_press_time"):
			self.midi_cc_ch_0_val_21.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_118_active_bank == 0):
			self.pick_brain(self.parameter_6_id_125)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_21.pre_val = value
		self.midi_cc_ch_0_val_21.prev_press_time = time.time()

	def midi_cc_ch_0_val_22_mode1_listener(self, value):
		self.midi_cc_ch_0_val_22.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_22, "pre_val"):
			self.midi_cc_ch_0_val_22.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_22, "prev_press_time"):
			self.midi_cc_ch_0_val_22.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_118_active_bank == 0):
			self.pick_brain(self.parameter_7_id_126)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_22.pre_val = value
		self.midi_cc_ch_0_val_22.prev_press_time = time.time()

	def midi_cc_ch_0_val_23_mode1_listener(self, value):
		self.midi_cc_ch_0_val_23.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_23, "pre_val"):
			self.midi_cc_ch_0_val_23.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_23, "prev_press_time"):
			self.midi_cc_ch_0_val_23.prev_press_time = time.time()
		######################################
		# send configs off to run
		if (self.device_id_118_active_bank == 0):
			self.pick_brain(self.parameter_8_id_127)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_23.pre_val = value
		self.midi_cc_ch_0_val_23.prev_press_time = time.time()

	def midi_cc_ch_0_val_56_mode1_listener(self, value):
		self.midi_cc_ch_0_val_56.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_56, "pre_val"):
			self.midi_cc_ch_0_val_56.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_56, "prev_press_time"):
			self.midi_cc_ch_0_val_56.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.reverb_id_129)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_56.pre_val = value
		self.midi_cc_ch_0_val_56.prev_press_time = time.time()

	def midi_cc_ch_0_val_57_mode1_listener(self, value):
		self.midi_cc_ch_0_val_57.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_57, "pre_val"):
			self.midi_cc_ch_0_val_57.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_57, "prev_press_time"):
			self.midi_cc_ch_0_val_57.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.delay_id_130)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_57.pre_val = value
		self.midi_cc_ch_0_val_57.prev_press_time = time.time()

	def midi_cc_ch_0_val_81_mode1_listener(self, value):
		self.midi_cc_ch_0_val_81.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_81, "pre_val"):
			self.midi_cc_ch_0_val_81.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_81, "prev_press_time"):
			self.midi_cc_ch_0_val_81.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.tap_tempo_id_131)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_81.pre_val = value
		self.midi_cc_ch_0_val_81.prev_press_time = time.time()

	def midi_cc_ch_0_val_82_mode1_listener(self, value):
		self.midi_cc_ch_0_val_82.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_82, "pre_val"):
			self.midi_cc_ch_0_val_82.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_82, "prev_press_time"):
			self.midi_cc_ch_0_val_82.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.tempo_decrement_id_132)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_82.pre_val = value
		self.midi_cc_ch_0_val_82.prev_press_time = time.time()

	def midi_cc_ch_0_val_83_mode1_listener(self, value):
		self.midi_cc_ch_0_val_83.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_83, "pre_val"):
			self.midi_cc_ch_0_val_83.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_83, "prev_press_time"):
			self.midi_cc_ch_0_val_83.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.tempo_increment_id_133)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_83.pre_val = value
		self.midi_cc_ch_0_val_83.prev_press_time = time.time()

	def midi_cc_ch_0_val_84_mode1_listener(self, value):
		self.midi_cc_ch_0_val_84.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_84, "pre_val"):
			self.midi_cc_ch_0_val_84.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_84, "prev_press_time"):
			self.midi_cc_ch_0_val_84.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.scene_select_decrement_id_134)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_84.pre_val = value
		self.midi_cc_ch_0_val_84.prev_press_time = time.time()

	def midi_cc_ch_0_val_85_mode1_listener(self, value):
		self.midi_cc_ch_0_val_85.cur_val = value # make current velocity value accessible on object
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_85, "pre_val"):
			self.midi_cc_ch_0_val_85.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_85, "prev_press_time"):
			self.midi_cc_ch_0_val_85.prev_press_time = time.time()
		######################################
		# send configs off to run
		self.pick_brain(self.scene_select_increment_id_135)
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_85.pre_val = value
		self.midi_cc_ch_0_val_85.prev_press_time = time.time()

	def midi_cc_ch_0_val_86_mode1_listener(self, value):
		self.midi_cc_ch_0_val_86.cur_val = value # make current velocity value accessible on object
		### Reaction Code start
		self.show_message = "BD: Stop Button Pressed"
		self.song().tracks[11].clip_slots[0].stop()
		
		### Reaction Code end
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_86, "pre_val"):
			self.midi_cc_ch_0_val_86.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_86, "prev_press_time"):
			self.midi_cc_ch_0_val_86.prev_press_time = time.time()
		######################################
		# send configs off to run
		# Reaction has no brain
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_86.pre_val = value
		self.midi_cc_ch_0_val_86.prev_press_time = time.time()

	def midi_cc_ch_0_val_87_mode1_listener(self, value):
		self.midi_cc_ch_0_val_87.cur_val = value # make current velocity value accessible on object
		### Reaction Code start
		self.show_message = "BD: Start Button Pressed"
		self.song().view.selected_scene.fire()
		
		### Reaction Code end
		######################################
		### Before running anything else #####
		if not hasattr(self.midi_cc_ch_0_val_87, "pre_val"):
			self.midi_cc_ch_0_val_87.pre_val = None
		if not hasattr(self.midi_cc_ch_0_val_87, "prev_press_time"):
			self.midi_cc_ch_0_val_87.prev_press_time = time.time()
		######################################
		# send configs off to run
		# Reaction has no brain
		######################################
		### After running everything #####
		self.midi_cc_ch_0_val_87.pre_val = value
		self.midi_cc_ch_0_val_87.prev_press_time = time.time()

	def _mode1_configs(self):
		self.mode_1_configs_map = [
			"volume_id_7",
			"apiano_id_17",
			"track_on_id_18",
			"power_id_19",
			"device_select___chain_1_id_21",
			"select_device_id_22",
			"device_select___chain_2_id_23",
			"select_device_id_24",
			"device_select___chain_3_id_25",
			"select_device_id_26",
			"device_select___chain_4_id_27",
			"select_device_id_28",
			"device_select___chain_5_id_29",
			"select_device_id_30",
			"epiano_id_31",
			"power_id_32",
			"select_device_id_33",
			"select_device_id_34",
			"select_device_id_35",
			"select_device_id_36",
			"select_device_id_37",
			"volume_id_38",
			"track_on_id_39",
			"device_select___chain_1_id_40",
			"device_select___chain_2_id_41",
			"device_select___chain_3_id_42",
			"device_select___chain_4_id_43",
			"device_select___chain_5_id_44",
			"synth_id_45",
			"power_id_46",
			"select_device_id_47",
			"select_device_id_48",
			"select_device_id_49",
			"select_device_id_50",
			"select_device_id_51",
			"volume_id_52",
			"track_on_id_53",
			"device_select___chain_1_id_54",
			"device_select___chain_2_id_55",
			"device_select___chain_3_id_56",
			"device_select___chain_4_id_57",
			"device_select___chain_5_id_58",
			"strings_id_59",
			"power_id_60",
			"select_device_id_61",
			"select_device_id_62",
			"select_device_id_63",
			"select_device_id_64",
			"select_device_id_65",
			"volume_id_66",
			"track_on_id_67",
			"device_select___chain_1_id_68",
			"device_select___chain_2_id_69",
			"device_select___chain_3_id_70",
			"device_select___chain_4_id_71",
			"device_select___chain_5_id_72",
			"organlead_id_73",
			"power_id_74",
			"select_device_id_75",
			"select_device_id_76",
			"select_device_id_77",
			"select_device_id_78",
			"select_device_id_79",
			"volume_id_80",
			"track_on_id_81",
			"device_select___chain_1_id_82",
			"device_select___chain_2_id_83",
			"device_select___chain_3_id_84",
			"device_select___chain_4_id_85",
			"device_select___chain_5_id_86",
			"alternates_id_87",
			"power_id_88",
			"select_device_id_89",
			"select_device_id_90",
			"select_device_id_91",
			"select_device_id_92",
			"select_device_id_93",
			"volume_id_94",
			"track_on_id_95",
			"device_select___chain_1_id_96",
			"device_select___chain_2_id_97",
			"device_select___chain_3_id_98",
			"device_select___chain_4_id_99",
			"device_select___chain_5_id_100",
			"split_id_101",
			"select_device_id_103",
			"select_device_id_104",
			"select_device_id_105",
			"select_device_id_106",
			"select_device_id_107",
			"volume_id_108",
			"device_select___chain_1_id_110",
			"device_select___chain_2_id_111",
			"device_select___chain_3_id_112",
			"device_select___chain_4_id_113",
			"device_select___chain_5_id_114",
			"master_track_id_115",
			"volume_8_id_116",
			"selected_track_id_117",
			"selected_device_id_118",
			"parameter_bank_1_id_119",
			"parameter_1_id_120",
			"parameter_2_id_121",
			"parameter_3_id_122",
			"parameter_4_id_123",
			"parameter_5_id_124",
			"parameter_6_id_125",
			"parameter_7_id_126",
			"parameter_8_id_127",
			"reverb_id_129",
			"delay_id_130",
			"tap_tempo_id_131",
			"tempo_decrement_id_132",
			"tempo_increment_id_133",
			"scene_select_decrement_id_134",
			"scene_select_increment_id_135"]
		self.volume_id_7 = {}
		self.volume_id_7["attached_to"] = "midi_cc_ch_0_val_7"
		self.volume_id_7["track"] = self.track_num(2)
		self.volume_id_7["module"] = "self.song().tracks[self.track_num(0)].mixer_device.volume"
		self.volume_id_7["element"] = "value"
		self.volume_id_7["output_type"] = "val"
		self.volume_id_7["minimum"] = round(0,2)
		self.volume_id_7["maximum"] = round(85,2)
		self.volume_id_7["decimal_places"] = 2
		self.volume_id_7["ui_listener"] = "value"
		self.volume_id_7["feedback_brain"] = "feedback_range"
		self.volume_id_7["ctrl_type"] = "absolute"
		self.volume_id_7["takeover_mode"] = "None"
		self.volume_id_7["enc_first"] = 0
		self.volume_id_7["enc_second"] = 127
		self.volume_id_7["reverse_mode"] = False
		self.volume_id_7["LED_mapping_type_needs_feedback"] = "1"
		self.volume_id_7["LED_feedback"] = "default"
		self.volume_id_7["LED_feedback_active"] = "1"
		self.volume_id_7["LED_on"] = "127"
		self.volume_id_7["LED_off"] = "0"
		self.volume_id_7["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_7"]
		self.volume_id_7["snap_to"] = True
		self.volume_id_7["json_id"] = 7
		self.volume_id_7["mapping_name"] = "Volume"
		self.volume_id_7["mapping_type"] = "Volume"
		self.volume_id_7["parent_json_id"] = 17
		self.volume_id_7["parent_name"] = "apiano_id_17"
		self.apiano_id_17 = {}
		self.apiano_id_17["track"] = self.track_num(2)
		self.apiano_id_17["module"] = "self.song().tracks[self.track_num(0)]"
		self.apiano_id_17["LED_mapping_type_needs_feedback"] = ""
		self.apiano_id_17["LED_feedback"] = "custom"
		self.apiano_id_17["LED_feedback_active"] = ""
		self.apiano_id_17["LED_on"] = "127"
		self.apiano_id_17["LED_off"] = "0"
		self.apiano_id_17["LED_send_feedback_to_selected"] = []
		self.apiano_id_17["json_id"] = 17
		self.apiano_id_17["mapping_name"] = "APiano"
		self.apiano_id_17["mapping_type"] = "Track"
		self.apiano_id_17["parent_json_id"] = 1
		self.apiano_id_17["parent_name"] = "main_id_1"
		self.track_on_id_18 = {}
		self.track_on_id_18["track"] = self.track_num(2)
		self.track_on_id_18["module"] = "self.song().tracks[self.track_num(0)].devices[0]"
		self.track_on_id_18["LED_mapping_type_needs_feedback"] = ""
		self.track_on_id_18["LED_feedback"] = "custom"
		self.track_on_id_18["LED_feedback_active"] = ""
		self.track_on_id_18["LED_on"] = "127"
		self.track_on_id_18["LED_off"] = "0"
		self.track_on_id_18["LED_send_feedback_to_selected"] = []
		self.track_on_id_18["json_id"] = 18
		self.track_on_id_18["mapping_name"] = "Track On"
		self.track_on_id_18["mapping_type"] = "Device"
		self.track_on_id_18["parent_json_id"] = 17
		self.track_on_id_18["parent_name"] = "apiano_id_17"
		self.power_id_19 = {}
		self.power_id_19["attached_to"] = "midi_note_ch_0_val_5"
		self.power_id_19["track"] = self.track_num(2)
		self.power_id_19["module"] = "self.song().tracks[self.track_num(0)].devices[0].parameters[0]"
		self.power_id_19["minimum"] = 0.0
		self.power_id_19["maximum"] = 1.0
		self.power_id_19["snap_to"] = 1
		self.power_id_19["element"] = "value"
		self.power_id_19["output_type"] = "val"
		self.power_id_19["ui_listener"] = "value"
		self.power_id_19["feedback_brain"] = "feedback_on_off"
		self.power_id_19["enc_first"] = 127
		self.power_id_19["enc_second"] = 0
		self.power_id_19["switch_type"] = "toggle"
		self.power_id_19["ctrl_type"] = "on/off"
		self.power_id_19["LED_mapping_type_needs_feedback"] = "1"
		self.power_id_19["LED_feedback"] = "default"
		self.power_id_19["LED_feedback_active"] = "1"
		self.power_id_19["LED_on"] = "127"
		self.power_id_19["LED_off"] = "0"
		self.power_id_19["LED_send_feedback_to_selected"] = ["midi_note_ch_0_val_5"]
		self.power_id_19["json_id"] = 19
		self.power_id_19["mapping_name"] = "Power"
		self.power_id_19["mapping_type"] = "On/Off"
		self.power_id_19["parent_json_id"] = 18
		self.power_id_19["parent_name"] = "track_on_id_18"
		self.device_select___chain_1_id_21 = {}
		self.device_select___chain_1_id_21["track"] = self.track_num(2)
		self.device_select___chain_1_id_21["module"] = "self.song().tracks[self.track_num(0)].devices[1].chains[0].devices[0]"
		self.device_select___chain_1_id_21["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_1_id_21["LED_feedback"] = "custom"
		self.device_select___chain_1_id_21["LED_feedback_active"] = ""
		self.device_select___chain_1_id_21["LED_on"] = "127"
		self.device_select___chain_1_id_21["LED_off"] = "0"
		self.device_select___chain_1_id_21["LED_send_feedback_to_selected"] = []
		self.device_select___chain_1_id_21["json_id"] = 21
		self.device_select___chain_1_id_21["mapping_name"] = "Device Select  - Chain 1"
		self.device_select___chain_1_id_21["mapping_type"] = "Device"
		self.device_select___chain_1_id_21["parent_json_id"] = 17
		self.device_select___chain_1_id_21["parent_name"] = "apiano_id_17"
		self.select_device_id_22 = {}
		self.select_device_id_22["attached_to"] = "midi_note_ch_0_val_0"
		self.select_device_id_22["module"] = "self"
		self.select_device_id_22["element"] = "select_a_device"
		self.select_device_id_22["output_type"] = "func"
		self.select_device_id_22["func_arg"] = "cnfg"
		self.select_device_id_22["parent_track"] = "self.song().tracks[self.track_num(0)]"
		self.select_device_id_22["device_chain"] = ".devices[1].chains[0].devices[0]"
		self.select_device_id_22["ctrl_type"] = "on/off"
		self.select_device_id_22["enc_first"] = 127
		self.select_device_id_22["enc_second"] = 0
		self.select_device_id_22["switch_type"] = "momentary"
		self.select_device_id_22["json_id"] = 22
		self.select_device_id_22["mapping_name"] = "Select Device"
		self.select_device_id_22["mapping_type"] = "Select Device"
		self.select_device_id_22["parent_json_id"] = 21
		self.select_device_id_22["parent_name"] = "device_select___chain_1_id_21"
		self.device_select___chain_2_id_23 = {}
		self.device_select___chain_2_id_23["track"] = self.track_num(2)
		self.device_select___chain_2_id_23["module"] = "self.song().tracks[self.track_num(0)].devices[1].chains[1].devices[0]"
		self.device_select___chain_2_id_23["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_2_id_23["LED_feedback"] = "custom"
		self.device_select___chain_2_id_23["LED_feedback_active"] = ""
		self.device_select___chain_2_id_23["LED_on"] = "127"
		self.device_select___chain_2_id_23["LED_off"] = "0"
		self.device_select___chain_2_id_23["LED_send_feedback_to_selected"] = []
		self.device_select___chain_2_id_23["json_id"] = 23
		self.device_select___chain_2_id_23["mapping_name"] = "Device Select  - Chain 2"
		self.device_select___chain_2_id_23["mapping_type"] = "Device"
		self.device_select___chain_2_id_23["parent_json_id"] = 17
		self.device_select___chain_2_id_23["parent_name"] = "apiano_id_17"
		self.select_device_id_24 = {}
		self.select_device_id_24["attached_to"] = "midi_note_ch_0_val_1"
		self.select_device_id_24["module"] = "self"
		self.select_device_id_24["element"] = "select_a_device"
		self.select_device_id_24["output_type"] = "func"
		self.select_device_id_24["func_arg"] = "cnfg"
		self.select_device_id_24["parent_track"] = "self.song().tracks[self.track_num(0)]"
		self.select_device_id_24["device_chain"] = ".devices[1].chains[1].devices[0]"
		self.select_device_id_24["ctrl_type"] = "on/off"
		self.select_device_id_24["enc_first"] = 127
		self.select_device_id_24["enc_second"] = 0
		self.select_device_id_24["switch_type"] = "momentary"
		self.select_device_id_24["json_id"] = 24
		self.select_device_id_24["mapping_name"] = "Select Device"
		self.select_device_id_24["mapping_type"] = "Select Device"
		self.select_device_id_24["parent_json_id"] = 23
		self.select_device_id_24["parent_name"] = "device_select___chain_2_id_23"
		self.device_select___chain_3_id_25 = {}
		self.device_select___chain_3_id_25["track"] = self.track_num(2)
		self.device_select___chain_3_id_25["module"] = "self.song().tracks[self.track_num(0)].devices[1].chains[2].devices[0]"
		self.device_select___chain_3_id_25["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_3_id_25["LED_feedback"] = "custom"
		self.device_select___chain_3_id_25["LED_feedback_active"] = ""
		self.device_select___chain_3_id_25["LED_on"] = "127"
		self.device_select___chain_3_id_25["LED_off"] = "0"
		self.device_select___chain_3_id_25["LED_send_feedback_to_selected"] = []
		self.device_select___chain_3_id_25["json_id"] = 25
		self.device_select___chain_3_id_25["mapping_name"] = "Device Select  - Chain 3"
		self.device_select___chain_3_id_25["mapping_type"] = "Device"
		self.device_select___chain_3_id_25["parent_json_id"] = 17
		self.device_select___chain_3_id_25["parent_name"] = "apiano_id_17"
		self.select_device_id_26 = {}
		self.select_device_id_26["attached_to"] = "midi_note_ch_0_val_2"
		self.select_device_id_26["module"] = "self"
		self.select_device_id_26["element"] = "select_a_device"
		self.select_device_id_26["output_type"] = "func"
		self.select_device_id_26["func_arg"] = "cnfg"
		self.select_device_id_26["parent_track"] = "self.song().tracks[self.track_num(0)]"
		self.select_device_id_26["device_chain"] = ".devices[1].chains[2].devices[0]"
		self.select_device_id_26["ctrl_type"] = "on/off"
		self.select_device_id_26["enc_first"] = 127
		self.select_device_id_26["enc_second"] = 0
		self.select_device_id_26["switch_type"] = "momentary"
		self.select_device_id_26["json_id"] = 26
		self.select_device_id_26["mapping_name"] = "Select Device"
		self.select_device_id_26["mapping_type"] = "Select Device"
		self.select_device_id_26["parent_json_id"] = 25
		self.select_device_id_26["parent_name"] = "device_select___chain_3_id_25"
		self.device_select___chain_4_id_27 = {}
		self.device_select___chain_4_id_27["track"] = self.track_num(2)
		self.device_select___chain_4_id_27["module"] = "self.song().tracks[self.track_num(0)].devices[1].chains[3].devices[0]"
		self.device_select___chain_4_id_27["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_4_id_27["LED_feedback"] = "custom"
		self.device_select___chain_4_id_27["LED_feedback_active"] = ""
		self.device_select___chain_4_id_27["LED_on"] = "127"
		self.device_select___chain_4_id_27["LED_off"] = "0"
		self.device_select___chain_4_id_27["LED_send_feedback_to_selected"] = []
		self.device_select___chain_4_id_27["json_id"] = 27
		self.device_select___chain_4_id_27["mapping_name"] = "Device Select  - Chain 4"
		self.device_select___chain_4_id_27["mapping_type"] = "Device"
		self.device_select___chain_4_id_27["parent_json_id"] = 17
		self.device_select___chain_4_id_27["parent_name"] = "apiano_id_17"
		self.select_device_id_28 = {}
		self.select_device_id_28["attached_to"] = "midi_note_ch_0_val_3"
		self.select_device_id_28["module"] = "self"
		self.select_device_id_28["element"] = "select_a_device"
		self.select_device_id_28["output_type"] = "func"
		self.select_device_id_28["func_arg"] = "cnfg"
		self.select_device_id_28["parent_track"] = "self.song().tracks[self.track_num(0)]"
		self.select_device_id_28["device_chain"] = ".devices[1].chains[3].devices[0]"
		self.select_device_id_28["ctrl_type"] = "on/off"
		self.select_device_id_28["enc_first"] = 127
		self.select_device_id_28["enc_second"] = 0
		self.select_device_id_28["switch_type"] = "momentary"
		self.select_device_id_28["json_id"] = 28
		self.select_device_id_28["mapping_name"] = "Select Device"
		self.select_device_id_28["mapping_type"] = "Select Device"
		self.select_device_id_28["parent_json_id"] = 27
		self.select_device_id_28["parent_name"] = "device_select___chain_4_id_27"
		self.device_select___chain_5_id_29 = {}
		self.device_select___chain_5_id_29["track"] = self.track_num(2)
		self.device_select___chain_5_id_29["module"] = "self.song().tracks[self.track_num(0)].devices[1].chains[4].devices[0]"
		self.device_select___chain_5_id_29["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_5_id_29["LED_feedback"] = "custom"
		self.device_select___chain_5_id_29["LED_feedback_active"] = ""
		self.device_select___chain_5_id_29["LED_on"] = "127"
		self.device_select___chain_5_id_29["LED_off"] = "0"
		self.device_select___chain_5_id_29["LED_send_feedback_to_selected"] = []
		self.device_select___chain_5_id_29["json_id"] = 29
		self.device_select___chain_5_id_29["mapping_name"] = "Device Select  - Chain 5"
		self.device_select___chain_5_id_29["mapping_type"] = "Device"
		self.device_select___chain_5_id_29["parent_json_id"] = 17
		self.device_select___chain_5_id_29["parent_name"] = "apiano_id_17"
		self.select_device_id_30 = {}
		self.select_device_id_30["attached_to"] = "midi_note_ch_0_val_4"
		self.select_device_id_30["module"] = "self"
		self.select_device_id_30["element"] = "select_a_device"
		self.select_device_id_30["output_type"] = "func"
		self.select_device_id_30["func_arg"] = "cnfg"
		self.select_device_id_30["parent_track"] = "self.song().tracks[self.track_num(0)]"
		self.select_device_id_30["device_chain"] = ".devices[1].chains[4].devices[0]"
		self.select_device_id_30["ctrl_type"] = "on/off"
		self.select_device_id_30["enc_first"] = 127
		self.select_device_id_30["enc_second"] = 0
		self.select_device_id_30["switch_type"] = "momentary"
		self.select_device_id_30["json_id"] = 30
		self.select_device_id_30["mapping_name"] = "Select Device"
		self.select_device_id_30["mapping_type"] = "Select Device"
		self.select_device_id_30["parent_json_id"] = 29
		self.select_device_id_30["parent_name"] = "device_select___chain_5_id_29"
		self.epiano_id_31 = {}
		self.epiano_id_31["track"] = self.track_num(2)
		self.epiano_id_31["module"] = "self.song().tracks[self.track_num(1)]"
		self.epiano_id_31["LED_mapping_type_needs_feedback"] = ""
		self.epiano_id_31["LED_feedback"] = "custom"
		self.epiano_id_31["LED_feedback_active"] = ""
		self.epiano_id_31["LED_on"] = "127"
		self.epiano_id_31["LED_off"] = "0"
		self.epiano_id_31["LED_send_feedback_to_selected"] = []
		self.epiano_id_31["json_id"] = 31
		self.epiano_id_31["mapping_name"] = "EPiano"
		self.epiano_id_31["mapping_type"] = "Track"
		self.epiano_id_31["parent_json_id"] = 1
		self.epiano_id_31["parent_name"] = "main_id_1"
		self.power_id_32 = {}
		self.power_id_32["attached_to"] = "midi_note_ch_1_val_5"
		self.power_id_32["track"] = self.track_num(2)
		self.power_id_32["module"] = "self.song().tracks[self.track_num(1)].devices[0].parameters[0]"
		self.power_id_32["minimum"] = 0.0
		self.power_id_32["maximum"] = 1.0
		self.power_id_32["snap_to"] = 1
		self.power_id_32["element"] = "value"
		self.power_id_32["output_type"] = "val"
		self.power_id_32["ui_listener"] = "value"
		self.power_id_32["feedback_brain"] = "feedback_on_off"
		self.power_id_32["enc_first"] = 127
		self.power_id_32["enc_second"] = 0
		self.power_id_32["switch_type"] = "toggle"
		self.power_id_32["ctrl_type"] = "on/off"
		self.power_id_32["LED_mapping_type_needs_feedback"] = "1"
		self.power_id_32["LED_feedback"] = "default"
		self.power_id_32["LED_feedback_active"] = "1"
		self.power_id_32["LED_on"] = "127"
		self.power_id_32["LED_off"] = "0"
		self.power_id_32["LED_send_feedback_to_selected"] = ["midi_note_ch_1_val_5"]
		self.power_id_32["json_id"] = 32
		self.power_id_32["mapping_name"] = "Power"
		self.power_id_32["mapping_type"] = "On/Off"
		self.power_id_32["parent_json_id"] = 39
		self.power_id_32["parent_name"] = "track_on_id_39"
		self.select_device_id_33 = {}
		self.select_device_id_33["attached_to"] = "midi_note_ch_1_val_0"
		self.select_device_id_33["module"] = "self"
		self.select_device_id_33["element"] = "select_a_device"
		self.select_device_id_33["output_type"] = "func"
		self.select_device_id_33["func_arg"] = "cnfg"
		self.select_device_id_33["parent_track"] = "self.song().tracks[self.track_num(1)]"
		self.select_device_id_33["device_chain"] = ".devices[1].chains[0].devices[0]"
		self.select_device_id_33["ctrl_type"] = "on/off"
		self.select_device_id_33["enc_first"] = 127
		self.select_device_id_33["enc_second"] = 0
		self.select_device_id_33["switch_type"] = "momentary"
		self.select_device_id_33["json_id"] = 33
		self.select_device_id_33["mapping_name"] = "Select Device"
		self.select_device_id_33["mapping_type"] = "Select Device"
		self.select_device_id_33["parent_json_id"] = 40
		self.select_device_id_33["parent_name"] = "device_select___chain_1_id_40"
		self.select_device_id_34 = {}
		self.select_device_id_34["attached_to"] = "midi_note_ch_1_val_1"
		self.select_device_id_34["module"] = "self"
		self.select_device_id_34["element"] = "select_a_device"
		self.select_device_id_34["output_type"] = "func"
		self.select_device_id_34["func_arg"] = "cnfg"
		self.select_device_id_34["parent_track"] = "self.song().tracks[self.track_num(1)]"
		self.select_device_id_34["device_chain"] = ".devices[1].chains[1].devices[0]"
		self.select_device_id_34["ctrl_type"] = "on/off"
		self.select_device_id_34["enc_first"] = 127
		self.select_device_id_34["enc_second"] = 0
		self.select_device_id_34["switch_type"] = "momentary"
		self.select_device_id_34["json_id"] = 34
		self.select_device_id_34["mapping_name"] = "Select Device"
		self.select_device_id_34["mapping_type"] = "Select Device"
		self.select_device_id_34["parent_json_id"] = 41
		self.select_device_id_34["parent_name"] = "device_select___chain_2_id_41"
		self.select_device_id_35 = {}
		self.select_device_id_35["attached_to"] = "midi_note_ch_1_val_2"
		self.select_device_id_35["module"] = "self"
		self.select_device_id_35["element"] = "select_a_device"
		self.select_device_id_35["output_type"] = "func"
		self.select_device_id_35["func_arg"] = "cnfg"
		self.select_device_id_35["parent_track"] = "self.song().tracks[self.track_num(1)]"
		self.select_device_id_35["device_chain"] = ".devices[1].chains[2].devices[0]"
		self.select_device_id_35["ctrl_type"] = "on/off"
		self.select_device_id_35["enc_first"] = 127
		self.select_device_id_35["enc_second"] = 0
		self.select_device_id_35["switch_type"] = "momentary"
		self.select_device_id_35["json_id"] = 35
		self.select_device_id_35["mapping_name"] = "Select Device"
		self.select_device_id_35["mapping_type"] = "Select Device"
		self.select_device_id_35["parent_json_id"] = 42
		self.select_device_id_35["parent_name"] = "device_select___chain_3_id_42"
		self.select_device_id_36 = {}
		self.select_device_id_36["attached_to"] = "midi_note_ch_1_val_3"
		self.select_device_id_36["module"] = "self"
		self.select_device_id_36["element"] = "select_a_device"
		self.select_device_id_36["output_type"] = "func"
		self.select_device_id_36["func_arg"] = "cnfg"
		self.select_device_id_36["parent_track"] = "self.song().tracks[self.track_num(1)]"
		self.select_device_id_36["device_chain"] = ".devices[1].chains[3].devices[0]"
		self.select_device_id_36["ctrl_type"] = "on/off"
		self.select_device_id_36["enc_first"] = 127
		self.select_device_id_36["enc_second"] = 0
		self.select_device_id_36["switch_type"] = "momentary"
		self.select_device_id_36["json_id"] = 36
		self.select_device_id_36["mapping_name"] = "Select Device"
		self.select_device_id_36["mapping_type"] = "Select Device"
		self.select_device_id_36["parent_json_id"] = 43
		self.select_device_id_36["parent_name"] = "device_select___chain_4_id_43"
		self.select_device_id_37 = {}
		self.select_device_id_37["attached_to"] = "midi_note_ch_1_val_4"
		self.select_device_id_37["module"] = "self"
		self.select_device_id_37["element"] = "select_a_device"
		self.select_device_id_37["output_type"] = "func"
		self.select_device_id_37["func_arg"] = "cnfg"
		self.select_device_id_37["parent_track"] = "self.song().tracks[self.track_num(1)]"
		self.select_device_id_37["device_chain"] = ".devices[1].chains[4].devices[0]"
		self.select_device_id_37["ctrl_type"] = "on/off"
		self.select_device_id_37["enc_first"] = 127
		self.select_device_id_37["enc_second"] = 0
		self.select_device_id_37["switch_type"] = "momentary"
		self.select_device_id_37["json_id"] = 37
		self.select_device_id_37["mapping_name"] = "Select Device"
		self.select_device_id_37["mapping_type"] = "Select Device"
		self.select_device_id_37["parent_json_id"] = 44
		self.select_device_id_37["parent_name"] = "device_select___chain_5_id_44"
		self.volume_id_38 = {}
		self.volume_id_38["attached_to"] = "midi_cc_ch_1_val_7"
		self.volume_id_38["track"] = self.track_num(2)
		self.volume_id_38["module"] = "self.song().tracks[self.track_num(1)].mixer_device.volume"
		self.volume_id_38["element"] = "value"
		self.volume_id_38["output_type"] = "val"
		self.volume_id_38["minimum"] = round(0,2)
		self.volume_id_38["maximum"] = round(85,2)
		self.volume_id_38["decimal_places"] = 2
		self.volume_id_38["ui_listener"] = "value"
		self.volume_id_38["feedback_brain"] = "feedback_range"
		self.volume_id_38["ctrl_type"] = "absolute"
		self.volume_id_38["takeover_mode"] = "None"
		self.volume_id_38["enc_first"] = 0
		self.volume_id_38["enc_second"] = 127
		self.volume_id_38["reverse_mode"] = False
		self.volume_id_38["LED_mapping_type_needs_feedback"] = "1"
		self.volume_id_38["LED_feedback"] = "default"
		self.volume_id_38["LED_feedback_active"] = "1"
		self.volume_id_38["LED_on"] = "127"
		self.volume_id_38["LED_off"] = "0"
		self.volume_id_38["LED_send_feedback_to_selected"] = ["midi_cc_ch_1_val_7"]
		self.volume_id_38["snap_to"] = True
		self.volume_id_38["json_id"] = 38
		self.volume_id_38["mapping_name"] = "Volume"
		self.volume_id_38["mapping_type"] = "Volume"
		self.volume_id_38["parent_json_id"] = 31
		self.volume_id_38["parent_name"] = "epiano_id_31"
		self.track_on_id_39 = {}
		self.track_on_id_39["track"] = self.track_num(2)
		self.track_on_id_39["module"] = "self.song().tracks[self.track_num(1)].devices[0]"
		self.track_on_id_39["LED_mapping_type_needs_feedback"] = ""
		self.track_on_id_39["LED_feedback"] = "custom"
		self.track_on_id_39["LED_feedback_active"] = ""
		self.track_on_id_39["LED_on"] = "127"
		self.track_on_id_39["LED_off"] = "0"
		self.track_on_id_39["LED_send_feedback_to_selected"] = []
		self.track_on_id_39["json_id"] = 39
		self.track_on_id_39["mapping_name"] = "Track On"
		self.track_on_id_39["mapping_type"] = "Device"
		self.track_on_id_39["parent_json_id"] = 31
		self.track_on_id_39["parent_name"] = "epiano_id_31"
		self.device_select___chain_1_id_40 = {}
		self.device_select___chain_1_id_40["track"] = self.track_num(2)
		self.device_select___chain_1_id_40["module"] = "self.song().tracks[self.track_num(1)].devices[1].chains[0].devices[0]"
		self.device_select___chain_1_id_40["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_1_id_40["LED_feedback"] = "custom"
		self.device_select___chain_1_id_40["LED_feedback_active"] = ""
		self.device_select___chain_1_id_40["LED_on"] = "127"
		self.device_select___chain_1_id_40["LED_off"] = "0"
		self.device_select___chain_1_id_40["LED_send_feedback_to_selected"] = []
		self.device_select___chain_1_id_40["json_id"] = 40
		self.device_select___chain_1_id_40["mapping_name"] = "Device Select  - Chain 1"
		self.device_select___chain_1_id_40["mapping_type"] = "Device"
		self.device_select___chain_1_id_40["parent_json_id"] = 31
		self.device_select___chain_1_id_40["parent_name"] = "epiano_id_31"
		self.device_select___chain_2_id_41 = {}
		self.device_select___chain_2_id_41["track"] = self.track_num(2)
		self.device_select___chain_2_id_41["module"] = "self.song().tracks[self.track_num(1)].devices[1].chains[1].devices[0]"
		self.device_select___chain_2_id_41["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_2_id_41["LED_feedback"] = "custom"
		self.device_select___chain_2_id_41["LED_feedback_active"] = ""
		self.device_select___chain_2_id_41["LED_on"] = "127"
		self.device_select___chain_2_id_41["LED_off"] = "0"
		self.device_select___chain_2_id_41["LED_send_feedback_to_selected"] = []
		self.device_select___chain_2_id_41["json_id"] = 41
		self.device_select___chain_2_id_41["mapping_name"] = "Device Select  - Chain 2"
		self.device_select___chain_2_id_41["mapping_type"] = "Device"
		self.device_select___chain_2_id_41["parent_json_id"] = 31
		self.device_select___chain_2_id_41["parent_name"] = "epiano_id_31"
		self.device_select___chain_3_id_42 = {}
		self.device_select___chain_3_id_42["track"] = self.track_num(2)
		self.device_select___chain_3_id_42["module"] = "self.song().tracks[self.track_num(1)].devices[1].chains[2].devices[0]"
		self.device_select___chain_3_id_42["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_3_id_42["LED_feedback"] = "custom"
		self.device_select___chain_3_id_42["LED_feedback_active"] = ""
		self.device_select___chain_3_id_42["LED_on"] = "127"
		self.device_select___chain_3_id_42["LED_off"] = "0"
		self.device_select___chain_3_id_42["LED_send_feedback_to_selected"] = []
		self.device_select___chain_3_id_42["json_id"] = 42
		self.device_select___chain_3_id_42["mapping_name"] = "Device Select  - Chain 3"
		self.device_select___chain_3_id_42["mapping_type"] = "Device"
		self.device_select___chain_3_id_42["parent_json_id"] = 31
		self.device_select___chain_3_id_42["parent_name"] = "epiano_id_31"
		self.device_select___chain_4_id_43 = {}
		self.device_select___chain_4_id_43["track"] = self.track_num(2)
		self.device_select___chain_4_id_43["module"] = "self.song().tracks[self.track_num(1)].devices[1].chains[3].devices[0]"
		self.device_select___chain_4_id_43["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_4_id_43["LED_feedback"] = "custom"
		self.device_select___chain_4_id_43["LED_feedback_active"] = ""
		self.device_select___chain_4_id_43["LED_on"] = "127"
		self.device_select___chain_4_id_43["LED_off"] = "0"
		self.device_select___chain_4_id_43["LED_send_feedback_to_selected"] = []
		self.device_select___chain_4_id_43["json_id"] = 43
		self.device_select___chain_4_id_43["mapping_name"] = "Device Select  - Chain 4"
		self.device_select___chain_4_id_43["mapping_type"] = "Device"
		self.device_select___chain_4_id_43["parent_json_id"] = 31
		self.device_select___chain_4_id_43["parent_name"] = "epiano_id_31"
		self.device_select___chain_5_id_44 = {}
		self.device_select___chain_5_id_44["track"] = self.track_num(2)
		self.device_select___chain_5_id_44["module"] = "self.song().tracks[self.track_num(1)].devices[1].chains[4].devices[0]"
		self.device_select___chain_5_id_44["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_5_id_44["LED_feedback"] = "custom"
		self.device_select___chain_5_id_44["LED_feedback_active"] = ""
		self.device_select___chain_5_id_44["LED_on"] = "127"
		self.device_select___chain_5_id_44["LED_off"] = "0"
		self.device_select___chain_5_id_44["LED_send_feedback_to_selected"] = []
		self.device_select___chain_5_id_44["json_id"] = 44
		self.device_select___chain_5_id_44["mapping_name"] = "Device Select  - Chain 5"
		self.device_select___chain_5_id_44["mapping_type"] = "Device"
		self.device_select___chain_5_id_44["parent_json_id"] = 31
		self.device_select___chain_5_id_44["parent_name"] = "epiano_id_31"
		self.synth_id_45 = {}
		self.synth_id_45["track"] = self.track_num(2)
		self.synth_id_45["module"] = "self.song().tracks[self.track_num(2)]"
		self.synth_id_45["LED_mapping_type_needs_feedback"] = ""
		self.synth_id_45["LED_feedback"] = "custom"
		self.synth_id_45["LED_feedback_active"] = ""
		self.synth_id_45["LED_on"] = "127"
		self.synth_id_45["LED_off"] = "0"
		self.synth_id_45["LED_send_feedback_to_selected"] = []
		self.synth_id_45["json_id"] = 45
		self.synth_id_45["mapping_name"] = "Synth"
		self.synth_id_45["mapping_type"] = "Track"
		self.synth_id_45["parent_json_id"] = 1
		self.synth_id_45["parent_name"] = "main_id_1"
		self.power_id_46 = {}
		self.power_id_46["attached_to"] = "midi_note_ch_2_val_5"
		self.power_id_46["track"] = self.track_num(2)
		self.power_id_46["module"] = "self.song().tracks[self.track_num(2)].devices[0].parameters[0]"
		self.power_id_46["minimum"] = 0.0
		self.power_id_46["maximum"] = 1.0
		self.power_id_46["snap_to"] = 1
		self.power_id_46["element"] = "value"
		self.power_id_46["output_type"] = "val"
		self.power_id_46["ui_listener"] = "value"
		self.power_id_46["feedback_brain"] = "feedback_on_off"
		self.power_id_46["enc_first"] = 127
		self.power_id_46["enc_second"] = 0
		self.power_id_46["switch_type"] = "toggle"
		self.power_id_46["ctrl_type"] = "on/off"
		self.power_id_46["LED_mapping_type_needs_feedback"] = "1"
		self.power_id_46["LED_feedback"] = "default"
		self.power_id_46["LED_feedback_active"] = "1"
		self.power_id_46["LED_on"] = "127"
		self.power_id_46["LED_off"] = "0"
		self.power_id_46["LED_send_feedback_to_selected"] = ["midi_note_ch_2_val_5"]
		self.power_id_46["json_id"] = 46
		self.power_id_46["mapping_name"] = "Power"
		self.power_id_46["mapping_type"] = "On/Off"
		self.power_id_46["parent_json_id"] = 53
		self.power_id_46["parent_name"] = "track_on_id_53"
		self.select_device_id_47 = {}
		self.select_device_id_47["attached_to"] = "midi_note_ch_2_val_0"
		self.select_device_id_47["module"] = "self"
		self.select_device_id_47["element"] = "select_a_device"
		self.select_device_id_47["output_type"] = "func"
		self.select_device_id_47["func_arg"] = "cnfg"
		self.select_device_id_47["parent_track"] = "self.song().tracks[self.track_num(2)]"
		self.select_device_id_47["device_chain"] = ".devices[1].chains[0].devices[0]"
		self.select_device_id_47["ctrl_type"] = "on/off"
		self.select_device_id_47["enc_first"] = 127
		self.select_device_id_47["enc_second"] = 0
		self.select_device_id_47["switch_type"] = "momentary"
		self.select_device_id_47["json_id"] = 47
		self.select_device_id_47["mapping_name"] = "Select Device"
		self.select_device_id_47["mapping_type"] = "Select Device"
		self.select_device_id_47["parent_json_id"] = 54
		self.select_device_id_47["parent_name"] = "device_select___chain_1_id_54"
		self.select_device_id_48 = {}
		self.select_device_id_48["attached_to"] = "midi_note_ch_2_val_1"
		self.select_device_id_48["module"] = "self"
		self.select_device_id_48["element"] = "select_a_device"
		self.select_device_id_48["output_type"] = "func"
		self.select_device_id_48["func_arg"] = "cnfg"
		self.select_device_id_48["parent_track"] = "self.song().tracks[self.track_num(2)]"
		self.select_device_id_48["device_chain"] = ".devices[1].chains[1].devices[0]"
		self.select_device_id_48["ctrl_type"] = "on/off"
		self.select_device_id_48["enc_first"] = 127
		self.select_device_id_48["enc_second"] = 0
		self.select_device_id_48["switch_type"] = "momentary"
		self.select_device_id_48["json_id"] = 48
		self.select_device_id_48["mapping_name"] = "Select Device"
		self.select_device_id_48["mapping_type"] = "Select Device"
		self.select_device_id_48["parent_json_id"] = 55
		self.select_device_id_48["parent_name"] = "device_select___chain_2_id_55"
		self.select_device_id_49 = {}
		self.select_device_id_49["attached_to"] = "midi_note_ch_2_val_2"
		self.select_device_id_49["module"] = "self"
		self.select_device_id_49["element"] = "select_a_device"
		self.select_device_id_49["output_type"] = "func"
		self.select_device_id_49["func_arg"] = "cnfg"
		self.select_device_id_49["parent_track"] = "self.song().tracks[self.track_num(2)]"
		self.select_device_id_49["device_chain"] = ".devices[1].chains[2].devices[0]"
		self.select_device_id_49["ctrl_type"] = "on/off"
		self.select_device_id_49["enc_first"] = 127
		self.select_device_id_49["enc_second"] = 0
		self.select_device_id_49["switch_type"] = "momentary"
		self.select_device_id_49["json_id"] = 49
		self.select_device_id_49["mapping_name"] = "Select Device"
		self.select_device_id_49["mapping_type"] = "Select Device"
		self.select_device_id_49["parent_json_id"] = 56
		self.select_device_id_49["parent_name"] = "device_select___chain_3_id_56"
		self.select_device_id_50 = {}
		self.select_device_id_50["attached_to"] = "midi_note_ch_2_val_3"
		self.select_device_id_50["module"] = "self"
		self.select_device_id_50["element"] = "select_a_device"
		self.select_device_id_50["output_type"] = "func"
		self.select_device_id_50["func_arg"] = "cnfg"
		self.select_device_id_50["parent_track"] = "self.song().tracks[self.track_num(2)]"
		self.select_device_id_50["device_chain"] = ".devices[1].chains[3].devices[0]"
		self.select_device_id_50["ctrl_type"] = "on/off"
		self.select_device_id_50["enc_first"] = 127
		self.select_device_id_50["enc_second"] = 0
		self.select_device_id_50["switch_type"] = "momentary"
		self.select_device_id_50["json_id"] = 50
		self.select_device_id_50["mapping_name"] = "Select Device"
		self.select_device_id_50["mapping_type"] = "Select Device"
		self.select_device_id_50["parent_json_id"] = 57
		self.select_device_id_50["parent_name"] = "device_select___chain_4_id_57"
		self.select_device_id_51 = {}
		self.select_device_id_51["attached_to"] = "midi_note_ch_2_val_4"
		self.select_device_id_51["module"] = "self"
		self.select_device_id_51["element"] = "select_a_device"
		self.select_device_id_51["output_type"] = "func"
		self.select_device_id_51["func_arg"] = "cnfg"
		self.select_device_id_51["parent_track"] = "self.song().tracks[self.track_num(2)]"
		self.select_device_id_51["device_chain"] = ".devices[1].chains[4].devices[0]"
		self.select_device_id_51["ctrl_type"] = "on/off"
		self.select_device_id_51["enc_first"] = 127
		self.select_device_id_51["enc_second"] = 0
		self.select_device_id_51["switch_type"] = "momentary"
		self.select_device_id_51["json_id"] = 51
		self.select_device_id_51["mapping_name"] = "Select Device"
		self.select_device_id_51["mapping_type"] = "Select Device"
		self.select_device_id_51["parent_json_id"] = 58
		self.select_device_id_51["parent_name"] = "device_select___chain_5_id_58"
		self.volume_id_52 = {}
		self.volume_id_52["attached_to"] = "midi_cc_ch_2_val_7"
		self.volume_id_52["track"] = self.track_num(2)
		self.volume_id_52["module"] = "self.song().tracks[self.track_num(2)].mixer_device.volume"
		self.volume_id_52["element"] = "value"
		self.volume_id_52["output_type"] = "val"
		self.volume_id_52["minimum"] = round(0,2)
		self.volume_id_52["maximum"] = round(85,2)
		self.volume_id_52["decimal_places"] = 2
		self.volume_id_52["ui_listener"] = "value"
		self.volume_id_52["feedback_brain"] = "feedback_range"
		self.volume_id_52["ctrl_type"] = "absolute"
		self.volume_id_52["takeover_mode"] = "None"
		self.volume_id_52["enc_first"] = 0
		self.volume_id_52["enc_second"] = 127
		self.volume_id_52["reverse_mode"] = False
		self.volume_id_52["LED_mapping_type_needs_feedback"] = "1"
		self.volume_id_52["LED_feedback"] = "default"
		self.volume_id_52["LED_feedback_active"] = "1"
		self.volume_id_52["LED_on"] = "127"
		self.volume_id_52["LED_off"] = "0"
		self.volume_id_52["LED_send_feedback_to_selected"] = ["midi_cc_ch_2_val_7"]
		self.volume_id_52["snap_to"] = True
		self.volume_id_52["json_id"] = 52
		self.volume_id_52["mapping_name"] = "Volume"
		self.volume_id_52["mapping_type"] = "Volume"
		self.volume_id_52["parent_json_id"] = 45
		self.volume_id_52["parent_name"] = "synth_id_45"
		self.track_on_id_53 = {}
		self.track_on_id_53["track"] = self.track_num(2)
		self.track_on_id_53["module"] = "self.song().tracks[self.track_num(2)].devices[0]"
		self.track_on_id_53["LED_mapping_type_needs_feedback"] = ""
		self.track_on_id_53["LED_feedback"] = "custom"
		self.track_on_id_53["LED_feedback_active"] = ""
		self.track_on_id_53["LED_on"] = "127"
		self.track_on_id_53["LED_off"] = "0"
		self.track_on_id_53["LED_send_feedback_to_selected"] = []
		self.track_on_id_53["json_id"] = 53
		self.track_on_id_53["mapping_name"] = "Track On"
		self.track_on_id_53["mapping_type"] = "Device"
		self.track_on_id_53["parent_json_id"] = 45
		self.track_on_id_53["parent_name"] = "synth_id_45"
		self.device_select___chain_1_id_54 = {}
		self.device_select___chain_1_id_54["track"] = self.track_num(2)
		self.device_select___chain_1_id_54["module"] = "self.song().tracks[self.track_num(2)].devices[1].chains[0].devices[0]"
		self.device_select___chain_1_id_54["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_1_id_54["LED_feedback"] = "custom"
		self.device_select___chain_1_id_54["LED_feedback_active"] = ""
		self.device_select___chain_1_id_54["LED_on"] = "127"
		self.device_select___chain_1_id_54["LED_off"] = "0"
		self.device_select___chain_1_id_54["LED_send_feedback_to_selected"] = []
		self.device_select___chain_1_id_54["json_id"] = 54
		self.device_select___chain_1_id_54["mapping_name"] = "Device Select  - Chain 1"
		self.device_select___chain_1_id_54["mapping_type"] = "Device"
		self.device_select___chain_1_id_54["parent_json_id"] = 45
		self.device_select___chain_1_id_54["parent_name"] = "synth_id_45"
		self.device_select___chain_2_id_55 = {}
		self.device_select___chain_2_id_55["track"] = self.track_num(2)
		self.device_select___chain_2_id_55["module"] = "self.song().tracks[self.track_num(2)].devices[1].chains[1].devices[0]"
		self.device_select___chain_2_id_55["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_2_id_55["LED_feedback"] = "custom"
		self.device_select___chain_2_id_55["LED_feedback_active"] = ""
		self.device_select___chain_2_id_55["LED_on"] = "127"
		self.device_select___chain_2_id_55["LED_off"] = "0"
		self.device_select___chain_2_id_55["LED_send_feedback_to_selected"] = []
		self.device_select___chain_2_id_55["json_id"] = 55
		self.device_select___chain_2_id_55["mapping_name"] = "Device Select  - Chain 2"
		self.device_select___chain_2_id_55["mapping_type"] = "Device"
		self.device_select___chain_2_id_55["parent_json_id"] = 45
		self.device_select___chain_2_id_55["parent_name"] = "synth_id_45"
		self.device_select___chain_3_id_56 = {}
		self.device_select___chain_3_id_56["track"] = self.track_num(2)
		self.device_select___chain_3_id_56["module"] = "self.song().tracks[self.track_num(2)].devices[1].chains[2].devices[0]"
		self.device_select___chain_3_id_56["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_3_id_56["LED_feedback"] = "custom"
		self.device_select___chain_3_id_56["LED_feedback_active"] = ""
		self.device_select___chain_3_id_56["LED_on"] = "127"
		self.device_select___chain_3_id_56["LED_off"] = "0"
		self.device_select___chain_3_id_56["LED_send_feedback_to_selected"] = []
		self.device_select___chain_3_id_56["json_id"] = 56
		self.device_select___chain_3_id_56["mapping_name"] = "Device Select  - Chain 3"
		self.device_select___chain_3_id_56["mapping_type"] = "Device"
		self.device_select___chain_3_id_56["parent_json_id"] = 45
		self.device_select___chain_3_id_56["parent_name"] = "synth_id_45"
		self.device_select___chain_4_id_57 = {}
		self.device_select___chain_4_id_57["track"] = self.track_num(2)
		self.device_select___chain_4_id_57["module"] = "self.song().tracks[self.track_num(2)].devices[1].chains[3].devices[0]"
		self.device_select___chain_4_id_57["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_4_id_57["LED_feedback"] = "custom"
		self.device_select___chain_4_id_57["LED_feedback_active"] = ""
		self.device_select___chain_4_id_57["LED_on"] = "127"
		self.device_select___chain_4_id_57["LED_off"] = "0"
		self.device_select___chain_4_id_57["LED_send_feedback_to_selected"] = []
		self.device_select___chain_4_id_57["json_id"] = 57
		self.device_select___chain_4_id_57["mapping_name"] = "Device Select  - Chain 4"
		self.device_select___chain_4_id_57["mapping_type"] = "Device"
		self.device_select___chain_4_id_57["parent_json_id"] = 45
		self.device_select___chain_4_id_57["parent_name"] = "synth_id_45"
		self.device_select___chain_5_id_58 = {}
		self.device_select___chain_5_id_58["track"] = self.track_num(2)
		self.device_select___chain_5_id_58["module"] = "self.song().tracks[self.track_num(2)].devices[1].chains[4].devices[0]"
		self.device_select___chain_5_id_58["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_5_id_58["LED_feedback"] = "custom"
		self.device_select___chain_5_id_58["LED_feedback_active"] = ""
		self.device_select___chain_5_id_58["LED_on"] = "127"
		self.device_select___chain_5_id_58["LED_off"] = "0"
		self.device_select___chain_5_id_58["LED_send_feedback_to_selected"] = []
		self.device_select___chain_5_id_58["json_id"] = 58
		self.device_select___chain_5_id_58["mapping_name"] = "Device Select  - Chain 5"
		self.device_select___chain_5_id_58["mapping_type"] = "Device"
		self.device_select___chain_5_id_58["parent_json_id"] = 45
		self.device_select___chain_5_id_58["parent_name"] = "synth_id_45"
		self.strings_id_59 = {}
		self.strings_id_59["track"] = self.track_num(2)
		self.strings_id_59["module"] = "self.song().tracks[self.track_num(3)]"
		self.strings_id_59["LED_mapping_type_needs_feedback"] = ""
		self.strings_id_59["LED_feedback"] = "custom"
		self.strings_id_59["LED_feedback_active"] = ""
		self.strings_id_59["LED_on"] = "127"
		self.strings_id_59["LED_off"] = "0"
		self.strings_id_59["LED_send_feedback_to_selected"] = []
		self.strings_id_59["json_id"] = 59
		self.strings_id_59["mapping_name"] = "Strings"
		self.strings_id_59["mapping_type"] = "Track"
		self.strings_id_59["parent_json_id"] = 1
		self.strings_id_59["parent_name"] = "main_id_1"
		self.power_id_60 = {}
		self.power_id_60["attached_to"] = "midi_note_ch_3_val_5"
		self.power_id_60["track"] = self.track_num(2)
		self.power_id_60["module"] = "self.song().tracks[self.track_num(3)].devices[0].parameters[0]"
		self.power_id_60["minimum"] = 0.0
		self.power_id_60["maximum"] = 1.0
		self.power_id_60["snap_to"] = 1
		self.power_id_60["element"] = "value"
		self.power_id_60["output_type"] = "val"
		self.power_id_60["ui_listener"] = "value"
		self.power_id_60["feedback_brain"] = "feedback_on_off"
		self.power_id_60["enc_first"] = 127
		self.power_id_60["enc_second"] = 0
		self.power_id_60["switch_type"] = "toggle"
		self.power_id_60["ctrl_type"] = "on/off"
		self.power_id_60["LED_mapping_type_needs_feedback"] = "1"
		self.power_id_60["LED_feedback"] = "default"
		self.power_id_60["LED_feedback_active"] = "1"
		self.power_id_60["LED_on"] = "127"
		self.power_id_60["LED_off"] = "0"
		self.power_id_60["LED_send_feedback_to_selected"] = ["midi_note_ch_3_val_5"]
		self.power_id_60["json_id"] = 60
		self.power_id_60["mapping_name"] = "Power"
		self.power_id_60["mapping_type"] = "On/Off"
		self.power_id_60["parent_json_id"] = 67
		self.power_id_60["parent_name"] = "track_on_id_67"
		self.select_device_id_61 = {}
		self.select_device_id_61["attached_to"] = "midi_note_ch_3_val_0"
		self.select_device_id_61["module"] = "self"
		self.select_device_id_61["element"] = "select_a_device"
		self.select_device_id_61["output_type"] = "func"
		self.select_device_id_61["func_arg"] = "cnfg"
		self.select_device_id_61["parent_track"] = "self.song().tracks[self.track_num(3)]"
		self.select_device_id_61["device_chain"] = ".devices[1].chains[0].devices[0]"
		self.select_device_id_61["ctrl_type"] = "on/off"
		self.select_device_id_61["enc_first"] = 127
		self.select_device_id_61["enc_second"] = 0
		self.select_device_id_61["switch_type"] = "momentary"
		self.select_device_id_61["json_id"] = 61
		self.select_device_id_61["mapping_name"] = "Select Device"
		self.select_device_id_61["mapping_type"] = "Select Device"
		self.select_device_id_61["parent_json_id"] = 68
		self.select_device_id_61["parent_name"] = "device_select___chain_1_id_68"
		self.select_device_id_62 = {}
		self.select_device_id_62["attached_to"] = "midi_note_ch_3_val_1"
		self.select_device_id_62["module"] = "self"
		self.select_device_id_62["element"] = "select_a_device"
		self.select_device_id_62["output_type"] = "func"
		self.select_device_id_62["func_arg"] = "cnfg"
		self.select_device_id_62["parent_track"] = "self.song().tracks[self.track_num(3)]"
		self.select_device_id_62["device_chain"] = ".devices[1].chains[1].devices[0]"
		self.select_device_id_62["ctrl_type"] = "on/off"
		self.select_device_id_62["enc_first"] = 127
		self.select_device_id_62["enc_second"] = 0
		self.select_device_id_62["switch_type"] = "momentary"
		self.select_device_id_62["json_id"] = 62
		self.select_device_id_62["mapping_name"] = "Select Device"
		self.select_device_id_62["mapping_type"] = "Select Device"
		self.select_device_id_62["parent_json_id"] = 69
		self.select_device_id_62["parent_name"] = "device_select___chain_2_id_69"
		self.select_device_id_63 = {}
		self.select_device_id_63["attached_to"] = "midi_note_ch_3_val_2"
		self.select_device_id_63["module"] = "self"
		self.select_device_id_63["element"] = "select_a_device"
		self.select_device_id_63["output_type"] = "func"
		self.select_device_id_63["func_arg"] = "cnfg"
		self.select_device_id_63["parent_track"] = "self.song().tracks[self.track_num(3)]"
		self.select_device_id_63["device_chain"] = ".devices[1].chains[2].devices[0]"
		self.select_device_id_63["ctrl_type"] = "on/off"
		self.select_device_id_63["enc_first"] = 127
		self.select_device_id_63["enc_second"] = 0
		self.select_device_id_63["switch_type"] = "momentary"
		self.select_device_id_63["json_id"] = 63
		self.select_device_id_63["mapping_name"] = "Select Device"
		self.select_device_id_63["mapping_type"] = "Select Device"
		self.select_device_id_63["parent_json_id"] = 70
		self.select_device_id_63["parent_name"] = "device_select___chain_3_id_70"
		self.select_device_id_64 = {}
		self.select_device_id_64["attached_to"] = "midi_note_ch_3_val_3"
		self.select_device_id_64["module"] = "self"
		self.select_device_id_64["element"] = "select_a_device"
		self.select_device_id_64["output_type"] = "func"
		self.select_device_id_64["func_arg"] = "cnfg"
		self.select_device_id_64["parent_track"] = "self.song().tracks[self.track_num(3)]"
		self.select_device_id_64["device_chain"] = ".devices[1].chains[3].devices[0]"
		self.select_device_id_64["ctrl_type"] = "on/off"
		self.select_device_id_64["enc_first"] = 127
		self.select_device_id_64["enc_second"] = 0
		self.select_device_id_64["switch_type"] = "momentary"
		self.select_device_id_64["json_id"] = 64
		self.select_device_id_64["mapping_name"] = "Select Device"
		self.select_device_id_64["mapping_type"] = "Select Device"
		self.select_device_id_64["parent_json_id"] = 71
		self.select_device_id_64["parent_name"] = "device_select___chain_4_id_71"
		self.select_device_id_65 = {}
		self.select_device_id_65["attached_to"] = "midi_note_ch_3_val_4"
		self.select_device_id_65["module"] = "self"
		self.select_device_id_65["element"] = "select_a_device"
		self.select_device_id_65["output_type"] = "func"
		self.select_device_id_65["func_arg"] = "cnfg"
		self.select_device_id_65["parent_track"] = "self.song().tracks[self.track_num(3)]"
		self.select_device_id_65["device_chain"] = ".devices[1].chains[4].devices[0]"
		self.select_device_id_65["ctrl_type"] = "on/off"
		self.select_device_id_65["enc_first"] = 127
		self.select_device_id_65["enc_second"] = 0
		self.select_device_id_65["switch_type"] = "momentary"
		self.select_device_id_65["json_id"] = 65
		self.select_device_id_65["mapping_name"] = "Select Device"
		self.select_device_id_65["mapping_type"] = "Select Device"
		self.select_device_id_65["parent_json_id"] = 72
		self.select_device_id_65["parent_name"] = "device_select___chain_5_id_72"
		self.volume_id_66 = {}
		self.volume_id_66["attached_to"] = "midi_cc_ch_3_val_7"
		self.volume_id_66["track"] = self.track_num(2)
		self.volume_id_66["module"] = "self.song().tracks[self.track_num(3)].mixer_device.volume"
		self.volume_id_66["element"] = "value"
		self.volume_id_66["output_type"] = "val"
		self.volume_id_66["minimum"] = round(0,2)
		self.volume_id_66["maximum"] = round(85,2)
		self.volume_id_66["decimal_places"] = 2
		self.volume_id_66["ui_listener"] = "value"
		self.volume_id_66["feedback_brain"] = "feedback_range"
		self.volume_id_66["ctrl_type"] = "absolute"
		self.volume_id_66["takeover_mode"] = "None"
		self.volume_id_66["enc_first"] = 0
		self.volume_id_66["enc_second"] = 127
		self.volume_id_66["reverse_mode"] = False
		self.volume_id_66["LED_mapping_type_needs_feedback"] = "1"
		self.volume_id_66["LED_feedback"] = "default"
		self.volume_id_66["LED_feedback_active"] = "1"
		self.volume_id_66["LED_on"] = "127"
		self.volume_id_66["LED_off"] = "0"
		self.volume_id_66["LED_send_feedback_to_selected"] = ["midi_cc_ch_3_val_7"]
		self.volume_id_66["snap_to"] = True
		self.volume_id_66["json_id"] = 66
		self.volume_id_66["mapping_name"] = "Volume"
		self.volume_id_66["mapping_type"] = "Volume"
		self.volume_id_66["parent_json_id"] = 59
		self.volume_id_66["parent_name"] = "strings_id_59"
		self.track_on_id_67 = {}
		self.track_on_id_67["track"] = self.track_num(2)
		self.track_on_id_67["module"] = "self.song().tracks[self.track_num(3)].devices[0]"
		self.track_on_id_67["LED_mapping_type_needs_feedback"] = ""
		self.track_on_id_67["LED_feedback"] = "custom"
		self.track_on_id_67["LED_feedback_active"] = ""
		self.track_on_id_67["LED_on"] = "127"
		self.track_on_id_67["LED_off"] = "0"
		self.track_on_id_67["LED_send_feedback_to_selected"] = []
		self.track_on_id_67["json_id"] = 67
		self.track_on_id_67["mapping_name"] = "Track On"
		self.track_on_id_67["mapping_type"] = "Device"
		self.track_on_id_67["parent_json_id"] = 59
		self.track_on_id_67["parent_name"] = "strings_id_59"
		self.device_select___chain_1_id_68 = {}
		self.device_select___chain_1_id_68["track"] = self.track_num(2)
		self.device_select___chain_1_id_68["module"] = "self.song().tracks[self.track_num(3)].devices[1].chains[0].devices[0]"
		self.device_select___chain_1_id_68["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_1_id_68["LED_feedback"] = "custom"
		self.device_select___chain_1_id_68["LED_feedback_active"] = ""
		self.device_select___chain_1_id_68["LED_on"] = "127"
		self.device_select___chain_1_id_68["LED_off"] = "0"
		self.device_select___chain_1_id_68["LED_send_feedback_to_selected"] = []
		self.device_select___chain_1_id_68["json_id"] = 68
		self.device_select___chain_1_id_68["mapping_name"] = "Device Select  - Chain 1"
		self.device_select___chain_1_id_68["mapping_type"] = "Device"
		self.device_select___chain_1_id_68["parent_json_id"] = 59
		self.device_select___chain_1_id_68["parent_name"] = "strings_id_59"
		self.device_select___chain_2_id_69 = {}
		self.device_select___chain_2_id_69["track"] = self.track_num(2)
		self.device_select___chain_2_id_69["module"] = "self.song().tracks[self.track_num(3)].devices[1].chains[1].devices[0]"
		self.device_select___chain_2_id_69["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_2_id_69["LED_feedback"] = "custom"
		self.device_select___chain_2_id_69["LED_feedback_active"] = ""
		self.device_select___chain_2_id_69["LED_on"] = "127"
		self.device_select___chain_2_id_69["LED_off"] = "0"
		self.device_select___chain_2_id_69["LED_send_feedback_to_selected"] = []
		self.device_select___chain_2_id_69["json_id"] = 69
		self.device_select___chain_2_id_69["mapping_name"] = "Device Select  - Chain 2"
		self.device_select___chain_2_id_69["mapping_type"] = "Device"
		self.device_select___chain_2_id_69["parent_json_id"] = 59
		self.device_select___chain_2_id_69["parent_name"] = "strings_id_59"
		self.device_select___chain_3_id_70 = {}
		self.device_select___chain_3_id_70["track"] = self.track_num(2)
		self.device_select___chain_3_id_70["module"] = "self.song().tracks[self.track_num(3)].devices[1].chains[2].devices[0]"
		self.device_select___chain_3_id_70["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_3_id_70["LED_feedback"] = "custom"
		self.device_select___chain_3_id_70["LED_feedback_active"] = ""
		self.device_select___chain_3_id_70["LED_on"] = "127"
		self.device_select___chain_3_id_70["LED_off"] = "0"
		self.device_select___chain_3_id_70["LED_send_feedback_to_selected"] = []
		self.device_select___chain_3_id_70["json_id"] = 70
		self.device_select___chain_3_id_70["mapping_name"] = "Device Select  - Chain 3"
		self.device_select___chain_3_id_70["mapping_type"] = "Device"
		self.device_select___chain_3_id_70["parent_json_id"] = 59
		self.device_select___chain_3_id_70["parent_name"] = "strings_id_59"
		self.device_select___chain_4_id_71 = {}
		self.device_select___chain_4_id_71["track"] = self.track_num(2)
		self.device_select___chain_4_id_71["module"] = "self.song().tracks[self.track_num(3)].devices[1].chains[3].devices[0]"
		self.device_select___chain_4_id_71["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_4_id_71["LED_feedback"] = "custom"
		self.device_select___chain_4_id_71["LED_feedback_active"] = ""
		self.device_select___chain_4_id_71["LED_on"] = "127"
		self.device_select___chain_4_id_71["LED_off"] = "0"
		self.device_select___chain_4_id_71["LED_send_feedback_to_selected"] = []
		self.device_select___chain_4_id_71["json_id"] = 71
		self.device_select___chain_4_id_71["mapping_name"] = "Device Select  - Chain 4"
		self.device_select___chain_4_id_71["mapping_type"] = "Device"
		self.device_select___chain_4_id_71["parent_json_id"] = 59
		self.device_select___chain_4_id_71["parent_name"] = "strings_id_59"
		self.device_select___chain_5_id_72 = {}
		self.device_select___chain_5_id_72["track"] = self.track_num(2)
		self.device_select___chain_5_id_72["module"] = "self.song().tracks[self.track_num(3)].devices[1].chains[4].devices[0]"
		self.device_select___chain_5_id_72["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_5_id_72["LED_feedback"] = "custom"
		self.device_select___chain_5_id_72["LED_feedback_active"] = ""
		self.device_select___chain_5_id_72["LED_on"] = "127"
		self.device_select___chain_5_id_72["LED_off"] = "0"
		self.device_select___chain_5_id_72["LED_send_feedback_to_selected"] = []
		self.device_select___chain_5_id_72["json_id"] = 72
		self.device_select___chain_5_id_72["mapping_name"] = "Device Select  - Chain 5"
		self.device_select___chain_5_id_72["mapping_type"] = "Device"
		self.device_select___chain_5_id_72["parent_json_id"] = 59
		self.device_select___chain_5_id_72["parent_name"] = "strings_id_59"
		self.organlead_id_73 = {}
		self.organlead_id_73["track"] = self.track_num(2)
		self.organlead_id_73["module"] = "self.song().tracks[self.track_num(4)]"
		self.organlead_id_73["LED_mapping_type_needs_feedback"] = ""
		self.organlead_id_73["LED_feedback"] = "custom"
		self.organlead_id_73["LED_feedback_active"] = ""
		self.organlead_id_73["LED_on"] = "127"
		self.organlead_id_73["LED_off"] = "0"
		self.organlead_id_73["LED_send_feedback_to_selected"] = []
		self.organlead_id_73["json_id"] = 73
		self.organlead_id_73["mapping_name"] = "Organ/Lead"
		self.organlead_id_73["mapping_type"] = "Track"
		self.organlead_id_73["parent_json_id"] = 1
		self.organlead_id_73["parent_name"] = "main_id_1"
		self.power_id_74 = {}
		self.power_id_74["attached_to"] = "midi_note_ch_4_val_5"
		self.power_id_74["track"] = self.track_num(2)
		self.power_id_74["module"] = "self.song().tracks[self.track_num(4)].devices[0].parameters[0]"
		self.power_id_74["minimum"] = 0.0
		self.power_id_74["maximum"] = 1.0
		self.power_id_74["snap_to"] = 1
		self.power_id_74["element"] = "value"
		self.power_id_74["output_type"] = "val"
		self.power_id_74["ui_listener"] = "value"
		self.power_id_74["feedback_brain"] = "feedback_on_off"
		self.power_id_74["enc_first"] = 127
		self.power_id_74["enc_second"] = 0
		self.power_id_74["switch_type"] = "toggle"
		self.power_id_74["ctrl_type"] = "on/off"
		self.power_id_74["LED_mapping_type_needs_feedback"] = "1"
		self.power_id_74["LED_feedback"] = "default"
		self.power_id_74["LED_feedback_active"] = "1"
		self.power_id_74["LED_on"] = "127"
		self.power_id_74["LED_off"] = "0"
		self.power_id_74["LED_send_feedback_to_selected"] = ["midi_note_ch_4_val_5"]
		self.power_id_74["json_id"] = 74
		self.power_id_74["mapping_name"] = "Power"
		self.power_id_74["mapping_type"] = "On/Off"
		self.power_id_74["parent_json_id"] = 81
		self.power_id_74["parent_name"] = "track_on_id_81"
		self.select_device_id_75 = {}
		self.select_device_id_75["attached_to"] = "midi_note_ch_4_val_0"
		self.select_device_id_75["module"] = "self"
		self.select_device_id_75["element"] = "select_a_device"
		self.select_device_id_75["output_type"] = "func"
		self.select_device_id_75["func_arg"] = "cnfg"
		self.select_device_id_75["parent_track"] = "self.song().tracks[self.track_num(4)]"
		self.select_device_id_75["device_chain"] = ".devices[1].chains[0].devices[0]"
		self.select_device_id_75["ctrl_type"] = "on/off"
		self.select_device_id_75["enc_first"] = 127
		self.select_device_id_75["enc_second"] = 0
		self.select_device_id_75["switch_type"] = "momentary"
		self.select_device_id_75["json_id"] = 75
		self.select_device_id_75["mapping_name"] = "Select Device"
		self.select_device_id_75["mapping_type"] = "Select Device"
		self.select_device_id_75["parent_json_id"] = 82
		self.select_device_id_75["parent_name"] = "device_select___chain_1_id_82"
		self.select_device_id_76 = {}
		self.select_device_id_76["attached_to"] = "midi_note_ch_4_val_1"
		self.select_device_id_76["module"] = "self"
		self.select_device_id_76["element"] = "select_a_device"
		self.select_device_id_76["output_type"] = "func"
		self.select_device_id_76["func_arg"] = "cnfg"
		self.select_device_id_76["parent_track"] = "self.song().tracks[self.track_num(4)]"
		self.select_device_id_76["device_chain"] = ".devices[1].chains[1].devices[0]"
		self.select_device_id_76["ctrl_type"] = "on/off"
		self.select_device_id_76["enc_first"] = 127
		self.select_device_id_76["enc_second"] = 0
		self.select_device_id_76["switch_type"] = "momentary"
		self.select_device_id_76["json_id"] = 76
		self.select_device_id_76["mapping_name"] = "Select Device"
		self.select_device_id_76["mapping_type"] = "Select Device"
		self.select_device_id_76["parent_json_id"] = 83
		self.select_device_id_76["parent_name"] = "device_select___chain_2_id_83"
		self.select_device_id_77 = {}
		self.select_device_id_77["attached_to"] = "midi_note_ch_4_val_2"
		self.select_device_id_77["module"] = "self"
		self.select_device_id_77["element"] = "select_a_device"
		self.select_device_id_77["output_type"] = "func"
		self.select_device_id_77["func_arg"] = "cnfg"
		self.select_device_id_77["parent_track"] = "self.song().tracks[self.track_num(4)]"
		self.select_device_id_77["device_chain"] = ".devices[1].chains[2].devices[0]"
		self.select_device_id_77["ctrl_type"] = "on/off"
		self.select_device_id_77["enc_first"] = 127
		self.select_device_id_77["enc_second"] = 0
		self.select_device_id_77["switch_type"] = "momentary"
		self.select_device_id_77["json_id"] = 77
		self.select_device_id_77["mapping_name"] = "Select Device"
		self.select_device_id_77["mapping_type"] = "Select Device"
		self.select_device_id_77["parent_json_id"] = 84
		self.select_device_id_77["parent_name"] = "device_select___chain_3_id_84"
		self.select_device_id_78 = {}
		self.select_device_id_78["attached_to"] = "midi_note_ch_4_val_3"
		self.select_device_id_78["module"] = "self"
		self.select_device_id_78["element"] = "select_a_device"
		self.select_device_id_78["output_type"] = "func"
		self.select_device_id_78["func_arg"] = "cnfg"
		self.select_device_id_78["parent_track"] = "self.song().tracks[self.track_num(4)]"
		self.select_device_id_78["device_chain"] = ".devices[1].chains[3].devices[0]"
		self.select_device_id_78["ctrl_type"] = "on/off"
		self.select_device_id_78["enc_first"] = 127
		self.select_device_id_78["enc_second"] = 0
		self.select_device_id_78["switch_type"] = "momentary"
		self.select_device_id_78["json_id"] = 78
		self.select_device_id_78["mapping_name"] = "Select Device"
		self.select_device_id_78["mapping_type"] = "Select Device"
		self.select_device_id_78["parent_json_id"] = 85
		self.select_device_id_78["parent_name"] = "device_select___chain_4_id_85"
		self.select_device_id_79 = {}
		self.select_device_id_79["attached_to"] = "midi_note_ch_4_val_4"
		self.select_device_id_79["module"] = "self"
		self.select_device_id_79["element"] = "select_a_device"
		self.select_device_id_79["output_type"] = "func"
		self.select_device_id_79["func_arg"] = "cnfg"
		self.select_device_id_79["parent_track"] = "self.song().tracks[self.track_num(4)]"
		self.select_device_id_79["device_chain"] = ".devices[1].chains[4].devices[0]"
		self.select_device_id_79["ctrl_type"] = "on/off"
		self.select_device_id_79["enc_first"] = 127
		self.select_device_id_79["enc_second"] = 0
		self.select_device_id_79["switch_type"] = "momentary"
		self.select_device_id_79["json_id"] = 79
		self.select_device_id_79["mapping_name"] = "Select Device"
		self.select_device_id_79["mapping_type"] = "Select Device"
		self.select_device_id_79["parent_json_id"] = 86
		self.select_device_id_79["parent_name"] = "device_select___chain_5_id_86"
		self.volume_id_80 = {}
		self.volume_id_80["attached_to"] = "midi_cc_ch_4_val_7"
		self.volume_id_80["track"] = self.track_num(2)
		self.volume_id_80["module"] = "self.song().tracks[self.track_num(4)].mixer_device.volume"
		self.volume_id_80["element"] = "value"
		self.volume_id_80["output_type"] = "val"
		self.volume_id_80["minimum"] = round(0,2)
		self.volume_id_80["maximum"] = round(85,2)
		self.volume_id_80["decimal_places"] = 2
		self.volume_id_80["ui_listener"] = "value"
		self.volume_id_80["feedback_brain"] = "feedback_range"
		self.volume_id_80["ctrl_type"] = "absolute"
		self.volume_id_80["takeover_mode"] = "None"
		self.volume_id_80["enc_first"] = 0
		self.volume_id_80["enc_second"] = 127
		self.volume_id_80["reverse_mode"] = False
		self.volume_id_80["LED_mapping_type_needs_feedback"] = "1"
		self.volume_id_80["LED_feedback"] = "default"
		self.volume_id_80["LED_feedback_active"] = "1"
		self.volume_id_80["LED_on"] = "127"
		self.volume_id_80["LED_off"] = "0"
		self.volume_id_80["LED_send_feedback_to_selected"] = ["midi_cc_ch_4_val_7"]
		self.volume_id_80["snap_to"] = True
		self.volume_id_80["json_id"] = 80
		self.volume_id_80["mapping_name"] = "Volume"
		self.volume_id_80["mapping_type"] = "Volume"
		self.volume_id_80["parent_json_id"] = 73
		self.volume_id_80["parent_name"] = "organlead_id_73"
		self.track_on_id_81 = {}
		self.track_on_id_81["track"] = self.track_num(2)
		self.track_on_id_81["module"] = "self.song().tracks[self.track_num(4)].devices[0]"
		self.track_on_id_81["LED_mapping_type_needs_feedback"] = ""
		self.track_on_id_81["LED_feedback"] = "custom"
		self.track_on_id_81["LED_feedback_active"] = ""
		self.track_on_id_81["LED_on"] = "127"
		self.track_on_id_81["LED_off"] = "0"
		self.track_on_id_81["LED_send_feedback_to_selected"] = []
		self.track_on_id_81["json_id"] = 81
		self.track_on_id_81["mapping_name"] = "Track On"
		self.track_on_id_81["mapping_type"] = "Device"
		self.track_on_id_81["parent_json_id"] = 73
		self.track_on_id_81["parent_name"] = "organlead_id_73"
		self.device_select___chain_1_id_82 = {}
		self.device_select___chain_1_id_82["track"] = self.track_num(2)
		self.device_select___chain_1_id_82["module"] = "self.song().tracks[self.track_num(4)].devices[1].chains[0].devices[0]"
		self.device_select___chain_1_id_82["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_1_id_82["LED_feedback"] = "custom"
		self.device_select___chain_1_id_82["LED_feedback_active"] = ""
		self.device_select___chain_1_id_82["LED_on"] = "127"
		self.device_select___chain_1_id_82["LED_off"] = "0"
		self.device_select___chain_1_id_82["LED_send_feedback_to_selected"] = []
		self.device_select___chain_1_id_82["json_id"] = 82
		self.device_select___chain_1_id_82["mapping_name"] = "Device Select  - Chain 1"
		self.device_select___chain_1_id_82["mapping_type"] = "Device"
		self.device_select___chain_1_id_82["parent_json_id"] = 73
		self.device_select___chain_1_id_82["parent_name"] = "organlead_id_73"
		self.device_select___chain_2_id_83 = {}
		self.device_select___chain_2_id_83["track"] = self.track_num(2)
		self.device_select___chain_2_id_83["module"] = "self.song().tracks[self.track_num(4)].devices[1].chains[1].devices[0]"
		self.device_select___chain_2_id_83["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_2_id_83["LED_feedback"] = "custom"
		self.device_select___chain_2_id_83["LED_feedback_active"] = ""
		self.device_select___chain_2_id_83["LED_on"] = "127"
		self.device_select___chain_2_id_83["LED_off"] = "0"
		self.device_select___chain_2_id_83["LED_send_feedback_to_selected"] = []
		self.device_select___chain_2_id_83["json_id"] = 83
		self.device_select___chain_2_id_83["mapping_name"] = "Device Select  - Chain 2"
		self.device_select___chain_2_id_83["mapping_type"] = "Device"
		self.device_select___chain_2_id_83["parent_json_id"] = 73
		self.device_select___chain_2_id_83["parent_name"] = "organlead_id_73"
		self.device_select___chain_3_id_84 = {}
		self.device_select___chain_3_id_84["track"] = self.track_num(2)
		self.device_select___chain_3_id_84["module"] = "self.song().tracks[self.track_num(4)].devices[1].chains[2].devices[0]"
		self.device_select___chain_3_id_84["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_3_id_84["LED_feedback"] = "custom"
		self.device_select___chain_3_id_84["LED_feedback_active"] = ""
		self.device_select___chain_3_id_84["LED_on"] = "127"
		self.device_select___chain_3_id_84["LED_off"] = "0"
		self.device_select___chain_3_id_84["LED_send_feedback_to_selected"] = []
		self.device_select___chain_3_id_84["json_id"] = 84
		self.device_select___chain_3_id_84["mapping_name"] = "Device Select  - Chain 3"
		self.device_select___chain_3_id_84["mapping_type"] = "Device"
		self.device_select___chain_3_id_84["parent_json_id"] = 73
		self.device_select___chain_3_id_84["parent_name"] = "organlead_id_73"
		self.device_select___chain_4_id_85 = {}
		self.device_select___chain_4_id_85["track"] = self.track_num(2)
		self.device_select___chain_4_id_85["module"] = "self.song().tracks[self.track_num(4)].devices[1].chains[3].devices[0]"
		self.device_select___chain_4_id_85["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_4_id_85["LED_feedback"] = "custom"
		self.device_select___chain_4_id_85["LED_feedback_active"] = ""
		self.device_select___chain_4_id_85["LED_on"] = "127"
		self.device_select___chain_4_id_85["LED_off"] = "0"
		self.device_select___chain_4_id_85["LED_send_feedback_to_selected"] = []
		self.device_select___chain_4_id_85["json_id"] = 85
		self.device_select___chain_4_id_85["mapping_name"] = "Device Select  - Chain 4"
		self.device_select___chain_4_id_85["mapping_type"] = "Device"
		self.device_select___chain_4_id_85["parent_json_id"] = 73
		self.device_select___chain_4_id_85["parent_name"] = "organlead_id_73"
		self.device_select___chain_5_id_86 = {}
		self.device_select___chain_5_id_86["track"] = self.track_num(2)
		self.device_select___chain_5_id_86["module"] = "self.song().tracks[self.track_num(4)].devices[1].chains[4].devices[0]"
		self.device_select___chain_5_id_86["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_5_id_86["LED_feedback"] = "custom"
		self.device_select___chain_5_id_86["LED_feedback_active"] = ""
		self.device_select___chain_5_id_86["LED_on"] = "127"
		self.device_select___chain_5_id_86["LED_off"] = "0"
		self.device_select___chain_5_id_86["LED_send_feedback_to_selected"] = []
		self.device_select___chain_5_id_86["json_id"] = 86
		self.device_select___chain_5_id_86["mapping_name"] = "Device Select  - Chain 5"
		self.device_select___chain_5_id_86["mapping_type"] = "Device"
		self.device_select___chain_5_id_86["parent_json_id"] = 73
		self.device_select___chain_5_id_86["parent_name"] = "organlead_id_73"
		self.alternates_id_87 = {}
		self.alternates_id_87["track"] = self.track_num(2)
		self.alternates_id_87["module"] = "self.song().tracks[self.track_num(5)]"
		self.alternates_id_87["LED_mapping_type_needs_feedback"] = ""
		self.alternates_id_87["LED_feedback"] = "custom"
		self.alternates_id_87["LED_feedback_active"] = ""
		self.alternates_id_87["LED_on"] = "127"
		self.alternates_id_87["LED_off"] = "0"
		self.alternates_id_87["LED_send_feedback_to_selected"] = []
		self.alternates_id_87["json_id"] = 87
		self.alternates_id_87["mapping_name"] = "Alternates"
		self.alternates_id_87["mapping_type"] = "Track"
		self.alternates_id_87["parent_json_id"] = 1
		self.alternates_id_87["parent_name"] = "main_id_1"
		self.power_id_88 = {}
		self.power_id_88["attached_to"] = "midi_note_ch_5_val_5"
		self.power_id_88["track"] = self.track_num(2)
		self.power_id_88["module"] = "self.song().tracks[self.track_num(5)].devices[0].parameters[0]"
		self.power_id_88["minimum"] = 0.0
		self.power_id_88["maximum"] = 1.0
		self.power_id_88["snap_to"] = 1
		self.power_id_88["element"] = "value"
		self.power_id_88["output_type"] = "val"
		self.power_id_88["ui_listener"] = "value"
		self.power_id_88["feedback_brain"] = "feedback_on_off"
		self.power_id_88["enc_first"] = 127
		self.power_id_88["enc_second"] = 0
		self.power_id_88["switch_type"] = "toggle"
		self.power_id_88["ctrl_type"] = "on/off"
		self.power_id_88["LED_mapping_type_needs_feedback"] = "1"
		self.power_id_88["LED_feedback"] = "default"
		self.power_id_88["LED_feedback_active"] = "1"
		self.power_id_88["LED_on"] = "127"
		self.power_id_88["LED_off"] = "0"
		self.power_id_88["LED_send_feedback_to_selected"] = ["midi_note_ch_5_val_5"]
		self.power_id_88["json_id"] = 88
		self.power_id_88["mapping_name"] = "Power"
		self.power_id_88["mapping_type"] = "On/Off"
		self.power_id_88["parent_json_id"] = 95
		self.power_id_88["parent_name"] = "track_on_id_95"
		self.select_device_id_89 = {}
		self.select_device_id_89["attached_to"] = "midi_note_ch_5_val_0"
		self.select_device_id_89["module"] = "self"
		self.select_device_id_89["element"] = "select_a_device"
		self.select_device_id_89["output_type"] = "func"
		self.select_device_id_89["func_arg"] = "cnfg"
		self.select_device_id_89["parent_track"] = "self.song().tracks[self.track_num(5)]"
		self.select_device_id_89["device_chain"] = ".devices[1].chains[0].devices[0]"
		self.select_device_id_89["ctrl_type"] = "on/off"
		self.select_device_id_89["enc_first"] = 127
		self.select_device_id_89["enc_second"] = 0
		self.select_device_id_89["switch_type"] = "momentary"
		self.select_device_id_89["json_id"] = 89
		self.select_device_id_89["mapping_name"] = "Select Device"
		self.select_device_id_89["mapping_type"] = "Select Device"
		self.select_device_id_89["parent_json_id"] = 96
		self.select_device_id_89["parent_name"] = "device_select___chain_1_id_96"
		self.select_device_id_90 = {}
		self.select_device_id_90["attached_to"] = "midi_note_ch_5_val_1"
		self.select_device_id_90["module"] = "self"
		self.select_device_id_90["element"] = "select_a_device"
		self.select_device_id_90["output_type"] = "func"
		self.select_device_id_90["func_arg"] = "cnfg"
		self.select_device_id_90["parent_track"] = "self.song().tracks[self.track_num(5)]"
		self.select_device_id_90["device_chain"] = ".devices[1].chains[1].devices[0]"
		self.select_device_id_90["ctrl_type"] = "on/off"
		self.select_device_id_90["enc_first"] = 127
		self.select_device_id_90["enc_second"] = 0
		self.select_device_id_90["switch_type"] = "momentary"
		self.select_device_id_90["json_id"] = 90
		self.select_device_id_90["mapping_name"] = "Select Device"
		self.select_device_id_90["mapping_type"] = "Select Device"
		self.select_device_id_90["parent_json_id"] = 97
		self.select_device_id_90["parent_name"] = "device_select___chain_2_id_97"
		self.select_device_id_91 = {}
		self.select_device_id_91["attached_to"] = "midi_note_ch_5_val_2"
		self.select_device_id_91["module"] = "self"
		self.select_device_id_91["element"] = "select_a_device"
		self.select_device_id_91["output_type"] = "func"
		self.select_device_id_91["func_arg"] = "cnfg"
		self.select_device_id_91["parent_track"] = "self.song().tracks[self.track_num(5)]"
		self.select_device_id_91["device_chain"] = ".devices[1].chains[2].devices[0]"
		self.select_device_id_91["ctrl_type"] = "on/off"
		self.select_device_id_91["enc_first"] = 127
		self.select_device_id_91["enc_second"] = 0
		self.select_device_id_91["switch_type"] = "momentary"
		self.select_device_id_91["json_id"] = 91
		self.select_device_id_91["mapping_name"] = "Select Device"
		self.select_device_id_91["mapping_type"] = "Select Device"
		self.select_device_id_91["parent_json_id"] = 98
		self.select_device_id_91["parent_name"] = "device_select___chain_3_id_98"
		self.select_device_id_92 = {}
		self.select_device_id_92["attached_to"] = "midi_note_ch_5_val_3"
		self.select_device_id_92["module"] = "self"
		self.select_device_id_92["element"] = "select_a_device"
		self.select_device_id_92["output_type"] = "func"
		self.select_device_id_92["func_arg"] = "cnfg"
		self.select_device_id_92["parent_track"] = "self.song().tracks[self.track_num(5)]"
		self.select_device_id_92["device_chain"] = ".devices[1].chains[3].devices[0]"
		self.select_device_id_92["ctrl_type"] = "on/off"
		self.select_device_id_92["enc_first"] = 127
		self.select_device_id_92["enc_second"] = 0
		self.select_device_id_92["switch_type"] = "momentary"
		self.select_device_id_92["json_id"] = 92
		self.select_device_id_92["mapping_name"] = "Select Device"
		self.select_device_id_92["mapping_type"] = "Select Device"
		self.select_device_id_92["parent_json_id"] = 99
		self.select_device_id_92["parent_name"] = "device_select___chain_4_id_99"
		self.select_device_id_93 = {}
		self.select_device_id_93["attached_to"] = "midi_note_ch_5_val_4"
		self.select_device_id_93["module"] = "self"
		self.select_device_id_93["element"] = "select_a_device"
		self.select_device_id_93["output_type"] = "func"
		self.select_device_id_93["func_arg"] = "cnfg"
		self.select_device_id_93["parent_track"] = "self.song().tracks[self.track_num(5)]"
		self.select_device_id_93["device_chain"] = ".devices[1].chains[4].devices[0]"
		self.select_device_id_93["ctrl_type"] = "on/off"
		self.select_device_id_93["enc_first"] = 127
		self.select_device_id_93["enc_second"] = 0
		self.select_device_id_93["switch_type"] = "momentary"
		self.select_device_id_93["json_id"] = 93
		self.select_device_id_93["mapping_name"] = "Select Device"
		self.select_device_id_93["mapping_type"] = "Select Device"
		self.select_device_id_93["parent_json_id"] = 100
		self.select_device_id_93["parent_name"] = "device_select___chain_5_id_100"
		self.volume_id_94 = {}
		self.volume_id_94["attached_to"] = "midi_cc_ch_5_val_7"
		self.volume_id_94["track"] = self.track_num(2)
		self.volume_id_94["module"] = "self.song().tracks[self.track_num(5)].mixer_device.volume"
		self.volume_id_94["element"] = "value"
		self.volume_id_94["output_type"] = "val"
		self.volume_id_94["minimum"] = round(0,2)
		self.volume_id_94["maximum"] = round(85,2)
		self.volume_id_94["decimal_places"] = 2
		self.volume_id_94["ui_listener"] = "value"
		self.volume_id_94["feedback_brain"] = "feedback_range"
		self.volume_id_94["ctrl_type"] = "absolute"
		self.volume_id_94["takeover_mode"] = "None"
		self.volume_id_94["enc_first"] = 0
		self.volume_id_94["enc_second"] = 127
		self.volume_id_94["reverse_mode"] = False
		self.volume_id_94["LED_mapping_type_needs_feedback"] = "1"
		self.volume_id_94["LED_feedback"] = "default"
		self.volume_id_94["LED_feedback_active"] = "1"
		self.volume_id_94["LED_on"] = "127"
		self.volume_id_94["LED_off"] = "0"
		self.volume_id_94["LED_send_feedback_to_selected"] = ["midi_cc_ch_5_val_7"]
		self.volume_id_94["snap_to"] = True
		self.volume_id_94["json_id"] = 94
		self.volume_id_94["mapping_name"] = "Volume"
		self.volume_id_94["mapping_type"] = "Volume"
		self.volume_id_94["parent_json_id"] = 87
		self.volume_id_94["parent_name"] = "alternates_id_87"
		self.track_on_id_95 = {}
		self.track_on_id_95["track"] = self.track_num(2)
		self.track_on_id_95["module"] = "self.song().tracks[self.track_num(5)].devices[0]"
		self.track_on_id_95["LED_mapping_type_needs_feedback"] = ""
		self.track_on_id_95["LED_feedback"] = "custom"
		self.track_on_id_95["LED_feedback_active"] = ""
		self.track_on_id_95["LED_on"] = "127"
		self.track_on_id_95["LED_off"] = "0"
		self.track_on_id_95["LED_send_feedback_to_selected"] = []
		self.track_on_id_95["json_id"] = 95
		self.track_on_id_95["mapping_name"] = "Track On"
		self.track_on_id_95["mapping_type"] = "Device"
		self.track_on_id_95["parent_json_id"] = 87
		self.track_on_id_95["parent_name"] = "alternates_id_87"
		self.device_select___chain_1_id_96 = {}
		self.device_select___chain_1_id_96["track"] = self.track_num(2)
		self.device_select___chain_1_id_96["module"] = "self.song().tracks[self.track_num(5)].devices[1].chains[0].devices[0]"
		self.device_select___chain_1_id_96["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_1_id_96["LED_feedback"] = "custom"
		self.device_select___chain_1_id_96["LED_feedback_active"] = ""
		self.device_select___chain_1_id_96["LED_on"] = "127"
		self.device_select___chain_1_id_96["LED_off"] = "0"
		self.device_select___chain_1_id_96["LED_send_feedback_to_selected"] = []
		self.device_select___chain_1_id_96["json_id"] = 96
		self.device_select___chain_1_id_96["mapping_name"] = "Device Select  - Chain 1"
		self.device_select___chain_1_id_96["mapping_type"] = "Device"
		self.device_select___chain_1_id_96["parent_json_id"] = 87
		self.device_select___chain_1_id_96["parent_name"] = "alternates_id_87"
		self.device_select___chain_2_id_97 = {}
		self.device_select___chain_2_id_97["track"] = self.track_num(2)
		self.device_select___chain_2_id_97["module"] = "self.song().tracks[self.track_num(5)].devices[1].chains[1].devices[0]"
		self.device_select___chain_2_id_97["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_2_id_97["LED_feedback"] = "custom"
		self.device_select___chain_2_id_97["LED_feedback_active"] = ""
		self.device_select___chain_2_id_97["LED_on"] = "127"
		self.device_select___chain_2_id_97["LED_off"] = "0"
		self.device_select___chain_2_id_97["LED_send_feedback_to_selected"] = []
		self.device_select___chain_2_id_97["json_id"] = 97
		self.device_select___chain_2_id_97["mapping_name"] = "Device Select  - Chain 2"
		self.device_select___chain_2_id_97["mapping_type"] = "Device"
		self.device_select___chain_2_id_97["parent_json_id"] = 87
		self.device_select___chain_2_id_97["parent_name"] = "alternates_id_87"
		self.device_select___chain_3_id_98 = {}
		self.device_select___chain_3_id_98["track"] = self.track_num(2)
		self.device_select___chain_3_id_98["module"] = "self.song().tracks[self.track_num(5)].devices[1].chains[2].devices[0]"
		self.device_select___chain_3_id_98["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_3_id_98["LED_feedback"] = "custom"
		self.device_select___chain_3_id_98["LED_feedback_active"] = ""
		self.device_select___chain_3_id_98["LED_on"] = "127"
		self.device_select___chain_3_id_98["LED_off"] = "0"
		self.device_select___chain_3_id_98["LED_send_feedback_to_selected"] = []
		self.device_select___chain_3_id_98["json_id"] = 98
		self.device_select___chain_3_id_98["mapping_name"] = "Device Select  - Chain 3"
		self.device_select___chain_3_id_98["mapping_type"] = "Device"
		self.device_select___chain_3_id_98["parent_json_id"] = 87
		self.device_select___chain_3_id_98["parent_name"] = "alternates_id_87"
		self.device_select___chain_4_id_99 = {}
		self.device_select___chain_4_id_99["track"] = self.track_num(2)
		self.device_select___chain_4_id_99["module"] = "self.song().tracks[self.track_num(5)].devices[1].chains[3].devices[0]"
		self.device_select___chain_4_id_99["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_4_id_99["LED_feedback"] = "custom"
		self.device_select___chain_4_id_99["LED_feedback_active"] = ""
		self.device_select___chain_4_id_99["LED_on"] = "127"
		self.device_select___chain_4_id_99["LED_off"] = "0"
		self.device_select___chain_4_id_99["LED_send_feedback_to_selected"] = []
		self.device_select___chain_4_id_99["json_id"] = 99
		self.device_select___chain_4_id_99["mapping_name"] = "Device Select  - Chain 4"
		self.device_select___chain_4_id_99["mapping_type"] = "Device"
		self.device_select___chain_4_id_99["parent_json_id"] = 87
		self.device_select___chain_4_id_99["parent_name"] = "alternates_id_87"
		self.device_select___chain_5_id_100 = {}
		self.device_select___chain_5_id_100["track"] = self.track_num(2)
		self.device_select___chain_5_id_100["module"] = "self.song().tracks[self.track_num(5)].devices[1].chains[4].devices[0]"
		self.device_select___chain_5_id_100["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_5_id_100["LED_feedback"] = "custom"
		self.device_select___chain_5_id_100["LED_feedback_active"] = ""
		self.device_select___chain_5_id_100["LED_on"] = "127"
		self.device_select___chain_5_id_100["LED_off"] = "0"
		self.device_select___chain_5_id_100["LED_send_feedback_to_selected"] = []
		self.device_select___chain_5_id_100["json_id"] = 100
		self.device_select___chain_5_id_100["mapping_name"] = "Device Select  - Chain 5"
		self.device_select___chain_5_id_100["mapping_type"] = "Device"
		self.device_select___chain_5_id_100["parent_json_id"] = 87
		self.device_select___chain_5_id_100["parent_name"] = "alternates_id_87"
		self.split_id_101 = {}
		self.split_id_101["track"] = self.track_num(2)
		self.split_id_101["module"] = "self.song().tracks[self.track_num(6)]"
		self.split_id_101["LED_mapping_type_needs_feedback"] = ""
		self.split_id_101["LED_feedback"] = "custom"
		self.split_id_101["LED_feedback_active"] = ""
		self.split_id_101["LED_on"] = "127"
		self.split_id_101["LED_off"] = "0"
		self.split_id_101["LED_send_feedback_to_selected"] = []
		self.split_id_101["json_id"] = 101
		self.split_id_101["mapping_name"] = "Split"
		self.split_id_101["mapping_type"] = "Track"
		self.split_id_101["parent_json_id"] = 1
		self.split_id_101["parent_name"] = "main_id_1"
		self.select_device_id_103 = {}
		self.select_device_id_103["attached_to"] = "midi_note_ch_6_val_0"
		self.select_device_id_103["module"] = "self"
		self.select_device_id_103["element"] = "select_a_device"
		self.select_device_id_103["output_type"] = "func"
		self.select_device_id_103["func_arg"] = "cnfg"
		self.select_device_id_103["parent_track"] = "self.song().tracks[self.track_num(6)]"
		self.select_device_id_103["device_chain"] = ".devices[1].chains[0].devices[0]"
		self.select_device_id_103["ctrl_type"] = "on/off"
		self.select_device_id_103["enc_first"] = 127
		self.select_device_id_103["enc_second"] = 0
		self.select_device_id_103["switch_type"] = "momentary"
		self.select_device_id_103["json_id"] = 103
		self.select_device_id_103["mapping_name"] = "Select Device"
		self.select_device_id_103["mapping_type"] = "Select Device"
		self.select_device_id_103["parent_json_id"] = 110
		self.select_device_id_103["parent_name"] = "device_select___chain_1_id_110"
		self.select_device_id_104 = {}
		self.select_device_id_104["attached_to"] = "midi_note_ch_6_val_1"
		self.select_device_id_104["module"] = "self"
		self.select_device_id_104["element"] = "select_a_device"
		self.select_device_id_104["output_type"] = "func"
		self.select_device_id_104["func_arg"] = "cnfg"
		self.select_device_id_104["parent_track"] = "self.song().tracks[self.track_num(6)]"
		self.select_device_id_104["device_chain"] = ".devices[1].chains[1].devices[0]"
		self.select_device_id_104["ctrl_type"] = "on/off"
		self.select_device_id_104["enc_first"] = 127
		self.select_device_id_104["enc_second"] = 0
		self.select_device_id_104["switch_type"] = "momentary"
		self.select_device_id_104["json_id"] = 104
		self.select_device_id_104["mapping_name"] = "Select Device"
		self.select_device_id_104["mapping_type"] = "Select Device"
		self.select_device_id_104["parent_json_id"] = 111
		self.select_device_id_104["parent_name"] = "device_select___chain_2_id_111"
		self.select_device_id_105 = {}
		self.select_device_id_105["attached_to"] = "midi_note_ch_6_val_2"
		self.select_device_id_105["module"] = "self"
		self.select_device_id_105["element"] = "select_a_device"
		self.select_device_id_105["output_type"] = "func"
		self.select_device_id_105["func_arg"] = "cnfg"
		self.select_device_id_105["parent_track"] = "self.song().tracks[self.track_num(6)]"
		self.select_device_id_105["device_chain"] = ".devices[1].chains[2].devices[0]"
		self.select_device_id_105["ctrl_type"] = "on/off"
		self.select_device_id_105["enc_first"] = 127
		self.select_device_id_105["enc_second"] = 0
		self.select_device_id_105["switch_type"] = "momentary"
		self.select_device_id_105["json_id"] = 105
		self.select_device_id_105["mapping_name"] = "Select Device"
		self.select_device_id_105["mapping_type"] = "Select Device"
		self.select_device_id_105["parent_json_id"] = 112
		self.select_device_id_105["parent_name"] = "device_select___chain_3_id_112"
		self.select_device_id_106 = {}
		self.select_device_id_106["attached_to"] = "midi_note_ch_6_val_3"
		self.select_device_id_106["module"] = "self"
		self.select_device_id_106["element"] = "select_a_device"
		self.select_device_id_106["output_type"] = "func"
		self.select_device_id_106["func_arg"] = "cnfg"
		self.select_device_id_106["parent_track"] = "self.song().tracks[self.track_num(6)]"
		self.select_device_id_106["device_chain"] = ".devices[1].chains[3].devices[0]"
		self.select_device_id_106["ctrl_type"] = "on/off"
		self.select_device_id_106["enc_first"] = 127
		self.select_device_id_106["enc_second"] = 0
		self.select_device_id_106["switch_type"] = "momentary"
		self.select_device_id_106["json_id"] = 106
		self.select_device_id_106["mapping_name"] = "Select Device"
		self.select_device_id_106["mapping_type"] = "Select Device"
		self.select_device_id_106["parent_json_id"] = 113
		self.select_device_id_106["parent_name"] = "device_select___chain_4_id_113"
		self.select_device_id_107 = {}
		self.select_device_id_107["attached_to"] = "midi_note_ch_6_val_4"
		self.select_device_id_107["module"] = "self"
		self.select_device_id_107["element"] = "select_a_device"
		self.select_device_id_107["output_type"] = "func"
		self.select_device_id_107["func_arg"] = "cnfg"
		self.select_device_id_107["parent_track"] = "self.song().tracks[self.track_num(6)]"
		self.select_device_id_107["device_chain"] = ".devices[1].chains[4].devices[0]"
		self.select_device_id_107["ctrl_type"] = "on/off"
		self.select_device_id_107["enc_first"] = 127
		self.select_device_id_107["enc_second"] = 0
		self.select_device_id_107["switch_type"] = "momentary"
		self.select_device_id_107["json_id"] = 107
		self.select_device_id_107["mapping_name"] = "Select Device"
		self.select_device_id_107["mapping_type"] = "Select Device"
		self.select_device_id_107["parent_json_id"] = 114
		self.select_device_id_107["parent_name"] = "device_select___chain_5_id_114"
		self.volume_id_108 = {}
		self.volume_id_108["attached_to"] = "midi_cc_ch_6_val_7"
		self.volume_id_108["track"] = self.track_num(2)
		self.volume_id_108["module"] = "self.song().tracks[self.track_num(6)].mixer_device.volume"
		self.volume_id_108["element"] = "value"
		self.volume_id_108["output_type"] = "val"
		self.volume_id_108["minimum"] = round(0,2)
		self.volume_id_108["maximum"] = round(85,2)
		self.volume_id_108["decimal_places"] = 2
		self.volume_id_108["ui_listener"] = "value"
		self.volume_id_108["feedback_brain"] = "feedback_range"
		self.volume_id_108["ctrl_type"] = "absolute"
		self.volume_id_108["takeover_mode"] = "None"
		self.volume_id_108["enc_first"] = 0
		self.volume_id_108["enc_second"] = 127
		self.volume_id_108["reverse_mode"] = False
		self.volume_id_108["LED_mapping_type_needs_feedback"] = "1"
		self.volume_id_108["LED_feedback"] = "default"
		self.volume_id_108["LED_feedback_active"] = "1"
		self.volume_id_108["LED_on"] = "127"
		self.volume_id_108["LED_off"] = "0"
		self.volume_id_108["LED_send_feedback_to_selected"] = ["midi_cc_ch_6_val_7"]
		self.volume_id_108["snap_to"] = True
		self.volume_id_108["json_id"] = 108
		self.volume_id_108["mapping_name"] = "Volume"
		self.volume_id_108["mapping_type"] = "Volume"
		self.volume_id_108["parent_json_id"] = 101
		self.volume_id_108["parent_name"] = "split_id_101"
		self.device_select___chain_1_id_110 = {}
		self.device_select___chain_1_id_110["track"] = self.track_num(2)
		self.device_select___chain_1_id_110["module"] = "self.song().tracks[self.track_num(6)].devices[1].chains[0].devices[0]"
		self.device_select___chain_1_id_110["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_1_id_110["LED_feedback"] = "custom"
		self.device_select___chain_1_id_110["LED_feedback_active"] = ""
		self.device_select___chain_1_id_110["LED_on"] = "127"
		self.device_select___chain_1_id_110["LED_off"] = "0"
		self.device_select___chain_1_id_110["LED_send_feedback_to_selected"] = []
		self.device_select___chain_1_id_110["json_id"] = 110
		self.device_select___chain_1_id_110["mapping_name"] = "Device Select  - Chain 1"
		self.device_select___chain_1_id_110["mapping_type"] = "Device"
		self.device_select___chain_1_id_110["parent_json_id"] = 101
		self.device_select___chain_1_id_110["parent_name"] = "split_id_101"
		self.device_select___chain_2_id_111 = {}
		self.device_select___chain_2_id_111["track"] = self.track_num(2)
		self.device_select___chain_2_id_111["module"] = "self.song().tracks[self.track_num(6)].devices[1].chains[1].devices[0]"
		self.device_select___chain_2_id_111["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_2_id_111["LED_feedback"] = "custom"
		self.device_select___chain_2_id_111["LED_feedback_active"] = ""
		self.device_select___chain_2_id_111["LED_on"] = "127"
		self.device_select___chain_2_id_111["LED_off"] = "0"
		self.device_select___chain_2_id_111["LED_send_feedback_to_selected"] = []
		self.device_select___chain_2_id_111["json_id"] = 111
		self.device_select___chain_2_id_111["mapping_name"] = "Device Select  - Chain 2"
		self.device_select___chain_2_id_111["mapping_type"] = "Device"
		self.device_select___chain_2_id_111["parent_json_id"] = 101
		self.device_select___chain_2_id_111["parent_name"] = "split_id_101"
		self.device_select___chain_3_id_112 = {}
		self.device_select___chain_3_id_112["track"] = self.track_num(2)
		self.device_select___chain_3_id_112["module"] = "self.song().tracks[self.track_num(6)].devices[1].chains[2].devices[0]"
		self.device_select___chain_3_id_112["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_3_id_112["LED_feedback"] = "custom"
		self.device_select___chain_3_id_112["LED_feedback_active"] = ""
		self.device_select___chain_3_id_112["LED_on"] = "127"
		self.device_select___chain_3_id_112["LED_off"] = "0"
		self.device_select___chain_3_id_112["LED_send_feedback_to_selected"] = []
		self.device_select___chain_3_id_112["json_id"] = 112
		self.device_select___chain_3_id_112["mapping_name"] = "Device Select  - Chain 3"
		self.device_select___chain_3_id_112["mapping_type"] = "Device"
		self.device_select___chain_3_id_112["parent_json_id"] = 101
		self.device_select___chain_3_id_112["parent_name"] = "split_id_101"
		self.device_select___chain_4_id_113 = {}
		self.device_select___chain_4_id_113["track"] = self.track_num(2)
		self.device_select___chain_4_id_113["module"] = "self.song().tracks[self.track_num(6)].devices[1].chains[3].devices[0]"
		self.device_select___chain_4_id_113["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_4_id_113["LED_feedback"] = "custom"
		self.device_select___chain_4_id_113["LED_feedback_active"] = ""
		self.device_select___chain_4_id_113["LED_on"] = "127"
		self.device_select___chain_4_id_113["LED_off"] = "0"
		self.device_select___chain_4_id_113["LED_send_feedback_to_selected"] = []
		self.device_select___chain_4_id_113["json_id"] = 113
		self.device_select___chain_4_id_113["mapping_name"] = "Device Select  - Chain 4"
		self.device_select___chain_4_id_113["mapping_type"] = "Device"
		self.device_select___chain_4_id_113["parent_json_id"] = 101
		self.device_select___chain_4_id_113["parent_name"] = "split_id_101"
		self.device_select___chain_5_id_114 = {}
		self.device_select___chain_5_id_114["track"] = self.track_num(2)
		self.device_select___chain_5_id_114["module"] = "self.song().tracks[self.track_num(6)].devices[1].chains[4].devices[0]"
		self.device_select___chain_5_id_114["LED_mapping_type_needs_feedback"] = ""
		self.device_select___chain_5_id_114["LED_feedback"] = "custom"
		self.device_select___chain_5_id_114["LED_feedback_active"] = ""
		self.device_select___chain_5_id_114["LED_on"] = "127"
		self.device_select___chain_5_id_114["LED_off"] = "0"
		self.device_select___chain_5_id_114["LED_send_feedback_to_selected"] = []
		self.device_select___chain_5_id_114["json_id"] = 114
		self.device_select___chain_5_id_114["mapping_name"] = "Device Select  - Chain 5"
		self.device_select___chain_5_id_114["mapping_type"] = "Device"
		self.device_select___chain_5_id_114["parent_json_id"] = 101
		self.device_select___chain_5_id_114["parent_name"] = "split_id_101"
		self.master_track_id_115 = {}
		self.master_track_id_115["track"] = self.track_num(2)
		self.master_track_id_115["module"] = "self.song().master_track"
		self.master_track_id_115["LED_mapping_type_needs_feedback"] = ""
		self.master_track_id_115["LED_feedback"] = "custom"
		self.master_track_id_115["LED_feedback_active"] = ""
		self.master_track_id_115["LED_on"] = "127"
		self.master_track_id_115["LED_off"] = "0"
		self.master_track_id_115["LED_send_feedback_to_selected"] = []
		self.master_track_id_115["json_id"] = 115
		self.master_track_id_115["mapping_name"] = "Master Track"
		self.master_track_id_115["mapping_type"] = "Track"
		self.master_track_id_115["parent_json_id"] = 1
		self.master_track_id_115["parent_name"] = "main_id_1"
		self.volume_8_id_116 = {}
		self.volume_8_id_116["attached_to"] = "midi_cc_ch_15_val_7"
		self.volume_8_id_116["track"] = self.track_num(2)
		self.volume_8_id_116["module"] = "self.song().master_track.mixer_device.volume"
		self.volume_8_id_116["element"] = "value"
		self.volume_8_id_116["output_type"] = "val"
		self.volume_8_id_116["minimum"] = round(0,2)
		self.volume_8_id_116["maximum"] = round(85,2)
		self.volume_8_id_116["decimal_places"] = 2
		self.volume_8_id_116["ui_listener"] = "value"
		self.volume_8_id_116["feedback_brain"] = "feedback_range"
		self.volume_8_id_116["ctrl_type"] = "absolute"
		self.volume_8_id_116["takeover_mode"] = "None"
		self.volume_8_id_116["enc_first"] = 0
		self.volume_8_id_116["enc_second"] = 127
		self.volume_8_id_116["reverse_mode"] = False
		self.volume_8_id_116["LED_mapping_type_needs_feedback"] = "1"
		self.volume_8_id_116["LED_feedback"] = "default"
		self.volume_8_id_116["LED_feedback_active"] = "1"
		self.volume_8_id_116["LED_on"] = "127"
		self.volume_8_id_116["LED_off"] = "0"
		self.volume_8_id_116["LED_send_feedback_to_selected"] = ["midi_cc_ch_15_val_7"]
		self.volume_8_id_116["snap_to"] = True
		self.volume_8_id_116["json_id"] = 116
		self.volume_8_id_116["mapping_name"] = "Volume 8"
		self.volume_8_id_116["mapping_type"] = "Volume"
		self.volume_8_id_116["parent_json_id"] = 115
		self.volume_8_id_116["parent_name"] = "master_track_id_115"
		self.selected_track_id_117 = {}
		self.selected_track_id_117["track"] = self.track_num(2)
		self.selected_track_id_117["module"] = "self.song().view.selected_track"
		self.selected_track_id_117["LED_mapping_type_needs_feedback"] = ""
		self.selected_track_id_117["LED_feedback"] = "custom"
		self.selected_track_id_117["LED_feedback_active"] = ""
		self.selected_track_id_117["LED_on"] = "127"
		self.selected_track_id_117["LED_off"] = "0"
		self.selected_track_id_117["LED_send_feedback_to_selected"] = []
		self.selected_track_id_117["json_id"] = 117
		self.selected_track_id_117["mapping_name"] = "Selected Track"
		self.selected_track_id_117["mapping_type"] = "Track"
		self.selected_track_id_117["parent_json_id"] = 1
		self.selected_track_id_117["parent_name"] = "main_id_1"
		self.selected_device_id_118 = {}
		self.selected_device_id_118["track"] = self.track_num(2)
		self.selected_device_id_118["module"] = "self.song().view.selected_track.view.selected_device"
		self.selected_device_id_118["LED_mapping_type_needs_feedback"] = ""
		self.selected_device_id_118["LED_feedback"] = "custom"
		self.selected_device_id_118["LED_feedback_active"] = ""
		self.selected_device_id_118["LED_on"] = "127"
		self.selected_device_id_118["LED_off"] = "0"
		self.selected_device_id_118["LED_send_feedback_to_selected"] = []
		self.selected_device_id_118["json_id"] = 118
		self.selected_device_id_118["mapping_name"] = "Selected Device"
		self.selected_device_id_118["mapping_type"] = "Device"
		self.selected_device_id_118["parent_json_id"] = 117
		self.selected_device_id_118["parent_name"] = "selected_track_id_117"
		self.parameter_bank_1_id_119 = {}
		self.parameter_bank_1_id_119["LED_mapping_type_needs_feedback"] = ""
		self.parameter_bank_1_id_119["LED_feedback"] = "custom"
		self.parameter_bank_1_id_119["LED_feedback_active"] = ""
		self.parameter_bank_1_id_119["LED_on"] = "127"
		self.parameter_bank_1_id_119["LED_off"] = "0"
		self.parameter_bank_1_id_119["LED_send_feedback_to_selected"] = []
		self.parameter_bank_1_id_119["json_id"] = 119
		self.parameter_bank_1_id_119["mapping_name"] = "Parameter Bank 1"
		self.parameter_bank_1_id_119["mapping_type"] = "Parameter Bank"
		self.parameter_bank_1_id_119["parent_json_id"] = 118
		self.parameter_bank_1_id_119["parent_name"] = "selected_device_id_118"
		self.parameter_1_id_120 = {}
		self.parameter_1_id_120["attached_to"] = "midi_cc_ch_0_val_16"
		self.parameter_1_id_120["track"] = self.track_num(2)
		self.parameter_1_id_120["module"] = "self.song().view.selected_track.view.selected_device.parameters[1]"
		self.parameter_1_id_120["element"] = "value"
		self.parameter_1_id_120["output_type"] = "val"
		self.parameter_1_id_120["minimum"] = round(0,2)
		self.parameter_1_id_120["maximum"] = round(100,2)
		self.parameter_1_id_120["decimal_places"] = 2
		self.parameter_1_id_120["ui_listener"] = "value"
		self.parameter_1_id_120["feedback_brain"] = "feedback_range"
		self.parameter_1_id_120["ctrl_type"] = "absolute"
		self.parameter_1_id_120["takeover_mode"] = "None"
		self.parameter_1_id_120["enc_first"] = 0
		self.parameter_1_id_120["enc_second"] = 127
		self.parameter_1_id_120["reverse_mode"] = False
		self.parameter_1_id_120["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_1_id_120["LED_feedback"] = "default"
		self.parameter_1_id_120["LED_feedback_active"] = "1"
		self.parameter_1_id_120["LED_on"] = "127"
		self.parameter_1_id_120["LED_off"] = "0"
		self.parameter_1_id_120["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_16"]
		self.parameter_1_id_120["snap_to"] = True
		self.parameter_1_id_120["json_id"] = 120
		self.parameter_1_id_120["mapping_name"] = "Parameter 1"
		self.parameter_1_id_120["mapping_type"] = "Parameter"
		self.parameter_1_id_120["parent_json_id"] = 119
		self.parameter_1_id_120["parent_name"] = "parameter_bank_1_id_119"
		self.parameter_2_id_121 = {}
		self.parameter_2_id_121["attached_to"] = "midi_cc_ch_0_val_17"
		self.parameter_2_id_121["track"] = self.track_num(2)
		self.parameter_2_id_121["module"] = "self.song().view.selected_track.view.selected_device.parameters[2]"
		self.parameter_2_id_121["element"] = "value"
		self.parameter_2_id_121["output_type"] = "val"
		self.parameter_2_id_121["minimum"] = round(0,2)
		self.parameter_2_id_121["maximum"] = round(100,2)
		self.parameter_2_id_121["decimal_places"] = 2
		self.parameter_2_id_121["ui_listener"] = "value"
		self.parameter_2_id_121["feedback_brain"] = "feedback_range"
		self.parameter_2_id_121["ctrl_type"] = "absolute"
		self.parameter_2_id_121["takeover_mode"] = "None"
		self.parameter_2_id_121["enc_first"] = 0
		self.parameter_2_id_121["enc_second"] = 127
		self.parameter_2_id_121["reverse_mode"] = False
		self.parameter_2_id_121["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_2_id_121["LED_feedback"] = "default"
		self.parameter_2_id_121["LED_feedback_active"] = "1"
		self.parameter_2_id_121["LED_on"] = "127"
		self.parameter_2_id_121["LED_off"] = "0"
		self.parameter_2_id_121["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_17"]
		self.parameter_2_id_121["snap_to"] = True
		self.parameter_2_id_121["json_id"] = 121
		self.parameter_2_id_121["mapping_name"] = "Parameter 2"
		self.parameter_2_id_121["mapping_type"] = "Parameter"
		self.parameter_2_id_121["parent_json_id"] = 119
		self.parameter_2_id_121["parent_name"] = "parameter_bank_1_id_119"
		self.parameter_3_id_122 = {}
		self.parameter_3_id_122["attached_to"] = "midi_cc_ch_0_val_18"
		self.parameter_3_id_122["track"] = self.track_num(2)
		self.parameter_3_id_122["module"] = "self.song().view.selected_track.view.selected_device.parameters[3]"
		self.parameter_3_id_122["element"] = "value"
		self.parameter_3_id_122["output_type"] = "val"
		self.parameter_3_id_122["minimum"] = round(0,2)
		self.parameter_3_id_122["maximum"] = round(100,2)
		self.parameter_3_id_122["decimal_places"] = 2
		self.parameter_3_id_122["ui_listener"] = "value"
		self.parameter_3_id_122["feedback_brain"] = "feedback_range"
		self.parameter_3_id_122["ctrl_type"] = "absolute"
		self.parameter_3_id_122["takeover_mode"] = "None"
		self.parameter_3_id_122["enc_first"] = 0
		self.parameter_3_id_122["enc_second"] = 127
		self.parameter_3_id_122["reverse_mode"] = False
		self.parameter_3_id_122["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_3_id_122["LED_feedback"] = "default"
		self.parameter_3_id_122["LED_feedback_active"] = "1"
		self.parameter_3_id_122["LED_on"] = "127"
		self.parameter_3_id_122["LED_off"] = "0"
		self.parameter_3_id_122["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_18"]
		self.parameter_3_id_122["snap_to"] = True
		self.parameter_3_id_122["json_id"] = 122
		self.parameter_3_id_122["mapping_name"] = "Parameter 3"
		self.parameter_3_id_122["mapping_type"] = "Parameter"
		self.parameter_3_id_122["parent_json_id"] = 119
		self.parameter_3_id_122["parent_name"] = "parameter_bank_1_id_119"
		self.parameter_4_id_123 = {}
		self.parameter_4_id_123["attached_to"] = "midi_cc_ch_0_val_19"
		self.parameter_4_id_123["track"] = self.track_num(2)
		self.parameter_4_id_123["module"] = "self.song().view.selected_track.view.selected_device.parameters[4]"
		self.parameter_4_id_123["element"] = "value"
		self.parameter_4_id_123["output_type"] = "val"
		self.parameter_4_id_123["minimum"] = round(0,2)
		self.parameter_4_id_123["maximum"] = round(100,2)
		self.parameter_4_id_123["decimal_places"] = 2
		self.parameter_4_id_123["ui_listener"] = "value"
		self.parameter_4_id_123["feedback_brain"] = "feedback_range"
		self.parameter_4_id_123["ctrl_type"] = "absolute"
		self.parameter_4_id_123["takeover_mode"] = "None"
		self.parameter_4_id_123["enc_first"] = 0
		self.parameter_4_id_123["enc_second"] = 127
		self.parameter_4_id_123["reverse_mode"] = False
		self.parameter_4_id_123["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_4_id_123["LED_feedback"] = "default"
		self.parameter_4_id_123["LED_feedback_active"] = "1"
		self.parameter_4_id_123["LED_on"] = "127"
		self.parameter_4_id_123["LED_off"] = "0"
		self.parameter_4_id_123["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_19"]
		self.parameter_4_id_123["snap_to"] = True
		self.parameter_4_id_123["json_id"] = 123
		self.parameter_4_id_123["mapping_name"] = "Parameter 4"
		self.parameter_4_id_123["mapping_type"] = "Parameter"
		self.parameter_4_id_123["parent_json_id"] = 119
		self.parameter_4_id_123["parent_name"] = "parameter_bank_1_id_119"
		self.parameter_5_id_124 = {}
		self.parameter_5_id_124["attached_to"] = "midi_cc_ch_0_val_20"
		self.parameter_5_id_124["track"] = self.track_num(2)
		self.parameter_5_id_124["module"] = "self.song().view.selected_track.view.selected_device.parameters[5]"
		self.parameter_5_id_124["element"] = "value"
		self.parameter_5_id_124["output_type"] = "val"
		self.parameter_5_id_124["minimum"] = round(0,2)
		self.parameter_5_id_124["maximum"] = round(100,2)
		self.parameter_5_id_124["decimal_places"] = 2
		self.parameter_5_id_124["ui_listener"] = "value"
		self.parameter_5_id_124["feedback_brain"] = "feedback_range"
		self.parameter_5_id_124["ctrl_type"] = "absolute"
		self.parameter_5_id_124["takeover_mode"] = "None"
		self.parameter_5_id_124["enc_first"] = 0
		self.parameter_5_id_124["enc_second"] = 127
		self.parameter_5_id_124["reverse_mode"] = False
		self.parameter_5_id_124["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_5_id_124["LED_feedback"] = "default"
		self.parameter_5_id_124["LED_feedback_active"] = "1"
		self.parameter_5_id_124["LED_on"] = "127"
		self.parameter_5_id_124["LED_off"] = "0"
		self.parameter_5_id_124["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_20"]
		self.parameter_5_id_124["snap_to"] = True
		self.parameter_5_id_124["json_id"] = 124
		self.parameter_5_id_124["mapping_name"] = "Parameter 5"
		self.parameter_5_id_124["mapping_type"] = "Parameter"
		self.parameter_5_id_124["parent_json_id"] = 119
		self.parameter_5_id_124["parent_name"] = "parameter_bank_1_id_119"
		self.parameter_6_id_125 = {}
		self.parameter_6_id_125["attached_to"] = "midi_cc_ch_0_val_21"
		self.parameter_6_id_125["track"] = self.track_num(2)
		self.parameter_6_id_125["module"] = "self.song().view.selected_track.view.selected_device.parameters[6]"
		self.parameter_6_id_125["element"] = "value"
		self.parameter_6_id_125["output_type"] = "val"
		self.parameter_6_id_125["minimum"] = round(0,2)
		self.parameter_6_id_125["maximum"] = round(100,2)
		self.parameter_6_id_125["decimal_places"] = 2
		self.parameter_6_id_125["ui_listener"] = "value"
		self.parameter_6_id_125["feedback_brain"] = "feedback_range"
		self.parameter_6_id_125["ctrl_type"] = "absolute"
		self.parameter_6_id_125["takeover_mode"] = "None"
		self.parameter_6_id_125["enc_first"] = 0
		self.parameter_6_id_125["enc_second"] = 127
		self.parameter_6_id_125["reverse_mode"] = False
		self.parameter_6_id_125["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_6_id_125["LED_feedback"] = "default"
		self.parameter_6_id_125["LED_feedback_active"] = "1"
		self.parameter_6_id_125["LED_on"] = "127"
		self.parameter_6_id_125["LED_off"] = "0"
		self.parameter_6_id_125["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_21"]
		self.parameter_6_id_125["snap_to"] = True
		self.parameter_6_id_125["json_id"] = 125
		self.parameter_6_id_125["mapping_name"] = "Parameter 6"
		self.parameter_6_id_125["mapping_type"] = "Parameter"
		self.parameter_6_id_125["parent_json_id"] = 119
		self.parameter_6_id_125["parent_name"] = "parameter_bank_1_id_119"
		self.parameter_7_id_126 = {}
		self.parameter_7_id_126["attached_to"] = "midi_cc_ch_0_val_22"
		self.parameter_7_id_126["track"] = self.track_num(2)
		self.parameter_7_id_126["module"] = "self.song().view.selected_track.view.selected_device.parameters[7]"
		self.parameter_7_id_126["element"] = "value"
		self.parameter_7_id_126["output_type"] = "val"
		self.parameter_7_id_126["minimum"] = round(0,2)
		self.parameter_7_id_126["maximum"] = round(100,2)
		self.parameter_7_id_126["decimal_places"] = 2
		self.parameter_7_id_126["ui_listener"] = "value"
		self.parameter_7_id_126["feedback_brain"] = "feedback_range"
		self.parameter_7_id_126["ctrl_type"] = "absolute"
		self.parameter_7_id_126["takeover_mode"] = "None"
		self.parameter_7_id_126["enc_first"] = 0
		self.parameter_7_id_126["enc_second"] = 127
		self.parameter_7_id_126["reverse_mode"] = False
		self.parameter_7_id_126["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_7_id_126["LED_feedback"] = "default"
		self.parameter_7_id_126["LED_feedback_active"] = "1"
		self.parameter_7_id_126["LED_on"] = "127"
		self.parameter_7_id_126["LED_off"] = "0"
		self.parameter_7_id_126["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_22"]
		self.parameter_7_id_126["snap_to"] = True
		self.parameter_7_id_126["json_id"] = 126
		self.parameter_7_id_126["mapping_name"] = "Parameter 7"
		self.parameter_7_id_126["mapping_type"] = "Parameter"
		self.parameter_7_id_126["parent_json_id"] = 119
		self.parameter_7_id_126["parent_name"] = "parameter_bank_1_id_119"
		self.parameter_8_id_127 = {}
		self.parameter_8_id_127["attached_to"] = "midi_cc_ch_0_val_23"
		self.parameter_8_id_127["track"] = self.track_num(2)
		self.parameter_8_id_127["module"] = "self.song().view.selected_track.view.selected_device.parameters[8]"
		self.parameter_8_id_127["element"] = "value"
		self.parameter_8_id_127["output_type"] = "val"
		self.parameter_8_id_127["minimum"] = round(0,2)
		self.parameter_8_id_127["maximum"] = round(100,2)
		self.parameter_8_id_127["decimal_places"] = 2
		self.parameter_8_id_127["ui_listener"] = "value"
		self.parameter_8_id_127["feedback_brain"] = "feedback_range"
		self.parameter_8_id_127["ctrl_type"] = "absolute"
		self.parameter_8_id_127["takeover_mode"] = "None"
		self.parameter_8_id_127["enc_first"] = 0
		self.parameter_8_id_127["enc_second"] = 127
		self.parameter_8_id_127["reverse_mode"] = False
		self.parameter_8_id_127["LED_mapping_type_needs_feedback"] = "1"
		self.parameter_8_id_127["LED_feedback"] = "default"
		self.parameter_8_id_127["LED_feedback_active"] = "1"
		self.parameter_8_id_127["LED_on"] = "127"
		self.parameter_8_id_127["LED_off"] = "0"
		self.parameter_8_id_127["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_23"]
		self.parameter_8_id_127["snap_to"] = True
		self.parameter_8_id_127["json_id"] = 127
		self.parameter_8_id_127["mapping_name"] = "Parameter 8"
		self.parameter_8_id_127["mapping_type"] = "Parameter"
		self.parameter_8_id_127["parent_json_id"] = 119
		self.parameter_8_id_127["parent_name"] = "parameter_bank_1_id_119"
		self.reverb_id_129 = {}
		self.reverb_id_129["attached_to"] = "midi_cc_ch_0_val_56"
		self.reverb_id_129["track"] = self.track_num(2)
		self.reverb_id_129["module"] = "self.song().view.selected_track.mixer_device.sends[0]"
		self.reverb_id_129["element"] = "value"
		self.reverb_id_129["output_type"] = "val"
		self.reverb_id_129["minimum"] = round(0,3)
		self.reverb_id_129["maximum"] = round(100,3)
		self.reverb_id_129["decimal_places"] = 3
		self.reverb_id_129["ui_listener"] = "value"
		self.reverb_id_129["feedback_brain"] = "feedback_range"
		self.reverb_id_129["ctrl_type"] = "absolute"
		self.reverb_id_129["takeover_mode"] = "None"
		self.reverb_id_129["enc_first"] = 0
		self.reverb_id_129["enc_second"] = 127
		self.reverb_id_129["reverse_mode"] = False
		self.reverb_id_129["LED_mapping_type_needs_feedback"] = "1"
		self.reverb_id_129["LED_feedback"] = "default"
		self.reverb_id_129["LED_feedback_active"] = "1"
		self.reverb_id_129["LED_on"] = "127"
		self.reverb_id_129["LED_off"] = "0"
		self.reverb_id_129["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_56"]
		self.reverb_id_129["snap_to"] = True
		self.reverb_id_129["json_id"] = 129
		self.reverb_id_129["mapping_name"] = "Reverb"
		self.reverb_id_129["mapping_type"] = "Send"
		self.reverb_id_129["parent_json_id"] = 128
		self.reverb_id_129["parent_name"] = "sends_1_id_128"
		self.delay_id_130 = {}
		self.delay_id_130["attached_to"] = "midi_cc_ch_0_val_57"
		self.delay_id_130["track"] = self.track_num(2)
		self.delay_id_130["module"] = "self.song().view.selected_track.mixer_device.sends[1]"
		self.delay_id_130["element"] = "value"
		self.delay_id_130["output_type"] = "val"
		self.delay_id_130["minimum"] = round(0,3)
		self.delay_id_130["maximum"] = round(100,3)
		self.delay_id_130["decimal_places"] = 3
		self.delay_id_130["ui_listener"] = "value"
		self.delay_id_130["feedback_brain"] = "feedback_range"
		self.delay_id_130["ctrl_type"] = "absolute"
		self.delay_id_130["takeover_mode"] = "None"
		self.delay_id_130["enc_first"] = 0
		self.delay_id_130["enc_second"] = 127
		self.delay_id_130["reverse_mode"] = False
		self.delay_id_130["LED_mapping_type_needs_feedback"] = "1"
		self.delay_id_130["LED_feedback"] = "default"
		self.delay_id_130["LED_feedback_active"] = "1"
		self.delay_id_130["LED_on"] = "127"
		self.delay_id_130["LED_off"] = "0"
		self.delay_id_130["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_57"]
		self.delay_id_130["snap_to"] = True
		self.delay_id_130["json_id"] = 130
		self.delay_id_130["mapping_name"] = "Delay"
		self.delay_id_130["mapping_type"] = "Send"
		self.delay_id_130["parent_json_id"] = 128
		self.delay_id_130["parent_name"] = "sends_1_id_128"
		self.tap_tempo_id_131 = {}
		self.tap_tempo_id_131["attached_to"] = "midi_cc_ch_0_val_81"
		self.tap_tempo_id_131["module"] = "self.song()"
		self.tap_tempo_id_131["element"] = "tap_tempo"
		self.tap_tempo_id_131["output_type"] = "func"
		self.tap_tempo_id_131["func_arg"] = ""
		self.tap_tempo_id_131["enc_first"] = 127
		self.tap_tempo_id_131["enc_second"] = 0
		self.tap_tempo_id_131["switch_type"] = "momentary"
		self.tap_tempo_id_131["ctrl_type"] = "on/off"
		self.tap_tempo_id_131["json_id"] = 131
		self.tap_tempo_id_131["mapping_name"] = "Tap Tempo"
		self.tap_tempo_id_131["mapping_type"] = "Tap Tempo"
		self.tap_tempo_id_131["parent_json_id"] = 1
		self.tap_tempo_id_131["parent_name"] = "main_id_1"
		self.tempo_decrement_id_132 = {}
		self.tempo_decrement_id_132["attached_to"] = "midi_cc_ch_0_val_82"
		self.tempo_decrement_id_132["module"] = "self.song()"
		self.tempo_decrement_id_132["element"] = "tempo"
		self.tempo_decrement_id_132["output_type"] = "val"
		self.tempo_decrement_id_132["minimum"] = round(40,2)
		self.tempo_decrement_id_132["maximum"] = round(240,2)
		self.tempo_decrement_id_132["decimal_places"] = 2
		self.tempo_decrement_id_132["ui_listener"] = "tempo"
		self.tempo_decrement_id_132["feedback_brain"] = "feedback_tempo"
		self.tempo_decrement_id_132["ctrl_type"] = "decrement"
		self.tempo_decrement_id_132["enc_first"] = 127
		self.tempo_decrement_id_132["enc_second"] = 0
		self.tempo_decrement_id_132["steps"] = 200
		self.tempo_decrement_id_132["switch_type"] = "momentary"
		self.tempo_decrement_id_132["LED_mapping_type_needs_feedback"] = "1"
		self.tempo_decrement_id_132["LED_feedback"] = "default"
		self.tempo_decrement_id_132["LED_feedback_active"] = "1"
		self.tempo_decrement_id_132["LED_on"] = "127"
		self.tempo_decrement_id_132["LED_off"] = "0"
		self.tempo_decrement_id_132["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_82"]
		self.tempo_decrement_id_132["snap_to"] = True
		self.tempo_decrement_id_132["json_id"] = 132
		self.tempo_decrement_id_132["mapping_name"] = "Tempo Decrement"
		self.tempo_decrement_id_132["mapping_type"] = "Tempo"
		self.tempo_decrement_id_132["parent_json_id"] = 1
		self.tempo_decrement_id_132["parent_name"] = "main_id_1"
		self.tempo_increment_id_133 = {}
		self.tempo_increment_id_133["attached_to"] = "midi_cc_ch_0_val_83"
		self.tempo_increment_id_133["module"] = "self.song()"
		self.tempo_increment_id_133["element"] = "tempo"
		self.tempo_increment_id_133["output_type"] = "val"
		self.tempo_increment_id_133["minimum"] = round(40,2)
		self.tempo_increment_id_133["maximum"] = round(240,2)
		self.tempo_increment_id_133["decimal_places"] = 2
		self.tempo_increment_id_133["ui_listener"] = "tempo"
		self.tempo_increment_id_133["feedback_brain"] = "feedback_tempo"
		self.tempo_increment_id_133["ctrl_type"] = "increment"
		self.tempo_increment_id_133["enc_first"] = 127
		self.tempo_increment_id_133["enc_second"] = 0
		self.tempo_increment_id_133["steps"] = 200
		self.tempo_increment_id_133["switch_type"] = "momentary"
		self.tempo_increment_id_133["LED_mapping_type_needs_feedback"] = "1"
		self.tempo_increment_id_133["LED_feedback"] = "default"
		self.tempo_increment_id_133["LED_feedback_active"] = "1"
		self.tempo_increment_id_133["LED_on"] = "127"
		self.tempo_increment_id_133["LED_off"] = "0"
		self.tempo_increment_id_133["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_83"]
		self.tempo_increment_id_133["snap_to"] = True
		self.tempo_increment_id_133["json_id"] = 133
		self.tempo_increment_id_133["mapping_name"] = "Tempo Increment"
		self.tempo_increment_id_133["mapping_type"] = "Tempo"
		self.tempo_increment_id_133["parent_json_id"] = 1
		self.tempo_increment_id_133["parent_name"] = "main_id_1"
		self.scene_select_decrement_id_134 = {}
		self.scene_select_decrement_id_134["attached_to"] = "midi_cc_ch_0_val_84"
		self.scene_select_decrement_id_134["module"] = "self"
		self.scene_select_decrement_id_134["element"] = "scroll_highlight"
		self.scene_select_decrement_id_134["output_type"] = "func"
		self.scene_select_decrement_id_134["func_arg"] = "cnfg"
		self.scene_select_decrement_id_134["tracks_scenes"] = "scenes"
		self.scene_select_decrement_id_134["ui_listener"] = "tracks"
		self.scene_select_decrement_id_134["feedback_brain"] = "feedback_highlight_nav"
		self.scene_select_decrement_id_134["ctrl_type"] = "decrement"
		self.scene_select_decrement_id_134["enc_first"] = 127
		self.scene_select_decrement_id_134["enc_second"] = 0
		self.scene_select_decrement_id_134["steps"] = 1
		self.scene_select_decrement_id_134["switch_type"] = "momentary"
		self.scene_select_decrement_id_134["LED_mapping_type_needs_feedback"] = "1"
		self.scene_select_decrement_id_134["LED_feedback"] = "custom"
		self.scene_select_decrement_id_134["LED_feedback_active"] = "false"
		self.scene_select_decrement_id_134["LED_on"] = "127"
		self.scene_select_decrement_id_134["LED_off"] = "0"
		self.scene_select_decrement_id_134["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_84"]
		self.scene_select_decrement_id_134["json_id"] = 134
		self.scene_select_decrement_id_134["mapping_name"] = "Scene Select Decrement"
		self.scene_select_decrement_id_134["mapping_type"] = "Highlight Navigation"
		self.scene_select_decrement_id_134["parent_json_id"] = 1
		self.scene_select_decrement_id_134["parent_name"] = "main_id_1"
		self.scene_select_increment_id_135 = {}
		self.scene_select_increment_id_135["attached_to"] = "midi_cc_ch_0_val_85"
		self.scene_select_increment_id_135["module"] = "self"
		self.scene_select_increment_id_135["element"] = "scroll_highlight"
		self.scene_select_increment_id_135["output_type"] = "func"
		self.scene_select_increment_id_135["func_arg"] = "cnfg"
		self.scene_select_increment_id_135["tracks_scenes"] = "scenes"
		self.scene_select_increment_id_135["ui_listener"] = "tracks"
		self.scene_select_increment_id_135["feedback_brain"] = "feedback_highlight_nav"
		self.scene_select_increment_id_135["ctrl_type"] = "increment"
		self.scene_select_increment_id_135["enc_first"] = 127
		self.scene_select_increment_id_135["enc_second"] = 0
		self.scene_select_increment_id_135["steps"] = 1
		self.scene_select_increment_id_135["switch_type"] = "momentary"
		self.scene_select_increment_id_135["LED_mapping_type_needs_feedback"] = "1"
		self.scene_select_increment_id_135["LED_feedback"] = "custom"
		self.scene_select_increment_id_135["LED_feedback_active"] = "false"
		self.scene_select_increment_id_135["LED_on"] = "127"
		self.scene_select_increment_id_135["LED_off"] = "0"
		self.scene_select_increment_id_135["LED_send_feedback_to_selected"] = ["midi_cc_ch_0_val_85"]
		self.scene_select_increment_id_135["json_id"] = 135
		self.scene_select_increment_id_135["mapping_name"] = "Scene Select Increment"
		self.scene_select_increment_id_135["mapping_type"] = "Highlight Navigation"
		self.scene_select_increment_id_135["parent_json_id"] = 1
		self.scene_select_increment_id_135["parent_name"] = "main_id_1"
		# Reaction has no config
		# Reaction has no config

	def _mode1_led_listeners(self):
		try:
			self._mode1_fire_all_feedback()
		except:
			self.log("_mode1_led_listeners tried to call _mode1_fire_all_feedback but it does not exist")
		try:
			self.song().add_tracks_listener(self._all_tracks_listener)
		except:
			self.log("_mode1_led_listeners tried to call add_tracks_listener but it does not exist")
		try:
			self.all_track_device_listeners()
		except:
			self.log("_mode1_led_listeners tried to call all_track_device_listeners but it does not exist")
		try:
			self._mode1_ui_listeners()
		except:
			self.log("_mode1_led_listeners tried to call _mode1_ui_listeners but it does not exist")
		self.track_feedback(1)
		self.device_feedback(1)
		self.mode_device_bank_leds(1)

	def _remove_mode1_led_listeners(self):
		try:
			self.song().remove_tracks_listener(self._all_tracks_listener)
		except:
			self.log("_remove_mode1_led_listeners tried to call remove_tracks_listener but it does not exist")
		try:
			self._remove_all_track_device_listeners()
		except:
			self.log("_remove_mode1_led_listeners tried to call _remove_all_track_device_listeners but it does not exist")
		try:
			self._remove_mode1_ui_listeners()
		except:
			self.log("_remove_mode1_led_listeners tried to call _remove_mode1_ui_listeners but it does not exist")
		self.turn_inputs_off()

	def _mode1_ui_listeners(self):
		try:
			self.volume_id_7_led = eval(self.volume_id_7["module"])
			self.volume_id_7_led.add_value_listener(self.volume_id_7_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_id_7["element"]) + " does not exist")
		try:
			self.power_id_19_led = eval(self.power_id_19["module"])
			self.power_id_19_led.add_value_listener(self.power_id_19_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.power_id_19["element"]) + " does not exist")
		try:
			self.power_id_32_led = eval(self.power_id_32["module"])
			self.power_id_32_led.add_value_listener(self.power_id_32_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.power_id_32["element"]) + " does not exist")
		try:
			self.volume_id_38_led = eval(self.volume_id_38["module"])
			self.volume_id_38_led.add_value_listener(self.volume_id_38_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_id_38["element"]) + " does not exist")
		try:
			self.power_id_46_led = eval(self.power_id_46["module"])
			self.power_id_46_led.add_value_listener(self.power_id_46_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.power_id_46["element"]) + " does not exist")
		try:
			self.volume_id_52_led = eval(self.volume_id_52["module"])
			self.volume_id_52_led.add_value_listener(self.volume_id_52_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_id_52["element"]) + " does not exist")
		try:
			self.power_id_60_led = eval(self.power_id_60["module"])
			self.power_id_60_led.add_value_listener(self.power_id_60_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.power_id_60["element"]) + " does not exist")
		try:
			self.volume_id_66_led = eval(self.volume_id_66["module"])
			self.volume_id_66_led.add_value_listener(self.volume_id_66_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_id_66["element"]) + " does not exist")
		try:
			self.power_id_74_led = eval(self.power_id_74["module"])
			self.power_id_74_led.add_value_listener(self.power_id_74_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.power_id_74["element"]) + " does not exist")
		try:
			self.volume_id_80_led = eval(self.volume_id_80["module"])
			self.volume_id_80_led.add_value_listener(self.volume_id_80_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_id_80["element"]) + " does not exist")
		try:
			self.power_id_88_led = eval(self.power_id_88["module"])
			self.power_id_88_led.add_value_listener(self.power_id_88_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.power_id_88["element"]) + " does not exist")
		try:
			self.volume_id_94_led = eval(self.volume_id_94["module"])
			self.volume_id_94_led.add_value_listener(self.volume_id_94_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_id_94["element"]) + " does not exist")
		try:
			self.volume_id_108_led = eval(self.volume_id_108["module"])
			self.volume_id_108_led.add_value_listener(self.volume_id_108_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_id_108["element"]) + " does not exist")
		try:
			self.volume_8_id_116_led = eval(self.volume_8_id_116["module"])
			self.volume_8_id_116_led.add_value_listener(self.volume_8_id_116_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.volume_8_id_116["element"]) + " does not exist")
		if self.device_id_118_active_bank == 0:
			try:
				self.parameter_1_id_120_led = eval(self.parameter_1_id_120["module"])
				self.parameter_1_id_120_led.add_value_listener(self.parameter_1_id_120_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_1_id_120["element"]) + " does not exist")
		if self.device_id_118_active_bank == 0:
			try:
				self.parameter_2_id_121_led = eval(self.parameter_2_id_121["module"])
				self.parameter_2_id_121_led.add_value_listener(self.parameter_2_id_121_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_2_id_121["element"]) + " does not exist")
		if self.device_id_118_active_bank == 0:
			try:
				self.parameter_3_id_122_led = eval(self.parameter_3_id_122["module"])
				self.parameter_3_id_122_led.add_value_listener(self.parameter_3_id_122_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_3_id_122["element"]) + " does not exist")
		if self.device_id_118_active_bank == 0:
			try:
				self.parameter_4_id_123_led = eval(self.parameter_4_id_123["module"])
				self.parameter_4_id_123_led.add_value_listener(self.parameter_4_id_123_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_4_id_123["element"]) + " does not exist")
		if self.device_id_118_active_bank == 0:
			try:
				self.parameter_5_id_124_led = eval(self.parameter_5_id_124["module"])
				self.parameter_5_id_124_led.add_value_listener(self.parameter_5_id_124_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_5_id_124["element"]) + " does not exist")
		if self.device_id_118_active_bank == 0:
			try:
				self.parameter_6_id_125_led = eval(self.parameter_6_id_125["module"])
				self.parameter_6_id_125_led.add_value_listener(self.parameter_6_id_125_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_6_id_125["element"]) + " does not exist")
		if self.device_id_118_active_bank == 0:
			try:
				self.parameter_7_id_126_led = eval(self.parameter_7_id_126["module"])
				self.parameter_7_id_126_led.add_value_listener(self.parameter_7_id_126_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_7_id_126["element"]) + " does not exist")
		if self.device_id_118_active_bank == 0:
			try:
				self.parameter_8_id_127_led = eval(self.parameter_8_id_127["module"])
				self.parameter_8_id_127_led.add_value_listener(self.parameter_8_id_127_led_listener)
			except:
				self.log("_mode1_ui_listeners: " + str(self.parameter_8_id_127["element"]) + " does not exist")
		try:
			self.reverb_id_129_led = eval(self.reverb_id_129["module"])
			self.reverb_id_129_led.add_value_listener(self.reverb_id_129_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.reverb_id_129["element"]) + " does not exist")
		try:
			self.delay_id_130_led = eval(self.delay_id_130["module"])
			self.delay_id_130_led.add_value_listener(self.delay_id_130_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.delay_id_130["element"]) + " does not exist")
		try:
			self.tempo_decrement_id_132_led = eval(self.tempo_decrement_id_132["module"])
			self.tempo_decrement_id_132_led.add_tempo_listener(self.tempo_decrement_id_132_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.tempo_decrement_id_132["element"]) + " does not exist")
		try:
			self.tempo_increment_id_133_led = eval(self.tempo_increment_id_133["module"])
			self.tempo_increment_id_133_led.add_tempo_listener(self.tempo_increment_id_133_led_listener)
		except:
			self.log("_mode1_ui_listeners: " + str(self.tempo_increment_id_133["element"]) + " does not exist")
		try:
			self.song().add_tracks_listener(self.scene_select_decrement_id_134_led_listener)
		except:
			self.log("_mode1_ui_listeners: self.song().add_track_listener does not exist")
		try:
			self.song().add_tracks_listener(self.scene_select_increment_id_135_led_listener)
		except:
			self.log("_mode1_ui_listeners: self.song().add_track_listener does not exist")

	def _remove_mode1_ui_listeners(self):
		try:
			self.volume_id_7_led.remove_value_listener(self.volume_id_7_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_id_7["element"]) + " does not exist")
		try:
			self.power_id_19_led.remove_value_listener(self.power_id_19_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.power_id_19["element"]) + " does not exist")
		try:
			self.power_id_32_led.remove_value_listener(self.power_id_32_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.power_id_32["element"]) + " does not exist")
		try:
			self.volume_id_38_led.remove_value_listener(self.volume_id_38_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_id_38["element"]) + " does not exist")
		try:
			self.power_id_46_led.remove_value_listener(self.power_id_46_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.power_id_46["element"]) + " does not exist")
		try:
			self.volume_id_52_led.remove_value_listener(self.volume_id_52_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_id_52["element"]) + " does not exist")
		try:
			self.power_id_60_led.remove_value_listener(self.power_id_60_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.power_id_60["element"]) + " does not exist")
		try:
			self.volume_id_66_led.remove_value_listener(self.volume_id_66_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_id_66["element"]) + " does not exist")
		try:
			self.power_id_74_led.remove_value_listener(self.power_id_74_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.power_id_74["element"]) + " does not exist")
		try:
			self.volume_id_80_led.remove_value_listener(self.volume_id_80_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_id_80["element"]) + " does not exist")
		try:
			self.power_id_88_led.remove_value_listener(self.power_id_88_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.power_id_88["element"]) + " does not exist")
		try:
			self.volume_id_94_led.remove_value_listener(self.volume_id_94_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_id_94["element"]) + " does not exist")
		try:
			self.volume_id_108_led.remove_value_listener(self.volume_id_108_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_id_108["element"]) + " does not exist")
		try:
			self.volume_8_id_116_led.remove_value_listener(self.volume_8_id_116_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.volume_8_id_116["element"]) + " does not exist")
		try:
			self.parameter_1_id_120_led.remove_value_listener(self.parameter_1_id_120_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_1_id_120["element"]) + " does not exist")
		try:
			self.parameter_2_id_121_led.remove_value_listener(self.parameter_2_id_121_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_2_id_121["element"]) + " does not exist")
		try:
			self.parameter_3_id_122_led.remove_value_listener(self.parameter_3_id_122_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_3_id_122["element"]) + " does not exist")
		try:
			self.parameter_4_id_123_led.remove_value_listener(self.parameter_4_id_123_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_4_id_123["element"]) + " does not exist")
		try:
			self.parameter_5_id_124_led.remove_value_listener(self.parameter_5_id_124_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_5_id_124["element"]) + " does not exist")
		try:
			self.parameter_6_id_125_led.remove_value_listener(self.parameter_6_id_125_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_6_id_125["element"]) + " does not exist")
		try:
			self.parameter_7_id_126_led.remove_value_listener(self.parameter_7_id_126_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_7_id_126["element"]) + " does not exist")
		try:
			self.parameter_8_id_127_led.remove_value_listener(self.parameter_8_id_127_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.parameter_8_id_127["element"]) + " does not exist")
		try:
			self.reverb_id_129_led.remove_value_listener(self.reverb_id_129_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.reverb_id_129["element"]) + " does not exist")
		try:
			self.delay_id_130_led.remove_value_listener(self.delay_id_130_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.delay_id_130["element"]) + " does not exist")
		try:
			self.tempo_decrement_id_132_led.remove_tempo_listener(self.tempo_decrement_id_132_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.tempo_decrement_id_132["element"]) + " does not exist")
		try:
			self.tempo_increment_id_133_led.remove_tempo_listener(self.tempo_increment_id_133_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: " + str(self.tempo_increment_id_133["element"]) + " does not exist")
		try:
			self.song().remove_tracks_listener(self.scene_select_decrement_id_134_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: self.song() does not exist for highlight nav feedback")
		try:
			self.song().remove_tracks_listener(self.scene_select_increment_id_135_led_listener)
		except:
			self.log("remove__mode1_ui_listeners: self.song() does not exist for highlight nav feedback")

	def _mode1_fire_all_feedback(self):
		self.volume_id_7_led_listener()
		self.power_id_19_led_listener()
		self.power_id_32_led_listener()
		self.volume_id_38_led_listener()
		self.power_id_46_led_listener()
		self.volume_id_52_led_listener()
		self.power_id_60_led_listener()
		self.volume_id_66_led_listener()
		self.power_id_74_led_listener()
		self.volume_id_80_led_listener()
		self.power_id_88_led_listener()
		self.volume_id_94_led_listener()
		self.volume_id_108_led_listener()
		self.volume_8_id_116_led_listener()
		if self.device_id_118_active_bank == 0:
			self.parameter_1_id_120_led_listener()
		if self.device_id_118_active_bank == 0:
			self.parameter_2_id_121_led_listener()
		if self.device_id_118_active_bank == 0:
			self.parameter_3_id_122_led_listener()
		if self.device_id_118_active_bank == 0:
			self.parameter_4_id_123_led_listener()
		if self.device_id_118_active_bank == 0:
			self.parameter_5_id_124_led_listener()
		if self.device_id_118_active_bank == 0:
			self.parameter_6_id_125_led_listener()
		if self.device_id_118_active_bank == 0:
			self.parameter_7_id_126_led_listener()
		if self.device_id_118_active_bank == 0:
			self.parameter_8_id_127_led_listener()
		self.reverb_id_129_led_listener()
		self.delay_id_130_led_listener()
		self.tempo_decrement_id_132_led_listener()
		self.tempo_increment_id_133_led_listener()
		self.scene_select_decrement_id_134_led_listener()
		self.scene_select_increment_id_135_led_listener()

	def volume_id_7_led_listener(self):
		self.feedback_brain(self.volume_id_7)

	def power_id_19_led_listener(self):
		self.feedback_brain(self.power_id_19)

	def power_id_32_led_listener(self):
		self.feedback_brain(self.power_id_32)

	def volume_id_38_led_listener(self):
		self.feedback_brain(self.volume_id_38)

	def power_id_46_led_listener(self):
		self.feedback_brain(self.power_id_46)

	def volume_id_52_led_listener(self):
		self.feedback_brain(self.volume_id_52)

	def power_id_60_led_listener(self):
		self.feedback_brain(self.power_id_60)

	def volume_id_66_led_listener(self):
		self.feedback_brain(self.volume_id_66)

	def power_id_74_led_listener(self):
		self.feedback_brain(self.power_id_74)

	def volume_id_80_led_listener(self):
		self.feedback_brain(self.volume_id_80)

	def power_id_88_led_listener(self):
		self.feedback_brain(self.power_id_88)

	def volume_id_94_led_listener(self):
		self.feedback_brain(self.volume_id_94)

	def volume_id_108_led_listener(self):
		self.feedback_brain(self.volume_id_108)

	def volume_8_id_116_led_listener(self):
		self.feedback_brain(self.volume_8_id_116)

	def parameter_1_id_120_led_listener(self):
		self.feedback_brain(self.parameter_1_id_120)

	def parameter_2_id_121_led_listener(self):
		self.feedback_brain(self.parameter_2_id_121)

	def parameter_3_id_122_led_listener(self):
		self.feedback_brain(self.parameter_3_id_122)

	def parameter_4_id_123_led_listener(self):
		self.feedback_brain(self.parameter_4_id_123)

	def parameter_5_id_124_led_listener(self):
		self.feedback_brain(self.parameter_5_id_124)

	def parameter_6_id_125_led_listener(self):
		self.feedback_brain(self.parameter_6_id_125)

	def parameter_7_id_126_led_listener(self):
		self.feedback_brain(self.parameter_7_id_126)

	def parameter_8_id_127_led_listener(self):
		self.feedback_brain(self.parameter_8_id_127)

	def reverb_id_129_led_listener(self):
		self.feedback_brain(self.reverb_id_129)

	def delay_id_130_led_listener(self):
		self.feedback_brain(self.delay_id_130)

	def tempo_decrement_id_132_led_listener(self):
		self.feedback_brain(self.tempo_decrement_id_132)

	def tempo_increment_id_133_led_listener(self):
		self.feedback_brain(self.tempo_increment_id_133)

	def scene_select_decrement_id_134_led_listener(self):
		self.feedback_brain(self.scene_select_decrement_id_134)

	def scene_select_increment_id_135_led_listener(self):
		self.feedback_brain(self.scene_select_increment_id_135)

################################################
################## CORE v1.2 #################
################################################
	def placehold_listener(self, value):
		return
	def pick_brain(self, obj):
		cnfg = obj.copy() 
		if cnfg["output_type"] == "val":
				self.val_brain(cnfg)
		elif cnfg["output_type"] == "func":
			self.func_brain(cnfg)
		elif cnfg["output_type"] == "bool":
			self.bool_brain(cnfg)
	def should_it_fire(self, cnfg):
		controller = getattr(self, cnfg["attached_to"])
		cnfg["value"] = controller.cur_val 
		cnfg["pre_val"] = controller.pre_val 
		cnfg["prev_press_time"] = controller.prev_press_time
		timenow = time.time()
		fire = 0;
		if (cnfg["ctrl_type"] == "on/off" or cnfg["ctrl_type"] == "increment" or cnfg["ctrl_type"] == "decrement"): 
			if(cnfg["switch_type"] == "delay"):
				if((cnfg["value"] == cnfg["enc_second"]) and (timenow - cnfg["prev_press_time"]) > cnfg["delay_amount"]):
					fire = 1;
			elif(cnfg["switch_type"] == "toggle"):
				if cnfg["value"] == cnfg["enc_first"] or cnfg["value"] == cnfg["enc_second"]:
					fire = 1;
			elif (cnfg["switch_type"] == "momentary" and cnfg["value"] == cnfg["enc_first"]):
				fire = 1;
		elif cnfg["ctrl_type"] == "absolute":
			if cnfg["value"] >= cnfg["enc_first"] and cnfg["value"] <= cnfg["enc_second"]:
				fire = 1;
		elif cnfg["ctrl_type"] == "relative":
			if cnfg["value"] == cnfg["enc_first"] or cnfg["value"] == cnfg["enc_second"]:
				fire = 1;
		return fire
	def bool_brain(self, cnfg):
		method_to_call = getattr(eval(cnfg["module"]), cnfg["element"])
		fire = self.should_it_fire(cnfg)
		if fire == 1:	
			if method_to_call is False:
				setattr(eval(cnfg["module"]), cnfg["element"], True)
			else: 
				setattr(eval(cnfg["module"]), cnfg["element"], False)
	def func_brain(self, cnfg):
		fire = self.should_it_fire(cnfg)
		if fire == 1: 
			method_to_call = getattr(eval(cnfg["module"]), cnfg["element"])
			if cnfg["func_arg"] != "" and cnfg["func_arg"] != "cnfg":
				method_to_call(cnfg["func_arg"]) 
			elif cnfg["func_arg"] == "cnfg":
				method_to_call(cnfg) 
			else: 
				method_to_call()
	def val_brain(self, cnfg):
		try:
			cnfg["current_position"] = getattr(eval(cnfg["module"]), cnfg["element"]) 
		except:
			self.show_message("This control does not exist in your session")
			return
		self._parameter_to_map_to = eval(cnfg["module"])
		if cnfg["ctrl_type"] != "on/off" and hasattr(self._parameter_to_map_to, "max") and hasattr(self._parameter_to_map_to, "min"):
			param_range = self._parameter_to_map_to.max - self._parameter_to_map_to.min
			if cnfg.has_key("minimum"):
				usermin = cnfg["minimum"] / 100.;
				min_value = float(usermin * param_range) 
				cnfg["minimum"] = min_value + self._parameter_to_map_to.min
			if cnfg.has_key("maximum") and cnfg["mapping_type"] != "On/Off":
				usermax = cnfg["maximum"] / 100.;
				max_value = float(usermax * param_range) 
				cnfg["maximum"] = max_value + self._parameter_to_map_to.min
		controller = getattr(self, cnfg["attached_to"])
		cnfg["value"] = controller.cur_val 
		cnfg["pre_val"] = controller.pre_val 
		if cnfg.has_key("decimal_places"):
			cnfg["current_position"] = round(cnfg["current_position"], cnfg["decimal_places"])
		if cnfg["ctrl_type"] == "absolute":
			cnfg["steps"] = (cnfg["enc_second"] - cnfg["enc_first"]) 
		if cnfg["ctrl_type"] != "on/off":
			cnfg["distance"] = cnfg["maximum"] - cnfg["minimum"] 
			cnfg["speed"] = cnfg["distance"] / cnfg["steps"] 
			cnfg["step_values"] = self.step_values(cnfg) 
			cnfg["velocity_seq"] = self._velocity_seq(cnfg) 
		
		if int(cnfg["current_position"]) < int(cnfg["minimum"]) or int(cnfg["current_position"]) > int(cnfg["maximum"]):
			new_val = self.snap_to_max_min(cnfg)
		elif cnfg["ctrl_type"] == "absolute":
			new_val = self.absolute_decision(cnfg)
		elif cnfg["ctrl_type"] == "relative":
			new_val = self.relative_decision(cnfg)
		elif cnfg["ctrl_type"] == "on/off" or cnfg["ctrl_type"] == "increment" or cnfg["ctrl_type"] == "decrement":
			new_val = self.button_decision(cnfg)
		try:
			setattr(eval(cnfg["module"]), cnfg["element"], new_val)
		except:
			return
	def snap_to_max_min(self, cnfg):
		if cnfg["snap_to"] == True and cnfg["value"] >= cnfg["enc_first"] and cnfg["value"] <= cnfg["enc_second"]:
			if int(cnfg["current_position"]) < int(cnfg["minimum"]):
				new_val = cnfg["minimum"]
				self.log("snapped to min")
			elif int(cnfg["current_position"]) > int(cnfg["maximum"]):
				new_val = cnfg["maximum"]
				self.log("snapped to max")
		else:
			new_val = cnfg["current_position"]
			self.show_message("remotify: snapping is off for this control. Check min / max values")
		return new_val
	def step_values(self, cnfg):
		calc = []
		for i in range(0, cnfg["steps"] +1):
			val = (i * cnfg["speed"]) + cnfg["minimum"]
			if cnfg.has_key("decimal_places"):
				val = round(val, cnfg["decimal_places"])
			calc.append(val)
		if "reverse_mode" in cnfg and cnfg["reverse_mode"] is True:
			calc = list(reversed(calc))
		return calc
	def relative_decision(self, cnfg):
		fire = 0
		new_val = cnfg["current_position"] 
		if cnfg["value"] == cnfg["enc_second"]: 
			max_min = "max" 
			fire = 1
		elif cnfg["value"] == cnfg["enc_first"]: 
			max_min = "min" 
			fire = 1
		if fire == 0:
			return new_val
		if cnfg["current_position"] in cnfg["step_values"]:
			current_pos_index = cnfg["step_values"].index(cnfg["current_position"])
			
			feedback = current_pos_index / cnfg["steps"] * 127
			feedback = round(feedback, 0)
			method_to_call = getattr(self, cnfg["attached_to"])
			incr_index = current_pos_index + 1
			decr_index = current_pos_index - 1
			if max_min == "max" and incr_index < len(cnfg["step_values"]): 
				incr = cnfg["step_values"][incr_index]
				while incr == cnfg["current_position"]:
					incr_index = incr_index + 1
					if incr_index < len(cnfg["step_values"]):
						incr = cnfg["step_values"][incr_index]
					else:
						break
				new_val = incr
			elif max_min == "min" and decr_index >= 0: 
				decr = cnfg["step_values"][decr_index]
				new_val = decr
			return new_val    
		else:   
			new_val = self.step_in_line(cnfg, max_min)
			return new_val
		return new_val
	def percent_as_value(self, param, percentage):
		param = 		eval(param)
		if hasattr(param, 'max') and hasattr(param, 'min'):
			param_range = param.max - param.min
			val = percentage * param_range / 100
			return val
		else: 
			self.log("param does not have min and/or max attribute(s)")
	def button_decision(self, cnfg):
		new_val = cnfg["current_position"] 
		fire = self.should_it_fire(cnfg)
		if fire == 0:
			return new_val;
		if cnfg["ctrl_type"] == "on/off":
			if(cnfg["switch_type"] == "toggle"):
				if cnfg["value"] == cnfg["enc_first"]:
					new_val = cnfg["maximum"]
					return new_val
				elif cnfg["value"] == cnfg["enc_second"]:
					new_val = cnfg["minimum"]
					return new_val
			elif(cnfg["switch_type"] == "momentary"):
				if(cnfg["current_position"] == cnfg["maximum"]):
					new_val = cnfg["minimum"]
				else: 
					new_val = cnfg["maximum"]
				return new_val
			elif(cnfg["switch_type"] == "delay"):
				if(cnfg["current_position"] == cnfg["maximum"]):
					new_val = cnfg["minimum"]
				elif (cnfg["current_position"] == cnfg["minimum"]):
					new_val = cnfg["maximum"]
				return new_val
			else:
				self.log("neither momentary or toggle were set for on off button")
				return new_val
		if cnfg["current_position"] in cnfg["step_values"]:
			current_pos_index = cnfg["step_values"].index(cnfg["current_position"])
			incr_index = current_pos_index + 1
			decr_index = current_pos_index - 1
			if cnfg["ctrl_type"] ==  "increment" and incr_index < len(cnfg["step_values"]): 
				incr = cnfg["step_values"][incr_index]
				new_val = incr
			elif cnfg["ctrl_type"] == "decrement" and decr_index >= 0: 
				decr = cnfg["step_values"][decr_index]
				new_val = decr
			return new_val
		else:
			if cnfg["ctrl_type"] ==  "increment": 
				max_min = "max"
			elif cnfg["ctrl_type"] == "decrement": max_min = "min"
			new_val = self.step_in_line(cnfg, max_min)
			return new_val
		return new_val
	def step_in_line(self, cnfg, max_min):
		previous = ""
		step_num = 0
		speed = 0 
		for step_val in cnfg["step_values"]:
			step_num += 1
			if cnfg["current_position"] > previous and cnfg["current_position"] < step_val:
				if max_min == "min":
					speed = cnfg["current_position"] - previous 
					new_val = previous
				elif max_min == "max":
					speed = step_val - cnfg["current_position"] 
					new_val = step_val
				break
			previous = step_val
		return new_val
	def absolute_decision(self, cnfg):
		if(cnfg["enc_first"] > cnfg["enc_second"]):
			self.log("enc_first is higher than enc_second, needs to be lower")
		new_val = cnfg["current_position"] 
		if cnfg["pre_val"] is None:
			return new_val
		######### Get pre_val details from list values ######### 
		######### ######### ######### ######## ######
		if cnfg["pre_val"] in cnfg["velocity_seq"]: 
			cnfg["previous_step_num"] = cnfg["velocity_seq"].index(cnfg["pre_val"]) 
			cnfg["previous_step_value"] = cnfg["step_values"][cnfg["previous_step_num"]] 
		else:
			cnfg["previous_step_value"] = None
		######### get value details from list ######### 
		######### ######### ######### ######### ######
		if cnfg["value"] in cnfg["velocity_seq"]:
			cnfg["step_num"] = cnfg["velocity_seq"].index(cnfg["value"]) 
			cnfg["step_value"] = cnfg["step_values"][cnfg["step_num"]] 
		else: 
			cnfg["step_num"] = None
			cnfg["step_value"] = None
			
		######### MAX OR MIN ########
		######### ######### ######### 
		if cnfg["reverse_mode"] is False:
			if cnfg["value"] > cnfg["pre_val"]: max_min = "max"
			elif cnfg["value"] < cnfg["pre_val"]: max_min = "min"
		elif cnfg["reverse_mode"] is True:
			if cnfg["value"] > cnfg["pre_val"]: max_min = "min"
			elif cnfg["value"] < cnfg["pre_val"]: max_min = "max"
		inside_outside = self.inside_outside_checks(cnfg)
		if inside_outside is not False:
			self.log("inside outside was not false")
			return inside_outside
		######### straight assign or takeover ######### 
		######### ######### ######### ######### #######
		if cnfg["previous_step_value"] == cnfg["current_position"]:
			new_val = cnfg["step_value"]
		elif cnfg["takeover_mode"] == "None": 
			new_val = cnfg["step_value"]
		elif cnfg["takeover_mode"] == "Pickup": 
			new_val = self.pickup(cnfg, max_min)
		elif cnfg["takeover_mode"] == "Value scaling": new_val = self.value_scaling(cnfg, max_min)
		else: self.log("nothing got decided")
			
		return new_val
	def inside_outside_checks(self, cnfg):
		new_val = cnfg["current_position"]
		if cnfg["reverse_mode"] is False: 
			minimum = cnfg["minimum"]
			maximum = cnfg["maximum"]
		elif cnfg["reverse_mode"] is True: 
			minimum = cnfg["maximum"]
			maximum = cnfg["minimum"]
		######### was outside and is still outside ######
		######### ######### ######### ######### ######### 
		if (cnfg["pre_val"] < cnfg["enc_first"] and cnfg["value"] < cnfg["enc_first"]):
			self.log("was below and still below")
			return new_val
		elif (cnfg["pre_val"] > cnfg["enc_second"] and cnfg["value"] > cnfg["enc_second"]):
			self.log("was above and still above")
			return new_val
		## 1. Going Below
		if (cnfg["pre_val"] >= cnfg["enc_first"] and cnfg["value"] < cnfg["enc_first"]): 
			self.log("going below enter")
			if cnfg["takeover_mode"] == "Pickup":
				if cnfg["reverse_mode"] is False and cnfg["current_position"] > cnfg["previous_step_value"]:
					return new_val
				elif cnfg["reverse_mode"] is True and cnfg["current_position"] < cnfg["previous_step_value"]:
					return new_val
			if cnfg["reverse_mode"] is False:
				new_val = minimum
				self.log("going below 1")
				return new_val
			elif cnfg["reverse_mode"] is True:
				new_val = minimum
				self.log("going below 2")
				return new_val
		## 2. Going Above
		if (cnfg["pre_val"] <= cnfg["enc_second"] and cnfg["value"] > cnfg["enc_second"]):
			if cnfg["takeover_mode"] == "Pickup":
				self.log("THIS SHOULD FIRE 1")
				if cnfg["reverse_mode"] is False and cnfg["current_position"] < cnfg["previous_step_value"]:
					self.log("THIS SHOULD FIRE 2")
					return new_val
				elif cnfg["reverse_mode"] is True and cnfg["current_position"] > cnfg["previous_step_value"]:
					return new_val 
			if cnfg["reverse_mode"] is False:
				new_val = maximum
				self.log("going above 1")
				return new_val
			elif cnfg["reverse_mode"] is True:
				new_val = maximum
				self.log("going above 2")
				return new_val
		#########  >>0<< Coming inside ########
		######### ######### ######### ######### 
		if (cnfg["pre_val"] < cnfg["enc_first"] and cnfg["value"] >= cnfg["enc_first"]):
			self.log("come in from below")
			
		elif (cnfg["pre_val"] > cnfg["enc_second"] and cnfg["value"] <= cnfg["enc_second"]):
			self.log("coming in from above")
		return False
	def _velocity_seq(self,cnfg):
		number_of_steps = cnfg['enc_second'] - cnfg['enc_first']
		arr = []
		i = 0
		sequence_num = cnfg['enc_first']
		while i <= number_of_steps:
			arr.append(sequence_num)
			i += 1
			sequence_num += 1
		return arr
	def pickup(self, cnfg, max_min):
		new_val = cnfg["current_position"] 
		found = False
		if cnfg["previous_step_value"] is None:
			self.log("just entered")
			
			if cnfg["reverse_mode"] is False:
				if cnfg["pre_val"] < cnfg["enc_first"] and cnfg["step_value"] > cnfg["current_position"]:
					new_val = cnfg["step_value"]
					found = True
					self.log("pickup 1 found")
				elif cnfg["pre_val"] > cnfg["enc_second"] and cnfg["step_value"] < cnfg["current_position"]:
					new_val = cnfg["step_value"]
					found = True
					self.log("pickup 2 found")
			elif cnfg["reverse_mode"] is True:
				if cnfg["pre_val"] < cnfg["enc_first"] and cnfg["step_value"] < cnfg["current_position"]:
					new_val = cnfg["step_value"]
					found = True
					self.log("pickup 3 found")
				elif cnfg["pre_val"] > cnfg["enc_second"] and cnfg["step_value"] > cnfg["current_position"]:
					new_val = cnfg["step_value"]
					found = True
					self.log("pickup 4 found")
		
		else:
			self.log("we were already in here")
			
			if cnfg["previous_step_value"] < cnfg["current_position"] and cnfg["step_value"] > cnfg["current_position"]: 
				new_val = cnfg["step_value"]
				found = True
				self.log("pickup 4 found")
			elif cnfg["previous_step_value"] > cnfg["current_position"] and cnfg["step_value"] < cnfg["current_position"] :
				new_val = cnfg["step_value"]
				found = True  
				self.log("pickup 5 found")
			else: 
				self.log("waiting for pickup")
		if found is False:
			msg = "remotify says: waiting for pickup " + str(cnfg["step_value"]) + " >> " + str(cnfg["current_position"])
			self.show_message(msg)
		return new_val
		step_num = cnfg["step_num"]
		step_value = cnfg["step_value"]
		remaining_steps = cnfg["steps"] - step_num 
		new_val = cnfg["current_position"] 
		distance_to_max = cnfg["maximum"] - cnfg["current_position"]
		distance_to_min = cnfg["current_position"] - cnfg["minimum"]
		speed_to_max = 0
		speed_to_min = 0
		if cnfg["current_position"] >= cnfg["minimum"] and cnfg["current_position"] <= cnfg["maximum"]:
			if max_min == "max" and distance_to_max > 0:
				if cnfg["reverse_mode"] is False and remaining_steps > 0: speed_to_max = distance_to_max / remaining_steps
				elif cnfg["reverse_mode"] is True and step_num > 0: speed_to_max = distance_to_max / step_num
				if speed_to_max is not 0: new_val = speed_to_max + cnfg["current_position"]
			elif max_min == "min" and distance_to_min > 0:
				if cnfg["reverse_mode"] is False and step_num > 0: speed_to_min = distance_to_min / step_num
				elif cnfg["reverse_mode"] is True and remaining_steps > 0: speed_to_min = distance_to_min / remaining_steps
				if speed_to_min is not 0: new_val = cnfg["current_position"] - speed_to_min
		return new_val
	def value_scaling(self, cnfg, max_min):
		step_num = cnfg["step_num"]
		step_value = cnfg["step_value"]
		remaining_steps = cnfg["steps"] - step_num 
		new_val = cnfg["current_position"] 
		distance_to_max = cnfg["maximum"] - cnfg["current_position"]
		distance_to_min = cnfg["current_position"] - cnfg["minimum"]
		speed_to_max = 0
		speed_to_min = 0
		if cnfg["current_position"] >= cnfg["minimum"] and cnfg["current_position"] <= cnfg["maximum"]:
			if max_min == "max" and distance_to_max > 0:
				if cnfg["reverse_mode"] is False and remaining_steps > 0: speed_to_max = distance_to_max / remaining_steps
				elif cnfg["reverse_mode"] is True and step_num > 0: speed_to_max = distance_to_max / step_num
				if speed_to_max is not 0: new_val = speed_to_max + cnfg["current_position"]
			elif max_min == "min" and distance_to_min > 0:
				if cnfg["reverse_mode"] is False and step_num > 0: speed_to_min = distance_to_min / step_num
				elif cnfg["reverse_mode"] is True and remaining_steps > 0: speed_to_min = distance_to_min / remaining_steps
				if speed_to_min is not 0: new_val = cnfg["current_position"] - speed_to_min
		return new_val
	def track_num(self, track_num):
		if ((hasattr(self, '_session')) and (self._session is not None)):
			track_num = track_num + self._session._track_offset
		else: 
			track_num = track_num
		return track_num
	def scene_num(self, scene_num):
		if ((hasattr(self, '_session')) and (self._session is not None)):
			scene_num = scene_num + self._session._scene_offset 
		else: 
			scene_num = scene_num
		return scene_num
	def log_cnfg_settings(self, cnfg):
		for i in cnfg:
			text = i + ": " + str(cnfg[i])
			self.log(text)
	def dump(self, obj):
		for attr in dir(obj):
			self.log("csslog: obj.%s = %r" % (attr, getattr(obj, attr)))
	def log(self, msg):
		if self.debug_on is True:
			self.log_message("csslog:" + str(msg))
	def pret(self, ugly):
		for key,value in sorted(ugly.items()):
			self.log_message(key)
			self.log_message(value)
			self.log_message("")
	################################################
	############# Extra Functions: LED Functions ###
	################################################
	def _quantizeDict(self):
		grid_setting = str(self.song().view.highlighted_clip_slot.clip.view.grid_quantization)
		is_it_triplet = self.song().view.highlighted_clip_slot.clip.view.grid_is_triplet
		if (is_it_triplet is True):
			grid_setting += "_triplet"
		RecordingQuantization = Live.Song.RecordingQuantization
		quantDict = {}
		quantDict["g_thirtysecond"] = RecordingQuantization.rec_q_thirtysecond
		quantDict["g_sixteenth"] = RecordingQuantization.rec_q_sixtenth
		quantDict["g_eighth"] = RecordingQuantization.rec_q_eight
		quantDict["g_quarter"] = RecordingQuantization.rec_q_quarter
		quantDict["g_eighth_triplet"] = RecordingQuantization.rec_q_eight_triplet
		quantDict["g_sixteenth_triplet"] = RecordingQuantization.rec_q_sixtenth_triplet
		return quantDict[grid_setting];
	def _arm_follow_track_selection(self):
		for track in self.song().tracks:
			if track.can_be_armed:
				track.arm = False
		if self.song().view.selected_track.can_be_armed:
			self.song().view.selected_track.arm = True
	def turn_inputs_off(self): 
		send_feedback = False
		if hasattr(self, "global_feedback"): 
			if self.global_feedback == "custom":
				if self.global_feedback_active == True: 
					send_feedback = True
			elif hasattr(self, "controller_LED_on") and hasattr(self, "controller_LED_off"):
				send_feedback = True
		if send_feedback == True: 
			for input_name in self.input_map:
				input_ctrl = getattr(self, input_name)
				input_ctrl.send_value(self.led_off)
	def feedback_brain(self, obj):
		cnfg = obj.copy() 
		try:
			method_to_call = getattr(self, cnfg["feedback_brain"])
			method_to_call(cnfg)
		except:
			return 
	def feedback_bool(self, feedback_to):
		control = 	eval("self." + str(feedback_to["attached_to"]))
		param = 		eval(feedback_to["module"] + "." + feedback_to["ui_listener"])
		ctrl_on = 	self.feedback_which_ctrl_on_off(feedback_to, "on")
		ctrl_off = 	self.feedback_which_ctrl_on_off(feedback_to, "off")
		if(feedback_to["mapping_type"] == "Mute"):
			if param == False:
				send_val = ctrl_on
			elif param == True:
				send_val = ctrl_off
		else: 
			if param == True:
				send_val = ctrl_on
			elif param == False:
				send_val = ctrl_off
		self.feedback_handler(feedback_to, send_val)
	def feedback_on_off(self, feedback_to):
		param = 		eval(feedback_to["module"])
		ctrl_on = 	self.feedback_which_ctrl_on_off(feedback_to, "on")
		ctrl_off = 	self.feedback_which_ctrl_on_off(feedback_to, "off")
		param_value = round(param.value,2) 
		mapping_type = str(feedback_to["mapping_type"])
		if feedback_to.has_key("maximum") and feedback_to.has_key("minimum"):
			max_val = feedback_to["maximum"]
			min_val = feedback_to["minimum"]
			if mapping_type != "On/Off":
				max_val = self.percent_as_value(feedback_to["module"], feedback_to["maximum"])
				max_val = round(max_val,2)
				min_val = self.percent_as_value(feedback_to["module"], feedback_to["minimum"])
				min_val = round(min_val,2)
		elif hasattr(param, "max") and hasattr(param, "min"): 
			max_val = param.max
			max_val = round(max_val,2)
			min_val = param.min
			min_val = round(min_val,2)
		else: 
			self.log_message(str(param) + " does not have a max/min param")
			return
		send_val = None
		if param_value == max_val:
			send_val = ctrl_on
		elif param_value == min_val:
			send_val = ctrl_off
		if send_val is not None:
			self.feedback_handler(feedback_to, send_val)
		else: 
			return
	def feedback_increment(self, feedback_to):
		control = 	eval("self." + str(feedback_to["attached_to"]))
		param = 		eval(feedback_to["module"])
		mapping_type = str(feedback_to["mapping_type"])
		ctrl_on = 	self.feedback_which_ctrl_on_off(feedback_to, "on")
		ctrl_off = 	self.feedback_which_ctrl_on_off(feedback_to, "off")
		snapping = feedback_to["snap_to"]
		mapping_type = str(feedback_to["mapping_type"])
		if feedback_to.has_key("maximum") and feedback_to.has_key("minimum"):
			max_val = feedback_to["maximum"]
			min_val = feedback_to["minimum"]
			if mapping_type != "On/Off":
				max_val = self.percent_as_value(feedback_to["module"], feedback_to["maximum"])
				min_val = self.percent_as_value(feedback_to["module"], feedback_to["minimum"])
		elif hasattr(param, "max") and hasattr(param, "min"): 
			max_val = param.max
			min_val = param.min
		else: 
			self.log_message(str(param) + " does not have a max/min param")
			return
		if snapping == False and param.value < min_val:
			send_val = ctrl_off
		elif param.value < max_val: 
			send_val = ctrl_on
		else: 
			send_val = ctrl_off
		self.feedback_handler(feedback_to, send_val)
	def feedback_decrement(self, feedback_to):
		control = 	eval("self." + str(feedback_to["attached_to"]))
		param = 		eval(feedback_to["module"])
		mapping_type = str(feedback_to["mapping_type"])
		ctrl_on = 	self.feedback_which_ctrl_on_off(feedback_to, "on")
		ctrl_off = 	self.feedback_which_ctrl_on_off(feedback_to, "off")
		snapping = feedback_to["snap_to"]
		if feedback_to.has_key("maximum") and feedback_to.has_key("minimum"):
			max_val = feedback_to["maximum"]
			min_val = feedback_to["minimum"]
			if mapping_type != "On/Off":
				max_val = self.percent_as_value(feedback_to["module"], feedback_to["maximum"])
				min_val = self.percent_as_value(feedback_to["module"], feedback_to["minimum"])
		elif hasattr(param, "max") and hasattr(param, "min"): 
			max_val = param.max
			min_val = param.min
		else: 
			self.log_message(str(param) + " does not have a max/min param")
			return
		if snapping == False and param.value > max_val:
			send_val = ctrl_off
		elif param.value > min_val: 
			send_val = ctrl_on
		else: 
			send_val = ctrl_off
		self.feedback_handler(feedback_to, send_val)
	def feedback_which_ctrl_on_off(self, feedback_to, on_off):
		if feedback_to["LED_feedback"] == "default":
			ctrl_on = self.led_on
			ctrl_off = self.led_off
		elif feedback_to["LED_feedback"] == "custom":
			if feedback_to["ctrl_type"] == "on/off" or feedback_to["ctrl_type"] == "increment" or feedback_to["ctrl_type"] == "decrement":
				ctrl_on = feedback_to["LED_on"]
				ctrl_off = feedback_to["LED_off"]
			elif feedback_to["ctrl_type"] == "absolute" or feedback_to["ctrl_type"] == "relative":
				ctrl_on = feedback_to["enc_first"]
				ctrl_off = feedback_to["enc_second"]
		if on_off == "on":
			value = ctrl_on
		elif on_off == "off":
			value = ctrl_off
		return value;
	def feedback_range(self, feedback_to):
		if feedback_to['ctrl_type'] == "on/off":
			self.feedback_on_off(feedback_to)
		elif feedback_to['ctrl_type'] == "increment":
			self.feedback_increment(feedback_to)
		elif feedback_to['ctrl_type'] == "decrement":
			self.feedback_decrement(feedback_to)
		control = 	eval("self." + str(feedback_to["attached_to"]))
		param = 		eval(feedback_to["module"])
		ctrl_min = 	feedback_to["minimum"]
		ctrl_max = 	feedback_to["maximum"]
		ctrl_type = feedback_to["ctrl_type"]
		default_ctrl_first = 0 
		default_ctrl_last = 127 
		if ctrl_type == "relative":
			crl_reverse = False
			ctrl_first = 0
			ctrl_last = 127
		else:
			crl_reverse = feedback_to["reverse_mode"]
			ctrl_first = feedback_to["enc_first"]
			ctrl_last = feedback_to["enc_second"]
		param_range = param.max - param.min 
		orig_param_range = param.max - param.min
		param_range = ctrl_max * orig_param_range / 100
		ctrl_min_as_val = ctrl_min * orig_param_range / 100
		param_range = param_range - ctrl_min_as_val
		param_value = param.value - ctrl_min_as_val
		
		if orig_param_range == 2.0 and param.min == -1.0:
			param_value = param_value + 1 
		percentage_control_is_at = param_value / param_range * 100
		ctrl_range = ctrl_last - ctrl_first
		percentage_of_ctrl_range = ctrl_range * percentage_control_is_at / 100 + ctrl_first
		percentage_of_ctrl_range = round(percentage_of_ctrl_range,0)
		if crl_reverse == True:
			percentage_of_ctrl_range = ctrl_range - percentage_of_ctrl_range
		self.feedback_handler(feedback_to, percentage_of_ctrl_range)
	def feedback_a_b_crossfade_assign(self, feedback_to):
		assigned_val = eval(str(feedback_to['parent_track']) + ".mixer_device.crossfade_assign")
		if(assigned_val == 0):
			send_val = feedback_to["LED_on"]
		elif(assigned_val == 1):
			send_val = feedback_to["LED_off"]
		elif(assigned_val == 2):
			send_val = feedback_to["LED_assigned_to_b"]
		else: 
			send_val = 0
		self.feedback_handler(feedback_to, send_val)
	def feedback_handler(self, config, send_val):
		send_feedback = False
		if config.has_key("LED_feedback"):
			if config["LED_feedback"] == "custom": 
				if config["LED_feedback_active"] == "1" or config["LED_feedback_active"] == "true": 
					send_feedback = True
			elif hasattr(self, "global_feedback"): 
				if self.global_feedback == "custom":
					if self.global_feedback_active == True: 
						send_feedback = True
				elif hasattr(self, "controller_LED_on") and hasattr(self, "controller_LED_off"):
					send_feedback = True
			if send_feedback == True: 
				if config["LED_feedback"] == "custom":
					for item in config["LED_send_feedback_to_selected"]:
						feedback_control = 	eval("self." + str(item))
						feedback_control.send_value(send_val)
				else: 
					control = 	eval("self." + str(config["attached_to"]))
					control.send_value(send_val)
			else:
				self.log("feedback_handler says 'not sending led feedback'")
	def sess_highlight_banking_calculate(self, feedback_to, num_of_tracks_scenes, offset_is_at):
		ctrl_first = feedback_to["enc_first"]
		ctrl_last = feedback_to["enc_second"]
		ctrl_range = ctrl_last - ctrl_first
		if feedback_to['ctrl_type'] == "absolute" or feedback_to['ctrl_type'] == "relative":
			percentage_control_is_at = offset_is_at / num_of_tracks_scenes * 100
			velocity_val = ctrl_range * percentage_control_is_at / 100 + ctrl_first
			velocity_val = int(velocity_val) 
		elif feedback_to['ctrl_type'] == "on/off" or feedback_to['ctrl_type'] == "increment":
			if offset_is_at == num_of_tracks_scenes:
				velocity_val = feedback_to["LED_on"]
			else:
				velocity_val = feedback_to["LED_off"]
		elif feedback_to['ctrl_type'] == "decrement":
			if offset_is_at == 0:
				velocity_val = feedback_to["LED_off"]
			else:
				velocity_val = feedback_to["LED_on"]
		if feedback_to['ctrl_type'] == "absolute" and feedback_to["reverse_mode"] == True:
			velocity_val = ctrl_range - velocity_val
		self.feedback_handler(feedback_to, velocity_val)
	def feedback_scroll_mode_selector(self, feedback_to):
		global active_mode
		num_of_tracks_scenes = len(self.modes) - 1
		count = 0
		for mode_num in self.modes.values():
			if mode_num == active_mode:
				offset_is_at = count
				break
			count += 1
		self.sess_highlight_banking_calculate(feedback_to, num_of_tracks_scenes, offset_is_at)
	def feedback_scroll_mode_selector_select(self, feedback_to):
		global active_mode
		mode_to_select = int(feedback_to["func_arg"])
		if int(active_mode) == mode_to_select:
			self.feedback_handler(feedback_to, feedback_to["LED_on"])
		else:
			self.feedback_handler(feedback_to, feedback_to["LED_off"])
	def feedback_param_banking_select(self, feedback_to):
		banking_number = int(feedback_to["banking_number"])
		parent_device_id = feedback_to["parent_device_id"]
		offset_is_at = getattr(self, "device_id_" + str(parent_device_id) + "_active_bank")
		if banking_number == offset_is_at:
			self.feedback_handler(feedback_to, feedback_to["LED_on"])
		else:
			self.feedback_handler(feedback_to, feedback_to["LED_off"])
	def feedback_param_banking(self, feedback_to):
		self.log_message("scroll banking fired")
		parent_device_id = feedback_to["parent_device_id"]
		bank_array = getattr(self, "device_id_" + str(parent_device_id) + "_banks")
		num_of_tracks_scenes = len(bank_array) - 1
		offset_is_at = getattr(self, "device_id_" + str(parent_device_id) + "_active_bank")
		self.sess_highlight_banking_calculate(feedback_to, num_of_tracks_scenes, offset_is_at)
	def feedback_highlight_nav_select(self, feedback_to):
		tracks_or_scenes = feedback_to["tracks_scenes"]
		tracks_scene_num = int(feedback_to["highlight_number"])
		if tracks_or_scenes == "tracks":
			offset_is_at = int(self.selected_track_idx()) - 1
		elif tracks_or_scenes == "scenes":
			offset_is_at = int(self.selected_scene_idx()) - 1
		if tracks_scene_num == offset_is_at:
			self.feedback_handler(feedback_to, feedback_to["LED_on"])
		else:
			self.feedback_handler(feedback_to, feedback_to["LED_off"])
	def feedback_highlight_nav(self, feedback_to):
		tracks_or_scenes = feedback_to["tracks_scenes"]
		if tracks_or_scenes == "tracks":
			offset_is_at = int(self.selected_track_idx()) - 1
			num_of_tracks_scenes = int(len(self.song().tracks)) - 1
		elif tracks_or_scenes == "scenes":
			offset_is_at = int(self.selected_scene_idx()) - 1
			num_of_tracks_scenes = int(len(self.song().scenes)) - 1
		self.sess_highlight_banking_calculate(feedback_to, num_of_tracks_scenes, offset_is_at)
	def feedback_sessbox_nav_select(self, feedback_to):
		try:
			self._session
		except:
			self.show_message("There's no Session Box to select for feedback")
			return
		tracks_scene_num = int(feedback_to["highlight_number"])
		tracks_or_scenes = feedback_to["tracks_scenes"]
		if tracks_or_scenes == "tracks":
			offset_is_at = int(self._session.track_offset())
		elif tracks_or_scenes == "scenes":
			offset_is_at = int(self._session.scene_offset())
		if tracks_scene_num == offset_is_at:
			self.feedback_handler(feedback_to, feedback_to["LED_on"])
		else:
			self.feedback_handler(feedback_to, feedback_to["LED_off"])
	def feedback_sessbox_nav(self, feedback_to):
		try:
			self._session
		except:
			self.show_message("There's no Session Box to scroll for feedback sir.")
			return
		tracks_or_scenes = feedback_to["tracks_scenes"]
		if tracks_or_scenes == "tracks":
			offset_is_at = int(self._session.track_offset())
			num_of_tracks_scenes = int(len(self.song().tracks)) - 1
		elif tracks_or_scenes == "scenes":
			offset_is_at = int(self._session.scene_offset())
			num_of_tracks_scenes = int(len(self.song().scenes)) - 1
		self.sess_highlight_banking_calculate(feedback_to, num_of_tracks_scenes, offset_is_at)
	def feedback_tempo(self, feedback_to):
		control = 	eval("self." + str(feedback_to["attached_to"]))
		param = 		eval(feedback_to["module"])
		ctrl_min = 	feedback_to["minimum"]
		ctrl_max = 	feedback_to["maximum"]
		ctrl_type = feedback_to["ctrl_type"]
		ctrl_first = feedback_to["enc_first"]
		ctrl_last = feedback_to["enc_second"]
		default_ctrl_first = 0 
		default_ctrl_last = 127 
		crl_reverse = feedback_to["reverse_mode"]
		param_range = ctrl_max - ctrl_min
		param = 		eval(feedback_to["module"] + "." + feedback_to["ui_listener"])
		zero = ctrl_min 
		if param < ctrl_min or param > ctrl_max:
			self.log("tempo is outside ctrl_min / ctrl_max")
		else:
			zerod_param = param - zero 
			percentage_control_is_at = zerod_param / param_range * 100
		ctrl_range = ctrl_last - ctrl_first
		percentage_of_ctrl_range = ctrl_range * percentage_control_is_at / 100 + ctrl_first
		if crl_reverse == True:
			percentage_of_ctrl_range = ctrl_range - percentage_of_ctrl_range
		self.feedback_handler(feedback_to, percentage_of_ctrl_range)
	def mode_device_bank_leds(self, mode_id):
		config_map = "mode_" + str(mode_id) + "_configs_map"
		config_map = getattr(self, config_map)
		for config_name in config_map:
			config = getattr(self, config_name)
			if config["mapping_type"] == "Parameter Bank":
				parent_id = config["parent_json_id"]
				bank_names_array_name = "device_id_" + str(parent_id) + "_banks"
				active_bank_name = "device_id_" + str(parent_id) + "_active_bank"
				bank_names_array = getattr(self, bank_names_array_name)
				active_bank = getattr(self, active_bank_name)
				for index, bank_name in enumerate(bank_names_array):
					if bank_name == config_name:
						if index == active_bank:
							led_on = config["LED_on"]
							self.feedback_handler(config, led_on)
						else: 
							led_off = config["LED_off"]
							self.feedback_handler(config, led_off)
	def bank_led_feedback(self, parent_device_id):
		global active_mode
		device = "device_id_" + str(parent_device_id);
		device_bank_array = getattr(self, device + "_banks")
		active_bank_idx = getattr(self, device + "_active_bank")
		device_bank_params = getattr(self, device + "_bank_parameters_" + str(active_bank_idx))
		for index, val in enumerate(device_bank_array):
			bank_cnfg = getattr(self, val)
			bank_cnfg["LED_feedback"] = "custom"; 
			if index == active_bank_idx:
					if bank_cnfg.has_key("LED_on"):
						led_on = bank_cnfg["LED_on"]
						self.feedback_handler(bank_cnfg, led_on)
			else: 
				if bank_cnfg.has_key("LED_off"):
					led_off = bank_cnfg["LED_off"]
					self.feedback_handler(bank_cnfg, led_off)
		
		remove_mode = getattr(self, "_remove_mode" + active_mode + "_ui_listeners")
		remove_mode()
		activate_mode = getattr(self, "_mode" + active_mode + "_ui_listeners")
		activate_mode()
		for param in device_bank_params:
			fire_param_feedback = getattr(self, param + "_led_listener")
			fire_param_feedback()
	def listening_to_devices(self):
		global active_mode, prev_active_mode, modes
		self.log("device added")
		mode_to_call = getattr(self, "_remove_mode" + active_mode + "_led_listeners")
		mode_to_call()
		mode_to_call = getattr(self, "_mode" + active_mode + "_led_listeners")
		mode_to_call()
	def _selected_device_listener(self):
		global active_mode, prev_active_mode, modes
		self.log("selected device changed")
		mode_to_call = getattr(self, "_remove_mode" + active_mode + "_led_listeners")
		mode_to_call()
		mode_to_call = getattr(self, "_mode" + active_mode + "_led_listeners")
		mode_to_call()
		self.device_feedback()
	def device_feedback(self, mode_id=None):
		if (mode_id == None):
			global active_mode
			mode_id = active_mode
		config_map = "mode_" + str(mode_id) + "_configs_map"
		config_map = getattr(self, config_map)
		for config_name in config_map:
			config = getattr(self, config_name)
			if config.has_key("mapping_type") and config["mapping_type"] == "Device":
				led_on = config["LED_on"]
				led_off = config["LED_off"]
				try: 
					device = eval(config["module"])
				except:
					self.feedback_handler(config, led_off)
					return
				find = config["module"].find("selected_track")
				if find >= 0: 
					selected_device = self.song().view.selected_track.view.selected_device
					if device == selected_device:
						self.feedback_handler(config, led_on)
					else: 
						self.feedback_handler(config, led_off)
				else:
					for parent_name in config_map:
						parent_config = getattr(self, parent_name)
						if parent_config["json_id"] == config["parent_json_id"]:
							parent_track = parent_config["module"]
							break
					tracks_selected_device = eval(parent_track + ".view.selected_device")
					if device == tracks_selected_device:
						self.feedback_handler(config, led_on)
					else: 
						self.feedback_handler(config, led_off)
	def _on_selected_track_changed(self):
		global active_mode, prev_active_mode, modes
		self.log("selected track changed")
		mode_to_call = getattr(self, "_remove_mode" + active_mode + "_led_listeners")
		mode_to_call()
		mode_to_call = getattr(self, "_mode" + active_mode + "_led_listeners")
		mode_to_call()
		self.track_feedback()
		self.device_feedback()
		self.refresh_state()
	def track_feedback(self, mode_id=None):
		if (mode_id == None):
			global active_mode
			mode_id = active_mode
		config_map = "mode_" + str(mode_id) + "_configs_map"
		config_map = getattr(self, config_map)
		selected_track = self.song().view.selected_track
		for config_name in config_map:
			config = getattr(self, config_name)
			if config.has_key("mapping_type") and config["mapping_type"] == "Track":
				led_on = config["LED_on"]
				led_off = config["LED_off"]
				try: 
					track = eval(config["module"])
				except:
					self.feedback_handler(config, led_off)
					return
				if track == selected_track:
					self.feedback_handler(config, led_on)
				else: 
					self.feedback_handler(config, led_off)
	def _on_selected_scene_changed(self):
		global active_mode, prev_active_mode, modes
		self.show_message("selected scene changed")
		mode_to_call = getattr(self, "_remove_mode" + active_mode + "_led_listeners")
		mode_to_call()
		mode_to_call = getattr(self, "_mode" + active_mode + "_led_listeners")
		mode_to_call()
		self.refresh_state()
	def _all_tracks_listener(self):
		global active_mode, prev_active_mode, modes
		self.show_message("mode 1 tracks listener")
		mode_to_call = getattr(self, "_remove_mode" + active_mode + "_led_listeners")
		mode_to_call()
		mode_to_call = getattr(self, "_mode" + active_mode + "_led_listeners")
		mode_to_call()
	def all_track_device_listeners(self):
		numtracks = len(self.song().tracks)
		for index in range(numtracks):
			try:
				self.song().tracks[index].view.add_selected_device_listener(self._selected_device_listener)
				self.song().tracks[index].add_devices_listener(self.listening_to_devices)
			except:
				self.log("all_track_device_listeners exception")
		num_returns = len(self.song().return_tracks)
		for index in range(num_returns):
			try:
				self.song().return_tracks[index].view.add_selected_device_listener(self._selected_device_listener)
				self.song().return_tracks[index].add_devices_listener(self.listening_to_devices)
			except:
				self.log("all_track_device_listeners exception")	
		try:
			self.song().master_track.view.add_selected_device_listener(self._selected_device_listener)
			self.song().master_track.add_devices_listener(self.listening_to_devices)
		except:
			self.log("all_track_device_listeners exception")	
	def _remove_all_track_device_listeners(self):
		numtracks = len(self.song().tracks)
		for index in range(numtracks):
			try:
				self.song().tracks[index].view.remove_selected_device_listener(self._selected_device_listener)
				self.song().tracks[index].remove_devices_listener(self.listening_to_devices)
			except:
				self.log("_remove_all_track_device_listeners exception")
		num_returns = len(self.song().return_tracks)
		for index in range(num_returns):
			try:
				self.song().return_tracks[index].view.remove_selected_device_listener(self._selected_device_listener)
				self.song().return_tracks[index].remove_devices_listener(self.listening_to_devices)
			except:
				self.log("_remove_all_track_device_listeners exception")
		try:
			self.song().master_track.view.remove_selected_device_listener(self._selected_device_listener)
			self.song().master_track.remove_devices_listener(self.listening_to_devices)
		except:
			self.log("_remove_all_track_device_listeners exception")
	################################################
	############# Extra Functions ##################
	################################################
	def scroll_through_devices(self, cnfg):
		NavDirection = Live.Application.Application.View.NavDirection
		if cnfg["ctrl_type"] == "absolute":
			if cnfg["value"] > cnfg["pre_val"]:
				if cnfg["reverse_mode"] is False: 
					goto = "right"
				elif cnfg["reverse_mode"] is True:
					goto = "left"
				times = 1;
			elif cnfg["value"] < cnfg["pre_val"]:
				if cnfg["reverse_mode"] is False: 
					goto = "left"
				elif cnfg["reverse_mode"] is True:
					goto = "right"
				times = 1;
		elif cnfg["ctrl_type"] == "relative":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = "left"
				times = cnfg["steps"];
			elif cnfg["enc_second"] == cnfg["value"]:
				goto = "right"
				times = cnfg["steps"];
		elif cnfg["ctrl_type"] == "on/off":	
			if cnfg["enc_first"] == cnfg["value"]:
					goto = "right"
			elif cnfg["enc_second"] == cnfg["value"]:
					goto = "right"
		elif cnfg["ctrl_type"] == "increment":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = "right"
				times = cnfg["steps"];
		elif cnfg["ctrl_type"] == "decrement":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = "left"
				times = cnfg["steps"];
		if goto == "right":
			for x in range(0, times):
				self._scroll_device_chain(NavDirection.right)
		elif goto == "left":
			for x in range(0, times):
				self._scroll_device_chain(NavDirection.left)
	def _scroll_device_chain(self, direction):
		view = self.application().view
		if not view.is_view_visible('Detail') or not view.is_view_visible('Detail/DeviceChain'):
			view.show_view('Detail')
			view.show_view('Detail/DeviceChain')
		else:
			view.scroll_view(direction, 'Detail/DeviceChain', False)
	def selected_device_idx(self):
		self._device = self.song().view.selected_track.view.selected_device
		return self.tuple_index(self.song().view.selected_track.devices, self._device)
	def selected_track_idx(self):
		self._track = self.song().view.selected_track
		self._track_num = self.tuple_index(self.song().tracks, self._track)
		self._track_num = self._track_num + 1
		return self._track_num
	def selected_scene_idx(self):
		self._scene = self.song().view.selected_scene
		self._scene_num = self.tuple_index(self.song().scenes, self._scene)
		self._scene_num = self._scene_num + 1
		return self._scene_num
	def tuple_index(self, tuple, obj):
		for i in xrange(0, len(tuple)):
			if (tuple[i] == obj):
				return i
		return(False)
	def select_a_device(self, cnfg):
		parent_track = cnfg["parent_track"]
		device_chain = cnfg["device_chain"]
		chain_selector = "self.song().view.selected_track" + device_chain
		try:
			self.song().view.selected_track = eval(parent_track)
			try:
				self.song().view.select_device(eval(chain_selector))
			except IndexError:
				self.show_message("Device you are trying to select does not exist on track.") 
		except IndexError:
			self.show_message("Track does not exist for the device you are selecting.")
	def a_b_crossfade_assign(self, cnfg):
		assignment_type = cnfg['assignment_type']; 
		if(assignment_type == "Scroll"):
			goto = self.scroll_a_b_assign(cnfg);
			if goto > 2:
				goto = 2
		elif cnfg["enc_first"] == cnfg["value"]:
			if assignment_type == "Select A":
				goto = 0
			elif assignment_type == "Select None":
				goto = 1
			elif assignment_type == "Select B":
				goto = 2
			else:
				goto = 0
		setattr(eval(str(cnfg['parent_track']) + ".mixer_device"), "crossfade_assign", goto)
	def scroll_a_b_assign(self, cnfg):
		should_it_fire = self.should_it_fire(cnfg)
		if(should_it_fire != 1):
			return
		current_assigned_value = eval(str(cnfg['parent_track']) + ".mixer_device.crossfade_assign")
		length = 3
		if cnfg["ctrl_type"] == "absolute":
			divider = (cnfg["enc_second"] - cnfg["enc_first"]) / length
			goto = int(cnfg["value"] / divider) 
			if cnfg["reverse_mode"] is True:
				if(goto >= 2):
					goto = 0
				elif(goto == 0):
					goto = 2
			goto = int(goto)
		elif cnfg["ctrl_type"] == "relative":
			self.log_message("csslog: relative");
			if cnfg["enc_first"] == cnfg["value"] and current_assigned_value > 0:
				goto = current_assigned_value - 1
			elif cnfg["enc_second"] == cnfg["value"] and current_assigned_value < 2:
				goto = current_assigned_value + 1
		elif cnfg["ctrl_type"] == "on/off":	
			if current_assigned_value < 2:
				goto = current_assigned_value + 1
			elif current_assigned_value >= 2:
				goto = 0
		elif cnfg["ctrl_type"] == "increment":
			if current_assigned_value < 2:
				goto = current_assigned_value + 1
			else: 
				goto = current_assigned_value
		elif cnfg["ctrl_type"] == "decrement":
			if current_assigned_value > 0:
				goto = current_assigned_value - 1
			else: 
				goto = current_assigned_value
		return int(goto)
	def scroll_highlight(self, cnfg):
		if cnfg["tracks_scenes"] == "tracks":
			length = len(self.song().tracks) - 1
			selected = self.selected_track_idx() - 1
		elif cnfg["tracks_scenes"] == "scenes":
			length = len(self.song().scenes)
			selected = self.selected_scene_idx() - 1
		else: 
			self.log("scroll_highlight error, tracks_scenes was not set")
		if cnfg["ctrl_type"] == "absolute":
			divider = (cnfg["enc_second"] - cnfg["enc_first"]) / length
			if cnfg["reverse_mode"] is False:
				goto = cnfg["value"] / divider
			elif cnfg["reverse_mode"] is True:
				goto = (divider * length) / cnfg["value"]
			goto = int(goto)
		elif cnfg["ctrl_type"] == "relative":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = selected - cnfg["steps"]
			elif cnfg["enc_second"] == cnfg["value"]:
				goto = selected + cnfg["steps"]
		elif cnfg["ctrl_type"] == "on/off":	
			if cnfg["enc_first"] == cnfg["value"]:
				goto = length
			elif cnfg["enc_second"] == cnfg["value"]:
				goto = 0
		elif cnfg["ctrl_type"] == "increment":
			goto = selected + cnfg["steps"]
		elif cnfg["ctrl_type"] == "decrement":
			goto = selected - cnfg["steps"]
		if goto <= length and goto >= 0 and goto != selected:
			cnfg["highlight_number"] = goto
			self.select_highlight(cnfg)
	def select_sess_offset(self, cnfg):
		try:
			self._session
		except:
			self.show_message("There's no Session Box to select, buddy.")
			return
		tracks_scenes = cnfg["tracks_scenes"]
		track_offset = self._session.track_offset()
		scene_offset = self._session.scene_offset()
		if tracks_scenes == "tracks":
			track_offset = cnfg["highlight_number"]
		elif tracks_scenes == "scenes":
			scene_offset = cnfg["highlight_number"]
		try:
			self._session.set_offsets(track_offset, scene_offset)
			self._session._reassign_scenes()
			self.set_highlighting_session_component(self._session)
			self.refresh_state()
		except:
			self.show_message("unable to move session box there.")
	def scroll_sess_offset(self, cnfg):
		try:
			self._session
		except:
			self.show_message("There's no Session Box to scroll, buddy.")
			return
		tracks_scenes = cnfg["tracks_scenes"]
		track_offset = self._session.track_offset()
		scene_offset = self._session.scene_offset()
		if cnfg["tracks_scenes"] == "tracks":
			length = len(self.song().tracks)
			selected = track_offset
		elif cnfg["tracks_scenes"] == "scenes":
			length = len(self.song().scenes)
			selected = scene_offset
		else: 
			self.log("scroll_sess_offset error, tracks_scenes was not set")
		if cnfg["ctrl_type"] == "absolute":
			divider = (cnfg["enc_second"] - cnfg["enc_first"]) / length
			goto = cnfg["value"] / divider
			if cnfg["reverse_mode"] is True:
				goto = length - goto
			goto = int(goto)
		elif cnfg["ctrl_type"] == "relative":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = selected - cnfg["steps"]
			elif cnfg["enc_second"] == cnfg["value"]:
				goto = selected + cnfg["steps"]
		elif cnfg["ctrl_type"] == "on/off":	
			if cnfg["enc_first"] == cnfg["value"] or cnfg["enc_second"] == cnfg["value"]:
				if selected != 0 and selected != length - 1:
					goto = length - 1
				elif selected == 0:
					goto = length - 1
				else: 
					goto = 0				
		elif cnfg["ctrl_type"] == "increment":
			goto = selected + cnfg["steps"]
		elif cnfg["ctrl_type"] == "decrement":
			goto = selected - cnfg["steps"]
		if cnfg["tracks_scenes"] == "tracks":
			track_offset = goto
		elif cnfg["tracks_scenes"] == "scenes":
			scene_offset = goto
		try:
			self._session.set_offsets(track_offset, scene_offset)
			self._session._reassign_scenes()
			self.set_highlighting_session_component(self._session)
			self.refresh_state()
		except:
			self.show_message("unable to move session box there.")
	def select_highlight(self, cnfg):
		tracks_scenes = cnfg["tracks_scenes"]
		change_to = cnfg["highlight_number"] 
		if tracks_scenes == "tracks":
			num_of_tracks_scenes = len(self.song().tracks)
		elif tracks_scenes == "scenes":
			num_of_tracks_scenes = len(self.song().scenes)
		if num_of_tracks_scenes >= change_to + 1:
			if tracks_scenes == "tracks":
				self.song().view.selected_track = self.song().tracks[change_to]
			elif tracks_scenes == "scenes":
				self.song().view.selected_scene = self.song().scenes[change_to]
		else: 
			self.show_message("Your Session doesn't have " + str(change_to + 1) + " " + tracks_scenes)
	def scroll_active_device_bank(self, cnfg):
		device_id = cnfg["parent_device_id"]
		device = "device_id_" + str(device_id);
		active_bank = getattr(self, device + "_active_bank")
		banks = getattr(self, device + "_banks")
		length = len(banks) - 1
		if cnfg["ctrl_type"] == "absolute":
			divider = (cnfg["enc_second"] - cnfg["enc_first"]) / length
			if cnfg["reverse_mode"] is False:
				goto = cnfg["value"] / divider
			elif cnfg["reverse_mode"] is True:
				goto = (divider * length) / cnfg["value"]
			goto = int(goto)
		elif cnfg["ctrl_type"] == "relative":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = active_bank - 1
			elif cnfg["enc_second"] == cnfg["value"]:
				goto = active_bank + 1
		elif cnfg["ctrl_type"] == "on/off":
			if cnfg["switch_type"] == "toggle":	
				if cnfg["enc_first"] == cnfg["value"]:
					goto = length
				elif cnfg["enc_second"] == cnfg["value"]:
					goto = 0
			elif active_bank == length:
				goto = 0
			else:  
				goto = length
		elif cnfg["ctrl_type"] == "increment":
				goto = active_bank + 1
		elif cnfg["ctrl_type"] == "decrement":
				goto = active_bank - 1
		if goto <= length and goto >= 0 and goto != active_bank:
			cnfg["banking_number"] = goto
			self.change_active_device_bank(cnfg)
	def change_active_device_bank(self, cnfg):
		global active_mode
		device_id = cnfg["parent_device_id"]
		change_to_bank = cnfg["banking_number"]
		device = "device_id_" + str(device_id);
		bank_names = getattr(self, device + "_bank_names")
		length = len(bank_names) - 1; 
		if change_to_bank <= length:
			setattr(self, device + "_active_bank", change_to_bank)
			self.bank_led_feedback(cnfg["parent_json_id"]);
			self.show_message("changed active bank to: " + bank_names[change_to_bank])
		elif change_to_bank > length:
			self.show_message("device does not have " + str(change_to_bank + 1) + " parameter banks set")
		fire_all_mode_feedback = getattr(self, "_mode" + active_mode + "_fire_all_feedback")
		fire_all_mode_feedback()
	def session_box(self, num_tracks, num_scenes, track_offset, scene_offset, clips, stop_all, stop_tracks, scene_launch, feedbackArr, combination_mode):
		self._session = SessionComponent(num_tracks, num_scenes)
		self._session.set_offsets(track_offset, scene_offset)
		self._session.add_offset_listener(self._on_session_offset_changes, identify_sender= False)
		self._session._reassign_scenes()
		self.set_highlighting_session_component(self._session)
		if clips: 
			self._grid = ButtonMatrixElement(rows=[clips[(index*num_tracks):(index*num_tracks)+num_tracks] for index in range(num_scenes)])
			self._session.set_clip_launch_buttons(self._grid)
		if stop_all:
			self._session.set_stop_all_clips_button(stop_all)
		if stop_tracks:
			self._session.set_stop_track_clip_buttons(tuple(stop_tracks))
		if scene_launch:
			scene_launch_buttons = ButtonMatrixElement(rows=[scene_launch])
			self._session.set_scene_launch_buttons(scene_launch_buttons)
			self._session.set_stop_clip_triggered_value(feedbackArr["StopClipTriggered"])
			self._session.set_stop_clip_value(feedbackArr["StopClip"])
		for scene_index in range(num_scenes):
			scene = self._session.scene(scene_index)
			scene.set_scene_value(feedbackArr["Scene"])
			scene.set_no_scene_value(feedbackArr["NoScene"])
			scene.set_triggered_value(feedbackArr["SceneTriggered"])
			for track_index in range(num_tracks):
				clip_slot = scene.clip_slot(track_index)
				clip_slot.set_triggered_to_play_value(feedbackArr["ClipTriggeredPlay"])
				clip_slot.set_triggered_to_record_value(feedbackArr["ClipTriggeredRecord"])
				clip_slot.set_record_button_value(feedbackArr["RecordButton"])
				clip_slot.set_stopped_value(feedbackArr["ClipStopped"])
				clip_slot.set_started_value(feedbackArr["ClipStarted"])
				clip_slot.set_recording_value(feedbackArr["ClipRecording"])
			for index in range(len(stop_tracks)):
				stop_track_button = stop_tracks[index]
				if feedbackArr["StopTrackPlaying"] and feedbackArr["StopTrackStopped"]:
					stop_track_button.set_on_off_values(feedbackArr["StopTrackPlaying"], feedbackArr["StopTrackStopped"])
			if stop_all:
				if feedbackArr["StopAllOn"] and feedbackArr["StopAllOff"]:
					stop_all.set_on_off_values(feedbackArr["StopAllOn"], feedbackArr["StopAllOff"])
		if combination_mode == "on":
			self._session._link()
		self.refresh_state()
	def _on_session_offset_changes(self):
		global active_mode
		try:
			remove_mode = getattr(self, "_remove_mode" + active_mode + "_led_listeners")
			remove_mode()
			activate_mode = getattr(self, "_mode" + active_mode + "_led_listeners")
			activate_mode()
		except:
			self.log("_on_session_offset_changes: could not remove / add led_listeners")
			return;
	def remove_session_box(self, combination_mode): 
		if hasattr(self, "_session"):
			self.current_track_offset = self._session._track_offset
			self.current_scene_offset = self._session._scene_offset
			self._session.set_clip_launch_buttons(None)
			self.set_highlighting_session_component(None)
			self._session.set_stop_all_clips_button(None)
			self._session.set_stop_track_clip_buttons(None)
			self._session.set_scene_launch_buttons(None)
			if combination_mode == "on":
				self._session._unlink()
			self._session = None
	def scroll_modes(self, cnfg):
		controller = getattr(self, cnfg["attached_to"])
		cnfg["value"] = controller.cur_val 
		if cnfg["ctrl_type"] == "absolute":
			divider = (cnfg["enc_second"] - cnfg["enc_first"]) / (len(self.modes) - 1)
			if cnfg["reverse_mode"] is False:
				goto = cnfg["value"] / divider
			elif cnfg["reverse_mode"] is True:
				length = len(self.modes) - 1
				goto = (divider * length) / cnfg["value"]
			goto = int(goto)
		elif cnfg["ctrl_type"] == "relative":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = self.key_num - 1
			elif cnfg["enc_second"] == cnfg["value"]:
				goto = self.key_num + 1
		elif cnfg["ctrl_type"] == "on/off":	
			if cnfg["enc_first"] == cnfg["value"]:
				goto = len(self.modes) - 1
			elif cnfg["enc_second"] == cnfg["value"]:
				goto = 0
		elif cnfg["ctrl_type"] == "increment":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = self.key_num + 1
		elif cnfg["ctrl_type"] == "decrement":
			if cnfg["enc_first"] == cnfg["value"]:
				goto = self.key_num - 1
		if goto <= len(self.modes) and goto >= 0 and active_mode != self.modes[goto]:
			self.set_active_mode(self.modes[goto])
	def listening_to_tracks(self):
		global active_mode
		self.remove_listening_to_tracks()
		for index in range(len(self.song().tracks)):
			_track = self.song().tracks[index]
			if _track.can_be_armed and hasattr(self, "_mode" + active_mode + "_arm_listener"):
				_track.add_arm_listener(getattr(self, "_mode" + active_mode + "_arm_listener"))
			if hasattr(self, "_mode" + active_mode + "_mute_listener"):
				_track.add_mute_listener(getattr(self, "_mode" + active_mode + "_mute_listener"))
			if hasattr(self, "_mode" + active_mode + "_solo_listener"):
				_track.add_solo_listener(getattr(self, "_mode" + active_mode + "_solo_listener"))
			if hasattr(self, "_mode" + active_mode + "_volume_listener"):
				_track.mixer_device.volume.add_value_listener(getattr(self, "_mode" + active_mode + "_volume_listener"))
			if hasattr(self, "_mode" + active_mode + "_panning_listener"):
				_track.mixer_device.panning.add_value_listener(getattr(self, "_mode" + active_mode + "_panning_listener"))
			if hasattr(self, "_mode" + active_mode + "_send_listener"):
				for send_index in range(len(_track.mixer_device.sends)):
					_track.mixer_device.sends[send_index].add_value_listener(getattr(self, "_mode" + active_mode + "_send_listener"))
		for index in range(len(self.song().return_tracks)):
			_return_track = self.song().return_tracks[index]
			if hasattr(self, "_mode" + active_mode + "_mute_listener"):
				_return_track.add_mute_listener(getattr(self, "_mode" + active_mode + "_mute_listener"))
			if hasattr(self, "_mode" + active_mode + "_solo_listener"):
				_return_track.add_solo_listener(getattr(self, "_mode" + active_mode + "_solo_listener"))
			if hasattr(self, "_mode" + active_mode + "_volume_listener"):
				_return_track.mixer_device.volume.add_value_listener(getattr(self, "_mode" + active_mode + "_volume_listener"))
			if hasattr(self, "_mode" + active_mode + "_panning_listener"):
				_return_track.mixer_device.panning.add_value_listener(getattr(self, "_mode" + active_mode + "_panning_listener"))
			if hasattr(self, "_mode" + active_mode + "_send_listener"):
				for send_index in range(len(_return_track.mixer_device.sends)):
					_return_track.mixer_device.sends[send_index].add_value_listener(getattr(self, "_mode" + active_mode + "_send_listener"))
		_master = self.song().master_track
		if hasattr(self, "_mode" + active_mode + "_volume_listener"):
			_master.mixer_device.volume.add_value_listener(getattr(self, "_mode" + active_mode + "_volume_listener"))
		if hasattr(self, "_mode" + active_mode + "_panning_listener"):
			_master.mixer_device.panning.add_value_listener(getattr(self, "_mode" + active_mode + "_panning_listener"))
	def remove_listening_to_tracks(self):
		global active_mode
		for index in range(len(self.song().tracks)):
			_track = self.song().tracks[index]
			if hasattr(self, "_mode" + active_mode + "_arm_listener"):
				if _track.arm_has_listener(getattr(self, "_mode" + active_mode + "_arm_listener")):
					_track.remove_arm_listener(getattr(self, "_mode" + active_mode + "_arm_listener"))
			if hasattr(self, "_mode" + active_mode + "_mute_listener"):
				if _track.mute_has_listener(getattr(self, "_mode" + active_mode + "_mute_listener")):
					_track.remove_mute_listener(getattr(self, "_mode" + active_mode + "_mute_listener"))
			if hasattr(self, "_mode" + active_mode + "_solo_listener"):
				if _track.solo_has_listener(getattr(self, "_mode" + active_mode + "_solo_listener")):
					_track.remove_solo_listener(getattr(self, "_mode" + active_mode + "_solo_listener"))
			if hasattr(self, "_mode" + active_mode + "_volume_listener"):
				if _track.mixer_device.volume.value_has_listener(getattr(self, "_mode" + active_mode + "_volume_listener")):
					_track.mixer_device.volume.remove_value_listener(getattr(self, "_mode" + active_mode + "_volume_listener"))
			if hasattr(self, "_mode" + active_mode + "_panning_listener"):
				if _track.mixer_device.panning.value_has_listener(getattr(self, "_mode" + active_mode + "_panning_listener")):
					_track.mixer_device.panning.remove_value_listener(getattr(self, "_mode" + active_mode + "_panning_listener"))
			if hasattr(self, "_mode" + active_mode + "_send_listener"):
				for send_index in range(len(_track.mixer_device.sends)):
					if _track.mixer_device.sends[send_index].value_has_listener(getattr(self, "_mode" + active_mode + "_send_listener")):
						_track.mixer_device.sends[send_index].remove_value_listener(getattr(self, "_mode" + active_mode + "_send_listener"))
		for index in range(len(self.song().return_tracks)):
			_return_track = self.song().return_tracks[index]
			if hasattr(self, "_mode" + active_mode + "_mute_listener"):
				if _return_track.mute_has_listener(getattr(self, "_mode" + active_mode + "_mute_listener")):
					_return_track.remove_mute_listener(getattr(self, "_mode" + active_mode + "_mute_listener"))
			if hasattr(self, "_mode" + active_mode + "_solo_listener"):
				if _return_track.solo_has_listener(getattr(self, "_mode" + active_mode + "_solo_listener")):
					_return_track.remove_solo_listener(getattr(self, "_mode" + active_mode + "_solo_listener"))
			if hasattr(self, "_mode" + active_mode + "_volume_listener"):
				if _return_track.mixer_device.volume.value_has_listener(getattr(self, "_mode" + active_mode + "_volume_listener")):
					_return_track.mixer_device.volume.remove_value_listener(getattr(self, "_mode" + active_mode + "_volume_listener"))
			if hasattr(self, "_mode" + active_mode + "_panning_listener"):
				if _return_track.mixer_device.panning.value_has_listener(getattr(self, "_mode" + active_mode + "_panning_listener")):
					_return_track.mixer_device.panning.remove_value_listener(getattr(self, "_mode" + active_mode + "_panning_listener"))
			if hasattr(self, "_mode" + active_mode + "_send_listener"):
				for send_index in range(len(_return_track.mixer_device.sends)):
					if _return_track.mixer_device.sends[send_index].value_has_listener(getattr(self, "_mode" + active_mode + "_send_listener")):
						_return_track.mixer_device.sends[send_index].remove_value_listener(getattr(self, "_mode" + active_mode + "_send_listener"))
		_master = self.song().master_track
		if hasattr(self, "_mode" + active_mode + "_volume_listener"):
			if _master.mixer_device.volume.value_has_listener(getattr(self, "_mode" + active_mode + "_volume_listener")):
				_master.mixer_device.volume.remove_value_listener(getattr(self, "_mode" + active_mode + "_volume_listener"))
		if hasattr(self, "_mode" + active_mode + "_panning_listener"):
			if _master.mixer_device.panning.value_has_listener(getattr(self, "_mode" + active_mode + "_panning_listener")):
				_master.mixer_device.panning.remove_value_listener(getattr(self, "_mode" + active_mode + "_panning_listener"))
	def set_active_mode(self, activate_new_mode):
		global active_mode, prev_active_mode, modes
	
		for number, mode_id in self.modes.items():
			if mode_id == activate_new_mode:
				self.key_num = mode_id
		if(activate_new_mode == "Previous Mode"):
			if 'prev_active_mode' not in globals():
				self.show_message("No previous mode is set yet.")
			else:
				remove_mode = getattr(self, "_remove_mode" + active_mode)
				remove_mode()
				activate_new_mode = prev_active_mode
				prev_active_mode = active_mode
				active_mode = activate_new_mode
				mode_to_call = getattr(self, "_mode" + activate_new_mode)
				mode_to_call()
		else:
			if 'active_mode' in globals():
				remove_mode = getattr(self, "_remove_mode" + active_mode)
				remove_mode()
				prev_active_mode = active_mode
			active_mode = activate_new_mode 
			mode_to_call = getattr(self, "_mode" + activate_new_mode)
			mode_to_call()
	def disconnect(self):
		super(css_bd_live_rig_controller_v1, self).disconnect()
