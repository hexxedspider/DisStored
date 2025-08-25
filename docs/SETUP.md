# DisStored Quick Setup Guide

## Quick Start (5 minutes)

### Option 1: Run from Source
1. **Install Python** (3.7 or higher)
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Set Discord webhook**: `set DISCORD_WEBHOOK_URL=your_webhook_url`
3.1 **Set Discord webhook - env**: open .env and set your webhook there
4. **Run**: `python app.py` or double-click `run.bat`

### Option 2: Eventually

// make it run from a single executable, or as an installer that adds shortcuts to run it.

## Discord Webhook Setup

1. **Go to Discord** → Your server → Channel settings
2. **Integrations** → **Webhooks** → **New Webhook**
3. **Copy the webhook URL**
4. **Set environment variable**:
   ```
   set DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN
   ```

## File Structure
```
DisStored/
├────templates/index.html # Web UI
├────docs/**              # The documents for other reasons not in README.md
├── .env                  # Your webhook will be set here
├── .gitignore            # Things that don't get pushed to GitHub
├── .gitattributes        > not really important for you
├── app.py                # Main application
├── config.py             # Configuration
├── files.json            # Data for the files you uploaded
├── run.bat               # Run from source
├── requirements.txt      # Dependencies
└── README.md             # Full documentation
```

## Usage
1. **Start the application**: whether by running the app.py file directly or using run.bat
2. **Browser opens automatically**: to `http://10.0.0.7:26435`, but you can also go to `127.0.0.1:26435`
3. **Drag & drop files**: or start an upload by clicking the upload area
4. **Create folders**: completely optional, only for organization
5. **Download or delete**: from there you can delete files from your access or download them- NOTE: does not remove the upload from Discord, only removes for you!

## Important Notes
- **Max file size**: there is no limit, but there's a certain point where waiting will take way longer than is really necessary, and other alternatives are better
- **Files stored locally**: stored in `files.json`, not the file themselves, but the data that makes that file even technically exist to DisStored
- **No authentication**: anyone on the same wifi can upload freely and download all files each indiviual uploads, or a singular person, without needing to do tests- planning on making it so it keeps your IP in memory so you can have other people access, but will need to input a password that you set in order to access, otherwise they'll be met with a `ERROR 100: NO ACCESS`
- **Port Number**: it has to be available, 26435, 5000, 2500, etc, whatever port has to be free