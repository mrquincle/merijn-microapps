#!/bin/bash

diff_files(){
	diff crownstone-microapp/example.c scons/src/main.c
	diff crownstone-microapp/include/generic_gcc_nrf52.ld scons/linkers/generic_gcc_nrf52.ld
	diff crownstone-microapp/include/Arduino.h scons/core/Arduino.h
	diff crownstone-microapp/include/microapp_symbols.ld.in scons/linkers/microapp_symbols.ld.in
	diff crownstone-microapp/include/nrf_symbols.ld scons/linkers/nrf_symbols.ld
	diff crownstone-microapp/include/String.h scons/core/String.h
	diff crownstone-microapp/include/config.h scons/linkers/config.h
	diff crownstone-microapp/include/microapp_symbols.ld scons/linkers/microapp_symbols.ld
	diff crownstone-microapp/include/Serial.h scons/core/Serial.h
	diff crownstone-microapp/include/Wire.h scons/core/Wire.h
	diff crownstone-microapp/include/microapp_header_symbols.ld scons/linkers/microapp_header_symbols.ld
	diff crownstone-microapp/include/nrf_common.ld scons/linkers/nrf_common.ld 
	
	diff crownstone-microapp/include/microapp.h scons/core/microapp.h
	diff crownstone-microapp/src/microapp.c scons/core/microapp.c
	
	diff crownstone-microapp/src/Arduino.c scons/core/Arduino.c
	diff crownstone-microapp/src/main.c scons/core/main.c
	diff crownstone-microapp/src/Serial.cpp scons/core/Serial.cpp
	diff crownstone-microapp/src/Wire.cpp scons/core/Wire.cpp
	
	diff crownstone-microapp/scripts/CRC.py scons/scripts/CRC.py
	diff crownstone-microapp/scripts/MicroappBinaryHeaderPacket.py scons/scripts/MicroappBinaryHeaderPacket.py
	diff crownstone-microapp/scripts/microapp_make.py scons/scripts/microapp_make.py
	diff crownstone-microapp/scripts/microapp.py scons/scripts/microapp.py
	
	diff crownstone-microapp/build/example.elf.tmp scons/build/main.elf.tmp
	diff crownstone-microapp/build/example.bin.tmp scons/build/main.bin.tmp
}

diff_files

#readelf -S crownstone-microapp/build/example.elf.tmp 
#readelf -S scons/build/main.elf.tmp
