@echo off


IF EXIST "env\Scripts\pyuic5.exe" (
  .\env\Scripts\pyuic5.exe -o ui/mainwindow.py ui/mainWindow.ui %*
  .\env\Scripts\pyuic5.exe -o ui/welcometab.py ui/welcomeTab.ui %*
) ELSE (
  echo Could not find pyuic5.exe
  PAUSE
)