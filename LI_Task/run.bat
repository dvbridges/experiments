REM Starting PsychoPy program (either builder or coder written)
REM If this fails to run on other PCs edit this
REM batch file and change the path to pickup your local copy of pythonw.exe
REM ...
"C:\Program Files (x86)\PsychoPy2\pythonw.exe" code\main.py

REM experiment finishing now ...
ping 1.1.1.1 -n 1 -w 5000 >NUL
REM ping command above is to delay exit so that any error messages stay on the screen for long enough to bre read!
