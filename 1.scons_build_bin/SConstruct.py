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
    BUILDERS=dict(
        ElfToBinTmp=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "binary",
                "$SOURCES",
                "$TARGET"
            ]), "Buidling $TARGET"),
            suffix=".bin.tmp"
        )
    )
)


Program(target="firmware.elf.tmp", source="main.c")
