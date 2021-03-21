import wave
from typing import List

from pyaudio import PyAudio


# https://dolby.io/blog/capturing-high-quality-audio-with-python-and-pyaudio

CHUNK = 1024


def get_asio_device_index(p: PyAudio) -> int:
	"""returns the index of the ASIO device"""
	info_api = [p.get_host_api_info_by_index(i) for i in range(0, p.get_host_api_count())]

	asio_api_info = None
	for api in info_api:
		if api["name"] == "ASIO":
			assert asio_api_info is None  # Multiple ASIO api's found
			asio_api_info = api
	assert asio_api_info is not None  # No ASIO api's found
	assert asio_api_info["type"] == 3  # Unexpected type (no big deal)
	assert asio_api_info["deviceCount"] == 1  # Multiple ASIO devices found
	assert asio_api_info["defaultInputDevice"] == asio_api_info["defaultOutputDevice"]
	return asio_api_info["defaultInputDevice"]


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

	no_of_channels = 2
	framerate = 48000
	sample_width = 2

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
		no_of_channels = wave_file.getnchannels()
		framerate = wave_file.getframerate()
		sample_width = wave_file.getsampwidth()

	# Audio device setup
	asio_device_index = get_asio_device_index(p)
	input_index = asio_device_index
	output_index = asio_device_index

	stream_format = p.get_format_from_width(sample_width)

	input_stream = None
	if input_enabled:
		# input_stream, input_info = open_input_stream(asio_device_index)
		input_stream = p.open(
			format=stream_format,
			channels=no_of_channels,
			rate=framerate,
			input=True,
			output_device_index=input_index,
		)

	# output_stream, output_info = open_output_stream(asio_device_index)
	output_stream = p.open(
		format=stream_format,
		channels=no_of_channels,
		rate=framerate,
		output=True,
		output_device_index=output_index,
	)

	wave_buffer = None
	input_buffer = None
	buffer = None
	while True:
		if wave_file_enabled:
			assert wave_file is not None
			wave_buffer = wave_file.readframes(CHUNK)
			if not wave_buffer:
				break
		elif input_enabled:
			assert input_stream is not None
			input_buffer = input_stream.read(CHUNK)

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
