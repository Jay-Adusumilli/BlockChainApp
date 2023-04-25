#!/bin/bash

# Scripts need to be zipped to be loaded onto the GENI machine.
# It is likely that we will needs to edit the server and node scripts multiple times.
# This script will automatically zip the scripts consistently. 

SERVERSCRIPT=server-setup.sh
NODESCRIPT=node-setup.sh
SERVERTARGET=server-setup.tar.gz
NODETARGET=node-setup.tar.gz

#if [ "$EUID" -ne 0 ]
#  then echo "Please run as root"
#  exit
#fi

# Make sure scripts have correct permissions
chmod -R 777 $SERVERSCRIPT
chmod -R 777 $NODESCRIPT

# Remove existing archives
if [ -f "$SERVERTARGET" ]; then
    rm -rf $SERVERTARGET
fi
if [ -f "$NODETARGET" ]; then
    rm -rf $NODETARGET
fi

# Zip scripts
tar -czvf $SERVERTARGET $SERVERSCRIPT
tar -cvzf $NODETARGET $NODESCRIPT

# Maybe not needed
chmod -R 777 $SERVERTARGET
chmod -R 777 $NODETARGET
