import threading

import pyaudio
import audioop
import traceback
import sys
import numpy as np

from util import map_value

# =========================== CALIBRATION AND SETTINGS =========================

# Set this to the maximum RMS of the audio (for plotting purposes)
MAX_RMS = 10000

# This defines the threshold for audio control
# (represented as a yellow line on the plot)
THRESHOLD_RMS = 1800

# ==============================================================================

CHUNK = 256
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

DATA_MAX_LENGTH = 500


AUDIO_GRAPH_HEIGHT = 200
AUDIO_GRAPH_WIDTH = DATA_MAX_LENGTH
AUDIO_GRAPH_CHANNELS = 3

class AudioGraph:
    def __init__(self):
        self.array = np.zeros(dtype=np.float32, shape=(AUDIO_GRAPH_HEIGHT, AUDIO_GRAPH_WIDTH, AUDIO_GRAPH_CHANNELS))

    def update(self, audio_data):
        self.array.fill(0)

        for x, vol in enumerate(audio_data):
            y = int(map_value(vol, 0, MAX_RMS, 0, AUDIO_GRAPH_HEIGHT))
            self.array[:y, x, :] = (255, 0, 0)

        # Draw threshold line
        threshold_y = int(map_value(THRESHOLD_RMS, 0, MAX_RMS, 0, AUDIO_GRAPH_HEIGHT))
        self.array[threshold_y, :, :] = (0, 255, 255)

class AudioHandler(threading.Thread):
    def __init__(self):
        super().__init__()
        self._p = pyaudio.PyAudio()
        self._stop_event = threading.Event()
        self._exception_info = None
        self._data = []

    def run(self):
        stream = None
        try:
            stream = self._p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)

            while True:
                data = stream.read(CHUNK)
                rms = audioop.rms(data, 2)
                rms = min(rms, MAX_RMS)
                self._data.append(rms)
                if len(self._data) > DATA_MAX_LENGTH:
                    self._data.pop(0)

                if self._stop_event.is_set():
                    break
        except Exception as e:
            tb = traceback.format_exc()
            self._exception_info = (e, tb)
        finally:
            if stream is not None:
                stream.stop_stream()
                stream.close()
            self._p.terminate()

    def check_exception(self):
        if self._exception_info:
            e, tb = self._exception_info
            print(tb, file = sys.stderr)
            raise e

    def get_data(self):
        return self._data

    def is_past_threshold(self):
        return self._data[-1] > THRESHOLD_RMS

    def get_current_rms(self):
        return self._data[-1]

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_event.set()
        self.join()



