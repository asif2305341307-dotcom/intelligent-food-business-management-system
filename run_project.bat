@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Creating virtual environment...
  py -3.14 -m venv .venv
)
echo Installing/checking dependencies...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
echo Starting Streamlit...
.venv\Scripts\python.exe -m streamlit run app.py
pause
