#!/bin/bash

# Make commands.txt executable
chmod +x commands.txt

# Create a symbolic link to the desktop
ln -s "/Users/sb/Desktop/projects_master/PDFSplitter/PDF Splitter.app" ~/Desktop/

# Ensure the Output Files directory exists and has proper permissions
mkdir -p "/Users/sb/Desktop/projects_master/PDFSplitter/Output Files"
chmod 755 "/Users/sb/Desktop/projects_master/PDFSplitter/Output Files" 