// YouTube Channel Discovery App - Enhanced UX JavaScript
// Modern interactions, animations, and user experience improvements

let cursorOverlay = null;

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 YouTube Discovery App Loading...');

    // Initialize cursor overlay effect
    cursorOverlay = new CursorOverlay();

    // Initialize application
    initializeApp();

    // Start API status monitoring
    startApiStatusMonitoring();

    // Add staggered animations to cards
    addStaggeredAnimations();

    // Initialize modern tooltips and popovers
    initializeTooltips();

    // Enhanced form interactions
    enhanceFormInteractions();

    // Modern table enhancements
    enhanceTableInteractions();

    // Add keyboard shortcuts
    addKeyboardShortcuts();

    // Performance monitoring
    monitorPerformance();
});

/**
 * Initialize core application functionality
 */
function initializeApp() {
    console.log('🔧 Initializing app components...');

    // Initialize Bootstrap components
    initializeBootstrapComponents();

    // Auto-hide alerts
    initializeAlertSystem();

    // Enhanced export buttons
    enhanceExportButtons();

    console.log('✅ App initialization complete');
}

/**
 * Initialize Bootstrap components
 */
function initializeBootstrapComponents() {
    // Enhanced tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            boundary: 'viewport',
            customClass: 'modern-tooltip'
        });
    });

    // Enhanced popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl, {
            trigger: 'hover focus',
            customClass: 'modern-popover'
        });
    });
}

/**
 * Add staggered animations to page elements
 */
function addStaggeredAnimations() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.classList.add('fade-in-up');
        card.style.animationDelay = `${index * 0.1}s`;
    });

    const buttons = document.querySelectorAll('.btn');
    buttons.forEach((btn, index) => {
        btn.style.animationDelay = `${index * 0.05}s`;
    });
}

/**
 * Enhanced alert dismissal with smooth animations
 */
function initializeAlertSystem() {
    // Auto-hide success alerts after 5 seconds
    const successAlerts = document.querySelectorAll('.alert-success');
    successAlerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentNode) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-20px)';
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 300);
            }
        }, 5000);
    });

    // Enhanced close button functionality
    const alertCloseButtons = document.querySelectorAll('.alert .btn-close');
    alertCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.closest('.alert');
            if (alert) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-20px)';
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 300);
            }
        });
    });
}

/**
 * Initialize modern tooltips
 */
function initializeTooltips() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            delay: { show: 300, hide: 100 },
            animation: true
        });
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl, {
            trigger: 'hover focus',
            delay: { show: 200, hide: 100 }
        });
    });

    console.log('✅ Tooltips and popovers initialized');
}

/**
 * Enhanced form interactions
 */
function enhanceFormInteractions() {
    const searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        const submitButton = searchForm.querySelector('button[type="submit"]');
        const keywordInput = searchForm.querySelector('input[name="keyword"]');

        if (submitButton && keywordInput) {
            // Add loading state on form submission
            searchForm.addEventListener('submit', function() {
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Searching...';
                submitButton.disabled = true;
            });

            // Real-time validation
            keywordInput.addEventListener('input', function() {
                const isValid = this.value.trim().length >= 2;

                if (isValid) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                    submitButton.disabled = false;
                } else {
                    this.classList.remove('is-valid');
                    if (this.value.length > 0) {
                        this.classList.add('is-invalid');
                    }
                    submitButton.disabled = true;
                }
            });
        }
    }
}

/**
 * Enhanced table interactions
 */
function enhanceTableInteractions() {
    const tables = document.querySelectorAll('.table');
    tables.forEach(table => {
        // Add hover effects to table rows
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.01)';
                this.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
            });

            row.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
                this.style.boxShadow = 'none';
            });
        });
    });
}

/**
 * Add keyboard shortcuts
 */
function addKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter for quick search
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const searchForm = document.querySelector('form[action*="search"]');
            if (searchForm) {
                searchForm.submit();
            }
        }
    });

    // Add keyboard hints to UI
    addKeyboardHints();
}

/**
 * Add keyboard shortcut hints to UI elements
 */
function addKeyboardHints() {
    const searchButton = document.querySelector('button[type="submit"]');
    if (searchButton) {
        searchButton.title = 'Click to search or press Ctrl+Enter';
    }
}

/**
 * Enhanced export button functionality
 */
function enhanceExportButtons() {
    const exportButtons = document.querySelectorAll('[data-export-format]');
    exportButtons.forEach(button => {
        button.addEventListener('click', function() {
            const format = this.dataset.exportFormat;
            const originalText = this.innerHTML;

            // Add loading state
            this.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Exporting ${format.toUpperCase()}...`;
            this.disabled = true;

            // Reset button after delay
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
                showToast(`${format.toUpperCase()} export completed!`, 'success');
            }, 2000);
        });
    });
}

/**
 * Monitor performance
 */
function monitorPerformance() {
    window.addEventListener('load', () => {
        const loadTime = performance.now();
        console.log(`🚀 Page loaded in ${loadTime.toFixed(2)}ms`);
    });
}

/**
 * Start API status monitoring
 */
function startApiStatusMonitoring() {
    updateApiStatus();
    // Update every 30 seconds
    setInterval(updateApiStatus, 30000);
}

/**
 * Update API status display
 */
function updateApiStatus() {
    fetch('/api/quota-status')
        .then(response => response.json())
        .then(data => {
            console.log('📊 API Status Update:', data);

            // Update quota display
            const quotaUsed = document.querySelector('.quota-used');
            const quotaLimit = document.querySelector('.quota-limit');
            const quotaPercentage = document.querySelector('.quota-percentage');
            const quotaStatus = document.querySelector('.quota-status');

            if (quotaUsed) quotaUsed.textContent = data.quota_used || 0;
            if (quotaLimit) quotaLimit.textContent = data.quota_limit || 10000;
            if (quotaPercentage) quotaPercentage.textContent = Math.round(data.quota_percentage || 0);

            // Update status indicator
            if (quotaStatus) {
                quotaStatus.className = `badge badge-${getStatusColor(data.status)}`;
                quotaStatus.textContent = (data.status || 'healthy').toUpperCase();
            }

            // Show error if present
            if (data.error_message) {
                console.warn('⚠️ API Status Warning:', data.error_message);

                const errorContainer = document.querySelector('.api-error-message');
                if (errorContainer) {
                    errorContainer.textContent = data.error_message;
                    errorContainer.style.display = 'block';
                }
            }
        })
        .catch(error => {
            console.error('❌ Failed to fetch API status:', error);

            const errorContainer = document.querySelector('.api-error-message');
            if (errorContainer) {
                errorContainer.textContent = 'Failed to connect to API status endpoint';
                errorContainer.style.display = 'block';
            }
        });
}

/**
 * Get status color based on API status
 */
function getStatusColor(status) {
    switch (status) {
        case 'healthy': return 'success';
        case 'warning': return 'warning';
        case 'critical': return 'danger';
        case 'error': return 'danger';
        default: return 'secondary';
    }
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info', duration = 4000) {
    const toastContainer = getOrCreateToastContainer();
    const toast = document.createElement('div');
    const toastId = 'toast-' + Date.now();

    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };

    const colors = {
        success: 'linear-gradient(135deg, #10b981, #059669)',
        error: 'linear-gradient(135deg, #ef4444, #dc2626)',
        warning: 'linear-gradient(135deg, #f59e0b, #d97706)',
        info: 'linear-gradient(135deg, #3b82f6, #2563eb)'
    };

    toast.id = toastId;
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <i class="${icons[type]} toast-icon"></i>
            <span class="toast-message">${message}</span>
            <button class="toast-close" onclick="closeToast('${toastId}')">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="toast-progress"></div>
    `;

    toast.style.background = colors[type];
    toastContainer.appendChild(toast);

    // Auto-remove after duration
    setTimeout(() => {
        closeToast(toastId);
    }, duration);
}

/**
 * Get or create toast container
 */
function getOrCreateToastContainer() {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
        `;
        document.body.appendChild(container);
    }
    return container;
}

/**
 * Close toast notification
 */
function closeToast(toastId) {
    const toast = document.getElementById(toastId);
    if (toast) {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 300);
    }
}

/**
 * Cursor overlay system for enhanced visual effects
 */
class CursorOverlay {
    constructor() {
        this.overlay = null;
        this.backgroundOverlay = null;
        this.customCursor = null;
        this.trails = [];
        this.cursorTrails = [];
        this.maxTrails = 8;
        this.maxCursorTrails = 5;
        this.isActive = false;
        this.isScrolling = false;
        this.lastMousePosition = { x: 0, y: 0 };
        this.scrollTrails = [];
        this.lastScrollTime = 0;
        this.scrollTimeout = null;

        this.init();
    }

    init() {
        // Skip on touch devices
        if ('ontouchstart' in window || navigator.maxTouchPoints > 0) {
            return;
        }

        // Respect reduced motion preference
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            return;
        }

        this.createOverlay();
        this.createBackgroundOverlay();
        this.createCustomCursor();
        this.bindEvents();
        this.startTrailSystem();
        this.startBackgroundSystem();
    }

    createOverlay() {
        this.overlay = document.createElement('div');
        this.overlay.className = 'cursor-overlay';
        document.body.appendChild(this.overlay);
    }

    createBackgroundOverlay() {
        this.backgroundOverlay = document.createElement('div');
        this.backgroundOverlay.className = 'background-hover-overlay';
        document.body.appendChild(this.backgroundOverlay);
    }

    createCustomCursor() {
        this.customCursor = document.createElement('div');
        this.customCursor.className = 'custom-cursor';
        this.customCursor.style.display = 'none';
        document.body.appendChild(this.customCursor);
    }

    bindEvents() {
        // Mouse movement
        document.addEventListener('mousemove', (e) => {
            this.handleMouseMove(e);
            this.handleBackgroundHover(e);
            this.updateCustomCursor(e);
        });

        // Mouse enter/leave window
        document.addEventListener('mouseenter', () => {
            this.activateOverlay();
            this.activateBackgroundOverlay();
        });

        document.addEventListener('mouseleave', () => {
            this.deactivateOverlay();
            this.deactivateBackgroundOverlay();
            this.hideCustomCursor();
        });

        // Click effects
        document.addEventListener('click', (e) => {
            this.createRipple(e.clientX, e.clientY);
            this.createBackgroundRipple(e.clientX, e.clientY);
        });

        // Enhanced scroll effects
        window.addEventListener('scroll', () => {
            this.handleScroll();
            this.handleScrollCursor();

            clearTimeout(this.scrollTimeout);
            this.scrollTimeout = setTimeout(() => {
                this.hideScrollTrails();
                this.endScrollCursor();
            }, 200);
        });

        // Wheel event for scroll detection
        window.addEventListener('wheel', () => {
            this.startScrollCursor();
        });

        // Hover effects for interactive elements
        this.addHoverEffects();
        this.addBackgroundHoverZones();
    }

    handleMouseMove(e) {
        this.lastMousePosition = { x: e.clientX, y: e.clientY };

        if (!this.isActive) {
            this.activateOverlay();
        }

        // Create trail effect
        this.createTrail(e.clientX, e.clientY);
    }

    activateOverlay() {
        if (!this.overlay) return;

        this.isActive = true;
        this.overlay.classList.add('active');
    }

    deactivateOverlay() {
        if (!this.overlay) return;

        this.isActive = false;
        this.overlay.classList.remove('active');

        // Clear trails after delay
        setTimeout(() => {
            this.clearTrails();
        }, 300);
    }

    createTrail(x, y) {
        if (!this.overlay || !this.isActive) return;

        const trail = document.createElement('div');
        trail.className = 'cursor-trail';
        trail.style.left = x + 'px';
        trail.style.top = y + 'px';

        // Add variation for different hover states
        const hoveredElement = document.elementFromPoint(x, y);
        if (hoveredElement && this.isInteractiveElement(hoveredElement)) {
            trail.classList.add('large');
        }

        this.overlay.appendChild(trail);
        this.trails.push({
            element: trail,
            timestamp: Date.now()
        });

        // Remove old trails
        if (this.trails.length > this.maxTrails) {
            const oldTrail = this.trails.shift();
            if (oldTrail.element && oldTrail.element.parentNode) {
                oldTrail.element.remove();
            }
        }
    }

    isInteractiveElement(element) {
        const interactiveTags = ['A', 'BUTTON', 'INPUT', 'SELECT', 'TEXTAREA'];
        const interactiveClasses = ['btn', 'link', 'clickable'];

        return interactiveTags.includes(element.tagName) ||
               interactiveClasses.some(cls => element.classList.contains(cls)) ||
               element.onclick !== null ||
               element.style.cursor === 'pointer';
    }

    clearTrails() {
        this.trails.forEach(trail => {
            if (trail.element && trail.element.parentNode) {
                trail.element.remove();
            }
        });
        this.trails = [];
    }

    createRipple(x, y) {
        if (!this.overlay) return;

        const ripple = document.createElement('div');
        ripple.className = 'click-ripple';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';

        this.overlay.appendChild(ripple);

        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.remove();
            }
        }, 600);
    }

    handleBackgroundHover(e) {
        // Background hover effects
    }

    activateBackgroundOverlay() {
        if (this.backgroundOverlay) {
            this.backgroundOverlay.classList.add('active');
        }
    }

    deactivateBackgroundOverlay() {
        if (this.backgroundOverlay) {
            this.backgroundOverlay.classList.remove('active');
        }
    }

    createBackgroundRipple(x, y) {
        // Background ripple effects
    }

    handleScroll() {
        // Scroll effects
    }

    handleScrollCursor() {
        // Scroll cursor effects
    }

    startScrollCursor() {
        // Start scroll cursor
    }

    hideScrollTrails() {
        // Hide scroll trails
    }

    endScrollCursor() {
        // End scroll cursor
    }

    updateCustomCursor(e) {
        // Update custom cursor position
    }

    hideCustomCursor() {
        if (this.customCursor) {
            this.customCursor.style.display = 'none';
        }
    }

    addHoverEffects() {
        // Add hover effects to interactive elements
    }

    addBackgroundHoverZones() {
        // Add background hover zones
    }

    startTrailSystem() {
        // Start trail animation system
        const updateTrails = () => {
            this.trails.forEach((trail, index) => {
                const age = Date.now() - trail.timestamp;
                const opacity = Math.max(0, 1 - (age / 500));
                const scale = Math.max(0.1, 1 - (age / 500));

                if (trail.element && trail.element.parentNode) {
                    trail.element.style.opacity = opacity;
                    trail.element.style.transform = `translate(-50%, -50%) scale(${scale})`;
                }
            });

            if (this.isActive) {
                requestAnimationFrame(updateTrails);
            }
        };

        updateTrails();
    }

    startBackgroundSystem() {
        // Background animation system
        const updateBackground = () => {
            if (this.backgroundOverlay && this.backgroundOverlay.classList.contains('active')) {
                // Handle background animations
            }

            requestAnimationFrame(updateBackground);
        };

        updateBackground();
    }

    // Public method to refresh hover effects for dynamically added elements
    refreshHoverEffects() {
        this.addHoverEffects();
    }
}

/**
 * Refresh cursor effects for dynamically added content
 */
function refreshCursorEffects() {
    if (cursorOverlay) {
        setTimeout(() => {
            cursorOverlay.refreshHoverEffects();
        }, 100);
    }
}

console.log('🎨 Modern UI/UX enhancements loaded successfully!');

/**
 * Modern copy to clipboard functionality
 */
window.copyToClipboard = function(text, element, successMessage = 'Copied to clipboard!') {
    navigator.clipboard.writeText(text).then(function() {
        const originalHTML = element.innerHTML;
        element.innerHTML = '<i class="fas fa-check text-success"></i> Copied!';
        element.style.transform = 'scale(0.95)';

        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 100);

        setTimeout(function() {
            element.innerHTML = originalHTML;
        }, 2000);

        showToast(successMessage, 'success', 2000);

    }).catch(function(err) {
        console.error('Failed to copy: ', err);
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);

        showToast('Copied (fallback method)', 'success', 2000);
    });
};

/**
 * Add CSS for additional animations
 */
function addAnimationStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }

        .toast-notification {
            animation: slideInRight 0.3s ease-out;
        }

        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        .toast-content {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .toast-close {
            background: none;
            border: none;
            color: inherit;
            cursor: pointer;
            padding: 0.25rem;
            border-radius: 0.25rem;
            transition: background-color 0.2s;
            margin-left: auto;
        }

        .toast-close:hover {
            background: rgba(255, 255, 255, 0.2);
        }

        kbd {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 0.25rem;
            padding: 0.125rem 0.25rem;
            font-size: 0.75rem;
            font-family: monospace;
        }
    `;
    document.head.appendChild(style);
}

// Initialize additional styles
addAnimationStyles();

// Export utility functions
window.utils = {
    formatNumber: function(num) {
        if (num >= 1000000000) {
            return (num / 1000000000).toFixed(1) + 'B';
        }
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num ? num.toString() : '0';
    },

    debounce: function(func, wait, immediate) {
        var timeout;
        return function() {
            var context = this, args = arguments;
            var later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    },

    showToast: showToast,

    animateValue: function(element, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const currentValue = Math.floor(progress * (end - start) + start);
            element.textContent = this.formatNumber(currentValue);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
};

// Initialize export button enhancements when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    enhanceExportButtons();
});

/**
 * Initialize search suggestions
 */
function initializeSearchSuggestions() {
    const searchInput = document.querySelector('#keyword');
    if (searchInput) {
        const suggestions = [
            'tech reviews', 'cooking tutorials', 'fitness channels', 'gaming streamers',
            'educational content', 'music production', 'photography tips', 'business advice'
        ];

        // Add input event listener for suggestions
        searchInput.addEventListener('input', function() {
            // Simple suggestion implementation
            const value = this.value.toLowerCase();
            // You can enhance this with a proper suggestion dropdown
        });
    }
}

/**
 * Add smooth transitions
 */
function addSmoothTransitions() {
    // Add intersection observer for animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    });

    // Observe elements with animation classes
    document.querySelectorAll('.feature-card-modern, .preset-card').forEach(el => {
        observer.observe(el);
    });
}