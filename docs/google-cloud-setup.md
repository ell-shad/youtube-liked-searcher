# Google Cloud Setup Guide

*Only needed for Advanced Setup - skip if using Quick Setup*

## Overview
This guide walks you through creating your own Google Cloud project and OAuth credentials for the YouTube Liked Videos Searcher.

## Step 1: Create Google Cloud Project

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create New Project**
   - Click "Select a project" dropdown at the top
   - Click "NEW PROJECT"
   - Project name: `YouTube Video Searcher` (or any name)
   - Click "CREATE"
   - Wait for project creation, then select it

## Step 2: Enable YouTube Data API

1. **Go to APIs & Services**
   - In the left sidebar: "APIs & Services" → "Library"
   
2. **Find YouTube Data API**
   - Search for "YouTube Data API v3"
   - Click on the result
   - Click "ENABLE"

## Step 3: Configure OAuth Consent Screen

1. **Go to OAuth consent screen**
   - Left sidebar: "APIs & Services" → "OAuth consent screen"

2. **Choose User Type**
   - Select "External" (allows anyone with Google account)
   - Click "CREATE"

3. **App Information** (Required fields only)
   - App name: `YouTube Video Searcher`
   - User support email: Your email
   - App logo: (optional)
   - App domain: (leave blank)
   - Authorized domains: (leave blank)
   - Developer contact: Your email
   - Click "SAVE AND CONTINUE"

4. **Scopes** (Step 2)
   - Click "SAVE AND CONTINUE" (no changes needed)

5. **Test Users** (Step 3)
   - Add your own email address
   - Add emails of people who will use the app (max 100)
   - Click "SAVE AND CONTINUE"

6. **Summary** (Step 4)
   - Review and click "BACK TO DASHBOARD"

## Step 4: Create OAuth Credentials

1. **Go to Credentials**
   - Left sidebar: "APIs & Services" → "Credentials"

2. **Create Credentials**
   - Click "CREATE CREDENTIALS" → "OAuth client ID"
   
3. **Configure OAuth Client**
   - Application type: "Desktop application"
   - Name: `YouTube Searcher Desktop`
   - Click "CREATE"

4. **Download Credentials**
   - A popup will show your client ID and secret
   - Click "DOWNLOAD JSON"
   - Save the file as `client_secret.json` in your project folder

## Step 5: Test Your Setup

1. **Verify Files**
    ``` 
    your-project-folder/
    ├── src/
    │   └── youtube_searcher.py
    ├── client_secret.json    ← Your downloaded file
    └── requirements.txt
    ```

2. **Run the Application**
   ```bash
   python src/youtube_searcher.py
   ```

3. **Test Authentication**
   - Click "Authenticate & Load Liked Videos"
   - Browser should open with Google login
   - Grant permissions when prompted

## Understanding API Quotas

### Daily Limits
- **Free quota**: 10,000 units per day
- **Typical usage**: 2-5 units per liked video
- **Example**: 2,000 liked videos = ~6,000 units

### Quota Usage
- Loading 100 videos ≈ 200-300 units
- Loading 1,000 videos ≈ 2,000-3,000 units
- Searching cached videos = 0 units

### If You Exceed Quota
- Wait until next day (resets at midnight Pacific Time)
- Or request quota increase (for heavy usage)

## Troubleshooting

### "OAuth consent screen configuration is incomplete"
**Solution:** Complete all required fields in OAuth consent screen setup

### "redirect_uri_mismatch" error
**Solution:** 
1. Go to Credentials → Edit your OAuth client
2. Add these Authorized redirect URIs:
   ```
   http://localhost:8080/
   http://localhost:8081/
   http://localhost:8082/
   ```

### "Access blocked: This app's request is invalid"
**Solution:** Make sure you:
- Enabled YouTube Data API v3
- Configured OAuth consent screen completely
- Added your email as a test user

### "The project does not have access to this API"
**Solution:** Enable YouTube Data API v3 in your project

### "insufficient_scope" error
**Solution:** Delete `token.json` file and re-authenticate

## Security Best Practices

### Protect Your Credentials
- ❌ **Never share your `client_secret.json` publicly**
- ❌ **Never commit it to public repositories**
- ✅ **Keep it in your local project folder only**

### For Multiple Users
If you want to share your app:
- Option 1: Each user creates their own OAuth app (this guide)
- Option 2: You share your OAuth app (add them as test users)

### Revoke Access
If you want to stop the app's access:
1. Go to [Google Account Permissions](https://myaccount.google.com/permissions)
2. Find your YouTube app
3. Click "Remove Access"

## Next Steps

Once you have `client_secret.json`:
1. Place it in your project root directory
2. Run the application
3. Authenticate with Google
4. Start searching your liked videos!

Need help? Create an [Issue](https://github.com/your-username/youtube-liked-searcher/issues) with your error details.