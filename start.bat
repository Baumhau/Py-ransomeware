@echo off
:start
pip3 install cryptography pycryptodome
python3 genkey.py
python3 enc.py
