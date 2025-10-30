// Main JavaScript file for VolunteerHub

// ==================== CUSTOM MODAL SYSTEM ====================
let modalResolve = null;

function showModal(options) {
    return new Promise((resolve) => {
        modalResolve = resolve;
        
        const modal = document.getElementById('customModal');
        const icon = document.getElementById('modalIcon');
        const title = document.getElementById('modalTitle');
        const body = document.getElementById('modalBody');
        const footer = document.getElementById('modalFooter');
        
        // Set modal type and icon
        const types = {
            success: { icon: '✅', title: 'Success' },
            error: { icon: '❌', title: 'Error' },
            warning: { icon: '⚠️', title: 'Warning' },
            info: { icon: 'ℹ️', title: 'Information' },
            confirm: { icon: '❓', title: 'Confirm' }
        };
        
        const type = types[options.type] || types.info;
        icon.textContent = options.icon || type.icon;
        title.textContent = options.title || type.title;
        body.innerHTML = options.message || 'No message provided';
        
        // Clear footer and add buttons based on type
        footer.innerHTML = '';
        
        if (options.type === 'confirm') {
            // Confirmation dialog with Yes/No buttons
            const cancelBtn = document.createElement('button');
            cancelBtn.className = 'modal-btn modal-btn-secondary';
            cancelBtn.textContent = options.cancelText || 'Cancel';
            cancelBtn.onclick = () => {
                closeModal();
                modalResolve(false);
            };
            
            const confirmBtn = document.createElement('button');
            confirmBtn.className = `modal-btn ${options.danger ? 'modal-btn-danger' : 'modal-btn-primary'}`;
            confirmBtn.textContent = options.confirmText || 'Confirm';
            confirmBtn.onclick = () => {
                closeModal();
                modalResolve(true);
            };
            
            footer.appendChild(cancelBtn);
            footer.appendChild(confirmBtn);
        } else {
            // Simple OK button
            const okBtn = document.createElement('button');
            okBtn.className = 'modal-btn modal-btn-primary';
            okBtn.textContent = 'OK';
            okBtn.onclick = () => {
                closeModal();
                modalResolve(true);
            };
            footer.appendChild(okBtn);
        }
        
        // Show modal
        modal.classList.add('active');
        
        // Close on overlay click
        modal.onclick = (e) => {
            if (e.target === modal) {
                closeModal();
                modalResolve(false);
            }
        };
        
        // Close on Escape key
        const escapeHandler = (e) => {
            if (e.key === 'Escape') {
                closeModal();
                modalResolve(false);
                document.removeEventListener('keydown', escapeHandler);
            }
        };
        document.addEventListener('keydown', escapeHandler);
    });
}

function closeModal() {
    const modal = document.getElementById('customModal');
    modal.classList.remove('active');
}

// Override default alert, confirm with custom modals
window.customAlert = function(message, title = 'Notification', type = 'info') {
    return showModal({ message, title, type });
};

window.customConfirm = function(message, options = {}) {
    return showModal({ 
        message, 
        type: 'confirm',
        title: options.title || 'Confirm',
        confirmText: options.confirmText || 'Confirm',
        cancelText: options.cancelText || 'Cancel',
        danger: options.danger || false
    });
};

window.customSuccess = function(message, title = 'Success') {
    return showModal({ message, title, type: 'success' });
};

window.customError = function(message, title = 'Error') {
    return showModal({ message, title, type: 'error' });
};

// ==================== SCROLL ANIMATIONS ====================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Observe elements on page load
document.addEventListener('DOMContentLoaded', function() {
    // Animate all elements with fade-in classes
    const fadeElements = document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right, .scale-in, .slide-up');
    fadeElements.forEach(el => observer.observe(el));
    
    // Auto-animate opportunity cards
    const oppCards = document.querySelectorAll('.opp-card');
    oppCards.forEach((card, index) => {
        card.classList.add('fade-in', `stagger-${(index % 6) + 1}`);
        observer.observe(card);
    });
    
    // Auto-animate stat items
    const statItems = document.querySelectorAll('.stat-item');
    statItems.forEach((item, index) => {
        item.classList.add('scale-in', `stagger-${(index % 4) + 1}`);
        observer.observe(item);
    });
    
    // Animate section headers
    const sectionHeaders = document.querySelectorAll('.section-header');
    sectionHeaders.forEach(header => {
        header.classList.add('fade-in');
        observer.observe(header);
    });
    
    // Animate dashboard cards
    const dashboardCards = document.querySelectorAll('.dashboard-card');
    dashboardCards.forEach((card, index) => {
        card.classList.add('fade-in', `stagger-${(index % 3) + 1}`);
        observer.observe(card);
    });
});

// ==================== NAVBAR SCROLL EFFECT ====================
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    if (navbar) {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
});

// ==================== PARALLAX EFFECT ====================
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.hero, .stats-section');
    
    parallaxElements.forEach(el => {
        const speed = 0.5;
        el.style.backgroundPositionY = -(scrolled * speed) + 'px';
    });
});

// ==================== COUNTER ANIMATION ====================
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = Math.ceil(target).toLocaleString();
            clearInterval(timer);
        } else {
            element.textContent = Math.ceil(start).toLocaleString();
        }
    }, 16);
}

// Animate stat numbers when they come into view
document.addEventListener('DOMContentLoaded', function() {
    const statNumbers = document.querySelectorAll('.stat-number');
    const statObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.animated) {
                const target = parseInt(entry.target.dataset.count || entry.target.textContent.replace(/,/g, ''));
                entry.target.dataset.animated = 'true';
                animateCounter(entry.target, target);
            }
        });
    }, { threshold: 0.5 });
    
    statNumbers.forEach(num => {
        num.dataset.count = num.textContent.replace(/,/g, '');
        num.textContent = '0';
        statObserver.observe(num);
    });
});

// Auto-hide flash messages
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const flashContainer = document.querySelector('.flash-container');
        if (flashContainer) {
            flashContainer.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => flashContainer.remove(), 300);
        }
    }, 5000);
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form validation helper
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// AJAX helper function
async function fetchData(url, options = {}) {
    try {
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

// Show loading spinner
function showLoading() {
    const spinner = document.createElement('div');
    spinner.id = 'loadingSpinner';
    spinner.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
    `;
    spinner.innerHTML = `
        <div style="background: white; padding: 30px; border-radius: 12px; text-align: center;">
            <div style="width: 50px; height: 50px; border: 4px solid #f3f3f3; border-top: 4px solid #0f4c5c; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 15px;"></div>
            <p style="color: #0f4c5c; font-weight: 600;">Loading...</p>
        </div>
    `;
    document.body.appendChild(spinner);
    
    // Add spin animation
    if (!document.getElementById('spinAnimation')) {
        const style = document.createElement('style');
        style.id = 'spinAnimation';
        style.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
    }
}

// Hide loading spinner
function hideLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.remove();
    }
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#dc3545' : '#17a2b8'};
        color: white;
        padding: 15px 20px;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 9999;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Confirm dialog helper
function confirmAction(message) {
    return confirm(message);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Format time
function formatTime(timeString) {
    return timeString; // Can be enhanced with time formatting logic
}

// Copy to clipboard
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Copied to clipboard!', 'success');
    } catch (err) {
        showNotification('Failed to copy', 'error');
    }
}

// Export functions for global use
window.volunteerHub = {
    validateEmail,
    debounce,
    fetchData,
    showLoading,
    hideLoading,
    showNotification,
    confirmAction,
    formatDate,
    formatTime,
    copyToClipboard
};
