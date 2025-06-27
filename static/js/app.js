// YouTube Channel Discovery App JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-info)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });

    // Initialize suggestion buttons
    const suggestionBtns = document.querySelectorAll('.suggestion-btn');
    const keywordInput = document.getElementById('keyword');
    
    if (suggestionBtns.length > 0 && keywordInput) {
        suggestionBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const keyword = this.getAttribute('data-keyword');
                keywordInput.value = keyword;
                keywordInput.focus();
                
                // Add visual feedback
                this.classList.add('btn-primary');
                this.classList.remove('btn-outline-secondary');
                
                // Reset other buttons
                suggestionBtns.forEach(otherBtn => {
                    if (otherBtn !== this) {
                        otherBtn.classList.remove('btn-primary');
                        otherBtn.classList.add('btn-outline-secondary');
                    }
                });
            });
        });
    }

    // Add loading state to form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && form.checkValidity()) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;
                
                // Re-enable after 30 seconds as fallback
                setTimeout(function() {
                    submitBtn.classList.remove('loading');
                    submitBtn.disabled = false;
                }, 30000);
            }
        });
    });

    // Search input enhancements
    const searchInput = document.getElementById('keyword');
    if (searchInput) {
        // Add search suggestions (you can expand this)
        const suggestions = [
            'Indian Vlogs',
            'Gaming',
            'Tech Reviews',
            'Cooking',
            'Travel',
            'Education',
            'Music',
            'Comedy',
            'Fitness',
            'DIY'
        ];

        // Create datalist for autocomplete
        const datalist = document.createElement('datalist');
        datalist.id = 'keywords';
        suggestions.forEach(function(suggestion) {
            const option = document.createElement('option');
            option.value = suggestion;
            datalist.appendChild(option);
        });
        
        searchInput.setAttribute('list', 'keywords');
        searchInput.parentNode.appendChild(datalist);

        // Focus on search input when page loads
        searchInput.focus();

        // Clear validation on input
        searchInput.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                this.classList.remove('is-invalid');
            }
        });
    }

    // Copy to clipboard functionality
    window.copyToClipboard = function(text, element) {
        navigator.clipboard.writeText(text).then(function() {
            // Show feedback
            const originalText = element.innerHTML;
            element.innerHTML = '<i class="fas fa-check text-success"></i> Copied!';
            setTimeout(function() {
                element.innerHTML = originalText;
            }, 2000);
        }).catch(function(err) {
            console.error('Failed to copy: ', err);
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            const originalText = element.innerHTML;
            element.innerHTML = '<i class="fas fa-check text-success"></i> Copied!';
            setTimeout(function() {
                element.innerHTML = originalText;
            }, 2000);
        });
    };

    // Enhanced table interactions
    const tables = document.querySelectorAll('.table');
    tables.forEach(function(table) {
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(function(row) {
            row.addEventListener('click', function(e) {
                // Don't trigger if clicking on a button or link
                if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON' || e.target.closest('a') || e.target.closest('button')) {
                    return;
                }
                
                // Add visual feedback
                row.style.backgroundColor = 'rgba(var(--bs-primary-rgb), 0.1)';
                setTimeout(function() {
                    row.style.backgroundColor = '';
                }, 200);
            });
        });
    });

    // Export button enhancements
    const exportButtons = document.querySelectorAll('a[href*="export_csv"]');
    exportButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            // Add loading state
            const originalHTML = button.innerHTML;
            button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Exporting...';
            button.classList.add('disabled');
            
            // Reset after download
            setTimeout(function() {
                button.innerHTML = originalHTML;
                button.classList.remove('disabled');
            }, 3000);
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('keyword');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }
        
        // Escape to clear search
        if (e.key === 'Escape') {
            const searchInput = document.getElementById('keyword');
            if (searchInput && document.activeElement === searchInput) {
                searchInput.value = '';
                searchInput.blur();
            }
        }
    });

    // Add keyboard shortcut hints
    const searchLabel = document.querySelector('label[for="keyword"]');
    if (searchLabel) {
        searchLabel.innerHTML += ' <small class="text-muted">(Ctrl+K)</small>';
    }
});

// Utility functions
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
        return num.toString();
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

    showToast: function(message, type = 'info') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 4 seconds
        setTimeout(function() {
            if (toast.parentNode) {
                const bsAlert = new bootstrap.Alert(toast);
                bsAlert.close();
            }
        }, 4000);
    }
};

// Performance monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const perfData = window.performance.timing;
            const loadTime = perfData.loadEventEnd - perfData.navigationStart;
            console.log(`Page load time: ${loadTime}ms`);
        }, 0);
    });
}
