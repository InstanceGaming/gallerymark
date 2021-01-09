@echo off

IF EXIST "env\Scripts\pyinstaller.exe" (
  REM use -w to hide console
  .\env\Scripts\pyinstaller.exe -s -F -w -i gallerymark.ico --add-data "gallerymark.ico;." gallerymark.py
) ELSE (
  echo Could not find pyinstaller.exe
  PAUSE
)