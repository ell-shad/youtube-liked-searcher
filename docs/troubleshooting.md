# Troubleshooting Guide

Common issues and solutions for YouTube Liked Videos Searcher.

## Installation Issues

### Python Not Found
```
'python' is not recognized as an internal or external command
```
**Solutions:**
- Install Python 3.7+ from [python.org](https://python.org)
- During installation, check "Add Python to PATH"
- Use `python3` instead of `python` on Mac/Linux
- Try `py` on Windows

### Package Installation Fails
```
ERROR: Could not find a version that satisfies the requirement...
```
**Solutions:**
- Update pip: `pip install --upgrade pip`
- Use Python 3.7+: `python --version`
- Try: `pip3 install -r requirements.txt`
- On Mac with M1: `arch -arm64 pip install -r requirements.txt`

### ModuleNotFoundError
```
ModuleNotFoundError: No module named 'googleapiclient'
```
**Solutions:**
- Install requirements: `pip install -r requirements.txt`
- Check you're in the correct directory
- Try: `pip install google-api-python-client`

## Authentication Issues

### Client Secret Not Found
```
client_secret.json not found
```
**Solutions:**
- **Quick Setup**: Download release ZIP (not source code)
- **Advanced Setup**: Complete Google Cloud setup first
- Ensure file is in project root, not in subdirectories

### "This app isn't verified by Google"
**Status:** This is normal for testing apps

**What to do:**
1. Click "Advanced"
2. Click "Go to [App Name] (unsafe)"
3. This is safe - just Google's warning for unverified apps

### Authentication Window Doesn't Open
**Solutions:**
- Check firewall blocking localhost connections
- Try different port: edit redirect URI in Google Cloud Console
- Manually copy URL from terminal and open in browser

### Token Expires After 7 Days
**Status:** Normal for testing OAuth apps

**Solutions:**
- Click "Authenticate & Load Liked Videos" again
- Delete `token.json` and re-authenticate
- This is expected behavior for unpublished apps

## API Issues

### Quota Exceeded Error
```
HttpError 403: quotaExceeded
```
**Solutions:**
- Wait until next day (quota resets midnight Pacific Time)
- Use cached data (works offline after first load)
- For heavy usage: request quota increase in Google Cloud Console

### No Videos Found
**Possible causes:**
- No liked videos in your YouTube account
- API permissions not granted correctly
- Account has YouTube restricted/disabled

**Solutions:**
- Check you have liked videos on YouTube.com
- Re-authenticate with full permissions
- Try with different Google account

### API Key Invalid
```
HttpError 400: keyInvalid
```
**Solutions:**
- Regenerate `client_secret.json` in Google Cloud Console
- Ensure YouTube Data API v3 is enabled
- Check project is selected correctly

## Application Issues

### Slow Loading
**Causes:**
- Large number of liked videos (1000+)
- Slow internet connection
- YouTube API rate limiting

**Solutions:**
- Wait for initial load (only happens once)
- Check internet connection
- Subsequent loads use cached data (much faster)

### Search Not Working
**Check:**
- Are videos loaded? (status shows "Loaded X videos")
- Try simpler search terms
- Search is case-insensitive

### Sorting Issues
**Solutions:**
- Click column header to sort
- Click again to reverse sort
- Look for ↑↓ arrows in headers

### Window Layout Problems
**Solutions:**
- Resize window manually
- Try maximizing window
- Restart application

## File Issues

### Permission Errors
```
PermissionError: [Errno 13] Permission denied
```
**Solutions:**
- Run as administrator/sudo (not recommended)
- Change folder permissions
- Move to user directory (Documents, Desktop)

### Cache File Corrupted
**Symptoms:** App crashes on startup

**Solutions:**
- Delete `liked_videos_cache.json`
- Delete `token.json`
- Restart and re-authenticate

## Platform-Specific Issues

### Windows
- Use `python` or `py` command
- Some antivirus may block network connections
- Windows Defender might flag the app (false positive)

### macOS
- Use `python3` command
- May need to allow app in Security & Privacy settings
- M1 Macs: ensure compatible Python packages

### Linux
- Use `python3` and `pip3`
- May need to install tkinter: `sudo apt install python3-tk`
- Ensure Python 3.7+ is installed

## Error Messages

### "Unable to open a web browser"
**Solutions:**
- Manually copy authentication URL from terminal
- Open URL in any browser
- Complete authentication process

### "Connection refused"
**Solutions:**
- Check internet connection
- Try different DNS (8.8.8.8, 1.1.1.1)
- Disable VPN temporarily

### "SSL Certificate error"
**Solutions:**
- Update Python certificates
- Check system date/time
- Update Python to latest version

## Getting More Help

### Before Reporting Issues
1. Check this troubleshooting guide
2. Try the solutions above
3. Update to latest version

### Reporting Bugs
Create an issue with:
- Operating system and version
- Python version (`python --version`)
- Complete error message
- Steps to reproduce

### Useful Information to Include
```bash
# System info
python --version
pip --version

# Package versions
pip list | grep google

# Error logs (run with verbose output)
python src/youtube_searcher.py --verbose
```

### Contact
- 🐛 [GitHub Issues](https://github.com/your-username/youtube-liked-searcher/issues)
- 📧 Email: ellshad.012@gmail.com

## Quick Fixes Summary

| Problem | Quick Fix |
|---------|-----------|
| Python not found | Install Python 3.7+ |
| Missing packages | `pip install -r requirements.txt` |
| Client secret missing | Download release ZIP |
| "App not verified" | Click Advanced → Go to app |
| No videos load | Check internet, re-authenticate |
| Quota exceeded | Wait until tomorrow |
| App crashes | Delete cache files, restart |
| Slow performance | Wait for initial load, use cache |

Most issues are solved by ensuring you have the correct Python version and following the setup instructions exactly.