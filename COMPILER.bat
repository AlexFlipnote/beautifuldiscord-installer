@echo off

set filename="beautifuldiscord"

:: Make it compile beautifuldiscord to an executable file
pyinstaller index.py --onefile --icon=logo.ico --name %filename%.exe

:: Copy compiled file to root
copy dist\%filename%.exe .
