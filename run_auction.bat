@echo off
echo 🏆 Universal Sports Auction - Quick Launcher
echo ============================================
echo.
echo Choose your version:
echo 1. Web Application (Browser-based)
echo 2. Python GUI Application (Desktop)
echo 3. Both Applications
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" goto web
if "%choice%"=="2" goto python
if "%choice%"=="3" goto both
goto end

:web
echo.
echo 🌐 Starting Web Application...
echo Server will start on http://localhost:8080
echo.
py scripts/server.py
goto end

:python
echo.
echo 🖥️ Starting Python GUI Application...
py -V:ContinuumAnalytics/Anaconda39-64 src/python/cricket_auction.py
goto end

:both
echo.
echo 🚀 Starting Both Applications...
echo Web server: http://localhost:8080
echo Python GUI: Opening in new window
echo.
start /b py scripts/server.py
timeout /t 2 >nul
py -V:ContinuumAnalytics/Anaconda39-64 src/python/cricket_auction.py
goto end

:end
echo.
echo Press any key to exit...
pause >nul
