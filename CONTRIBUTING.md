# 🤝 Contributing to VolunteerHub

Thank you for contributing to VolunteerHub! This document provides guidelines for team members and external contributors.

## 👥 Team Structure

### Current Team Members
- **Tobias** - Home Page Development
- **Sreehass** - Interactive Map & Browse Features
- **Thomas** - Booking System
- **Eshaan** - Authentication & Dashboard

## 🚀 Getting Started

### 1. Set Up Your Development Environment

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/volunteer-hub.git
cd volunteer-hub

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
flask init-db

# Run the application
python app.py
```

### 2. Create a Branch

Always create a new branch for your work:

```bash
# For new features
git checkout -b feature/your-feature-name

# For bug fixes
git checkout -b fix/bug-description

# For documentation
git checkout -b docs/what-you-are-documenting
```

### 3. Make Your Changes

- Write clean, readable code
- Add comments for complex logic
- Follow the existing code style
- Test your changes thoroughly

### 4. Commit Your Changes

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "Add: Brief description of what you added"
```

**Commit Message Prefixes:**
- `Add:` - New features
- `Fix:` - Bug fixes
- `Update:` - Changes to existing features
- `Refactor:` - Code improvements without changing functionality
- `Docs:` - Documentation changes
- `Style:` - Formatting, missing semicolons, etc.
- `Test:` - Adding tests

**Good Examples:**
```
Add: User profile picture upload feature
Fix: Booking form validation error
Update: Improved map marker clustering
Docs: Add API documentation for booking endpoint
```

**Bad Examples:**
```
updated stuff
fixed things
changes
```

### 5. Push and Create Pull Request

```bash
git push origin your-branch-name
```

Then go to GitHub and create a Pull Request.

## 📝 Code Style Guidelines

### Python (Backend)

```python
# Use meaningful variable names
user_bookings = Booking.query.filter_by(user_id=current_user.id).all()

# Add docstrings to functions
def get_user_stats(user_id):
    """
    Calculate statistics for a given user.
    
    Args:
        user_id (int): The user's ID
        
    Returns:
        dict: Statistics including total_hours, bookings_count, etc.
    """
    pass

# Use type hints when possible
def create_booking(user_id: int, opportunity_id: int) -> Booking:
    pass

# Keep functions small and focused
# Each function should do one thing well
```

### HTML/CSS (Frontend)

```html
<!-- Use semantic HTML -->
<section class="opportunities">
    <h2>Featured Opportunities</h2>
    <div class="opportunity-grid">
        <!-- content -->
    </div>
</section>

<!-- Add comments for complex sections -->
<!-- Search Filter Section -->
<div class="search-filters">
    <!-- filters -->
</div>
```

```css
/* Use consistent naming conventions */
.opportunity-card { }
.opportunity-card__title { }
.opportunity-card__action { }

/* Add comments for sections */
/* ==================== NAVIGATION ==================== */
nav { }

/* Group related styles */
.btn {
    /* Base button styles */
}

.btn-primary {
    /* Primary button variant */
}
```

### JavaScript

```javascript
// Use const/let, avoid var
const opportunityId = 123;
let selectedDate = null;

// Use meaningful function names
function filterOpportunitiesByCategory(category) {
    // implementation
}

// Add JSDoc comments for complex functions
/**
 * Fetches opportunity data from the API
 * @param {number} opportunityId - The ID of the opportunity
 * @returns {Promise<Object>} The opportunity data
 */
async function fetchOpportunity(opportunityId) {
    // implementation
}
```

## 🌿 Branch Strategy

### Main Branches
- `main` - Production-ready code
- `develop` - Integration branch for features

### Supporting Branches
- `feature/*` - New features
- `fix/*` - Bug fixes
- `hotfix/*` - Critical production fixes

### Workflow

1. Create feature branch from `develop`
2. Make changes and commit
3. Push branch and create PR to `develop`
4. Get code review from team member
5. Merge to `develop`
6. When ready, merge `develop` to `main` for release

## 🔍 Code Review Process

### For Reviewers

- Be constructive and kind
- Check for bugs and edge cases
- Verify code follows style guidelines
- Test the changes locally
- Approve or request changes

### Checklist for PRs

- [ ] Code runs without errors
- [ ] New features have been tested
- [ ] Code follows project style guide
- [ ] Comments added for complex logic
- [ ] No sensitive data (API keys, passwords) in code
- [ ] Database migrations included if needed
- [ ] Documentation updated if needed

## 🐛 Reporting Bugs

### Before Submitting

1. Check if bug already reported
2. Try to reproduce the bug
3. Gather information about your environment

### Bug Report Template

```markdown
**Description:**
Clear description of the bug

**Steps to Reproduce:**
1. Go to...
2. Click on...
3. See error

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Screenshots:**
If applicable

**Environment:**
- OS: [e.g., Windows 10]
- Browser: [e.g., Chrome 120]
- Python Version: [e.g., 3.11]
```

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Feature Description:**
Clear description of the feature

**Problem it Solves:**
What problem does this solve?

**Proposed Solution:**
How should it work?

**Alternative Solutions:**
Any alternative approaches?

**Additional Context:**
Mockups, examples, etc.
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_booking.py

# Run with coverage
python -m pytest --cov=app
```

### Writing Tests

```python
def test_create_booking():
    """Test booking creation"""
    # Arrange
    user = User(email='test@test.com')
    opportunity = Opportunity(title='Test Event')
    
    # Act
    booking = create_booking(user.id, opportunity.id)
    
    # Assert
    assert booking is not None
    assert booking.status == 'confirmed'
```

## 📚 Documentation

### When to Update Docs

- Adding new features
- Changing existing functionality
- Adding new API endpoints
- Changing configuration options

### Documentation Locations

- `README.md` - Project overview and setup
- `DEPLOYMENT.md` - Deployment instructions
- `CONTRIBUTING.md` - This file
- Code comments - For implementation details
- Docstrings - For function/class documentation

## 🔐 Security

### Important Rules

- **Never commit:**
  - API keys
  - Passwords
  - Database credentials
  - Secret keys

- **Always:**
  - Use environment variables for secrets
  - Keep `.env` in `.gitignore`
  - Hash passwords before storing
  - Validate user input
  - Use HTTPS in production

### Reporting Security Issues

**Do not** open public issues for security vulnerabilities.
Email: security@volunteerhub.org

## 🎨 Design Guidelines

### Colors
- Primary: `#0f4c5c` (Deep teal)
- Secondary: `#5fb3c5` (Light teal)
- Text: `#2c3e50` (Dark gray)
- Background: `#f8f9fa` (Light gray)

### Typography
- Headings: Segoe UI, sans-serif
- Body: Segoe UI, sans-serif
- Font sizes maintain hierarchy

### Spacing
- Use consistent padding/margin
- 8px base unit (8, 16, 24, 32, 40, etc.)

## 🏆 Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Credited in documentation

## 📞 Communication

### Team Channels
- **GitHub Issues** - Bug reports and feature requests
- **Pull Requests** - Code reviews and discussions
- **Email** - team@volunteerhub.org

### Response Times
We aim to respond to:
- Security issues: Within 24 hours
- Bug reports: Within 2-3 days
- Feature requests: Within 1 week
- Pull requests: Within 3-5 days

## 🎯 Priorities

### High Priority
- Security fixes
- Critical bugs
- Performance issues

### Medium Priority
- New features
- Improvements to existing features
- Documentation

### Low Priority
- Nice-to-have features
- Minor UI tweaks
- Code refactoring

## 📖 Learning Resources

### For Team Members New to:

**Flask:**
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

**Git:**
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [Learn Git Branching](https://learngitbranching.js.org/)

**HTML/CSS/JavaScript:**
- [MDN Web Docs](https://developer.mozilla.org/)
- [CSS-Tricks](https://css-tricks.com/)

**SQLAlchemy:**
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/en/14/tutorial/)

## ✅ Checklist for New Contributors

- [ ] Read this document
- [ ] Set up development environment
- [ ] Run the application locally
- [ ] Explore the codebase
- [ ] Pick an issue to work on
- [ ] Create a branch
- [ ] Make changes
- [ ] Test thoroughly
- [ ] Commit with clear message
- [ ] Push and create PR
- [ ] Respond to code review feedback

## 🙏 Thank You!

Thank you for contributing to VolunteerHub! Every contribution, no matter how small, helps make our platform better and helps more people connect with volunteering opportunities.

**Together, we're making a difference! 🤝**

---

Questions? Contact us at team@volunteerhub.org
