# https://github.com/spatialaudio/python-sounddevice/issues/229#issuecomment-598354523
import sounddevice as sd
print(sd.query_devices())
print(sd.get_portaudio_version())
print(sd.query_hostapis())

from ctypes.util import find_library
print(find_library('portaudio'))
print(find_library('libportaudio64bit'))