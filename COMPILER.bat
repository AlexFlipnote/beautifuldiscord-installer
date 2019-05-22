@echo off

set filename="beautifuldiscord"

:: Make it compile beautifuldiscord to an executable file
pyinstaller index.py --onefile --icon=logo.ico --name %filename%.exe

:: Copy compiled file to root
copy dist\%filename%.exe .

:: Sign that nice software
bin\signtool.exe sign /f "%userprofile%\.ssl\sign.pfx" /t http://timestamp.verisign.com/scripts/timstamp.dll %filename%.exe
