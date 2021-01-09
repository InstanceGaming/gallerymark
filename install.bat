@echo off

pip install virtualenv

IF NOT EXIST "env\Scripts\python.exe" (
  echo Creating virtualenv.
  virtualenv env
) ELSE (
  echo Virtualenv already exists.
)

IF EXIST "env\Scripts\python.exe" (
  echo Installing Python packages...
  .\env\Scripts\pip.exe install -r requirements.txt
) ELSE (
  echo Could not find python.exe
)

echo Installation finished.
PAUSE