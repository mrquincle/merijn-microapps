#!/bin/bash
# Script to create and update repo's for platformio packages/platforms

working_dir=$(pwd)

can_clean_pio_dirs=false

arg1=$1

setup_repo(){
	echo =====================================================================
	echo - SETTING UP: $2
	echo =====================================================================
	mkdir ~/.piorepos/$2/
	cd ~/.piorepos/$2/
	git init
	git remote add origin $3
	git pull origin master
}

update_repo(){

	[ "$arg1" = "-d" ] && clear_pio_dir $2 && return
	[ "$arg1" = "-n" ] && clear_pio_dir $2

	if [ ! -d ~/.piorepos/$2/ ]; then
		setup_repo $1 $2 $3
	fi

	# Remove all old files except for the .git folder
	cd ~/.piorepos/$2/
	rm -r $(ls ~/.piorepos/$2 -I .git)

	## Copy new files to repo and upload them
	cp -rf $working_dir/$1/$2 ~/.piorepos/

	echo =====================================================================
	echo - UPDATING: $2
	echo =====================================================================
	cd ~/.piorepos/$2/
	git add -A
	git commit -m "..."
	git push --set-upstream origin master

}

clear_pio_dir(){

	echo removing: $1
	rm -rf ~/.platformio/packages/$1/
	rm -rf ~/.platformio/platforms/"${1:9}"
}

mkdir -p ~/.piorepos

update_repo\
	"ble_uploader"\
	"tool-cs-ble-uploader"\
	"git@gitlab.com:mPlagge/tool-cs-ble-uploader.git"

update_repo\
	"framework"\
	"framework-arduinomicroapps"\
	"git@gitlab.com:mPlagge/framework-arduinomicroapps.git"

update_repo\
	"header_tool"\
	"tool-cs-header-maker"\
	"git@gitlab.com:mPlagge/tool-cs-header-maker.git"

update_repo\
	"platform"\
	"platform-csmicroapps"\
	"git@gitlab.com:mPlagge/platform-csmicroapps.git"

