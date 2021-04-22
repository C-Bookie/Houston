"""
	pyaudio utility functions based on https://github.com/intxcc/pyaudio_portaudio/blob/master/example/echo_python3.py
	https://people.csail.mit.edu/hubert/pyaudio/docs/
"""
from typing import Optional

import pyaudio

CHUNK_SIZE = 1024
# CHUNK_SIZE = 800  # 60fps@48KHz


def get_api_by_name(p: pyaudio.PyAudio, api_name) -> dict:
	info_api = [p.get_host_api_info_by_index(i) for i in range(0, p.get_host_api_count())]

	api_info = None
	for api in info_api:
		if api["name"] == api_name:
			assert api_info is None  # Multiple ASIO api's found
			api_info = api
	assert api_info is not None  # No api's found
	return api_info


def get_input_device_indexes(p:pyaudio.PyAudio):  # todo add a star next to the default device
	return[
		i
		for i in range(p.get_device_count())
		if p.get_device_info_by_index(i)["maxInputChannels"] > 0
	]


def get_output_device_indexes(p:pyaudio.PyAudio):
	return[
		i
		for i in range(p.get_device_count())
		if p.get_device_info_by_index(i)["maxOutputChannels"] > 0
	]


def ask_for_device(p: pyaudio.PyAudio, as_input: bool = False) -> Optional[int]:  # todo return device_info? and filter for input/output
	"""returns the device_id selected by the user"""

	if p.get_device_count() == 0:
		raise Exception("No devices available")

	default_device_index = p.get_default_input_device_info()["index"] if as_input else p.get_default_output_device_info()["index"]

	for i in (get_input_device_indexes(p) if as_input else get_output_device_indexes(p)):
		info = p.get_device_info_by_index(i)
		index = info["index"]
		api_name = p.get_host_api_info_by_index(info["hostApi"])["name"]
		device_name = info["name"]
		print(f"{index}:  \t {api_name} \t {device_name}")

	device_id = None
	while device_id is None:
		user_input = input("Choose device index: ")
		if user_input:
			try:
				device_id = int(user_input)
			except ValueError:
				print(f"Could not cast to int: {user_input}")
		else:
			print(f"Using default device index: {default_device_index}")
			device_id = default_device_index

	return device_id


def get_device_info(p: pyaudio.PyAudio, as_input: bool = False, device_id: Optional[int] = None):
	while True:
		if device_id is None:
			device_id = ask_for_device(p, as_input)
		try:
			device_info = p.get_device_info_by_index(device_id)
			return device_info
		except IOError:
			print(f"Failed to open device index {device_id}!")  # todo improve message with device index and name
			device_id = None
		print("Please select another device")


def open_stream(
		p: pyaudio.PyAudio,
		device_info,
		as_input: bool = False,
		channels: Optional[int] = None,
		sample_width: Optional[int] = None,
		stream_format: Optional[int] = None,
		sample_rate: Optional[int] = None,
		chunk_size: Optional[int] = CHUNK_SIZE,
):
	"""
	opens a stream in either input or output
	if a dual stream is needed, then it may be easier to just use p.open() directly

	"""
	if channels is None:
		channels = device_info["maxInputChannels"] if as_input else device_info["maxOutputChannels"]
	if sample_width is None:
		sample_width = channels
	if stream_format is None:
		stream_format = p.get_format_from_width(sample_width)
	if sample_rate is None:
		sample_rate = int(device_info["defaultSampleRate"])  # todo review if casting is needed

	stream = p.open(
		format=stream_format,
		channels=channels,
		rate=sample_rate,
		frames_per_buffer=chunk_size,
		# as_loopback=True,  # fixme if as_input, see url in header
		# stream_callback=callback,  # todo look into
		**{
			"input" if as_input else "output": True,
			"input_device_index" if as_input else "output_device_index": device_info["index"],
		}
	)

	return stream

