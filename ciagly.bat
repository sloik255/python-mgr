@echo on
cd ..
cd ..
cd ..
P:
cd %~dp0\source
for /l %%x in (1, 1, 1000) do (
   echo %%x
   python main.py
   pause
)