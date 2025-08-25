# DisStored Troubleshooting Guide

## Common Issues and Solutions

### 1. "ordinal not found" Error

**Problem**: The executable shows "ordinal not found" when trying to run.

**Solutions**:
- **Rebuild the executable**: Run `python build.py` to create a fresh build
- **Clean build directories**: Delete `dist/` and `build/` folders before rebuilding
- **Update PyInstaller**: `pip install --upgrade pyinstaller`
- **Check Python version**: Ensure you're using Python 3.7+ and PyInstaller 6.0+

### 2. Executable Won't Start

**Problem**: Double-clicking the .exe file does nothing.

**Solutions**:
- **Run from command line**: Open cmd/PowerShell and run `.\dist\DisStored.exe`
- **Check Windows Defender**: Add the executable to exclusions
- **Run as Administrator**: Right-click → "Run as administrator"
- **Check dependencies**: Ensure all required DLLs are present

### 3. "File too large" Error

**Problem**: Still getting 9.99MB limit error.

**Solutions**:
- **Restart the application**: Close and reopen DisStored
- **Clear browser cache**: Press Ctrl+F5 in your browser
- **Check configuration**: Verify the config shows 100MB limit
- **Update executable**: Rebuild with latest code

### 4. Discord Webhook Issues

**Problem**: Files not uploading to Discord.

**Solutions**:
- **Check webhook URL**: Verify it's correct and active
- **Test webhook**: Try uploading a small file first
- **Check Discord permissions**: Ensure webhook has upload permissions
- **Environment variable**: Set `DISCORD_WEBHOOK_URL` correctly

### 5. Port Already in Use

**Problem**: "Port 5000 already in use" error.

**Solutions**:
- **Close other applications**: Check what's using port 5000
- **Change port**: Edit `config.py` and change the PORT value
- **Restart computer**: Sometimes needed to free up ports

### 6. Import Errors

**Problem**: "No module named 'flask'" or similar errors.

**Solutions**:
- **Install dependencies**: `pip install -r requirements.txt`
- **Check Python environment**: Ensure you're in the right virtual environment
- **Rebuild executable**: Run `python build.py` again

### 7. File Upload Fails

**Problem**: Files won't upload or show errors.

**Solutions**:
- **Check file size**: Ensure it's under 100MB
- **Check file permissions**: Ensure you can read the file
- **Try different file**: Test with a small text file first
- **Check console output**: Look for error messages

### 8. Browser Won't Open

**Problem**: Web interface doesn't open automatically.

**Solutions**:
- **Manual navigation**: Go to `http://127.0.0.1:5000` in your browser
- **Check firewall**: Allow the application through Windows Firewall
- **Try different browser**: Use Chrome, Firefox, or Edge

## Quick Fixes

### For Most Issues:
1. **Stop the application** (Ctrl+C in terminal)
2. **Delete build files**: `Remove-Item -Recurse -Force dist, build`
3. **Rebuild**: `python build.py`
4. **Run fresh**: `.\dist\DisStored.exe`

### For Webhook Issues:
1. **Create .env file** with your webhook URL
2. **Test webhook** with a small file first
3. **Check Discord** for uploaded files

### For Large Files:
1. **Verify chunking** is working in console output
2. **Check Discord** for chunk files
3. **Test download** to ensure reconstruction works

## Getting Help

If you're still having issues:

1. **Check the console output** for error messages
2. **Try running from source**: `python app.py`
3. **Test with a simple file** first
4. **Check all dependencies** are installed

## System Requirements

- **Windows 10/11** (64-bit)
- **Python 3.7+** (for building)
- **4GB RAM** minimum
- **100MB free space** for the executable
- **Internet connection** for Discord uploads
