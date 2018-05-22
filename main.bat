@echo off
echo Uruchamiam program... prosze czekac...
cd ..
cd ..
cd ..
P:
cd %~dp0\source
python main.py
echo Poprawnie zakonczono dzialanie programu
pause