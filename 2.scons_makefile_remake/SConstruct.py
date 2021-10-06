from SCons.Script import(DefaultEnvironment)

env = DefaultEnvironment()

cc_flags = """-mthumb -ffunction-sections -fdata-sections -Wall -Werror
	  -fno-strict-aliasing -fno-builtin -fshort-enums -Wno-error=format
	  -Wno-error=unused-function -Os -fomit-frame-pointer -Wl,-z,nocopyreloc 
	  -mcpu=cortex-m4 -mfloat-abi=hard -mfpu=fpv4-sp-d16 -u _printf_float""".split()

cc_includes="-Iinclude -Linclude".split()
linker_flags=["-Tgeneric_gcc_nrf52.ld"]

env.Replace(
    CC="arm-none-eabi-gcc",
    OBJCOPY="arm-none-eabi-objcopy"
)

env.Append(
    CCFLAGS=cc_flags + cc_includes,
    LINKFLAGS=cc_flags + cc_includes + linker_flags
)

env.Append(
    BUILDERS = dict(
        build_elf_to_bin_tmp=Builder(
            action="$OBJCOPY -O binary $SOURCE $TARGET",
            suffix=".bin.tmp",
            src_suffix='.elf.tmp',
        ),
        build_microapp_header_symbols=Builder(
            action="./scripts/microapp_make.py -i $SOURCE $TARGET",
            suffix="_header.ld",
            src_suffix='.bin.tmp'
        ),
        build_elf=Builder(
            action="$CC $FLAGS $SOURCE -Iinclude -Linclude -Tgeneric_gcc_nrf52.ld -o firmware.elf",
            src_suffix='.c'
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
            action="$CC -E -P -x c -Iinclude $SOURCE -o $TARGET",
            suffix=".ld",
            src_suffix='.ld.in',
        ),
    )
)

firmware_symbols = env.build_microapp_symbols("include/microapp_symbols.ld.in")

firmware_elf_tmp = env.Program(target="firmware.elf.tmp", source="main.c")
Depends(firmware_elf_tmp, firmware_symbols)

firmware_bin_tmp = env.build_elf_to_bin_tmp(firmware_elf_tmp)
firmware_header_ld = env.build_microapp_header_symbols(firmware_bin_tmp)

# Build main elf file, it depends on generating the firmware headers first
firmware_elf = env.build_elf("main.c")
Depends(firmware_elf, "firmware_header.ld")

# Convert elf to flashable hex
firmware_hex = env.build_hex("firmware.elf")
Depends(firmware_hex, "firmware.elf")

firmware_bin = env.build_bin("firmware.elf")
Depends(firmware_bin, "firmware.elf")
