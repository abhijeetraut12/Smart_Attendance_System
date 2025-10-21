#!/bin/bash
apt-get update
apt-get install -y cmake build-essential portaudio19-dev
pip install --upgrade pip
pip install -r requirements.txt

