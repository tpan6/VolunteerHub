# 🚀 Deployment Guide

This guide covers deploying your VolunteerHub application to various platforms.

## Table of Contents
- [Heroku (Recommended for Beginners)](#heroku)
- [PythonAnywhere](#pythonanywhere)
- [DigitalOcean](#digitalocean)
- [AWS EC2](#aws-ec2)
- [Google Cloud Platform](#google-cloud)
- [Docker](#docker)

---

## 🔵 Heroku (Recommended)

Heroku is the easiest platform for beginners. Free tier available!

### Prerequisites
- Heroku account (free): https://signup.heroku.com/
- Heroku CLI installed: https://devcenter.heroku.com/articles/heroku-cli

### Step 1: Prepare Your Application

Create `Procfile` in the root directory:
```
web: gunicorn app:app
```

Create `runtime.txt`:
```
python-3.11.0
```

Update `requirements.txt` to add:
```
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

### Step 2: Configure for Production

Update `app.py` - change the last line:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

### Step 3: Initialize Git (if not done)
```bash
git init
git add .
git commit -m "Prepare for Heroku deployment"
```

### Step 4: Deploy to Heroku
```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-volunteerhub-app

# Deploy
git push heroku main

# Initialize database
heroku run flask init-db

# Open your app
heroku open
```

### Step 5: Set Environment Variables
```bash
heroku config:set SECRET_KEY='your-secret-key-here'
heroku config:set FLASK_ENV=production
```

### Troubleshooting
```bash
# View logs
heroku logs --tail

# Restart app
heroku restart

# Check dyno status
heroku ps
```

---

## 🐍 PythonAnywhere

Great for Python web apps, free tier with yourusername.pythonanywhere.com

### Step 1: Upload Your Code

1. Sign up at https://www.pythonanywhere.com
2. Open a Bash console
3. Clone your repository:
```bash
git clone https://github.com/YOUR-USERNAME/volunteer-hub.git
cd volunteer-hub
```

### Step 2: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 venv
pip install -r requirements.txt
```

### Step 3: Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Select "Flask"
4. Point to your app.py file
5. Set working directory to `/home/yourusername/volunteer-hub`

### Step 4: Configure WSGI file

Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
```python
import sys
path = '/home/yourusername/volunteer-hub'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### Step 5: Initialize Database
```bash
cd /home/yourusername/volunteer-hub
flask init-db
```

### Step 6: Reload Web App
Click "Reload" button in the Web tab

---

## 🌊 DigitalOcean

More control, great for production. $6/month starts.

### Step 1: Create Droplet

1. Sign up at https://www.digitalocean.com
2. Create a Droplet (Ubuntu 22.04)
3. Choose $6/month plan
4. SSH into your droplet:
```bash
ssh root@your-droplet-ip
```

### Step 2: Install Dependencies
```bash
apt update
apt upgrade -y
apt install python3-pip python3-venv nginx -y
```

### Step 3: Clone and Setup
```bash
cd /var/www
git clone https://github.com/YOUR-USERNAME/volunteer-hub.git
cd volunteer-hub

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Step 4: Configure Gunicorn

Create `/etc/systemd/system/volunteerhub.service`:
```ini
[Unit]
Description=VolunteerHub
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/volunteer-hub
Environment="PATH=/var/www/volunteer-hub/venv/bin"
ExecStart=/var/www/volunteer-hub/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 app:app

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
systemctl start volunteerhub
systemctl enable volunteerhub
```

### Step 5: Configure Nginx

Create `/etc/nginx/sites-available/volunteerhub`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /var/www/volunteer-hub/static;
    }
}
```

Enable site:
```bash
ln -s /etc/nginx/sites-available/volunteerhub /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Step 6: SSL with Let's Encrypt (Optional but Recommended)
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com
```

---

## 🐳 Docker (Advanced)

For containerized deployment.

### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=your-secret-key
      - DATABASE_URL=sqlite:///volunteer.db
    volumes:
      - ./:/app
    command: gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

### Deploy
```bash
docker-compose up -d
```

---

## ☁️ AWS EC2

Similar to DigitalOcean but with AWS infrastructure.

### Step 1: Launch EC2 Instance
1. Go to AWS Console
2. Launch Ubuntu 22.04 instance
3. Configure security groups (allow HTTP/HTTPS)
4. Download key pair

### Step 2: Connect
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### Step 3: Follow DigitalOcean steps above
The setup is identical to DigitalOcean after connecting.

---

## 🔧 Production Checklist

Before deploying to production:

### Security
- [ ] Change SECRET_KEY to a strong random value
- [ ] Set `DEBUG = False` in production
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS/SSL
- [ ] Set up CORS if needed
- [ ] Add rate limiting
- [ ] Implement CSRF protection

### Database
- [ ] Use production database (PostgreSQL/MySQL)
- [ ] Set up regular backups
- [ ] Configure connection pooling
- [ ] Add database migrations

### Performance
- [ ] Enable caching (Redis)
- [ ] Optimize static file serving
- [ ] Use CDN for assets
- [ ] Configure proper logging
- [ ] Set up monitoring (New Relic, Sentry)

### Environment Variables
```python
# Add to app.py
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
```

Create `.env` file:
```
SECRET_KEY=your-super-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
FLASK_ENV=production
```

---

## 📊 Monitoring & Maintenance

### Set Up Logging
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('error.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Health Check Endpoint
Add to `app.py`:
```python
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200
```

### Backup Database
```bash
# SQLite
cp volunteer.db volunteer_backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump dbname > backup_$(date +%Y%m%d).sql
```

---

## 🆘 Troubleshooting

### Common Issues

**500 Error:**
- Check logs
- Verify database connection
- Check file permissions

**Static files not loading:**
- Configure Nginx to serve static files
- Check static file paths

**Database errors:**
- Run migrations
- Check database credentials
- Verify database exists

**Performance issues:**
- Add caching
- Optimize database queries
- Use CDN for static files

---

## 📚 Additional Resources

- [Flask Deployment Options](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [Heroku Python Support](https://devcenter.heroku.com/articles/python-support)
- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials)
- [Docker Documentation](https://docs.docker.com/)

---

## 🎉 You're Live!

Once deployed, don't forget to:
- Test all features
- Monitor logs
- Set up SSL certificate
- Configure domain name
- Share with the world! 🌍

Good luck with your deployment! 🚀
