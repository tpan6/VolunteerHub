# 🤝 VolunteerHub - Community Volunteering Platform

> A comprehensive web application connecting volunteers with meaningful opportunities in their community. Built for the Congressional App Challenge.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📖 About

VolunteerHub is a modern web platform that makes it easy for people to find, book, and track volunteer opportunities in their community. With an intuitive interface, interactive maps, and seamless booking, VolunteerHub aims to lower the barrier to volunteering and increase community impact.

### ✨ Key Features

- **Interactive Map** - Browse opportunities on an interactive map with location-based search
- **Smart Booking System** - OpenTable-style time slot selection for easy registration
- **User Dashboard** - Track volunteer hours, manage bookings, and view history
- **Advanced Search** - Filter by category, date, location, and duration
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Secure Authentication** - User registration and login with password hashing
- **Analytics** - Track impact with volunteer hour statistics and badges
- **Beautiful UI** - Ocean-inspired professional theme with smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. Clone the repository
```bash
git clone https://github.com/tpan6/VolunteerHub.git
cd VolunteerHub
```

2. Create a virtual environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Initialize the database (see QUICKSTART.md for details)
```bash
flask init-db
```

5. Run the application
```bash
python app.py
```

6. Open your browser
Navigate to `http://localhost:5000`

## 📁 Project Structure

The repository layout at the project root (updated to match the repository):

````markdown
```
.toplevel files and directories
├── .env.example          # Example env vars for local development
├── .gitignore
├── DEPLOYMENT.md         # Deployment instructions and notes
├── GOOGLE_MAPS_SETUP.md  # How to configure Google Maps API keys
├── GOOGLE_OAUTH_SETUP.md # Google OAuth setup instructions
├── LICENSE
├── QUICKSTART.md         # Quickstart guide for developers
├── README.md             # This file (updated)
├── app.py                # Main Flask application entrypoint
├── models.py             # Database models and schema definitions
├── requirements.txt      # Python dependencies
├── setup.bat             # Windows setup helper script
├── setup.sh              # macOS/Linux setup helper script
├── static/               # Static frontend assets
│   ├── css/              # Project CSS files (e.g., style.css)
│   ├── js/               # JavaScript files (e.g., main.js)
│   └── images/           # Image assets (add your own)
└── templates/            # Jinja2 HTML templates used by Flask
    ├── base.html
    ├── index.html
    ├── map.html
    ├── booking.html
    ├── login.html
    ├── signup.html
    ├── dashboard.html
    ├── opportunity_detail.html
    └── search_results.html
```
```
````

Notes:
- The project root is intentionally flat and centered around `app.py` and `models.py` (Flask-style single-module app).
- The `static/` and `templates/` directories contain frontend assets and Jinja2 templates used by Flask; add new assets to the appropriate subdirectory.
- `DEPLOYMENT.md`, `QUICKSTART.md`, and the GOOGLE_* docs contain environment-specific instructions — check them when setting up external services.

## 👥 Team Contributions

### Home Page - Tobias
- Hero section with call-to-action, featured opportunities grid, stats dashboard, search bar, "How It Works"

### Map/Browse Page - Sreehass
- Interactive map with markers, sidebar filters, real-time filtering, location-based recommendations

### Booking System - Thomas
- OpenTable-style time slot selection, date picker, booking form validation, confirmation flow

### Authentication & Volunteer Dashboard - Eshaan
- User registration and secure login, password hashing, dashboard with stats and booking management

## 🛠 Technology Stack

**Backend:**
- Flask 3.0.0
- SQLAlchemy
- Flask-Login
- SQLite (development)

**Frontend:**
- HTML5/CSS3
- JavaScript (ES6+)
- Google Maps (interactive maps)

Security and best practices:
- Password hashing with Werkzeug
- CSRF protection
- Input validation and secure session management

## 📄 Pages & Routes

| Route | Description | Owner |
|-------|-------------|-------|
| `/` | Home page with featured opportunities | Tobias |
| `/opportunities` | Interactive map view | Sreehass |
| `/map` | Alias for opportunities | Sreehass |
| `/opportunity/<id>` | Detailed opportunity view | Shared |
| `/booking/<id>` | Booking page | Thomas |
| `/login` | User login | Eshaan |
| `/signup` | User registration | Eshaan |
| `/dashboard` | User dashboard | Thomas |
| `/search` | Search results | Shared |

## 🗄 Database Schema (summary)

### User
- Email, username, password (hashed), profile info, role, created/last login

### Opportunity
- Title, description, category, date/time, location (address, lat/long), organization, spots available

### Booking
- User & opportunity references, booking time, status (confirmed/cancelled/completed), notes

### Organization
- Name, description, contact info, logo, verification status

## 🎨 Design & Accessibility

- Ocean-inspired color palette (teal/deep blue), parallax and smooth animations
- Accessibility: high-contrast text, keyboard navigation, screen-reader friendly

## 🔒 Security Features

- Password hashing, CSRF protection, SQL injection & XSS mitigations, secure session handling

## 📈 Future Enhancements

- [ ] Email notifications
- [ ] Calendar integration (iCal export)
- [ ] Mobile app (React Native)
- [ ] Organization admin panel
- [ ] Advanced analytics dashboard
- [ ] Badge/achievement system
- [ ] Social sharing features
- [ ] Review and rating system
- [ ] Multi-language support

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👩‍💻 Development Team

- Tobias — Home Page
- Sreehass — Map & Browse
- Thomas — Booking System
- Eshaan — Authentication & Dashboard

## ✉️ Contact

- GitHub Issues: https://github.com/tpan6/VolunteerHub/issues
- Email: volunteerhub6@gmail.com

---

**Built for the Congressional App Challenge 2025**
