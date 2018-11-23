@echo off

:: BatchGotAdmin
:-------------------------------------
REM  --> Check for permissions
    IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

REM --> If error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params= %*
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs" 
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0

echo Setup Started...

set PYTHONSETUP=%CD%
set "RUN=\Code\Run.py
FOR  /F "tokens=*" %%F IN ('where python') DO (SET PYTHONPATH="%%F")
set PYTHONRUN="%PYTHONSETUP%%RUN%"

set PYTHONSETUP=%CD%
set "MAESTRO=\Code\Maestro.py
set PYTHONMAESTRO="%PYTHONSETUP%%MAESTRO%"

echo PATH Setup...

@echo @echo off  > Run.bat
@echo %PYTHONPATH% %PYTHONRUN% >> Run.bat
@echo echo: >> Run.bat
@echo pause  >> Run.bat

@echo @echo off  > Maestro.bat
@echo %PYTHONPATH% %PYTHONMAESTRO% >> Maestro.bat
@echo echo: >> Run.bat
@echo pause  >> Maestro.bat

echo File Run Succesfuly Created...
echo:
echo Do you want to install python modules? (They are necessary for program execution)
echo:
:start 
	echo 1. Yes
	echo 2. No
	echo:
set /p x=Option(1 or 2):
IF '%x%' == '1' GOTO NUM_1
IF '%x%' == '2' GOTO NUM_2
GOTO start

:NUM_1
	echo:
	echo Installing Modules ...
	echo:
	pip install requests
	pip install xlsxwriter
	pip install requests_oauthlib
	
	echo:
	echo Modules installed:
	echo 	Requests
	echo 	xlsxwriter
	echo	requests_oauthlib
	echo:
	echo Correctly Setup ...

	goto END
	
:NUM_2
	echo:
	echo "Modules not installed"
	echo:
	echo "Correctly Setup..."
	goto END

:END
	echo:
	echo Press any key to finish the Setup...
	pause >nul
