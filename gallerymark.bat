@echo off

IF EXIST "env\Scripts\pythonw.exe" (
  .\env\Scripts\pythonw.exe gallerymark.py %*
) ELSE (
  echo Could not find Python, did you run install.bat?
  PAUSE
)