from SCons.Script import(DefaultEnvironment)
import subprocess
import os
import shutil

from os.path import join

def create_empty_header_symbols_file():
    print("Creating empty header file")
    src_file = env['HEADER_LD_EMPTY']
    dst_file = env['HEADER_LD']
    shutil.copyfile(src_file, dst_file)

env = DefaultEnvironment()
platform = env.PioPlatform()


env.Append(
    CWD = os.getcwd()
)
env.Append(
    CORE = join(env['CWD'], 'core'),
    INCLUDE = join(env['CWD'], 'include'),
    SRC = join(os.getcwd(), 'src'),
    BUILD = env['BUILD_DIR'],
    SCRIPTS = join(env['CWD'], 'scripts'),
)

env.Append(
    HEADER_LD = join(env['INCLUDE'], "microapp_header_symbols.ld"),
    HEADER_LD_EMPTY =  join(env['INCLUDE'], "microapp_header_symbols_empty.ld"),
    SYMBOLS_LD = join(env['INCLUDE'], "microapp_symbols.ld"),
    SYMBOLS_IN = join(env['INCLUDE'], "microapp_symbols.ld.in"),
    MAIN_C = join(env['SRC'], "main.c"),
    MAIN_ELF =  join(env['BUILD'], "main.elf"),
    MAIN_ELF_TMP = join(env['BUILD'], "main.elf.tmp"),
    MAIN_BIN_TMP = join(env['BUILD'], "main.bin.tmp"),
    MAIN_HEX = join(env['BUILD'], "main.hex"),
    MAIN_BIN = join(env['BUILD'], "main.bin"),
    MICROAPP_MAKE_SCRIPT = join(env['SCRIPTS'], "microapp_make.py"),
    GENERIC_GCC_NRF52_LD = "generic_gcc_nrf52.ld",
    CCFLAGS = """-std=c++17 -mthumb -ffunction-sections -fdata-sections -Wall -Werror
	  -fno-strict-aliasing -fno-builtin -fshort-enums -Wno-error=format 
	  -fno-exceptions -fno-enforce-eh-specs
	  -nostdlib -ffreestanding -fno-threadsafe-statics
	  -Wl,--gc-sections
	  -Wno-error=unused-function -Os -fomit-frame-pointer -Wl,-z,nocopyreloc
	  -mcpu=cortex-m4 -mfloat-abi=hard -mfpu=fpv4-sp-d16 -u _printf_float""".split()
)

core_files="Arduino.c main.c microapp.c Serial.cpp Wire.cpp ipc/cs_IpcRamData.c".split()
for index, file_ in enumerate(core_files):
    core_files[index] = join(env['CORE'], file_)
env.Append(CORE_FILES = core_files)

env.Replace(
    CC="arm-none-eabi-g++",
    OBJCOPY="arm-none-eabi-objcopy"
)

print(env['CORE'])

env.Append(
    BUILDERS = dict(
        build_elf_tmp=Builder(
            action="$CC $CCFLAGS $CORE_FILES $SOURCE -I$INCLUDE -I$CORE -L$INCLUDE -T$GENERIC_GCC_NRF52_LD -o $TARGET",
        ),
        build_bin_tmp=Builder(
            action="$OBJCOPY -O binary $SOURCE $TARGET",
        ),
        build_microapp_header_symbols=Builder(
            action="$MICROAPP_MAKE_SCRIPT -i $SOURCE $HEADER_LD",
        ),
        build_elf=Builder(
            action="$CC $CCFLAGS $CORE_FILES $SOURCE $HEADER_LD -I$CORE -I$INCLUDE -L$INCLUDE -T$GENERIC_GCC_NRF52_LD -o $TARGET",
        ),
        build_microapp_symbols=Builder(
            action="$CC -CC -E -P -x c -I$INCLUDE $SOURCE -o $TARGET",
        ),
        build_hex=Builder(
            action="$OBJCOPY -O ihex $SOURCE $TARGET",
        ),
        build_bin=Builder(
            action="$OBJCOPY -O binary $SOURCE $TARGET",
        ),
    )
)

#
# Building microapp
# 

if env.GetOption('clean'):
    create_empty_header_symbols_file()
    env.NoClean("$HEADER_LD")

microapp_symbols = env.build_microapp_symbols(source="$SYMBOLS_IN", target="$SYMBOLS_LD")

firmware_elf_tmp = env.build_elf_tmp(source="$MAIN_C", target="$MAIN_ELF_TMP")
Depends(firmware_elf_tmp, microapp_symbols)

firmware_bin_tmp = env.build_bin_tmp(source="$MAIN_ELF_TMP", target="$MAIN_BIN_TMP")

firmware_header_ld = env.build_microapp_header_symbols(target="$HEADER_LD",source="$MAIN_BIN_TMP")

env.NoClean("$HEADER_LD")
env.AlwaysBuild("$HEADER_LD")

firmware_elf = env.build_elf(target='$MAIN_ELF', source='$MAIN_C')
Depends(firmware_elf, firmware_header_ld)

firmware_hex = env.build_hex(target="$MAIN_HEX", source="$MAIN_ELF")
firmware_bin = env.build_bin(target="$MAIN_BIN", source="$MAIN_ELF")

#
# Targets and defaults
#

upload_actions = "python3 /home/m/workspace/concepts/7.scons_variable_locations_files/upload_microapp.py -a FD:FC:93:F8:97:BA -f $MAIN_BIN"
env.AddPlatformTarget("upload", firmware_bin, upload_actions)

t= firmware_bin
upload = env.Alias(["upload"], t)
AlwaysBuild(upload)
Default(t)

#print(f"PWD: {os.getcwd()}")
#print(env["BUILD_DIR"])
#print( vars(env))

