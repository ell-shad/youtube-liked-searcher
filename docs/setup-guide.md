
# Setup Guide - YouTube Liked Videos Searcher

## Choose Your Installation Method

### 🚀 Option 1: Quick Setup (Recommended)
*Perfect for most users - no Google Cloud setup needed*

#### Prerequisites
- Python 3.7 or higher installed
- Google account with YouTube

#### Steps
1. **Download the latest release**
   - Go to [Releases](https://github.com/your-username/youtube-liked-searcher/releases)
   - Download `youtube-liked-searcher-v1.x.zip`
   - Extract to a folder on your computer

2. **Install Python dependencies**
   ```bash
   # Open terminal/command prompt in the extracted folder
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python src/youtube_searcher.py
   ```

4. **Authenticate**
   - Click "Authenticate & Load Liked Videos"
   - Your browser will open
   - Sign in to your Google account
   - You'll see a warning: "This app isn't verified by Google"
   - Click "Advanced" → "Go to YouTube Searcher (unsafe)" 
   - Grant permissions

5. **Start using!**
   - Videos will load automatically (may take a few minutes)
   - Use the search box to find specific videos
   - Click videos to see full details
   - Double-click to open in YouTube

---

### 🔧 Option 2: Advanced Setup
*Create your own Google Cloud OAuth app*

#### Why Choose This Option?
- Get your own 10,000 daily API quota
- Complete independence from the shared app
- Maximum security and control

#### Prerequisites
- Python 3.7 or higher
- Google account with access to Google Cloud Console
- Basic technical knowledge

#### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/youtube-liked-searcher.git
   cd youtube-liked-searcher
   ```

2. **Set up Google Cloud Project**
   - Follow the [Google Cloud Setup Guide](google-cloud-setup.md)
   - Download your `client_secret.json` file
   - Place it in the project root directory

3. **Install and run**
   ```bash
   pip install -r requirements.txt
   python src/youtube_searcher.py
   ```

## Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'googleapiclient'"
**Solution:** Install the required packages
```bash
pip install -r requirements.txt
```

#### "client_secret.json not found"
**Solution:** 
- **Quick Setup**: Make sure you downloaded the release ZIP (not the source code)
- **Advanced Setup**: Complete the Google Cloud setup and place the file correctly

#### "This app isn't verified by Google"
**Solution:** This is normal for testing apps
1. Click "Advanced"
2. Click "Go to YouTube Searcher (unsafe)"
3. This is safe - it's just Google's warning for unverified apps

#### Authentication expires after 7 days
**Solution:** This is normal for testing apps
- Just click "Authenticate & Load Liked Videos" again
- For permanent tokens, the app would need to be published (complex process)

#### Videos not loading / API errors
**Solution:** Check these common causes:
- Internet connection working?
- Google account has YouTube liked videos?
- API quota exceeded? (Try again tomorrow)

#### Performance issues with many videos
**Solution:** 
- The app caches videos locally after first load
- Large collections (1000+ videos) may take time initially
- Subsequent runs will be much faster

## File Explanations

### Generated Files
- `token.json` - Your authentication token (don't share this)
- `liked_videos_cache.json` - Local cache of your videos
- `youtube_liked_search_results_*.json` - Exported search results

### Safe to Delete
If you want to reset the app, you can safely delete:
- `token.json` (will need to re-authenticate)
- `liked_videos_cache.json` (will need to reload videos)

## Features Guide

### Search Tips
- Search across titles, channel names, and descriptions
- Use specific keywords for better results
- Search is case-insensitive

### Sorting
- Click any column header to sort
- Click again to reverse sort order
- Look for ↑↓ arrows showing current sort

### Keyboard Shortcuts
- `Ctrl+Q` - Quit application
- `Ctrl+R` - Refresh videos from YouTube
- `Ctrl+E` - Export current search results
- `F1` - Show help

### Export Options
- **Export Current Results** - Only videos matching your search
- **Export All Videos** - Your complete liked videos collection
- Files are saved as JSON format

## Privacy & Data

### What Data is Accessed?
- Your YouTube liked videos list only
- Video titles, descriptions, channel names, dates

### Where is Data Stored?
- Everything stays on your computer
- No data sent to external servers (except Google for authentication)
- Cache files are stored locally for faster loading

### How to Remove Data?
- Delete the application folder
- Revoke access: [Google Account Permissions](https://myaccount.google.com/permissions)

Need more help? Check [Troubleshooting Guide](troubleshooting.md) or create an [Issue](https://github.com/your-username/youtube-liked-searcher/issues).


