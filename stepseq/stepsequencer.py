import time
import traceback

import launchpad_py as launchpad
from stepseq import StepSequencer, PadMapper
from input_listener import InputListener
from colors import ColorMapper
from midi import MidiSender

def main():
    try:
        pad = launchpad.LaunchpadMk2()
        pad.Open()
        pad.Reset()
    except:
        pad = None
    try:
        color_mapper = ColorMapper()
        pad_mapper = PadMapper(pad, color_mapper, use_pad=bool(pad))
        midi_sender = MidiSender()

        seq = StepSequencer(pad_mapper, midi_sender, bpm=100)
        listener = InputListener(pad, seq)

        if not pad:
            # test pattern
            seq.updateState(7, 0)
            seq.updateState(5, 2)
            seq.updateState(7, 4)
            seq.updateState(5, 6)
            seq.updateState(4, 7)

            seq.updateState(1, 0)
            seq.updateState(1, 2)
            seq.updateState(1, 4)
            seq.updateState(1, 6)
        while True:
            pass

    except KeyboardInterrupt:
        print("Stopping sequencer...")
    except Exception as e:
        traceback.print_exc()
    finally:
        seq.stop()
        listener.stop()
        midi_sender.stop()
        if pad:
            pad.Reset()
            pad.Close()

main()