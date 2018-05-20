import os
from modules import xml

ASSETS_DIR = 'assets'
TMP_DIR = "tmp"
FFMPEG_BIN = "ffmpeg"
FRAMERATES = [
    '25',
    '4',
    '7',
    '15',
    '20',
    '30',
    '60',
]
DISPLAY = os.environ['DISPLAY']
HOME = os.environ['HOME']
EXT = {
    'Video': 'mp4',
    'Audio': 'wav',
    'AV': 'mkv',
}
SETTINGS = xml.ParseXMLSettings()