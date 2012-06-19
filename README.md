po_to_xml
=========

Simple Python script that converts Transifex PO language files to Eden compatible XML files.

This script expects the PO files to be saved as strings.po inside the language folder:
    language/English/strings.po

To run the script, start the from the folder containing the po_to_xml.py file in the following manor

    Windows:
        \Python27\python.exe po_to_xml.py "C:\XBMC Stuff\scripts\script.cdartmanager"

    Linux:
        python py_to_xml.py "/home/xbmc/scripts/script.cdartmanager"

This should also run on OSX(just not sure the method(probably similar to Linux)

The full path is needed for the script to convert.  If there is a space in the path, the double quotes are needed.

The script will then search through the language folders and convert the strings.po to a compatible strings.xml file, overwriting the old strings.xml file

This script should work on all addon types, including skins.

