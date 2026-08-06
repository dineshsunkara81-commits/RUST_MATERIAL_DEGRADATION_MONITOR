// Welcome message
function welcome() {
    console.log("🛡️ Welcome to Rust / Material Degradation Monitor");
    console.log("🔬 AI-Powered Corrosion Risk Assessment");
}

// Call on page load
document.addEventListener('DOMContentLoaded', function() {
    welcome();
});

// Format numbers with commas
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Add animation to cards on scroll
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

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.stat-card, .feature-card, .chart-box').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Override for visible class
const style = document.createElement('style');
style.textContent = `
    .stat-card.visible, .feature-card.visible, .chart-box.visible {
        opacity: 1 !important;
        transform: translateY(0) !important;
    }
`;
document.head.appendChild(style);