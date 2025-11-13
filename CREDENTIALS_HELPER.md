# YouTube API Credentials Helper

## Quick Summary: What You Need to Do

You need to obtain credentials from Google Cloud that allow the agent to access your YouTube channel. This requires:

1. Creating a Google Cloud Project
2. Enabling YouTube Data API v3
3. Creating OAuth 2.0 Desktop Application credentials
4. Downloading the credentials JSON file

## Security Level: 2-Step Verification Required

Google Cloud now requires 2-Step Verification (2SV/MFA) on all accounts.

### If you DON'T have 2-Step Verification enabled:

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click **Security** in the left menu
3. Click **2-Step Verification**
4. Follow the prompts (takes ~5 minutes)
   - Choose phone-based verification or authenticator app
   - Verify your phone number
   - Save backup codes in a safe place

### Once 2-Step Verification is enabled:

1. Refresh your browser (you should now have access to Google Cloud)
2. Follow the SETUP_GUIDE.md steps

## The Complete Credentials Workflow

### Phase 1: Google Cloud Setup (15 minutes)

```
1. Login to console.cloud.google.com
2. Create new project "youtube-automation-agent"
3. Go to APIs & Services > Library
4. Search and enable "YouTube Data API v3"
5. Go to Credentials
6. Create OAuth 2.0 Desktop Application credentials
7. Download as JSON (save as client_secret.json)
```

### Phase 2: Authentication (5 minutes first time)

```
1. Place client_secret.json in project root
2. Run: python youtube_agent.py
3. Browser opens automatically
4. Grant permissions to your channel
5. token.pickle is created automatically
6. Ready to use!
```

## File Locations

After setup, you'll have:

- `client_secret.json` - Downloaded from Google Cloud Console
- `token.pickle` - Auto-created on first run
- `.env` - Your custom configuration

## Your Current Status

✅ Agent code is complete  
✅ Documentation is ready  
✅ setup.sh is ready  
⏳ Need: Your YouTube API credentials from Google Cloud  

## Next Action

**Enable 2-Step Verification first** (if not already done):

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Click "2-Step Verification"
3. Follow phone verification
4. Come back and follow SETUP_GUIDE.md

## Alternative: Use Service Account (if you want)

If you want to use a Service Account instead of OAuth:

1. In Google Cloud Console, go to Credentials
2. Create Service Account
3. Create and download JSON key
4. Place in project root
5. Uncomment service account code in youtube_agent.py

(Not recommended for personal channel, but available)

## Troubleshooting

### "Access Blocked" message
- **Cause:** 2-Step Verification not enabled
- **Fix:** Enable it at myaccount.google.com/security

### "Invalid Client" error  
- **Cause:** client_secret.json in wrong location
- **Fix:** Place in root directory where youtube_agent.py is

### "Permissions denied" after clicking Allow
- **Cause:** Wrong OAuth scope permissions
- **Fix:** Delete token.pickle and try again

### "API not enabled" error
- **Cause:** YouTube Data API v3 not enabled in project
- **Fix:** Go to APIs & Services > Library, search YouTube, enable

## Getting Help

1. Check SETUP_GUIDE.md for complete instructions
2. Verify all files are in correct locations
3. Check logs/agent.log for specific errors
4. Open GitHub issue if still stuck

## Important Security Notes

⚠️ **NEVER:**
- Commit client_secret.json to Git
- Share token.pickle with anyone
- Expose .env file publicly

✅ **DO:**
- Keep these files in .gitignore (already configured)
- Store backups safely
- Use different credentials for different projects

## Time Estimate

- Enable 2-Step Verification: 5-10 minutes
- Get API Credentials: 10-15 minutes
- First Agent Run: 2-5 minutes
- **Total: 20-30 minutes for complete setup**

## You're Almost There!

The agent is 100% ready. You just need your YouTube credentials.
Once you have the client_secret.json file, you can immediately start uploading!
