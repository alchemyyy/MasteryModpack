@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PYTHON_CMD=python"

if not "%PYTHON%"=="" set "PYTHON_CMD=%PYTHON%"

"%PYTHON_CMD%" "%SCRIPT_DIR%compile_mrpack.py" %*
exit /b %ERRORLEVEL%
