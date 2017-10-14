import time

from Queue import Queue
from threading import Thread
from collections import namedtuple

from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import NOTE_ON, NOTE_OFF


MidiNote = Point = namedtuple('MidiNote', ['channel', 'note', 'duration', 'velocity'], verbose=True)


class MidiNoteWorker(Thread):
   
    def __init__(self, id, queue, midiout):
        Thread.__init__(self)
        self.daemon = True
        self.id = id
        self.stopped = False
        self.midiout = midiout
        self.queue = queue
        self.last_note = None

    def run(self):
        print("Starting note worker %s" % self.id)
        while not self.stopped:
            # Get the work from the queue and expand the tuple
            note = self.queue.get()
            if not note:
                # sentinel: exit worker
                self.stop()
                return
            self.sendNote(note)
            self.last_note = note
            self.queue.task_done()

    def sendNote(self, note):
        note_on = [NOTE_ON | note.channel + 1, note.note, note.velocity]
        self.midiout.send_message(note_on)
        time.sleep(note.duration)
        note_off = [NOTE_OFF | note.channel + 1, note.note, 0]
        self.midiout.send_message(note_off)

    def stop(self):
        self.stopped = True
        if self.last_note:
            note_off = [NOTE_OFF | self.last_note.channel + 1, self.last_note.note, 0]
            self.midiout.send_message(note_off)


class MidiSender(object):

    def __init__(self, polyphony=16, base_note=36, midi_port=2):
        self.polyphony = polyphony
        self.workers = []
        self.base_note = base_note
        self.midiout, port_name = open_midioutput(midi_port,
                                                  client_name="GamePad Step Sequencer",
                                                  port_name="MIDI Out")
        self._initWorkers(polyphony)

    def _initWorkers(self, polyphony):
        self.queue = Queue()
        for i in range(polyphony):
            worker = MidiNoteWorker(i, self.queue, self.midiout)
            worker.start()
            self.workers.append(worker)

    def sendNote(self, channel, row, duration):
        note = self.base_note + (7 - row)
        note = MidiNote(channel=channel,
                        note=note,
                        duration=duration,
                        velocity=127)
        self.queue.put(note)

    def stop(self):
        for _ in range(len(self.workers)):
            # send sentinel to stop worker
            self.queue.put(None)
