# 🚀 Quick Start Guide

Get VolunteerHub running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (comes with Python)
- Git (optional, for cloning)

## Option 1: Automated Setup (Recommended)

### On macOS/Linux:
```bash
chmod +x setup.sh
./setup.sh
```

### On Windows:
```cmd
setup.bat
```

## Option 2: Manual Setup

### Step 1: Create Virtual Environment
```bash
python -m venv venv
```

### Step 2: Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```cmd
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
flask init-db
```

This creates sample data including:
- 3 organizations
- 3 volunteer opportunities
- Database tables

### Step 5: Run the Application
```bash
python app.py
```

### Step 6: Open Your Browser
Navigate to: `http://localhost:5000`

## 🎯 First Steps After Launch

1. **Browse Opportunities**
   - Click "Browse" in the navigation
   - See opportunities on the interactive map
   - Use filters to find what you're looking for

2. **Create an Account**
   - Click "Sign Up" in the navigation
   - Fill in your information
   - Start booking volunteer opportunities!

3. **Book Your First Opportunity**
   - Click on any opportunity card
   - View the details
   - Click "Book Your Spot"
   - Select your preferred time slot

4. **Access Your Dashboard**
   - Click "Dashboard" after logging in
   - View your upcoming bookings
   - Track your volunteer hours

## 🛠️ Troubleshooting

### "Flask command not found"
Make sure you've activated the virtual environment.

### "Module not found" errors
Run: `pip install -r requirements.txt`

### Database errors
Run: `flask init-db` to recreate the database

### Port 5000 already in use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📝 Test Accounts

After running `flask init-db`, you can create a test account through the signup page.

## 🎨 Customization

### Adding Your Own Photos
1. Place images in `static/images/`
2. Update image URLs in opportunities
3. Recommended size: 1200x800px for hero images

### Changing Colors
Edit `static/css/style.css` and update the CSS variables:
```css
:root {
    --primary-color: #0f4c5c;
    --secondary-color: #5fb3c5;
    /* ... */
}
```

## 📧 Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Review the code comments
- Check Flask documentation: https://flask.palletsprojects.com/

## 🎉 You're Ready!

Your VolunteerHub application is now running. Start exploring and making a difference in your community!

---

**Built for Congressional App Challenge 2025** 🏆
