@echo off
echo ================================
echo.
echo DisStored - Discord File Storage
echo.
echo ================================

echo.
echo Starting DisStored...
echo.

if not exist ".env" (
    echo Creating default .env file...
    (
        echo # DisStored Configuration
        echo BOT_TOKEN=
        echo DEBUG=True
        echo PORT=5000
    ) > ".env"
    echo .env file created. Please update it with your values, then continue so it can run properly without relaunching.
    pause
)

python app.py