# Google Maps API Setup Guide

## Why Google Maps?

Google Maps provides better map quality, more features, and a more professional appearance compared to OpenStreetMap/Leaflet. Since you already have a Google Cloud project for OAuth, setting up Maps is easy!

## Step 1: Enable Google Maps JavaScript API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your existing project (the one you used for OAuth)
3. Go to **"APIs & Services" > "Library"**
4. Search for **"Maps JavaScript API"**
5. Click on it and press **"Enable"**
6. Also enable **"Places API"** (optional, for future features)

## Step 2: Create API Key

1. Go to **"APIs & Services" > "Credentials"**
2. Click **"Create Credentials" > "API Key"**
3. Your API key will be created (looks like: `AIzaSyXxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
4. **IMPORTANT**: Click "Restrict Key" to secure it

## Step 3: Restrict Your API Key (Important for Security)

1. After creating the key, click on it to edit
2. Under **"Application restrictions"**:
   - Select "HTTP referrers (web sites)"
   - Add referrers:
     - `http://localhost:3000/*` (for development)
     - `https://yourdomain.com/*` (for production)

3. Under **"API restrictions"**:
   - Select "Restrict key"
   - Choose:
     - Maps JavaScript API
     - Places API (if you enabled it)

4. Click **"Save"**

## Step 4: Add API Key to Your .env File

1. Open `/Users/qpan/Downloads/volunteer-app/.env`
2. Find the line: `GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here`
3. Replace with your actual key:
   ```
   GOOGLE_MAPS_API_KEY=AIzaSyXxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

## Step 5: Test It!

1. Restart your Flask app
2. Go to http://localhost:3000/map
3. You should see a beautiful Google Map with your volunteer opportunities!

## Features You Get with Google Maps

✅ **Better map quality** - High-resolution satellite imagery
✅ **Advanced markers** - Modern, customizable pins
✅ **Better performance** - Faster loading and smoother interactions
✅ **Street View** - Can add street view integration
✅ **Places integration** - Can search for nearby places
✅ **Directions** - Can add routing features
✅ **Geocoding** - Convert addresses to coordinates easily

## Pricing

- **FREE**: Up to 28,000 map loads per month
- **$7 per 1,000 loads** after that
- For a volunteer app, you'll likely stay well within the free tier!

## Security Notes

- ✅ Always restrict your API keys
- ✅ Never commit API keys to version control (already in .gitignore)
- ✅ Use different keys for development and production
- ✅ Monitor your API usage in Google Cloud Console

## Troubleshooting

**Map shows "For development purposes only" watermark:**
- This is normal without restrictions
- Add billing info to remove it (you won't be charged unless you exceed free tier)

**Map doesn't load:**
- Check that the API key is correct in .env
- Make sure Maps JavaScript API is enabled
- Check browser console for errors
- Verify your domain is in the allowed referrers list

**Map shows gray area:**
- API key might be restricted too much
- Check that your current URL is in the allowed referrers

## Useful Links

- [Google Maps JavaScript API Documentation](https://developers.google.com/maps/documentation/javascript)
- [API Key Best Practices](https://developers.google.com/maps/api-security-best-practices)
- [Google Cloud Console](https://console.cloud.google.com/)
