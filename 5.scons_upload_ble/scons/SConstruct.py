from SCons.Script import(DefaultEnvironment)

env = DefaultEnvironment()

cc_flags = """-std=c++17 -mthumb -ffunction-sections -fdata-sections -Wall -Werror
	  -fno-strict-aliasing -fno-builtin -fshort-enums -Wno-error=format 
	  -fno-exceptions -fno-enforce-eh-specs
	  -nostdlib -ffreestanding -fno-threadsafe-statics
	  -Wl,--gc-sections
	  -Wno-error=unused-function -Os -fomit-frame-pointer -Wl,-z,nocopyreloc
	  -mcpu=cortex-m4 -mfloat-abi=hard -mfpu=fpv4-sp-d16 -u _printf_float""".split()

core_files="core/Arduino.c core/main.c core/microapp.c core/Serial.cpp core/Wire.cpp core/ipc/cs_IpcRamData.c".split()

cc_includes="-Iinclude -Linclude".split()
linker_flags=["-Tgeneric_gcc_nrf52.ld"]

env.Replace(
    CC="arm-none-eabi-g++",
    OBJCOPY="arm-none-eabi-objcopy"
)

env.Append(
    CCFLAGS=cc_flags + core_files +  cc_includes,
    LINKFLAGS=cc_flags + core_files + cc_includes + linker_flags
)

env.Append(
    BUILDERS = dict(
        build_elf_tmp=Builder(
            action="$CC $CCFLAGS $SOURCE -Iinclude -Icore -Linclude -Tgeneric_gcc_nrf52.ld -o $TARGET",
            suffix="elf.tmp",
            src_suffix=".c",
        ),
        build_bin_tmp=Builder(
            action="$OBJCOPY -O binary main.elf.tmp main.bin.tmp",
            suffix=".bin.tmp",
            src_suffix='.elf.tmp'
        ),
        build_microapp_header_symbols=Builder(
            action="./scripts/microapp_make.py -i $SOURCE include/microapp_header_symbols.ld",
            src_suffix='.bin.tmp',
            suffix="microapp_header_symbols.ld",
        ),
        build_elf=Builder(
            action="$CC $CCFLAGS main.c include/microapp_header_symbols.ld -Icore -Iinclude -Linclude -Tgeneric_gcc_nrf52.ld -o main.elf",
        ),
        build_hex=Builder(
            action="$OBJCOPY -O ihex $SOURCE $TARGET",
            suffix=".hex",
            src_suffix='.elf',
        ),
        build_bin=Builder(
            action="$OBJCOPY -O binary $SOURCE $TARGET",
            suffix=".bin",
            src_suffix='.elf',
        ),
        build_microapp_symbols=Builder(
            action="$CC -CC -E -P -x c -Iinclude $SOURCE -o $TARGET",
            suffix=".ld",
            src_suffix='.ld.in',
        ),
    )
)

microapp_symbols = env.build_microapp_symbols("include/microapp_symbols.ld.in")

firmware_elf_tmp = env.build_elf_tmp("main.c")
Depends(firmware_elf_tmp, microapp_symbols)

firmware_bin_tmp = env.build_bin_tmp("main.elf.tmp")

firmware_header_ld = env.build_microapp_header_symbols("main.bin.tmp")
print(firmware_header_ld)

#firmware_elf = env.build_elf()
#Depends(firmware_elf, firmware_header_ld)
#
#firmware_hex = env.build_hex("main.elf")
#firmware_bin = env.build_bin("main.elf")
