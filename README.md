# Requirements

Program uses ffmpeg and libx264 to encode files. If this is not installed
you will need to install it using: *sudo apt-get install ffmpeg* on Ubuntu
or *sudo dnf in ffmpeg* on Fedora or Centos.

The provided virtual environment should contain all necessary python libraries; however,
the program does require:
* python-vlc
* PyQt5
* gtk+ 3.0

If you encounter problems, please try installing these Python libraries manually.
Finally, the program will only run in Python 3.6.

# Installing on Linux

The software should run within the source directory if you use *git clone https://github.com/aristarchusthefgreat/screencastre.git*.

There is also an installer (install.sh):

*Usage: sudo install.sh [INSTALL DIRECTORY]*

This will install the program in your chosen directory and create a symbolic link in
*/usr/bin/*. Just type screencastre into terminal to run.

# Screencastre