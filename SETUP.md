# DisStored Quick Setup Guide

## Quick Start (5 minutes)

### Option 1: Run from Source
1. **Install Python** (3.7 or higher)
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Set Discord webhook**: `set DISCORD_WEBHOOK_URL=your_webhook_url`
4. **Run**: `python app.py` or double-click `run.bat`

### Option 2: Build Executable
1. **Install dependencies**: `pip install -r requirements.txt`
2. **Build executable**: Double-click `build_executable.bat`
3. **Run**: Double-click `launch.bat` or run `dist/DisStored.exe`

## 🔧 Discord Webhook Setup

1. **Go to Discord** → Your server → Channel settings
2. **Integrations** → **Webhooks** → **New Webhook**
3. **Copy the webhook URL**
4. **Set environment variable**:
   ```bash
   set DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN
   ```

## 📁 File Structure
```
DisStored/
├── app.py                 # Main application
├── config.py              # Configuration
├── build.py               # Build script
├── run.bat               # Run from source
├── launch.bat            # Launcher with env support
├── build_executable.bat  # Build executable
├── requirements.txt      # Dependencies
├── templates/index.html  # Web interface
└── README.md            # Full documentation
```

## 🌐 Usage
1. **Start the application**
2. **Browser opens automatically** to `http://127.0.0.1:5000`
3. **Drag & drop files** or click to upload
4. **Create folders** to organize files
5. **Download or delete** files as needed

## ⚠️ Important Notes
- **Max file size**: 9.99MB (Discord limit)
- **Files stored locally** in `files.json`
- **No authentication** (single-user)
- **Port 5000** must be available

## 🆘 Troubleshooting
- **"Webhook not set"**: Set `DISCORD_WEBHOOK_URL` environment variable
- **"Port in use"**: Close other apps using port 5000
- **"File too large"**: Split files or use alternative storage
- **Executable won't run**: Check Windows Defender/firewall

## 📞 Support
- Check console output for errors
- Verify webhook URL is correct
- Ensure proper file permissions
