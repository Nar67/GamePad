import time

from Queue import Queue
from threading import Thread


class InputListener(Thread):

    def __init__(self, pad, sequencer):
        Thread.__init__(self)
        self.daemon = True
        self.stopped = False
        self.pad = pad
        self.sequencer = sequencer
        self.start()

    def run(self):
        if not self.pad:
            return
        while not self.stopped:
            state = self.pad.ButtonStateXY()
            if state:
                x, y, pressed = state
                if self._isChannelButton(x, y):
                    self.sequencer.updateCurrentChannel(x)
                else:
                    if pressed:
                        self.sequencer.updateState(y - 9, x)

    def _isChannelButton(self, x, y):
        return y == 0

    def stop(self):
        self.stopped = True
            