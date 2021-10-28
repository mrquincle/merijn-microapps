#!/bin/bash

PWD=$(pwd)

clean_builds(){
	cd crownstone-microapp
	make clean
	cd ../
}

compaire_source_files(){

	cd crownstone-microapp
	make
	diff crownstone-microapp/build/example.c  pio/src/main.c &&\
		echo No difference in example.c and main.c
	make clean
	cd ../
}

get_cmds(){
	cd crownstone-microapp
	make clean
	make -n > ../unitest_files/cmd_makefile
	cd ../

	cd pio
	pio run -t clean
	pio run > ../unitest_files/cmd_pio
	cd ../
}
compaire_cmds(){
	tail -n+5 unitest_files/cmd_pio |\
		sed -e "s/\/home\/m\/.platformio\/packages\/framework-arduinomicroapps\/cores\/Crownstone\///g" |\
		head -n -1 |\
		sed -e "s/.pio\/build\/microapp\//build\//g" >\
		unitest_files/cmd_pio_stripped



	# Remove echo's
	# Remove catting example.ino into example.c
	# Remove location to bluenet
	cat unitest_files/cmd_makefile |\
		grep -v echo |\
		tail -n+3 |\
		sed -e "s/\/home\/m\/workspace\/bluenet-2\/tools\/gcc_arm_none_eabi\/bin\///g" >\
		unitest_files/cmd_makefile_stripped
	
	#diff unitest_files/cmd_makefile_stripped unitest_files/cmd_pio_stripped
	cat unitest_files/cmd_makefile_stripped
	cat unitest_files/cmd_pio_stripped

}

clean_builds
compaire_source_files
get_cmds
compaire_cmds
