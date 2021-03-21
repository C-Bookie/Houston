
#https://github.com/intxcc/pyaudio_portaudio/blob/master/example/echo.py
from typing import Optional

import pyaudio

CHUNK_SIZE = 1024


def get_input_device_indexes(p:pyaudio.PyAudio):
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

	try:
		default_device_index = p.get_default_input_device_info()
	except IOError:
		default_device_index = p.get_device_info_by_index(0)["index"]

	for i in (get_input_device_indexes() if as_input else get_output_device_indexes()):
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


def open_stream(p: pyaudio.PyAudio, as_input: bool = False, device_id: int = None):
	"""
	if id is None, a list of appropriate ID's shall be printed

	"""
	device_info = get_device_info(p, as_input, device_id)

	stream = p.open(
		format=pyaudio.paInt16,
		channels=device_info["maxInputChannels"] if as_input else device_info["maxOutputChannels"],
		rate=int(device_info["defaultSampleRate"]),
		input=as_input,
		frames_per_buffer=CHUNK_SIZE,  # int(device_info["defaultSampleRate"] / framerate)
		input_device_index=device_info["index"],
		# as_loopback=True,  # fixme if as_input
	)

	return stream, device_info
