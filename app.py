from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import db and models
from models import db, User, Opportunity, Booking, Organization, TimeSlot

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///volunteer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Google OAuth Config
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')

# Google Maps API Key
app.config['GOOGLE_MAPS_API_KEY'] = os.getenv('GOOGLE_MAPS_API_KEY')

# Initialize db with app
db.init_app(app)

# Initialize OAuth (only if credentials are provided)
oauth = OAuth(app)
if app.config.get('GOOGLE_CLIENT_ID') and app.config['GOOGLE_CLIENT_ID'] != 'your-google-client-id-here':
    google = oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
else:
    google = None

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== ROLE-BASED ACCESS DECORATORS ====================
def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def organization_required(f):
    """Decorator to require organization role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'organization':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# Context processor to make variables available to all templates
@app.context_processor
def inject_globals():
    return {
        'GOOGLE_MAPS_API_KEY': app.config.get('GOOGLE_MAPS_API_KEY', '')
    }

# ==================== HOME PAGE ====================
@app.route('/')
def index():
    """Home page - Tobias"""
    opportunities = Opportunity.query.filter_by(is_active=True).limit(6).all()
    stats = {
        'total_opportunities': Opportunity.query.filter_by(is_active=True).count(),
        'total_hours': db.session.query(db.func.sum(Booking.hours)).scalar() or 0,
        'total_volunteers': User.query.filter_by(role='volunteer').count(),
        'total_organizations': Organization.query.count()
    }
    return render_template('index.html', opportunities=opportunities, stats=stats)

# ==================== MAP/BROWSE PAGE ====================
@app.route('/opportunities')
@app.route('/map')
def opportunities_map():
    """Map page with opportunities - Sreehass"""
    opportunities = Opportunity.query.filter_by(is_active=True).all()
    # Convert to JSON for map markers
    opportunities_json = [{
        'id': opp.id,
        'title': opp.title,
        'organization': opp.organization.name if opp.organization else 'Unknown',
        'latitude': opp.latitude,
        'longitude': opp.longitude,
        'date': opp.date.strftime('%b %d, %Y') if opp.date else 'TBD',
        'time_slots': [slot.start_time for slot in sorted(opp.time_slots, key=lambda s: datetime.strptime(s.start_time, '%I:%M %p').time())] if opp.time_slots else [],
        'hours': opp.hours,
        'category': opp.category
    } for opp in opportunities if opp.latitude and opp.longitude]
    
    return render_template('map.html', opportunities=opportunities, opportunities_json=opportunities_json)

# ==================== OPPORTUNITY DETAIL PAGE ====================
@app.route('/opportunity/<int:id>')
def opportunity_detail(id):
    """Individual opportunity detail page"""
    opportunity = Opportunity.query.get_or_404(id)
    return render_template('opportunity_detail.html', opportunity=opportunity)

# ==================== BOOKING PAGE ====================
@app.route('/booking/<int:opportunity_id>')
@login_required
def booking_page(opportunity_id):
    """OpenTable-style booking page - Thomas"""
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    
    # Get all time slots for this opportunity with remaining spots
    time_slots = TimeSlot.query.filter_by(
        opportunity_id=opportunity_id,
        is_available=True
    ).order_by(TimeSlot.start_time).all()
    
    return render_template('booking.html', opportunity=opportunity, time_slots=time_slots)

@app.route('/book', methods=['POST'])
@login_required
def create_booking():
    """Create a new booking"""
    data = request.get_json()
    
    time_slot_id = data.get('time_slot_id')
    time_slot = TimeSlot.query.get_or_404(time_slot_id)
    opportunity = Opportunity.query.get_or_404(time_slot.opportunity_id)
    
    # Check if slot is still available
    if time_slot.is_full:
        return jsonify({'success': False, 'message': 'This time slot is now full'}), 400
    
    if not time_slot.is_available:
        return jsonify({'success': False, 'message': 'This time slot is not available'}), 400
    
    # Create booking
    booking = Booking(
        user_id=current_user.id,
        opportunity_id=opportunity.id,
        time_slot_id=time_slot.id,
        booking_time=datetime.combine(opportunity.date, datetime.strptime(time_slot.start_time, '%I:%M %p').time()),
        hours=opportunity.hours,
        status='confirmed'
    )
    
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'message': f'Booking confirmed for {time_slot.start_time}!', 
        'booking_id': booking.id
    })

@app.route('/booking/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    """Cancel a booking"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Verify the booking belongs to the current user
    if booking.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Update booking status to cancelled
    booking.status = 'cancelled'
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Booking cancelled successfully'})

# ==================== AUTHENTICATION ====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page - Eshaan"""
    if current_user.is_authenticated:
        # Redirect to appropriate dashboard based on role
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'organization':
            return redirect(url_for('organization_dashboard'))
        else:
            return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Redirect based on user role
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            elif user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'organization':
                return redirect(url_for('organization_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    # Check if Google OAuth is configured
    google_oauth_enabled = bool(app.config.get('GOOGLE_CLIENT_ID') and 
                                app.config['GOOGLE_CLIENT_ID'] != 'your-google-client-id-here')
    
    return render_template('login.html', google_oauth_enabled=google_oauth_enabled)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page - Eshaan"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return redirect(url_for('signup'))
        
        # Create new user
        user = User(
            email=email,
            username=username,
            full_name=full_name,
            password_hash=generate_password_hash(password),
            role='volunteer'
        )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Account created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    # Check if Google OAuth is configured
    google_oauth_enabled = bool(app.config.get('GOOGLE_CLIENT_ID') and 
                                app.config['GOOGLE_CLIENT_ID'] != 'your-google-client-id-here')
    
    return render_template('signup.html', google_oauth_enabled=google_oauth_enabled)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

# ==================== ADMIN PORTAL ====================
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email, role='admin').first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'danger')
    
    return render_template('admin_login.html')

# ==================== ORGANIZATION PORTAL ====================
@app.route('/organization/login', methods=['GET', 'POST'])
def organization_login():
    """Organization login page"""
    if current_user.is_authenticated and current_user.role == 'organization':
        return redirect(url_for('organization_dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email, role='organization').first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            return redirect(url_for('organization_dashboard'))
        else:
            flash('Invalid organization credentials', 'danger')
    
    return render_template('organization_login.html')

@app.route('/organization/signup', methods=['GET', 'POST'])
def organization_signup():
    """Organization signup page"""
    if current_user.is_authenticated:
        if current_user.role == 'organization':
            return redirect(url_for('organization_dashboard'))
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Get form data
        org_name = request.form.get('org_name')
        description = request.form.get('description')
        contact_email = request.form.get('contact_email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')
        website = request.form.get('website')
        
        # User account details
        username = request.form.get('username')
        full_name = request.form.get('full_name')
        password = request.form.get('password')
        
        # Check if email already exists
        if User.query.filter_by(email=contact_email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('organization_signup'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'error')
            return redirect(url_for('organization_signup'))
        
        # Create organization
        organization = Organization(
            name=org_name,
            description=description,
            contact_email=contact_email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            website=website,
            is_verified=False  # Needs admin approval
        )
        db.session.add(organization)
        db.session.flush()  # Get the organization ID
        
        # Create organization user account
        user = User(
            email=contact_email,
            username=username,
            full_name=full_name,
            password_hash=generate_password_hash(password),
            role='organization',
            organization_id=organization.id
        )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Organization registered successfully! Your account is pending verification by an administrator.', 'success')
        return redirect(url_for('organization_dashboard'))
    
    return render_template('organization_signup.html')

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard with statistics"""
    # Calculate statistics
    total_users = User.query.count()
    volunteers = User.query.filter_by(role='volunteer').count()
    organizations_count = User.query.filter_by(role='organization').count()
    
    total_opportunities = Opportunity.query.count()
    active_opportunities = Opportunity.query.filter_by(is_active=True).count()
    
    total_bookings = Booking.query.count()
    confirmed_bookings = Booking.query.filter_by(status='confirmed').count()
    
    total_hours = db.session.query(db.func.sum(Booking.hours)).filter_by(status='completed').scalar() or 0
    
    # Hours this month
    from datetime import date
    first_day_of_month = date.today().replace(day=1)
    hours_this_month = db.session.query(db.func.sum(Booking.hours)).filter(
        Booking.status == 'completed',
        Booking.completed_at >= first_day_of_month
    ).scalar() or 0
    
    stats = {
        'total_users': total_users,
        'volunteers': volunteers,
        'organizations': organizations_count,
        'total_opportunities': total_opportunities,
        'active_opportunities': active_opportunities,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'total_hours': total_hours,
        'hours_this_month': hours_this_month
    }
    
    # Recent activity
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()
    
    recent_activity = []
    for user in recent_users:
        recent_activity.append({
            'time': user.created_at.strftime('%Y-%m-%d %H:%M'),
            'description': f'New {user.role} registered: {user.full_name or user.username}'
        })
    
    for booking in recent_bookings:
        recent_activity.append({
            'time': booking.created_at.strftime('%Y-%m-%d %H:%M'),
            'description': f'New booking: {booking.user.username} → {booking.opportunity.title}'
        })
    
    recent_activity = sorted(recent_activity, key=lambda x: x['time'], reverse=True)[:10]
    
    return render_template('admin_dashboard.html', stats=stats, recent_activity=recent_activity)

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    """Admin users management page"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/organizations', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_organizations():
    """Admin organizations management page"""
    if request.method == 'POST':
        action = request.form.get('action')
        organization_id = request.form.get('organization_id')
        
        if action and organization_id:
            org = Organization.query.get(organization_id)
            if org:
                if action == 'verify':
                    org.is_verified = True
                    flash(f'{org.name} has been verified', 'success')
                elif action == 'unverify':
                    org.is_verified = False
                    flash(f'{org.name} verification has been removed', 'warning')
                db.session.commit()
        return redirect(url_for('admin_organizations'))
    
    organizations = Organization.query.order_by(Organization.created_at.desc()).all()
    total_opportunities = Opportunity.query.count()
    return render_template('admin_organizations.html', 
                         organizations=organizations,
                         total_opportunities=total_opportunities)

@app.route('/admin/opportunities', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_opportunities():
    """Admin opportunities management page"""
    if request.method == 'POST':
        action = request.form.get('action')
        opportunity_id = request.form.get('opportunity_id')
        
        if action and opportunity_id:
            opp = Opportunity.query.get(opportunity_id)
            if opp:
                if action == 'activate':
                    opp.is_active = True
                    flash(f'{opp.title} has been activated', 'success')
                elif action == 'deactivate':
                    opp.is_active = False
                    flash(f'{opp.title} has been deactivated', 'warning')
                elif action == 'delete':
                    # Delete associated bookings first
                    Booking.query.filter_by(opportunity_id=opp.id).delete()
                    db.session.delete(opp)
                    flash(f'{opp.title} has been deleted', 'info')
                db.session.commit()
        return redirect(url_for('admin_opportunities'))
    
    opportunities = Opportunity.query.order_by(Opportunity.created_at.desc()).all()
    total_bookings = Booking.query.count()
    total_hours = db.session.query(db.func.sum(Opportunity.hours)).scalar() or 0
    return render_template('admin_opportunities.html', 
                         opportunities=opportunities,
                         total_bookings=total_bookings,
                         total_hours=total_hours)

@app.route('/admin/bookings', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_bookings():
    """Admin bookings management page"""
    if request.method == 'POST':
        action = request.form.get('action')
        booking_id = request.form.get('booking_id')
        
        if action and booking_id:
            booking = Booking.query.get(booking_id)
            if booking:
                if action == 'cancel':
                    booking.status = 'cancelled'
                    flash(f'Booking #{booking.id} has been cancelled', 'info')
                db.session.commit()
        return redirect(url_for('admin_bookings'))
    
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    unique_volunteers = db.session.query(Booking.user_id).distinct().count()
    total_hours = db.session.query(db.func.sum(Opportunity.hours)).join(Booking).scalar() or 0
    return render_template('admin_bookings.html', 
                         bookings=bookings,
                         unique_volunteers=unique_volunteers,
                         total_hours=total_hours)

@app.route('/organization/dashboard')
@login_required
@organization_required
def organization_dashboard():
    """Organization dashboard"""
    # Get organization
    organization = Organization.query.get(current_user.organization_id) if current_user.organization_id else None
    
    if not organization:
        flash('No organization linked to your account', 'warning')
        return redirect(url_for('index'))
    
    # Calculate stats
    total_opportunities = Opportunity.query.filter_by(organization_id=organization.id).count()
    active_opportunities = Opportunity.query.filter_by(organization_id=organization.id, is_active=True).count()
    
    # Get all bookings for this organization's opportunities
    org_opportunity_ids = [opp.id for opp in organization.opportunities]
    total_bookings = Booking.query.filter(Booking.opportunity_id.in_(org_opportunity_ids)).count()
    
    total_hours = db.session.query(db.func.sum(Booking.hours)).filter(
        Booking.opportunity_id.in_(org_opportunity_ids),
        Booking.status == 'completed'
    ).scalar() or 0
    
    # Upcoming events
    from datetime import date
    upcoming_events = Opportunity.query.filter(
        Opportunity.organization_id == organization.id,
        Opportunity.date >= date.today(),
        Opportunity.is_active == True
    ).count()
    
    # Volunteers this week
    import datetime as dt
    week_ago = dt.datetime.now() - dt.timedelta(days=7)
    volunteers_this_week = Booking.query.filter(
        Booking.opportunity_id.in_(org_opportunity_ids),
        Booking.created_at >= week_ago
    ).count()
    
    pending_bookings = Booking.query.filter(
        Booking.opportunity_id.in_(org_opportunity_ids),
        Booking.status == 'confirmed'
    ).count()
    
    stats = {
        'total_opportunities': total_opportunities,
        'active_opportunities': active_opportunities,
        'total_bookings': total_bookings,
        'total_hours': total_hours,
        'upcoming_events': upcoming_events,
        'volunteers_this_week': volunteers_this_week,
        'pending_bookings': pending_bookings
    }
    
    # Recent opportunities
    recent_opportunities = Opportunity.query.filter_by(
        organization_id=organization.id
    ).order_by(Opportunity.created_at.desc()).limit(5).all()
    
    return render_template('organization_dashboard.html', 
                         organization=organization, 
                         stats=stats, 
                         recent_opportunities=recent_opportunities)

@app.route('/organization/opportunities')
@login_required
@organization_required
def organization_opportunities():
    """List all opportunities for organization"""
    organization = Organization.query.get(current_user.organization_id)
    opportunities = Opportunity.query.filter_by(organization_id=organization.id).order_by(Opportunity.created_at.desc()).all()
    
    # Calculate stats
    total_bookings = sum(len(opp.bookings) for opp in opportunities)
    unique_volunteers = len(set(booking.user_id for opp in opportunities for booking in opp.bookings))
    
    return render_template('organization_opportunities.html', 
                         opportunities=opportunities, 
                         organization=organization,
                         total_bookings=total_bookings,
                         total_volunteers=unique_volunteers)

@app.route('/organization/opportunities/create', methods=['GET', 'POST'])
@login_required
@organization_required
def organization_create_opportunity():
    """Create new opportunity"""
    if request.method == 'POST':
        from datetime import datetime
        
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        hours = int(request.form.get('hours'))
        date_str = request.form.get('date')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')
        requirements = request.form.get('requirements', '')
        what_to_bring = request.form.get('what_to_bring', '')
        image_url = request.form.get('image_url', 'https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800&q=80')
        
        # Get time slots
        time_slots_list = request.form.getlist('time_slots[]')
        spots_per_slot_list = request.form.getlist('spots_per_slot[]')
        
        # Convert times to readable format (HH:MM to H:MM AM/PM)
        formatted_slots = []
        for time_str in time_slots_list:
            hour, minute = map(int, time_str.split(':'))
            period = 'AM' if hour < 12 else 'PM'
            display_hour = hour if hour <= 12 else hour - 12
            if display_hour == 0:
                display_hour = 12
            formatted_slots.append(f"{display_hour}:{minute:02d} {period}")
        
        time_slots = ','.join(formatted_slots)
        spots_per_slot = int(spots_per_slot_list[0]) if spots_per_slot_list else 10
        
        # Parse date
        event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Create opportunity
        opportunity = Opportunity(
            title=title,
            description=description,
            organization_id=current_user.organization_id,
            category=category,
            date=event_date,
            hours=hours,
            latitude=42.3601,  # Default Boston coordinates
            longitude=-71.0589,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            requirements=requirements,
            what_to_bring=what_to_bring,
            time_slots=time_slots,
            spots_per_slot=spots_per_slot,
            image_url=image_url,
            is_active=True
        )
        
        db.session.add(opportunity)
        db.session.commit()
        
        flash(f'Opportunity "{title}" created successfully!', 'success')
        return redirect(url_for('organization_opportunities'))
    
    # GET request
    from datetime import date
    return render_template('organization_create_opportunity.html', today=date.today().isoformat())

@app.route('/organization/opportunities/<int:opportunity_id>/edit', methods=['GET', 'POST'])
@login_required
@organization_required
def organization_edit_opportunity(opportunity_id):
    """Edit opportunity"""
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    # Verify ownership
    if opportunity.organization_id != current_user.organization_id:
        abort(403)
    
    if request.method == 'POST':
        # Update opportunity fields
        opportunity.title = request.form.get('title')
        opportunity.description = request.form.get('description')
        opportunity.category = request.form.get('category')
        opportunity.requirements = request.form.get('requirements', '')
        opportunity.what_to_bring = request.form.get('what_to_bring', '')
        
        db.session.commit()
        flash('Opportunity updated successfully!', 'success')
        return redirect(url_for('organization_opportunities'))
    
    return render_template('organization_edit_opportunity.html', opportunity=opportunity)

@app.route('/organization/opportunities/<int:opportunity_id>/bookings')
@login_required
@organization_required
def organization_opportunity_bookings(opportunity_id):
    """View bookings for an opportunity"""
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    if opportunity.organization_id != current_user.organization_id:
        abort(403)
    bookings = Booking.query.filter_by(opportunity_id=opportunity_id).order_by(Booking.created_at.desc()).all()
    return render_template('organization_opportunity_bookings.html', opportunity=opportunity, bookings=bookings)

@app.route('/organization/volunteers')
@login_required
@organization_required
def organization_volunteers():
    """View all volunteers who booked opportunities"""
    organization = Organization.query.get(current_user.organization_id)
    org_opportunity_ids = [opp.id for opp in organization.opportunities]
    
    # Get all unique volunteers who have booked
    bookings = Booking.query.filter(Booking.opportunity_id.in_(org_opportunity_ids)).all()
    volunteer_ids = set(booking.user_id for booking in bookings)
    volunteers = User.query.filter(User.id.in_(volunteer_ids)).all()
    
    # Calculate totals
    total_bookings = len(bookings)
    total_hours = sum(booking.opportunity.hours for booking in bookings)
    
    return render_template('organization_volunteers.html', 
                         volunteers=volunteers,
                         opportunities=organization.opportunities,
                         organization=organization,
                         total_bookings=total_bookings,
                         total_hours=total_hours)

@app.route('/organization/profile', methods=['GET', 'POST'])
@login_required
@organization_required
def organization_profile():
    """Organization profile page"""
    organization = Organization.query.get(current_user.organization_id)
    
    if request.method == 'POST':
        # Update organization details
        organization.name = request.form.get('name')
        organization.description = request.form.get('description')
        organization.contact_email = request.form.get('contact_email')
        organization.phone = request.form.get('phone', '')
        organization.website = request.form.get('website', '')
        organization.address = request.form.get('address', '')
        organization.city = request.form.get('city', '')
        organization.state = request.form.get('state', '')
        organization.zip_code = request.form.get('zip_code', '')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('organization_profile'))
    
    return render_template('organization_profile.html', organization=organization)

# ==================== GOOGLE OAUTH ====================
@app.route('/login/google')
def google_login():
    """Initiate Google OAuth login"""
    # Check if Google OAuth is configured
    if not app.config.get('GOOGLE_CLIENT_ID') or app.config['GOOGLE_CLIENT_ID'] == 'your-google-client-id-here':
        flash('Google Sign-In is not configured yet. Please contact the administrator or use email/password login.', 'warning')
        return redirect(url_for('login'))
    
    # Use localhost instead of 127.0.0.1 for better OAuth compatibility
    redirect_uri = url_for('google_authorize', _external=True, _scheme='http')
    # Force localhost in the redirect URI
    redirect_uri = redirect_uri.replace('127.0.0.1', 'localhost')
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize/google')
def google_authorize():
    """Handle Google OAuth callback"""
    try:
        token = google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if user_info:
            email = user_info.get('email')
            name = user_info.get('name')
            google_id = user_info.get('sub')
            
            # Check if user exists
            user = User.query.filter_by(email=email).first()
            
            if not user:
                # Create new user with Google account
                username = email.split('@')[0]
                # Make username unique if it already exists
                base_username = username
                counter = 1
                while User.query.filter_by(username=username).first():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User(
                    email=email,
                    username=username,
                    full_name=name,
                    password_hash=generate_password_hash(os.urandom(24).hex()),  # Random password
                    role='volunteer'
                )
                db.session.add(user)
                db.session.commit()
                flash('Account created successfully with Google!', 'success')
            else:
                flash('Welcome back!', 'success')
            
            # Log the user in
            login_user(user)
            
            # Redirect based on user role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'organization':
                return redirect(url_for('organization_dashboard'))
            else:  # volunteer
                return redirect(url_for('dashboard'))
        else:
            flash('Failed to get user info from Google', 'error')
            return redirect(url_for('login'))
            
    except Exception as e:
        flash(f'Authentication failed: {str(e)}', 'error')
        return redirect(url_for('login'))

# ==================== DASHBOARD ====================
@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - Eshaan"""
    upcoming_bookings_raw = Booking.query.filter_by(
        user_id=current_user.id,
        status='confirmed'
    ).join(Opportunity).filter(
        Opportunity.date >= datetime.now().date()
    ).all()
    
    past_bookings_raw = Booking.query.filter_by(
        user_id=current_user.id
    ).join(Opportunity).filter(
        Opportunity.date < datetime.now().date()
    ).all()
    
    # Group bookings by opportunity
    def group_bookings(bookings):
        grouped = {}
        for booking in bookings:
            opp_id = booking.opportunity.id
            if opp_id not in grouped:
                grouped[opp_id] = {
                    'opportunity': booking.opportunity,
                    'bookings': [],
                    'time_slots': [],
                    'booking_ids': [],
                    'total_hours': 0
                }
            grouped[opp_id]['bookings'].append(booking)
            grouped[opp_id]['booking_ids'].append(booking.id)
            grouped[opp_id]['time_slots'].append(booking.time_slot)
            grouped[opp_id]['total_hours'] += booking.hours
        
        # Sort time slots chronologically for each opportunity
        for group in grouped.values():
            group['time_slots'].sort(key=lambda ts: datetime.strptime(ts.start_time, '%I:%M %p').time())
        
        return list(grouped.values())
    
    upcoming_bookings = group_bookings(upcoming_bookings_raw)
    past_bookings = group_bookings(past_bookings_raw)
    
    total_hours = db.session.query(
        db.func.sum(Booking.hours)
    ).filter_by(
        user_id=current_user.id,
        status='completed'
    ).scalar() or 0
    
    return render_template('dashboard.html', 
                         upcoming_bookings=upcoming_bookings,
                         past_bookings=past_bookings,
                         total_hours=total_hours)

@app.route('/dashboard/bookings')
@login_required
def my_bookings():
    """View all bookings"""
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/dashboard/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('profile.html')

@app.route('/dashboard/history')
@login_required
def volunteer_history():
    """Volunteer history"""
    completed_bookings = Booking.query.filter_by(
        user_id=current_user.id,
        status='completed'
    ).all()
    return render_template('history.html', bookings=completed_bookings)

# ==================== SEARCH & FILTER ====================
@app.route('/search')
def search():
    """Search opportunities"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    date = request.args.get('date', '')
    
    opportunities = Opportunity.query.filter_by(is_active=True)
    
    if query:
        opportunities = opportunities.filter(
            db.or_(
                Opportunity.title.ilike(f'%{query}%'),
                Opportunity.description.ilike(f'%{query}%')
            )
        )
    
    if category:
        opportunities = opportunities.filter_by(category=category)
    
    if date:
        opportunities = opportunities.filter_by(date=datetime.strptime(date, '%Y-%m-%d').date())
    
    opportunities = opportunities.all()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify([{
            'id': opp.id,
            'title': opp.title,
            'organization': opp.organization.name if opp.organization else 'Unknown',
            'date': opp.date.strftime('%b %d, %Y') if opp.date else 'TBD',
            'time': opp.time,
            'hours': opp.hours,
            'spots_available': opp.spots_available
        } for opp in opportunities])
    
    return render_template('search_results.html', opportunities=opportunities, query=query)

# ==================== API ENDPOINTS ====================
@app.route('/api/opportunities')
def api_opportunities():
    """API endpoint for opportunities (for map)"""
    opportunities = Opportunity.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': opp.id,
        'title': opp.title,
        'organization': opp.organization.name if opp.organization else 'Unknown',
        'latitude': opp.latitude,
        'longitude': opp.longitude,
        'date': opp.date.isoformat() if opp.date else None,
        'time': opp.time,
        'hours': opp.hours,
        'category': opp.category,
        'spots_available': opp.spots_available
    } for opp in opportunities if opp.latitude and opp.longitude])

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# ==================== DATABASE INITIALIZATION ====================
@app.cli.command()
def init_db():
    """Initialize the database with sample data"""
    db.create_all()
    
    # Clear existing data
    Booking.query.delete()
    TimeSlot.query.delete()
    Opportunity.query.delete()
    Organization.query.delete()
    User.query.delete()
    db.session.commit()
    
    # Create sample organizations
    organizations = [
        Organization(
            name='Boston Green Space Alliance',
            description='Creating and maintaining green spaces throughout Boston',
            contact_email='info@bostongreenspace.org',
            phone='617-555-0100',
            address='100 Cambridge St, Boston, MA 02114'
        ),
        Organization(
            name='Massachusetts Food Bank',
            description='Fighting hunger across Massachusetts',
            contact_email='help@mafoodbank.org',
            phone='617-555-0200',
            address='70 South Bay Ave, Boston, MA 02118'
        ),
        Organization(
            name='Cambridge Public Library',
            description='Serving the Cambridge community through literacy',
            contact_email='volunteer@cambridgelibrary.org',
            phone='617-555-0300',
            address='449 Broadway, Cambridge, MA 02138'
        ),
        Organization(
            name='Worcester Youth Center',
            description='Empowering youth through education and mentorship',
            contact_email='info@worcesteryouth.org',
            phone='508-555-0400',
            address='11 Ionic Ave, Worcester, MA 01608'
        ),
        Organization(
            name='Cape Cod Animal Shelter',
            description='Providing care for animals in need',
            contact_email='adopt@capecodanimals.org',
            phone='508-555-0500',
            address='1577 Falmouth Rd, Centerville, MA 02632'
        ),
        Organization(
            name='Springfield Community Kitchen',
            description='Feeding families in Western Massachusetts',
            contact_email='meals@springfieldkitchen.org',
            phone='413-555-0600',
            address='1095 Main St, Springfield, MA 01103'
        ),
        Organization(
            name='Salem Historical Society',
            description='Preserving Salem\'s rich history',
            contact_email='volunteer@salemhistory.org',
            phone='978-555-0700',
            address='132 Essex St, Salem, MA 01970'
        ),
        Organization(
            name='Lowell Tech Mentorship',
            description='Teaching technology skills to underserved communities',
            contact_email='mentor@lowelltech.org',
            phone='978-555-0800',
            address='35 Kirk St, Lowell, MA 01852'
        ),
        Organization(
            name='New Bedford Harbor Initiative',
            description='Protecting and cleaning our waterways',
            contact_email='harbor@newbedford.org',
            phone='508-555-0900',
            address='175 William St, New Bedford, MA 02740'
        ),
        Organization(
            name='Quincy Healthcare Volunteers',
            description='Supporting patients and families',
            contact_email='care@quincyhealth.org',
            phone='617-555-1000',
            address='114 Whitwell St, Quincy, MA 02169'
        ),
    ]
    
    db.session.add_all(organizations)
    db.session.commit()
    
    # Create sample users for admin and organization portals
    from werkzeug.security import generate_password_hash
    
    admin_user = User(
        email='admin@volunteerhub.com',
        username='admin',
        full_name='System Administrator',
        password_hash=generate_password_hash('admin123'),
        role='admin'
    )
    db.session.add(admin_user)
    
    # Create organization users linked to their organizations
    org_user1 = User(
        email='manager@bostongreen.org',
        username='bostongreen',
        full_name='Sarah Johnson',
        password_hash=generate_password_hash('org123'),
        role='organization',
        organization_id=1
    )
    
    org_user2 = User(
        email='coordinator@mafoodbank.org',
        username='mafoodbank',
        full_name='Michael Chen',
        password_hash=generate_password_hash('org123'),
        role='organization',
        organization_id=2
    )
    
    org_user3 = User(
        email='director@cambridgelibrary.org',
        username='cambridgelib',
        full_name='Emily Rodriguez',
        password_hash=generate_password_hash('org123'),
        role='organization',
        organization_id=3
    )
    
    org_user4 = User(
        email='volunteer@worcestermedia.org',
        username='worcestermedia',
        full_name='David Kim',
        password_hash=generate_password_hash('org123'),
        role='organization',
        organization_id=4
    )
    
    org_user5 = User(
        email='outreach@framinghamarts.org',
        username='framinghamarts',
        full_name='Jessica Martinez',
        password_hash=generate_password_hash('org123'),
        role='organization',
        organization_id=5
    )
    
    db.session.add_all([org_user1, org_user2, org_user3, org_user4, org_user5])
    db.session.commit()
    
    # Create unique opportunities (NO DUPLICATES!)
    opportunities_data = [
        # Boston Area
        {
            'title': 'Charles River Cleanup',
            'description': 'Help us clean up the beautiful Charles River Esplanade. We provide all equipment including gloves, bags, and grabbers. Great for families and individuals looking to make a difference!',
            'organization_id': 1,
            'category': 'Environment',
            'date': datetime(2025, 11, 2).date(),
            'hours': 1,
            'latitude': 42.3601,
            'longitude': -71.0942,
            'address': 'Charles River Esplanade, Boston, MA 02116',
            'city': 'Boston',
            'state': 'MA',
            'zip_code': '02116',
            'requirements': 'Comfortable walking shoes, weather-appropriate clothing',
            'what_to_bring': 'Water bottle, sunscreen',
            'time_slots': ['9:00 AM', '10:00 AM', '11:00 AM', '1:00 PM', '2:00 PM'],
            'spots_per_slot': 15,
            'image_url': 'https://images.unsplash.com/photo-1618477461853-cf6ed80faba5?w=800&q=80'
        },
        {
            'title': 'Food Bank Sorting & Distribution',
            'description': 'Sort and package food donations for distribution to families in need. Physical work but very rewarding!',
            'organization_id': 2,
            'category': 'Food Security',
            'date': datetime(2025, 11, 3).date(),
            'hours': 1,
            'latitude': 42.3396,
            'longitude': -71.0663,
            'address': '70 South Bay Ave, Boston, MA 02118',
            'city': 'Boston',
            'state': 'MA',
            'zip_code': '02118',
            'requirements': 'Must be 16 or older',
            'what_to_bring': 'Closed-toe shoes required',
            'time_slots': ['9:00 AM', '10:00 AM', '11:00 AM', '1:00 PM', '2:00 PM', '3:00 PM'],
            'spots_per_slot': 10,
            'image_url': 'https://images.unsplash.com/photo-1593113598332-cd288d649433?w=800&q=80'
        },
        {
            'title': 'Community Garden Planting',
            'description': 'Help plant vegetables and flowers in our community garden. All supplies provided!',
            'organization_id': 1,
            'category': 'Environment',
            'date': datetime(2025, 11, 12).date(),
            'hours': 1,
            'latitude': 42.3555,
            'longitude': -71.0642,
            'address': 'South End Community Garden, Boston, MA 02118',
            'city': 'Boston',
            'state': 'MA',
            'zip_code': '02118',
            'requirements': 'None - all skill levels welcome!',
            'what_to_bring': 'Gardening gloves if you have them, water bottle',
            'time_slots': ['9:00 AM', '10:00 AM', '11:00 AM'],
            'spots_per_slot': 10,
            'image_url': 'https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=800&q=80'
        },
        
        # Cambridge
        {
            'title': 'Reading Buddies Program',
            'description': 'Read with elementary school children to help improve their literacy skills. Training provided!',
            'organization_id': 3,
            'category': 'Education',
            'date': datetime(2025, 11, 4).date(),
            'hours': 1,
            'latitude': 42.3736,
            'longitude': -71.1097,
            'address': '449 Broadway, Cambridge, MA 02138',
            'city': 'Cambridge',
            'state': 'MA',
            'zip_code': '02138',
            'requirements': 'Background check required, love of reading',
            'what_to_bring': 'Enthusiasm and patience',
            'time_slots': ['2:00 PM', '3:00 PM', '4:00 PM'],
            'spots_per_slot': 8,
            'image_url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800&q=80'
        },
        
        # Worcester
        {
            'title': 'Youth Homework Help',
            'description': 'Help middle school students with homework and test preparation. Great for college students!',
            'organization_id': 4,
            'category': 'Education',
            'date': datetime(2025, 11, 5).date(),
            'hours': 1,
            'latitude': 42.2626,
            'longitude': -71.8023,
            'address': '11 Ionic Ave, Worcester, MA 01608',
            'city': 'Worcester',
            'state': 'MA',
            'zip_code': '01608',
            'requirements': 'High school diploma or currently in college',
            'what_to_bring': 'Positive attitude',
            'time_slots': ['3:00 PM', '4:00 PM', '5:00 PM'],
            'spots_per_slot': 6,
            'image_url': 'https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=800&q=80'
        },
        
        # Cape Cod
        {
            'title': 'Animal Shelter Dog Walking',
            'description': 'Take our shelter dogs for walks and provide socialization. Perfect for animal lovers!',
            'organization_id': 5,
            'category': 'Animal Welfare',
            'date': datetime(2025, 11, 6).date(),
            'hours': 1,
            'latitude': 41.6688,
            'longitude': -70.3545,
            'address': '1577 Falmouth Rd, Centerville, MA 02632',
            'city': 'Centerville',
            'state': 'MA',
            'zip_code': '02632',
            'requirements': 'Must be comfortable with dogs',
            'what_to_bring': 'Comfortable shoes, weather-appropriate clothing',
            'time_slots': ['10:00 AM', '11:00 AM', '1:00 PM', '2:00 PM', '3:00 PM'],
            'spots_per_slot': 5,
            'image_url': 'https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=800&q=80'
        },
        
        # Springfield
        {
            'title': 'Community Kitchen Meal Service',
            'description': 'Prepare and serve meals to community members in need. Very rewarding experience!',
            'organization_id': 6,
            'category': 'Food Security',
            'date': datetime(2025, 11, 7).date(),
            'hours': 1,
            'latitude': 42.1015,
            'longitude': -72.5898,
            'address': '1095 Main St, Springfield, MA 01103',
            'city': 'Springfield',
            'state': 'MA',
            'zip_code': '01103',
            'requirements': 'Food handler certification preferred but not required',
            'what_to_bring': 'Hairnet provided, closed-toe shoes',
            'time_slots': ['11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM'],
            'spots_per_slot': 12,
            'image_url': 'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=800&q=80'
        },
        
        # Salem
        {
            'title': 'Historical Site Tour Guide',
            'description': 'Lead tours through Salem\'s historic downtown. Training and script provided!',
            'organization_id': 7,
            'category': 'Technology',
            'date': datetime(2025, 11, 8).date(),
            'hours': 1,
            'latitude': 42.5195,
            'longitude': -70.8967,
            'address': '132 Essex St, Salem, MA 01970',
            'city': 'Salem',
            'state': 'MA',
            'zip_code': '01970',
            'requirements': 'Good public speaking skills, interest in history',
            'what_to_bring': 'Comfortable shoes for walking',
            'time_slots': ['10:00 AM', '11:00 AM', '2:00 PM', '3:00 PM'],
            'spots_per_slot': 4,
            'image_url': 'https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800&q=80'
        },
        
        # Lowell
        {
            'title': 'Computer Skills Workshop Assistant',
            'description': 'Help teach basic computer skills to seniors and job seekers. Tech knowledge required!',
            'organization_id': 8,
            'category': 'Technology',
            'date': datetime(2025, 11, 9).date(),
            'hours': 1,
            'latitude': 42.6334,
            'longitude': -71.3162,
            'address': '35 Kirk St, Lowell, MA 01852',
            'city': 'Lowell',
            'state': 'MA',
            'zip_code': '01852',
            'requirements': 'Proficiency in Microsoft Office and basic troubleshooting',
            'what_to_bring': 'Patience and enthusiasm',
            'time_slots': ['2:00 PM', '3:00 PM', '4:00 PM'],
            'spots_per_slot': 6,
            'image_url': 'https://images.unsplash.com/photo-1531482615713-2afd69097998?w=800&q=80'
        },
        
        # New Bedford
        {
            'title': 'Harbor Cleanup Boat Crew',
            'description': 'Join our team on the water removing debris from New Bedford Harbor. Boating experience helpful!',
            'organization_id': 9,
            'category': 'Environment',
            'date': datetime(2025, 11, 10).date(),
            'hours': 1,
            'latitude': 41.6362,
            'longitude': -70.9342,
            'address': '175 William St, New Bedford, MA 02740',
            'city': 'New Bedford',
            'state': 'MA',
            'zip_code': '02740',
            'requirements': 'Must be able to swim, life jackets provided',
            'what_to_bring': 'Sunscreen, water bottle, change of clothes',
            'time_slots': ['9:00 AM', '10:00 AM', '11:00 AM', '1:00 PM'],
            'spots_per_slot': 8,
            'image_url': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=80'
        },
        
        # Quincy
        {
            'title': 'Hospital Patient Companion',
            'description': 'Provide companionship and comfort to patients. Bring smiles and conversation!',
            'organization_id': 10,
            'category': 'Healthcare',
            'date': datetime(2025, 11, 11).date(),
            'hours': 1,
            'latitude': 42.2529,
            'longitude': -71.0023,
            'address': '114 Whitwell St, Quincy, MA 02169',
            'city': 'Quincy',
            'state': 'MA',
            'zip_code': '02169',
            'requirements': 'Background check required, compassionate nature',
            'what_to_bring': 'Friendly smile',
            'time_slots': ['10:00 AM', '11:00 AM', '2:00 PM', '3:00 PM'],
            'spots_per_slot': 5,
            'image_url': 'https://images.unsplash.com/photo-1576765608535-5f04d1e3f289?w=800&q=80'
        },
        
        # Framingham
        {
            'title': 'Weekend Food Pantry',
            'description': 'Stock shelves and help distribute groceries to families. Fast-paced and fulfilling!',
            'organization_id': 2,
            'category': 'Food Security',
            'date': datetime(2025, 11, 13).date(),
            'hours': 1,
            'latitude': 42.2808,
            'longitude': -71.4166,
            'address': 'Framingham Food Pantry, Framingham, MA 01702',
            'city': 'Framingham',
            'state': 'MA',
            'zip_code': '01702',
            'requirements': 'Must be 14 or older',
            'what_to_bring': 'Comfortable shoes',
            'time_slots': ['9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM'],
            'spots_per_slot': 8,
            'image_url': 'https://images.unsplash.com/photo-1593113646773-028c64a8f1b8?w=800&q=80'
        },
    ]
    
    # Create opportunities and their time slots
    for opp_data in opportunities_data:
        # Extract time slot data
        time_slots = opp_data.pop('time_slots')
        spots_per_slot = opp_data.pop('spots_per_slot')
        
        # Create opportunity
        opp = Opportunity(**opp_data, is_active=True)
        db.session.add(opp)
        db.session.flush()  # Get the opportunity ID
        
        # Create time slots for this opportunity
        for time in time_slots:
            slot = TimeSlot(
                opportunity_id=opp.id,
                start_time=time,
                spots_available=spots_per_slot,
                is_available=True
            )
            db.session.add(slot)
    
    db.session.commit()
    
    total_opps = len(opportunities_data)
    total_slots = sum(len(opp['time_slots']) for opp in [
        {'time_slots': ['9:00 AM', '10:00 AM', '11:00 AM', '1:00 PM', '2:00 PM']},
        {'time_slots': ['9:00 AM', '10:00 AM', '11:00 AM', '1:00 PM', '2:00 PM', '3:00 PM']},
        {'time_slots': ['9:00 AM', '10:00 AM', '11:00 AM']},
        {'time_slots': ['2:00 PM', '3:00 PM', '4:00 PM']},
        {'time_slots': ['3:00 PM', '4:00 PM', '5:00 PM']},
        {'time_slots': ['10:00 AM', '11:00 AM', '1:00 PM', '2:00 PM', '3:00 PM']},
        {'time_slots': ['11:00 AM', '12:00 PM', '1:00 PM', '2:00 PM']},
        {'time_slots': ['10:00 AM', '11:00 AM', '2:00 PM', '3:00 PM']},
        {'time_slots': ['2:00 PM', '3:00 PM', '4:00 PM']},
        {'time_slots': ['9:00 AM', '10:00 AM', '11:00 AM', '1:00 PM']},
        {'time_slots': ['10:00 AM', '11:00 AM', '2:00 PM', '3:00 PM']},
        {'time_slots': ['9:00 AM', '10:00 AM', '11:00 AM', '12:00 PM']},
    ])
    
    print(f'✅ Database initialized successfully!')
    print(f'📊 {len(organizations)} organizations')
    print(f'🎯 {total_opps} unique volunteer opportunities')
    print(f'🕐 {total_slots} total time slots (OpenTable style!)')
    print(f'📍 Locations: Boston, Cambridge, Worcester, Cape Cod, Springfield, Salem, Lowell, New Bedford, Quincy, Framingham')
    print(f'\n💡 Each opportunity now has multiple hourly time slots - just like OpenTable!')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=3000)
