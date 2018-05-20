#!/usr/bin/env bash

HERE="$(dirname "$(readlink -f "${0}")")"
INSTALL_DIR=$1
USER_HOME=$(eval echo ~${SUDO_USER})

if [ "$#" -ne 1 ] || ! [ -d "$1" ]; then
  echo "Usage: $0 [INSTALL DIRECTORY]" >&2
  exit 1
fi

if [ "$EUID" -ne 0 ]
    then echo "Please run as root!"
    exit
fi

if [ -d ${HERE}'/windows' ] && [ -d ${HERE}'/assets' ]
    then echo "Exists"
else exit 1
fi

if [ ! -d ${INSTALL_DIR}'/screencaster' ]
    then mkdir -v ${INSTALL_DIR}'/screencaster'
fi

rsync -Pa ${HERE}'/assets' ${INSTALL_DIR}'/screencaster/'
rsync -Pa ${HERE}'/tmp' ${INSTALL_DIR}'/screencaster/'
rsync -Pa ${HERE}'/__main__.py' ${INSTALL_DIR}'/screencaster/'
rsync -Pa ${HERE}'/_constants.py' ${INSTALL_DIR}'/screencaster/'
rsync -Pa ${HERE}'/config.ini' ${INSTALL_DIR}'/screencaster/'
rsync -Pa ${HERE}'/getting_started.txt' ${INSTALL_DIR}'/screencaster/'
rsync -Pa ${HERE}'/README.txt' ${INSTALL_DIR}'/screencaster/'
rsync -Pa ${HERE}'/screencaster' ${INSTALL_DIR}'/screencaster/'
rsync -Pa ${HERE}'/settings.py' ${INSTALL_DIR}'/screencaster/'
rsync -Pa ${HERE}'/setup.py' ${INSTALL_DIR}'/screencaster/'
rsync -Pa ${HERE}'/venv' ${INSTALL_DIR}'/screencaster/'

ln -s ${INSTALL_DIR}'/screencaster/screencaster' '/usr/bin/screencaster'

echo 'Installing custom python modules...'

python3 ${HERE}'/'setup.py install
python3 ${HERE}'/'init.py ${USER_HOME} ${INSTALL_DIR}'/screencaster'

echo "All Done."


