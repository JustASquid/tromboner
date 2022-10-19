import datetime
import time

class FPS:
	def __init__(self):
		# store the start time, end time, and total number of frames
		# that were examined between the start and end intervals
		self._start = None
		self._end = None
		self._numFrames = 0

	def start(self):
		# start the timer
		self._start = datetime.datetime.now()
		return self

	def stop(self):
		# stop the timer
		self._end = datetime.datetime.now()

	def update(self):
		# increment the total number of frames examined during the
		# start and end intervals
		self._numFrames += 1

	def elapsed(self):
		# return the total number of seconds between the start and
		# end interval
		return (self._end - self._start).total_seconds()

	def fps(self):
		# compute the (approximate) frames per second
		return self._numFrames / self.elapsed()

class PeriodFPS:
	def __init__(self, buffer_size):
		self._frame_times = []
		self._buffer_size = buffer_size
		self._last_frame_time = time.perf_counter()

	def update(self):
		cur_time = time.perf_counter()
		elapsed = cur_time - self._last_frame_time
		self._frame_times.append(elapsed)
		if len(self._frame_times) > self._buffer_size:
			self._frame_times.pop(0)
		self._last_frame_time = cur_time

	def get_fps(self):
		avg_time = sum(self._frame_times) / len(self._frame_times)
		return 1.0 / avg_time