@echo off

set "VENV_DIR=.venv"

where py >nul 2>&1
if %errorlevel%==0 (
  set "PYTHON_CMD=py -3"
) else (
  where python >nul 2>&1
  if %errorlevel%==0 (
    set "PYTHON_CMD=python"
  ) else (
    echo Error: Python 3 was not found in PATH.
    exit /b 1
  )
)

if not exist "%VENV_DIR%\Scripts\python.exe" (
  echo Creating virtual environment in %VENV_DIR%...
  %PYTHON_CMD% -m venv "%VENV_DIR%"
  if errorlevel 1 exit /b 1
) else (
  echo Virtual environment already exists at %VENV_DIR%.
)

echo Installing dependencies from requirements.txt...
"%VENV_DIR%\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 exit /b 1

"%VENV_DIR%\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

call "%VENV_DIR%\Scripts\activate.bat"

echo Setup complete. Virtual environment is active.
