#!venv/bin/python3

import sys, os, xml.etree.cElementTree as ET


if not len(sys.argv) < 3:

    HOME_DIR = sys.argv[1]
    INST_DIR = sys.argv[2]

    print('Initializing final setup...')

    print('Setting up default settings...')
    root = ET.Element("SETTINGS")
    defaults = ET.SubElement(root, "DEFAULTS")

    ET.SubElement(defaults, "save_dir").text = HOME_DIR
    ET.SubElement(defaults, "av").text = 'True'
    ET.SubElement(defaults, 'ext').text = 'mkv'

    tree = ET.ElementTree(root)

    print('Writing XML files...')
    tree.write(os.path.join(INST_DIR, "settings.xml"))
else:
    print("Insufficient arguments. Exiting...")
