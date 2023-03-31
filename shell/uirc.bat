::  This batch file checks if it is present in the Windows startup folder, and if not, 
::  copies itself to the folder so that it runs automatically during startup. It then 
::  modifies the Windows Explorer settings to show all file extensions, and to show hidden 
::  and super-hidden files. Finally, it restarts the Windows Explorer process to apply 
::  the changes made to the registry.

@echo off
:: Turn off command echoing

:: Check if the batch file is present in the startup folder
for /F "skip=2 tokens=2*" %%j in ('reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v "Startup"') do set STARTUP=%%k
:: Query the Windows registry for the location of the startup folder for the current user, and store it in the STARTUP variable

c:
cd %STARTUP%
:: Change the current directory to the startup folder

if not exist %STARTUP%\%~nx0 ( 
	echo %~nx0 not in startup
	:: If the batch file is not present in the startup folder, print a message
	echo copying the %~nx0 to startup
	:: Copy the batch file to the startup folder using the xcopy command
	xcopy "%~f0" "%STARTUP%\%~nx0*"
	echo done!
	:: Print a message indicating that the copy is complete
)

:: Modify the Windows Explorer settings to show all file extensions, and to show hidden and super-hidden files
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v HideFileExt /t REG_DWORD /d 0 /f
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v Hidden /t REG_DWORD /d 1 /f
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v ShowSuperHidden /t REG_DWORD /d 1 /f

:: Restart the Windows Explorer process to apply the changes
taskkill /im explorer.exe /f && start explorer.exe
