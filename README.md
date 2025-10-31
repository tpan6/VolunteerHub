# 🤝 VolunteerHub - Community Volunteering Platform

> A comprehensive web application connecting volunteers with meaningful opportunities in their community. Built for the Congressional App Challenge.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📖 About

VolunteerHub is a modern web platform that makes it easy for people to find, book, and track volunteer opportunities in their community. With an intuitive interface, interactive maps, and seamless booking system, we're making volunteering accessible to everyone.

### ✨ Key Features

- ** Interactive Map** - Browse opportunities on an interactive map with location-based search
- ** Smart Booking System** - OpenTable-style time slot selection for easy registration
- ** User Dashboard** - Track volunteer hours, manage bookings, and view history
- ** Advanced Search** - Filter by category, date, location, and duration
- ** Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- ** Secure Authentication** - User registration and login with password hashing
- ** Analytics** - Track impact with volunteer hour statistics and badges
- ** Beautiful UI** - Ocean-inspired professional theme with smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/volunteer-hub.git
cd volunteer-hub
```

2. **Create a virtual environment**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the database**
```bash
flask init-db
```

5. **Run the application**
```bash
python app.py
```

6. **Open your browser**
Navigate to `http://localhost:5000`

## 📁 Project Structure

```
volunteer-app/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── main.js       # JavaScript utilities
│   └── images/           # Image assets (add your own)
│
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Home page (Tobias)
    ├── map.html          # Interactive map (Sreehass)
    ├── booking.html      # Booking system (Thomas)
    ├── login.html        # Login page (Eshaan)
    ├── signup.html       # Registration page (Eshaan)
    ├── dashboard.html    # User dashboard (Eshaan)
    ├── opportunity_detail.html
    └── search_results.html
```

## 👥 Team Contributions

### Home Page - Tobias
- Hero section with compelling call-to-action
- Featured opportunities grid
- Stats dashboard
- Search bar integration
- "How It Works" section

### Map/Browse Page - Sreehass
- Interactive Google API map with markers
- Sidebar with filters and search
- Real-time opportunity filtering
- Location-based recommendations
- Category and date filtering

### Booking System - Thomas
- OpenTable-style time slot selection
- Date picker interface
- Booking form with validation
- Booking summary
- Confirmation flow

### Authentication & Volunteer Dashboard - Eshaan
- User registration with validation
- Secure login system
- Password hashing
- User dashboard with stats
- Booking management
- Volunteer history tracking
- Profile settings

## 🛠️ Technology Stack

**Backend:**
- Flask 3.0.0 - Web framework
- SQLAlchemy - ORM for database
- Flask-Login - User authentication
- SQLite - Database (development)

**Frontend:**
- HTML5/CSS3
- JavaScript (ES6+)
- Google Maps - Interactive maps
- Responsive design

**Key Features:**
- RESTful API design
- Password hashing with Werkzeug
- Session management
- CSRF protection
- SQL injection prevention

## 📱 Pages & Routes

| Route | Description | Team Member |
|-------|-------------|-------------|
| `/` | Home page with featured opportunities | Tobias |
| `/opportunities` | Interactive map view | Sreehass |
| `/map` | Alias for opportunities | Sreehass |
| `/opportunity/<id>` | Detailed opportunity view | Shared |
| `/booking/<id>` | Booking page | Thomas |
| `/login` | User login | Eshaan |
| `/signup` | User registration | Eshaan |
| `/dashboard` | User dashboard | Thomas |
| `/search` | Search results | Shared |

## 🗄️ Database Schema

### User Model
- Email, username, password (hashed)
- Profile information
- Role (volunteer/admin/organization)
- Created date and last login

### Opportunity Model
- Title, description, category
- Date, time, duration
- Location (address, lat/long)
- Organization reference
- Spots available/filled

### Booking Model
- User and opportunity references
- Booking time
- Status (confirmed/cancelled/completed)
- Emergency contact info
- Notes

### Organization Model
- Name, description
- Contact information
- Logo and website
- Verification status

## 🎨 Design Features

**Ocean-Inspired, Calming Theme:**
- Teal and deep blue color palette
- Professional and calming aesthetic
- High-quality photo backgrounds
- Parallax scrolling effects

**Smooth Animations:**
- Subtle hover effects
- Smooth page transitions
- Fade-in on scroll
- Interactive button feedback

**Accessibility:**
- High contrast text
- Keyboard navigation
- Screen reader friendly
- Responsive typography

## 🔒 Security Features

- Password hashing with Werkzeug
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure session management
- Input validation

## 📊 Future Enhancements

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

## 👨‍💻 Development Team

- **Tobias** - Home Page Development
- **Sreehass** - Interactive Map & Browse Features
- **Thomas** - Booking System
- **Eshaan** - Authentication & Dashboard

## 📧 Contact

For questions or feedback about this project:
- GitHub Issues: [Create an issue](https://github.com/yourusername/volunteer-hub/issues)
- Email: volunteerhub6@gmail.com

## 🙏 Acknowledgments

- Congressional App Challenge for this Constest
- Unsplash for placeholder images
- Google for mapping functionality
- Flask community for excellent documentation

---

**Built for the Congressional App Challenge 2025**
# VolunteerHub
