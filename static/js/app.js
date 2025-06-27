// YouTube Channel Discovery App - Enhanced UX JavaScript
// Modern interactions, animations, and user experience improvements

document.addEventListener('DOMContentLoaded', function() {


    // Initialize cursor overlay effect
    cursorOverlay = new CursorOverlay();


    // Initialize application
    initializeApp();

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
    // Initialize Bootstrap components
    initializeBootstrapComponents();

    // Auto-dismiss alerts with enhanced animation
    autoHideAlerts();

    // Add loading states to forms
    addFormLoadingStates();

    // Initialize search suggestions
    initializeSearchSuggestions();

    // Add smooth transitions to page elements
    addSmoothTransitions();

    console.log('🚀 YouTube Channel Discovery Tool initialized');
}

/**


/**
 * Enhanced Cursor & Background Overlay Effect System
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

        // Limit number of trails
        if (this.trails.length > this.maxTrails) {
            const oldTrail = this.trails.shift();
            if (oldTrail.element.parentNode) {
                oldTrail.element.parentNode.removeChild(oldTrail.element);
            }
        }

        // Auto-remove trail
        setTimeout(() => {
            this.removeTrail(trail);
        }, 200);
    }

    removeTrail(trailElement) {
        if (trailElement && trailElement.parentNode) {
            trailElement.style.opacity = '0';
            trailElement.style.transform += ' scale(0.5)';
            
            setTimeout(() => {
                if (trailElement.parentNode) {
                    trailElement.parentNode.removeChild(trailElement);
                }
            }, 100);
        }

        // Clean up trails array
        this.trails = this.trails.filter(trail => trail.element !== trailElement);
    }

    clearTrails() {
        this.trails.forEach(trail => {
            if (trail.element.parentNode) {
                trail.element.parentNode.removeChild(trail.element);
            }
        });
        this.trails = [];
    }

    createRipple(x, y) {
        const ripple = document.createElement('div');
        ripple.className = 'cursor-ripple';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        
        document.body.appendChild(ripple);

        // Remove after animation
        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 600);
    }

    handleScroll() {
        this.lastScrollTime = Date.now();
        
        // Create scroll trail on the right side
        const scrollTrail = document.createElement('div');
        scrollTrail.className = 'scroll-trail active';
        scrollTrail.style.right = '10px';
        scrollTrail.style.top = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * (window.innerHeight - 40) + 'px';
        
        document.body.appendChild(scrollTrail);
        this.scrollTrails.push(scrollTrail);

        // Limit scroll trails
        if (this.scrollTrails.length > 5) {
            const oldTrail = this.scrollTrails.shift();
            if (oldTrail.parentNode) {
                oldTrail.parentNode.removeChild(oldTrail);
            }
        }

        // Auto-fade scroll trail
        setTimeout(() => {
            scrollTrail.style.opacity = '0';
            setTimeout(() => {
                if (scrollTrail.parentNode) {
                    scrollTrail.parentNode.removeChild(scrollTrail);
                }
            }, 200);
        }, 100);
    }

    hideScrollTrails() {
        this.scrollTrails.forEach(trail => {
            if (trail.parentNode) {
                trail.classList.remove('active');
                setTimeout(() => {
                    if (trail.parentNode) {
                        trail.parentNode.removeChild(trail);
                    }
                }, 200);
            }
        });
        this.scrollTrails = [];
    }

    isInteractiveElement(element) {
        const interactiveSelectors = [
            'a', 'button', 'input', 'select', 'textarea',
            '.btn', '.card', '.nav-link', '.dropdown-toggle',
            '.hero-search-btn', '.hero-filters-btn', '.preset-card',
            '.feature-card-modern', '.stat-item', '.quick-tag'
        ];

        return interactiveSelectors.some(selector => {
            return element.matches(selector) || element.closest(selector);
        });
    }

    addHoverEffects() {
        // Add hover effect class to interactive elements
        const interactiveElements = document.querySelectorAll(`
            .btn, .card, .nav-link, .dropdown-toggle,
            .hero-search-btn, .hero-filters-btn, .preset-card,
            .feature-card-modern, .stat-item, .quick-tag,
            .preset-card-small, a[href]
        `);

        interactiveElements.forEach(element => {
            if (!element.classList.contains('cursor-hover-effect')) {
                element.classList.add('cursor-hover-effect');
            }
        });
    }

    handleBackgroundHover(e) {
        if (!this.backgroundOverlay) return;

        // Check if hovering over background areas (not interactive elements)
        const target = document.elementFromPoint(e.clientX, e.clientY);
        const isBackground = !this.isInteractiveElement(target) || 
                           target.matches('.hero-section-main, .features-section, .quota-status-section');

        if (isBackground) {
            this.createBackgroundGlow(e.clientX, e.clientY);
        }
    }

    createBackgroundGlow(x, y) {
        if (!this.backgroundOverlay) return;

        // Remove existing glow
        const existingGlow = this.backgroundOverlay.querySelector('.background-hover-glow');
        if (existingGlow) {
            existingGlow.remove();
        }

        // Create new glow
        const glow = document.createElement('div');
        glow.className = 'background-hover-glow';
        glow.style.left = x + 'px';
        glow.style.top = y + 'px';

        // Add intensity for hero section
        const heroSection = document.querySelector('.hero-section-main');
        if (heroSection) {
            const rect = heroSection.getBoundingClientRect();
            if (y >= rect.top && y <= rect.bottom) {
                glow.classList.add('intense');
            }
        }

        this.backgroundOverlay.appendChild(glow);

        // Smooth position updates
        let lastX = x, lastY = y;
        const updateGlow = (newX, newY) => {
            if (glow.parentNode) {
                lastX += (newX - lastX) * 0.1;
                lastY += (newY - lastY) * 0.1;
                glow.style.left = lastX + 'px';
                glow.style.top = lastY + 'px';
            }
        };

        // Store reference for smooth updates
        this.currentGlow = { element: glow, update: updateGlow };
    }

    createBackgroundRipple(x, y) {
        if (!this.backgroundOverlay) return;

        const ripple = document.createElement('div');
        ripple.className = 'background-hover-glow';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.style.width = '50px';
        ripple.style.height = '50px';
        ripple.style.background = 'radial-gradient(circle, rgba(99, 102, 241, 0.2) 0%, transparent 70%)';
        ripple.style.animation = 'backgroundRipple 1s ease-out forwards';

        this.backgroundOverlay.appendChild(ripple);

        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.parentNode.removeChild(ripple);
            }
        }, 1000);
    }

    activateBackgroundOverlay() {
        if (this.backgroundOverlay) {
            this.backgroundOverlay.classList.add('active');
        }
    }

    deactivateBackgroundOverlay() {
        if (this.backgroundOverlay) {
            this.backgroundOverlay.classList.remove('active');
            // Clear existing glows
            const glows = this.backgroundOverlay.querySelectorAll('.background-hover-glow');
            glows.forEach(glow => glow.remove());
        }
    }

    // Scroll-Aware Cursor System
    startScrollCursor() {
        if (!this.customCursor) return;

        this.isScrolling = true;
        document.body.classList.add('cursor-scrolling');
        this.customCursor.style.display = 'block';
        this.customCursor.classList.add('scrolling');
    }

    endScrollCursor() {
        if (!this.customCursor) return;

        this.isScrolling = false;
        document.body.classList.remove('cursor-scrolling');
        
        setTimeout(() => {
            if (!this.isScrolling) {
                this.customCursor.style.display = 'none';
                this.customCursor.classList.remove('scrolling');
                this.clearCursorTrails();
            }
        }, 500);
    }

    handleScrollCursor() {
        if (this.isScrolling && this.customCursor) {
            this.createCursorTrail();
        }
    }

    updateCustomCursor(e) {
        if (!this.customCursor) return;

        this.customCursor.style.left = e.clientX + 'px';
        this.customCursor.style.top = e.clientY + 'px';

        // Update glow position smoothly
        if (this.currentGlow && this.currentGlow.update) {
            this.currentGlow.update(e.clientX, e.clientY);
        }
    }

    createCursorTrail() {
        if (!this.customCursor || !this.isScrolling) return;

        const trail = document.createElement('div');
        trail.className = 'custom-cursor-trail';
        trail.style.left = this.customCursor.style.left;
        trail.style.top = this.customCursor.style.top;
        
        document.body.appendChild(trail);
        this.cursorTrails.push({
            element: trail,
            timestamp: Date.now()
        });

        // Limit trails
        if (this.cursorTrails.length > this.maxCursorTrails) {
            const oldTrail = this.cursorTrails.shift();
            if (oldTrail.element.parentNode) {
                oldTrail.element.parentNode.removeChild(oldTrail.element);
            }
        }

        // Auto-remove trail
        setTimeout(() => {
            if (trail.parentNode) {
                trail.style.opacity = '0';
                setTimeout(() => {
                    if (trail.parentNode) {
                        trail.parentNode.removeChild(trail);
                    }
                }, 200);
            }
        }, 300);
    }

    clearCursorTrails() {
        this.cursorTrails.forEach(trail => {
            if (trail.element.parentNode) {
                trail.element.parentNode.removeChild(trail.element);
            }
        });
        this.cursorTrails = [];
    }

    hideCustomCursor() {
        if (this.customCursor) {
            this.customCursor.style.display = 'none';
        }
        this.clearCursorTrails();
    }

    addBackgroundHoverZones() {
        // Add background interaction zones
        const backgroundSections = document.querySelectorAll(`
            .hero-section-main,
            .features-section,
            .quota-status-section,
            .advanced-search-section
        `);

        backgroundSections.forEach(section => {
            section.addEventListener('mousemove', (e) => {
                if (e.target === section || section.contains(e.target)) {
                    const rect = section.getBoundingClientRect();
                    const x = e.clientX;
                    const y = e.clientY;
                    
                    // Create subtle background effect
                    if (this.backgroundOverlay && this.backgroundOverlay.classList.contains('active')) {
                        this.createBackgroundGlow(x, y);
                    }
                }
            });
        });
    }

    startTrailSystem() {
        // Enhanced trail movement system
        const updateTrails = () => {
            this.trails.forEach((trail, index) => {
                const age = Date.now() - trail.timestamp;
                const opacity = Math.max(0, 1 - (age / 200));
                const scale = Math.max(0.3, 1 - (age / 300));
                
                if (trail.element && trail.element.parentNode) {
                    trail.element.style.opacity = opacity;
                    trail.element.style.transform = `translate(-50%, -50%) scale(${scale})`;
                }
            });

            // Update cursor trails
            this.cursorTrails.forEach((trail, index) => {
                const age = Date.now() - trail.timestamp;
                const opacity = Math.max(0, 1 - (age / 300));
                
                if (trail.element && trail.element.parentNode) {
                    trail.element.style.opacity = opacity;
                }
            });

            if (this.isActive) {
                requestAnimationFrame(updateTrails);
            }
        };

        updateTrails();
    }

    startBackgroundSystem() {
        // Background glow animation system
        const updateBackground = () => {
            if (this.backgroundOverlay && this.backgroundOverlay.classList.contains('active')) {
                // Handle background glow animations
                const glows = this.backgroundOverlay.querySelectorAll('.background-hover-glow');
                glows.forEach(glow => {
                    if (glow.style.animation) {
                        // Handle animated glows
                    }
                });
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

// Initialize cursor overlay system
let cursorOverlay;


 * Initialize Bootstrap tooltips and popovers with modern styling
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
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-info)');
    alerts.forEach(function(alert, index) {
        // Add entrance animation
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-20px)';

        setTimeout(() => {
            alert.style.transition = 'all 0.3s ease-out';
            alert.style.opacity = '1';
            alert.style.transform = 'translateY(0)';
        }, index * 100);

        // Auto-hide after 5 seconds
        setTimeout(function() {
            alert.style.transition = 'all 0.3s ease-in';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';

            setTimeout(() => {
                if (alert.parentNode) {
                    const bsAlert = new bootstrap.Alert(alert);
                    if (bsAlert) {
                        bsAlert.close();
                    }
                }
            }, 300);
        }, 5000 + (index * 200));
    });
}

/**
 * Enhanced search suggestions with modern styling
 */
function initializeSearchSuggestions() {
    const searchInput = document.getElementById('keyword');
    if (!searchInput) return;

    const suggestions = [
        'Tech Reviews', 'Gaming Commentary', 'Cooking Tutorials', 'Travel Vlogs',
        'DIY Projects', 'Fitness Training', 'Music Production', 'Photography Tips',
        'Business Advice', 'Educational Content', 'Comedy Sketches', 'Product Reviews',
        'Lifestyle Vlogs', 'Science Experiments', 'Art Tutorials', 'Language Learning'
    ];

    // Create modern datalist
    const datalist = document.createElement('datalist');
    datalist.id = 'modern-keywords';
    suggestions.forEach(function(suggestion) {
        const option = document.createElement('option');
        option.value = suggestion;
        datalist.appendChild(option);
    });

    searchInput.setAttribute('list', 'modern-keywords');
    searchInput.parentNode.appendChild(datalist);

    // Auto-focus with smooth animation
    setTimeout(() => {
        searchInput.focus();
        searchInput.style.boxShadow = '0 0 0 3px rgba(79, 70, 229, 0.1)';
    }, 500);

    // Enhanced input interactions
    searchInput.addEventListener('input', function(e) {
        if (this.classList.contains('is-invalid')) {
            this.classList.remove('is-invalid');
        }

        // Add subtle glow effect when typing
        this.style.borderColor = 'rgba(79, 70, 229, 0.5)';
        this.style.boxShadow = '0 0 0 3px rgba(79, 70, 229, 0.1)';
    });

    searchInput.addEventListener('blur', function() {
        this.style.borderColor = '';
        this.style.boxShadow = '';
    });
}

/**
 * Add modern loading states to form submissions
 */
function addFormLoadingStates() {
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && form.checkValidity()) {
                // Add enhanced loading state
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;

                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';

                // Add pulsing effect to form
                form.style.opacity = '0.7';
                form.style.pointerEvents = 'none';

                // Fallback re-enable
                setTimeout(function() {
                    submitBtn.classList.remove('loading');
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                    form.style.opacity = '1';
                    form.style.pointerEvents = 'auto';
                }, 30000);
            }
        });
    });
}

/**
 * Enhanced table interactions with modern animations
 */
function enhanceTableInteractions() {
    const tables = document.querySelectorAll('.table');
    tables.forEach(function(table) {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row, index) {
            // Add entrance animation
            row.style.opacity = '0';
            row.style.transform = 'translateY(20px)';

            setTimeout(() => {
                row.style.transition = 'all 0.3s ease-out';
                row.style.opacity = '1';
                row.style.transform = 'translateY(0)';
            }, index * 50);

            // Enhanced hover effects
            row.addEventListener('mouseenter', function() {
                this.style.transform = 'translateX(4px)';
                this.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';

                // Highlight related cells
                const cells = this.querySelectorAll('td');
                cells.forEach(cell => {
                    cell.style.transition = 'background-color 0.2s ease';
                    cell.style.backgroundColor = 'rgba(79, 70, 229, 0.05)';
                });
            });

            row.addEventListener('mouseleave', function() {
                this.style.transform = 'translateX(0)';
                this.style.boxShadow = '';

                const cells = this.querySelectorAll('td');
                cells.forEach(cell => {
                    cell.style.backgroundColor = '';
                });
            });

            // Click ripple effect
            row.addEventListener('click', function(e) {
                if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON' || 
                    e.target.closest('a') || e.target.closest('button')) {
                    return;
                }

                createRippleEffect(e, this);
            });
        });
    });
}

/**
 * Create modern ripple effect
 */
function createRippleEffect(event, element) {
    const rect = element.getBoundingClientRect();
    const ripple = document.createElement('div');
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;

    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(79, 70, 229, 0.3);
        border-radius: 50%;
        pointer-events: none;
        transform: scale(0);
        animation: ripple 0.6s linear;
        z-index: 1;
    `;

    element.style.position = 'relative';
    element.style.overflow = 'hidden';
    element.appendChild(ripple);

    ripple.addEventListener('animationend', () => {
        ripple.remove();
    });
}

/**
 * Enhanced export button interactions
 */
function enhanceExportButtons() {
    const exportButtons = document.querySelectorAll('a[href*="export"]');
    exportButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            const originalHTML = button.innerHTML;
            const originalClasses = button.className;

            // Enhanced loading state
            button.innerHTML = '<i class="fas fa-download fa-bounce me-2"></i>Preparing Export...';
            button.classList.add('loading', 'disabled');
            button.style.background = 'linear-gradient(45deg, #4f46e5, #7c3aed)';
            button.style.color = 'white';

            // Show progress indication
            let progress = 0;
            const progressInterval = setInterval(() => {
                progress += 10;
                button.style.background = `linear-gradient(90deg, #4f46e5 ${progress}%, #7c3aed ${progress}%)`;

                if (progress >= 100) {
                    clearInterval(progressInterval);
                    button.innerHTML = '<i class="fas fa-check me-2"></i>Download Ready!';

                    setTimeout(() => {
                        button.innerHTML = originalHTML;
                        button.className = originalClasses;
                        button.style.background = '';
                        button.style.color = '';
                    }, 2000);
                }
            }, 200);
        });
    });
}

/**
 * Advanced keyboard shortcuts
 */
function addKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for search focus
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('keyword');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();

                // Add visual feedback
                searchInput.style.transform = 'scale(1.02)';
                setTimeout(() => {
                    searchInput.style.transform = 'scale(1)';
                }, 200);

                showToast('🔍 Search focused! Start typing...', 'info', 2000);
            }
        }

        // Escape key interactions
        if (e.key === 'Escape') {
            const searchInput = document.getElementById('keyword');
            if (searchInput && document.activeElement === searchInput) {
                searchInput.value = '';
                searchInput.blur();
                showToast('Search cleared', 'success', 1500);
            }

            // Close any open dropdowns
            const openDropdowns = document.querySelectorAll('.dropdown-menu.show');
            openDropdowns.forEach(dropdown => {
                dropdown.classList.remove('show');
            });
        }

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
    const searchLabel = document.querySelector('label[for="keyword"]');
    if (searchLabel) {
        const hint = document.createElement('small');
        hint.className = 'text-muted ms-2';
        hint.innerHTML = '<kbd>Ctrl</kbd>+<kbd>K</kbd>';
        hint.style.opacity = '0.7';
        searchLabel.appendChild(hint);
    }
}

/**
 * Modern toast notification system
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

    // Apply styles
    toast.style.cssText = `
        background: ${colors[type]};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transform: translateX(100%);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    `;

    toastContainer.appendChild(toast);

    // Animate in
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
    }, 10);

    // Progress bar animation
    const progressBar = toast.querySelector('.toast-progress');
    progressBar.style.cssText = `
        position: absolute;
        bottom: 0;
        left: 0;
        height: 3px;
        background: rgba(255, 255, 255, 0.3);
        width: 100%;
        transform: scaleX(0);
        transform-origin: left;
        transition: transform ${duration}ms linear;
    `;

    setTimeout(() => {
        progressBar.style.transform = 'scaleX(1)';
    }, 100);

    // Auto remove
    setTimeout(() => {
        closeToast(toastId);
    }, duration);
}

/**
 * Close toast notification
 */
function closeToast(toastId) {
    const toast = document.getElementById(toastId);
    if (toast) {
        toast.style.transform = 'translateX(100%)';
        toast.style.opacity = '0';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }
}

/**
 * Get or create toast container
 */
function getOrCreateToastContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
            width: 100%;
        `;
        document.body.appendChild(container);
    }
    return container;
}

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
 * Performance monitoring and optimization
 */
function monitorPerformance() {
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(function() {
                const perfData = window.performance.timing;
                const loadTime = perfData.loadEventEnd - perfData.navigationStart;

                console.log(`⚡ Page load time: ${loadTime}ms`);

                // Show performance feedback for very fast loads
                if (loadTime < 1000) {
                    setTimeout(() => {
                        showToast('⚡ Lightning fast load!', 'success', 2000);
                    }, 1000);
                }
            }, 0);
        });
    }

    // Monitor for large layout shifts
    if ('ResizeObserver' in window) {
        const resizeObserver = new ResizeObserver(entries => {
            // Smooth resize handling
            entries.forEach(entry => {
                entry.target.style.transition = 'all 0.2s ease-out';
            });
        });

        document.querySelectorAll('.card, .table-responsive').forEach(el => {
            resizeObserver.observe(el);
        });
    }
}

/**
 * Enhance form interactions with modern UX patterns
 */
function enhanceFormInteractions() {
    // Floating labels effect
    const formControls = document.querySelectorAll('.form-control, .form-select');
    formControls.forEach(control => {
        const label = document.querySelector(`label[for="${control.id}"]`);
        if (label) {
            control.addEventListener('focus', function() {
                label.style.transform = 'translateY(-8px) scale(0.85)';
                label.style.color = 'var(--primary-color)';
            });

            control.addEventListener('blur', function() {
                if (!this.value) {
                    label.style.transform = '';
                    label.style.color = '';
                }
            });
        }

        // Real-time validation feedback
        control.addEventListener('input', function() {
            if (this.checkValidity()) {
                this.style.borderColor = 'var(--accent-green)';
                this.style.boxShadow = '0 0 0 3px rgba(16, 185, 129, 0.1)';
            } else {
                this.style.borderColor = 'var(--accent-red)';
                this.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.1)';
            }
        });
    });

    // Enhanced button interactions
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });

        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });

        button.addEventListener('mousedown', function() {
            this.style.transform = 'translateY(0) scale(0.98)';
        });

        button.addEventListener('mouseup', function() {
            this.style.transform = 'translateY(-2px) scale(1)';
        });
    });
}

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

console.log('🎨 Modern UI/UX enhancements loaded successfully!');

/**
 * Initialize tooltips
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
 * Initialize Bootstrap components
 */
function initializeBootstrapComponents() {
    // Initialize dropdowns
    var dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
    var dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
        return new bootstrap.Dropdown(dropdownToggleEl);
    });

    // Initialize modals
    var modalElementList = [].slice.call(document.querySelectorAll('.modal'));
    var modalList = modalElementList.map(function (modalEl) {
        return new bootstrap.Modal(modalEl);
    });

    console.log('✅ Bootstrap components initialized');
}

/**
 * Auto-hide alerts with animation
 */
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert[data-bs-dismiss="alert"]');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });
}

/**
 * Add loading states to forms
 */
function addFormLoadingStates() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            }
        });
    });
}

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

/**
 * Add staggered animations
 */
function addStaggeredAnimations() {
    const cards = document.querySelectorAll('.feature-card-modern, .preset-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        setTimeout(() => {
            card.classList.add('animate-in');
        }, index * 100);
    });
}

/**
 * Enhance form interactions
 */
function enhanceFormInteractions() {
    // Add focus classes to form groups
    const formControls = document.querySelectorAll('.form-control-modern');
    formControls.forEach(input => {
        const formGroup = input.closest('.form-group-modern');

        input.addEventListener('focus', () => {
            if (formGroup) formGroup.classList.add('form-group-focused');
        });

        input.addEventListener('blur', () => {
            if (formGroup) formGroup.classList.remove('form-group-focused');
        });
    });

    // Add search input enhancements
    const searchInput = document.querySelector('.hero-search-input');
    const searchGroup = document.querySelector('.search-input-group');

    if (searchInput && searchGroup) {
        searchInput.addEventListener('focus', () => {
            searchGroup.classList.add('search-focused');
        });

        searchInput.addEventListener('blur', () => {
            searchGroup.classList.remove('search-focused');
        });

        searchInput.addEventListener('input', () => {
            if (searchInput.value.length > 0) {
                searchGroup.classList.add('search-has-value');
            } else {
                searchGroup.classList.remove('search-has-value');
            }
        });
    }
}

/**
 * Enhance table interactions
 */
function enhanceTableInteractions() {
    // Add hover effects to table rows
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', () => {
            row.style.transform = 'translateY(-2px)';
            row.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
        });

        row.addEventListener('mouseleave', () => {
            row.style.transform = '';
            row.style.boxShadow = '';
        });
    });
}

/**
 * Add keyboard shortcuts
 */
function addKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K for search focus
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('#keyword');
            if (searchInput) {
                searchInput.focus();
            }
        }
    });


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

// Call refresh function after dynamic content changes
document.addEventListener('DOMContentLoaded', function() {
    // Refresh cursor effects after any dynamic content loads
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                refreshCursorEffects();
            }
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});


}

/**
 * Monitor performance
 */
function monitorPerformance() {
    // Simple performance monitoring
    window.addEventListener('load', () => {
        const loadTime = performance.now();
        console.log(`🚀 Page loaded in ${loadTime.toFixed(2)}ms`);
    });
}