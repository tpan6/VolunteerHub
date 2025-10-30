# Google OAuth Setup Guide

## Current Status

⚠️ **Google OAuth is currently NOT configured** - The "Sign in with Google" button will not appear until you complete the setup below.

## Step 1: Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API"
   - Click "Enable"

4. Create OAuth credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Web application"
   - Add authorized redirect URIs:
     - For development: `http://localhost:3000/authorize/google`
     - For production: `https://yourdomain.com/authorize/google`
   - Click "Create"
   - **IMPORTANT:** A popup will appear with your **Client ID** and **Client Secret**
   - **Copy BOTH values immediately** - especially the Client Secret!
   - If you missed it: Click on your OAuth client name in the credentials list to view them again

## Step 2: Configure Your Application

1. Your `.env` file already exists. Open it and update these values:

2. **SECRET_KEY** - Already generated for you! ✅
   
3. **GOOGLE_CLIENT_ID** - Already added! ✅

4. **GOOGLE_CLIENT_SECRET** - You need to add this:
   - Go to [Google Cloud Console Credentials](https://console.cloud.google.com/apis/credentials)
   - Click on your OAuth 2.0 Client ID name
   - Copy the **Client secret** value
   - Paste it in your `.env` file where it says `PASTE_YOUR_CLIENT_SECRET_HERE`

Your `.env` should look like:
```
SECRET_KEY=eafb8901db66380b25e0936d69a7076dc2877524135cab16
GOOGLE_CLIENT_ID=222807778441-p977abrlc6mnovl1mqk4vksrcscahbd4.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
(The client secret usually starts with `GOCSPX-`)

## Step 3: Test the Integration

1. Start your Flask application
2. Go to the login or signup page
3. Click "Sign in with Google"
4. You should be redirected to Google's login page
5. After authentication, you'll be redirected back to your app and logged in

## How It Works

- When users click "Sign in with Google", they're redirected to `/login/google`
- This initiates the OAuth flow with Google
- Google authenticates the user and redirects to `/authorize/google`
- Your app receives the user's email, name, and Google ID
- If the user doesn't exist, a new account is created
- The user is logged in and redirected to the dashboard

## Security Notes

- Never commit your `.env` file to version control
- Use different credentials for development and production
- Keep your CLIENT_SECRET secure
- In production, always use HTTPS
