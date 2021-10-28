#!/bin/bash
# 

diff crownstone-microapp/include/generic_gcc_nrf52.ld scons/linkers/generic_gcc_nrf52.ld
diff crownstone-microapp/include/Arduino.h scons/core/Arduino.h
#diff crownstone-microapp/include/microapp_symbols.ld.in scons/linkers/microapp_header_symbols.ld.in
#diff crownstone-microapp/include/nrf_symbols.ld scons/linkers/nrf_symbols.ld
#diff crownstone-microapp/include/String.h scons/core/String.h
#diff crownstone-microapp/include/config.h scons/linkers/config.h
#diff crownstone-microapp/include/microapp.h scons/core/microapp.h
#diff crownstone-microapp/include/microapp_symbols.ld scons/linkers/microapp_symbols.ld
#diff crownstone-microapp/include/nrf_common.ld scons/linkers/nrf_common.ld
#diff crownstone-microapp/include/Serial.h scons/core/Serial.h
#diff crownstone-microapp/include/Wire.h scons/core/Wire.h
diff crownstone-microapp/include/microapp_header_symbols.ld scons/linkers/microapp_header_symbols.ld
