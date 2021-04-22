"""
https://dolby.io/blog/capturing-high-quality-audio-with-python-and-pyaudio
"""

import wave
from typing import List

from pyaudio import PyAudio

from scrambler.audio_streams import get_api_by_name, open_stream, CHUNK_SIZE


def run_experiment(p, experiment) -> None:
	"""
	:param p: instance of PyAudio
	:param experiment: the name of the experiment from {valid_experiments}
	:return:
	"""
	valid_experiments = ["wave", "echo", "mix"]
	assert experiment in valid_experiments
	wave_file_enabled = experiment in ["wave", "mix"]
	input_enabled = experiment in ["echo", "mix"]

	channels = None
	sample_width = None
	sample_rate = None
	chunk_size = CHUNK_SIZE

	wave_file = None
	if wave_file_enabled:
		# Wave files
		waves: List[wave.Wave_read] = [
			wave.open(path, 'rb') for path in [
				"spiritus_lumina/audio/mass.wav",
				"spiritus_lumina/audio/mass48.wav"
			]
		]
		info = [
			{
				"framerate": wave_file.getframerate(),
				"compname": wave_file.getcompname(),
				"comptype": wave_file.getcomptype(),
				"fp": wave_file.getfp(),
				# "mark": wave_file.getmark(),
				"markers": wave_file.getmarkers(),
				"nchannels": wave_file.getnchannels(),
				"nframes": wave_file.getnframes(),
				"params": wave_file.getparams(),
				"sampwidth": wave_file.getsampwidth(),
			} for wave_file in waves
		]
		wave_file = waves[1]  # todo add variable
		channels = wave_file.getnchannels()
		sample_rate = wave_file.getframerate()
		sample_width = wave_file.getsampwidth()

	# Audio device setup
	api_info = get_api_by_name(p, "ASIO")
	# api_info = p.get_default_host_api_info()

	input_device_info = p.get_device_info_by_index(api_info["defaultInputDevice"])
	output_device_info = p.get_device_info_by_index(api_info["defaultOutputDevice"])

	input_stream = None
	if input_enabled:
		input_stream = open_stream(p, input_device_info, True,
			channels=channels,
			sample_width=sample_width,
			sample_rate=sample_rate,
			chunk_size=chunk_size,
		)

	output_stream = open_stream(p, output_device_info, False,
			channels=channels,
			sample_width=sample_width,
			sample_rate=sample_rate,
			chunk_size=chunk_size,
	)

	wave_buffer = None
	input_buffer = None
	buffer = None
	while True:
		if wave_file_enabled:
			assert wave_file is not None
			wave_buffer = wave_file.readframes(chunk_size)
			if not wave_buffer:
				break
		elif input_enabled:
			assert input_stream is not None
			input_buffer = input_stream.read(chunk_size)

		if experiment == "wave":
			assert wave_buffer is not None
			buffer = wave_buffer
		elif experiment == "echo":
			assert input_buffer is not None
			buffer = input_buffer
		elif experiment == "mix":
			assert wave_file is not None
			assert input_buffer is not None
			buffer = wave_buffer + input_buffer

		output_stream.write(buffer)

	output_stream.stop_stream()
	output_stream.close()


def main() -> None:
	p = PyAudio()
	try:
		info_device = [p.get_device_info_by_index(i) for i in range(0, p.get_device_count())]
		info_api = [p.get_host_api_info_by_index(i) for i in range(0, p.get_host_api_count())]
		run_experiment(p, "echo")
	finally:
		p.terminate()


if __name__ == "__main__":
	main()
