CC=arm-none-eabi-gcc
OBJCOPY=arm-none-eabi-objcopy

TARGET=main

FLAGS=-mthumb -ffunction-sections -fdata-sections -Wall -Werror \
	  -fno-strict-aliasing -fno-builtin -fshort-enums -Wno-error=format \
	  -Wno-error=unused-function -Os -fomit-frame-pointer -Wl,-z,nocopyreloc \
	  -mcpu=cortex-m4 -mfloat-abi=hard -mfpu=fpv4-sp-d16 -u _printf_float

all: $(TARGET).elf $(TARGET).hex

$(TARGET).elf: $(TARGET).c
	$(CC) $(FLAGS)  $^ -Iinclude -Linclude -Tgeneric_gcc_nrf52.ld -o $@

$(TARGET).hex: $(TARGET).elf
	@echo "Create hex file"
	@$(OBJCOPY) -O ihex $^ $@
