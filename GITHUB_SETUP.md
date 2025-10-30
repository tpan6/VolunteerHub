# 📦 Pushing to GitHub

Follow these steps to upload your VolunteerHub project to GitHub.

## Prerequisites

- A GitHub account ([sign up here](https://github.com/join))
- Git installed on your computer ([download here](https://git-scm.com/downloads))

## Step-by-Step Guide

### 1. Create a New Repository on GitHub

1. Go to [github.com](https://github.com)
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the details:
   - **Repository name**: `volunteer-hub` (or your preferred name)
   - **Description**: "Community volunteering platform built for Congressional App Challenge"
   - **Visibility**: Public or Private
   - ⚠️ **Do NOT** initialize with README, .gitignore, or license (we already have these)
5. Click "Create repository"

### 2. Initialize Git in Your Project

Open terminal/command prompt in the `volunteer-app` directory and run:

```bash
git init
```

### 3. Add All Files

```bash
git add .
```

### 4. Make Your First Commit

```bash
git commit -m "Initial commit: Complete VolunteerHub application"
```

### 5. Connect to GitHub

Replace `YOUR-USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR-USERNAME/volunteer-hub.git
```

### 6. Push to GitHub

```bash
git branch -M main
git push -u origin main
```

### 7. Enter Your Credentials

GitHub will prompt you for authentication. Use one of these methods:

**Option A: Personal Access Token (Recommended)**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` permissions
3. Use the token as your password

**Option B: SSH Keys**
Set up SSH keys following [GitHub's guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

## ✅ Verify Upload

1. Go to `https://github.com/YOUR-USERNAME/volunteer-hub`
2. You should see all your files!
3. The README.md will be displayed automatically

## 🎨 Enhance Your Repository

### Add Topics
1. Go to your repository
2. Click the gear icon next to "About"
3. Add topics: `flask`, `volunteering`, `python`, `congressional-app-challenge`

### Add Repository Description
Add a short description: "Community volunteering platform with interactive maps and booking system"

### Enable GitHub Pages (Optional)
If you want to host documentation:
1. Go to Settings → Pages
2. Select source: `main` branch, `/docs` folder
3. Add documentation to a `docs/` folder

## 📊 Update README

Before pushing, update the README.md:

1. Replace placeholder URLs:
```markdown
# Change this:
git clone https://github.com/yourusername/volunteer-hub.git

# To this:
git clone https://github.com/YOUR-USERNAME/volunteer-hub.git
```

2. Add screenshots (optional):
```markdown
## Screenshots

![Home Page](screenshots/home.png)
![Map View](screenshots/map.png)
```

## 🔄 Future Updates

After making changes to your code:

```bash
git add .
git commit -m "Description of your changes"
git push
```

## 🌟 Common Commands

```bash
# Check status
git status

# View commit history
git log

# Create a new branch
git checkout -b feature-name

# Switch branches
git checkout main

# Pull latest changes
git pull

# View remote URLs
git remote -v
```

## 🎓 For Congressional App Challenge

### Important Files to Include:
- ✅ README.md with project description
- ✅ Clear installation instructions
- ✅ Code comments
- ✅ .gitignore to exclude unnecessary files
- ✅ requirements.txt for dependencies

### Repository Best Practices:
1. **Write clear commit messages**
   - Good: "Add booking system with time slot selection"
   - Bad: "updated stuff"

2. **Add a LICENSE file**
   ```bash
   # Add MIT License
   curl https://raw.githubusercontent.com/licenses/license-templates/master/templates/mit.txt > LICENSE
   ```

3. **Create a CONTRIBUTORS.md**
   ```markdown
   # Contributors

   - **Tobias** - Home Page Development
   - **Sreehass** - Interactive Map & Browse Features  
   - **Thomas** - Booking System
   - **Eshaan** - Authentication & Dashboard
   ```

4. **Add screenshots to README**
   - Create a `screenshots/` folder
   - Take screenshots of key features
   - Reference them in README.md

## 🚨 Important Notes

### Don't Commit:
- ❌ `venv/` folder (already in .gitignore)
- ❌ `__pycache__/` folders (already in .gitignore)
- ❌ `.env` files with secrets
- ❌ `*.db` database files with personal data

### Do Commit:
- ✅ All `.py` files
- ✅ All `.html` templates
- ✅ All `.css` and `.js` files
- ✅ `requirements.txt`
- ✅ README.md and documentation
- ✅ .gitignore

## 🎉 You're Done!

Your project is now on GitHub! Share the link with:
- Congressional App Challenge judges
- Your team members
- On your resume/portfolio

Example: `https://github.com/YOUR-USERNAME/volunteer-hub`

## 📝 Next Steps

1. **Add GitHub Actions** for automated testing
2. **Set up CI/CD** for deployment
3. **Enable Dependabot** for security updates
4. **Add badges** to README (build status, license, etc.)
5. **Write a CONTRIBUTING.md** if you want collaborators

---

**Need help?** Check out [GitHub's documentation](https://docs.github.com/)
