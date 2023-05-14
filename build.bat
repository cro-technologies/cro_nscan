@echo off
cls
rem mode con cols=60 lines=10
title "building oport"
set name="oport.spec"
pyinstaller  --noconfirm --clean %name%
rmdir /s /q build
pause
exit
