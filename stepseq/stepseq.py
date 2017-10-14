import time

from threading import Thread
from colors import ColorMapper


class SequencerState(object):

    def __init__(self, size=8):
        self.size = size
        self.state = [[False] * self.size for i in range(self.size)]

    def updateState(self, x, y): 
        self.state[x][y] = not self.state[x][y]

    def draw(self):
        for row in self.state:
            print("\n")
            for val in row:
                if val:
                    print('[X]'),
                else:
                    print('[.]'),
        print("\n")
        print("-" * self.size * 2)

    def iterateState(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                val = self.state[i][j] 
                if val:
                    yield j, i

    def iterateBeat(self, beat):
        for i in range(0, self.size):
            val = self.state[i][beat]
            if val:
                yield i

class PadMapper(object):

    def __init__(self, pad, colors, use_pad=True):
        self.pad = pad
        self.colors = colors
        self.use_pad = use_pad

    def newBeat(self):
        if not self.use_pad:
            return
        self.pad.Reset()

    def drawCurrentBeat(self, beat):
        if not self.use_pad:
            return
        for i in range(0, 8):
            x, y = self._mapCoords(beat, i)
            self.pad.LedCtrlXYByCode(x, y, self.colors.beat_line_color)

    def drawChannelBar(self, channels):
        for channel in channels:
            self.pad.LedCtrlXYByCode(channel.id, 0, channel.color)            

    def drawState(self, channel):
        if not self.use_pad:
            return
        for i, j in channel.state.iterateState():
            x, y = self._mapCoords(i, j)
            self.pad.LedCtrlXYByCode(x, y, channel.color)

    def _mapCoords(self, x, y):
        return x, y + 1


class InstrumentChannel(object):

    def __init__(self, id):
        self.id = id
        self.color = ColorMapper.getChannelColor(id)
        self.state = SequencerState()


class StepSequencer(Thread):

    def __init__(self, pad_mapper, midi_sender, bpm=120):
        Thread.__init__(self)
        self.pad = pad_mapper
        self.midi_sender = midi_sender
        self.stopped = False
        self.bpm = bpm
        self.interval = 15.0 / self.bpm
        self.daemon = True
        self.num_beats = 0
        self.beats_per_bar = 8  # assume 4/4, with 1/8 resolution
        self.beat_in_bar = 0
        self.channels = {}
        self.current_channel = 0
        self._initChannels()
        self.start()

    def _initChannels(self, num_channels=8):
        for i in range(0, num_channels):
            channel = InstrumentChannel(i)
            self.channels[i] = channel

    def run(self):
        self.started = time.time()
        while not self.stopped:
            self.beat_in_bar = (self.beat_in_bar + 1) % self.beats_per_bar
            self.num_beats += 1
            self.draw()
            # avoid accumulating tempo drift by computing next beat time
            next_time = self.started + self.num_beats * self.interval
            wait_time = max(0, next_time - time.time())
            self.sendMidi(wait_time)
            if wait_time:
                time.sleep(wait_time)

    def draw(self):
        channel = self.currentChannel()
        # channel.state.draw()
        self.pad.newBeat()
        self.pad.drawChannelBar(self.channels.values())
        self.pad.drawCurrentBeat(self.beat_in_bar)
        self.pad.drawState(channel)

    def currentChannel(self):
        return self.channels[self.current_channel]

    def sendMidi(self, duration):
        for channel in self.channels.itervalues():
            for i in channel.state.iterateBeat(self.beat_in_bar):
                self.midi_sender.sendNote(channel.id, i, duration)

    def updateState(self, x, y):
        channel = self.currentChannel()
        channel.state.updateState(x, y)

    def updateCurrentChannel(self, channel):
        self.current_channel = channel
        self.draw()

    def stop(self):
        self.stopped = True