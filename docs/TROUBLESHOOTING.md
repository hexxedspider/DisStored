# DisStored Troubleshooting Guide

## Common Issues and Solutions

### 1. Discord Webhook Issues

**Problem**: Files not uploading to Discord.

**Solutions**:
- **Check webhook URL**: Verify it's correct and active
- **Test webhook**: Try uploading a small file first
- **Check Discord permissions**: Ensure webhook has upload permissions
- **Environment variable**: Set `DISCORD_WEBHOOK_URL` correctly
- **.env file**: Verify your webhook is properly in the .env file

### 2. Port Already in Use

**Problem**: "Port 5000 already in use" error.

**Solutions**:
- **Close other applications**: Check what's using port 5000
- **Change port**: Edit `config.py` and change the PORT value
- **Restart computer**: Sometimes needed to free up ports- last resort

### 3. Import Errors

**Problem**: "No module named 'flask'" or similar errors.

**Solutions**:
- **Install dependencies**: `pip install -r requirements.txt`
- **Check Python environment**: Ensure you're in the right virtual environment- if any
- **Install dependencies manually**: `pip install` for each `import {module}`

### 4. File Upload Fails

**Problem**: Files won't upload or show errors.

**Solutions**:
- **Check file size**: Ensure the file isn't too large- shouldn't be an issue, but still a valid concern
- **Check file permissions**: Ensure you can read the file
- **Try different file**: Test with a small text file first
- **Check console output**: Look for error messages
- **Ensure DisStored is running**: Make sure it's still running and not closed accidentally
- **Verify the file is intact**: Make sure the file isn't corrupt, moved, deleted, renamed, etc

### 5. Browser Won't Open

**Problem**: Web interface doesn't open automatically.

**Solutions**:
- **Manual navigation**: Go to `http://127.0.0.1:5000` or `10.0.0.7:26435` in your browser- test on a different device if unsure too (the device has to be connected to the same wifi in order to access DisStored)
- **Check firewall**: Allow the application through Windows Firewall
- **Try different browser**: Use Chrome, Firefox, Brave, Vivaldi, DuckDuckGo, etc

## Quick Fixes

### For Most Issues:
1. **Stop the application**: CTRL+C in terminal, closing the Python window, or using task manager to close Python
2. **Re-run the application**: could potentially solve issues with it not starting right on first launch

### For Webhook Issues:
1. **Create .env file**: with your webhook URL
2. **Test webhook**: start with a small file first
3. **Check Discord**: for uploaded files/chunks
4. **Copy webhook again**: incase you didn't copy every single letter, or it bugged

### For Large Files:
1. **Verify chunking**: working properly based on console output
2. **Check Discord**: for chunk files being sent
3. **Test download**: to ensure reconstruction works fully
4. **Verifiy file is stored safely**: make sure the file isn't being modified in any way

## Getting Help

If you're still having issues:

1. **Check the console output** for error messages
2. **Try running from source**: `python app.py`
3. **Test with a simple file** first
4. **Check all dependencies** are installed

## System Requirements

- **Windows 10/11** (64-bit)
- **Python 3.7+** (for building)
- **1 GB RAM** (2 GB or more recommended- could potentially run on less but you would either be suffering waiting or not able to do anything else while running)
- **Internet connection** for Discord uploads
