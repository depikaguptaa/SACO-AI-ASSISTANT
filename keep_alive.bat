@echo off
echo Starting keep-alive for SACO AI Assistant backend...
echo Press Ctrl+C to stop
echo.

:loop
python simple_keep_alive.py
timeout /t 5 /nobreak >nul
goto loop
