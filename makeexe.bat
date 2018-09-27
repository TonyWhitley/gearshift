@echo off
setlocal

goto not37

python -V | find "3.7"
if errorlevel 1 goto not37
::python -V
echo pyinstaller only works with versions up to 3.6
pause
goto :eof

:not37
set path=c:\Python36;c:\Python36\scripts;%path%
set path=%path%;"C:\Program Files (x86)\Windows Kits\10\Redist\ucrt\DLLs\x64"

pyinstaller -v
@echo.


if exist env\scripts 	set path=%path%;env\Scripts
if not exist env\scripts	python.exe -m venv env && env/Scripts/activate && python -m pip install -r requirements.txt 

::   --debug=imports 
::  --clean 
::  --paths env\Lib\site-packages 
::  --hidden-import pygame.base 

pyinstaller ^
  --onefile ^
  --distpath . ^
  "%~dp0\gearshift.py "
pause

