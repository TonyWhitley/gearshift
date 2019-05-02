goto :or
set local
set path="c:\Program Files\Git\bin";%path%
python -m revisionCountFromGit.py
pause
goto :eof

:nogit
@echo .git folder must be present
goto quit:

:or
if not exist .git goto nogit
"c:\Program Files\Git\bin\git" rev-list --count master..

:quit
pause
