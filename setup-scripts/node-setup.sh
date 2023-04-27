#!/bin/bash

# test

echo "Test"

# 1. Download Python, PyCryptodome
sudo apt-get update
sudo apt-get install python3.8 python3-pip -y

sudo apt-get install pycryptodome -y


# 2. Clone repository
git clone https://github.com/Jay-Adusumilli/BlockChainApp & EPID=$!
wait $EPID

# 3. Starts the Client.py
python client.py
