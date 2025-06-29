@echo off
REM Silent Wallpaper Changer Launcher for Windows
REM This runs the Python script completely hidden

REM Change to your specific directory - UPDATE THIS PATH
cd /d "C:\Users\YOUR_USERNAME\OneDrive\Documents\Python Projects\Wallpaper Changer"

REM Run Python script completely invisibly
powershell.exe -WindowStyle Hidden -Command "Start-Process pythonw.exe -ArgumentList 'wallpaper_changer.py --silent' -WindowStyle Hidden"

exit
