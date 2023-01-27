
build:
	#protoc --python_out=./python/ --nanopb_out=./lens/src/ ./protobuf/example.proto
	cd protobuf; protoc --python_out=../python/ --nanopb_out=../lens/src/ ./example.proto

upload:
	cd lens; platformio run --target upload

monitor:
	cd lens; platformio device monitor

debug:
	cd lens; pio debug --interface=gdb -- -x .pioinit
