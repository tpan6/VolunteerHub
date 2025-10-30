from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for volunteers and organizations"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    zip_code = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    role = db.Column(db.String(20), default='volunteer')  # volunteer, admin, organization
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))  # For organization users
    profile_image = db.Column(db.String(255))
    interests = db.Column(db.Text)  # Comma-separated interests
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')
    managed_organization = db.relationship('Organization', backref='manager', foreign_keys='User.organization_id')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    @property
    def total_hours(self):
        """Calculate total volunteer hours"""
        return sum(booking.hours for booking in self.bookings if booking.status == 'completed')
    
    @property
    def upcoming_bookings_count(self):
        """Count upcoming bookings"""
        return len([b for b in self.bookings if b.opportunity.date >= datetime.now().date()])

class Organization(db.Model):
    """Organization model for nonprofits"""
    __tablename__ = 'organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    logo = db.Column(db.String(255))
    website = db.Column(db.String(255))
    contact_email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Relationships
    opportunities = db.relationship('Opportunity', backref='organization', lazy=True)
    
    def __repr__(self):
        return f'<Organization {self.name}>'

class Opportunity(db.Model):
    """Volunteer opportunity model"""
    __tablename__ = 'opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    category = db.Column(db.String(50))  # Environment, Education, Food Security, etc.
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(20))
    hours = db.Column(db.Integer)  # Duration in hours
    spots_available = db.Column(db.Integer, default=1)
    spots_filled = db.Column(db.Integer, default=0)
    
    # Location
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Details
    requirements = db.Column(db.Text)
    what_to_bring = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    is_recurring = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_urgent = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='opportunity', lazy=True, cascade='all, delete-orphan')
    time_slots = db.relationship('TimeSlot', backref='opportunity', lazy=True, cascade='all, delete-orphan', order_by='TimeSlot.start_time')
    
    def __repr__(self):
        return f'<Opportunity {self.title}>'
    
    @property
    def spots_remaining(self):
        """Calculate total remaining spots across all time slots"""
        if self.time_slots:
            # If opportunity has time slots, sum up remaining spots from all slots
            return sum(slot.spots_remaining for slot in self.time_slots)
        else:
            # Fallback for opportunities without time slots
            confirmed_bookings = len([b for b in self.bookings if b.status == 'confirmed'])
            return self.spots_available - confirmed_bookings
    
    @property
    def is_full(self):
        """Check if all time slots are full"""
        if self.time_slots:
            return all(slot.is_full for slot in self.time_slots)
        else:
            return self.spots_remaining <= 0
    
    @property
    def formatted_date(self):
        """Return formatted date string"""
        return self.date.strftime('%B %d, %Y') if self.date else 'TBD'

class Booking(db.Model):
    """Booking/Registration model"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'), nullable=False)
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slots.id'))  # Link to specific time slot
    booking_time = db.Column(db.DateTime, nullable=False)
    hours = db.Column(db.Integer)  # Actual hours volunteered
    status = db.Column(db.String(20), default='confirmed')  # confirmed, cancelled, completed, no-show
    notes = db.Column(db.Text)
    emergency_contact = db.Column(db.String(100))
    emergency_phone = db.Column(db.String(20))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Booking {self.id} - User {self.user_id} - Opp {self.opportunity_id}>'
    
    @property
    def can_cancel(self):
        """Check if booking can be cancelled (24 hours before)"""
        if not self.opportunity.date:
            return False
        time_until = datetime.combine(self.opportunity.date, datetime.min.time()) - datetime.now()
        return time_until.days >= 1

class TimeSlot(db.Model):
    """Time slot model for OpenTable-style booking"""
    __tablename__ = 'time_slots'
    
    id = db.Column(db.Integer, primary_key=True)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'), nullable=False)
    start_time = db.Column(db.String(20), nullable=False)  # e.g., "9:00 AM"
    end_time = db.Column(db.String(20))  # e.g., "10:00 AM"
    spots_available = db.Column(db.Integer, default=1)
    is_available = db.Column(db.Boolean, default=True)
    
    # Relationships
    bookings = db.relationship('Booking', backref='time_slot', lazy=True)
    
    def __repr__(self):
        return f'<TimeSlot {self.start_time} for Opportunity {self.opportunity_id}>'
    
    @property
    def spots_remaining(self):
        """Calculate remaining spots for this time slot"""
        confirmed_bookings = len([b for b in self.bookings if b.status == 'confirmed'])
        return self.spots_available - confirmed_bookings
    
    @property
    def is_full(self):
        """Check if this time slot is full"""
        return self.spots_remaining <= 0
