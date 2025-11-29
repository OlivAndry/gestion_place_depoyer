// Simple JavaScript for interactivity

// Navbar toggle for mobile
document.addEventListener('DOMContentLoaded', function() {
    const nav = document.querySelector('nav ul');
    const toggleBtn = document.createElement('button');
    toggleBtn.textContent = '☰';
    toggleBtn.style.display = 'none';
    toggleBtn.style.background = 'none';
    toggleBtn.style.border = 'none';
    toggleBtn.style.color = 'white';
    toggleBtn.style.fontSize = '24px';
    toggleBtn.style.cursor = 'pointer';
    toggleBtn.style.padding = '10px';

    document.querySelector('nav').prepend(toggleBtn);

    // Show toggle button on small screens
    function checkScreenSize() {
        if (window.innerWidth <= 768) {
            toggleBtn.style.display = 'block';
            nav.style.display = 'none';
        } else {
            toggleBtn.style.display = 'none';
            nav.style.display = 'flex';
        }
    }

    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);

    toggleBtn.addEventListener('click', function() {
        if (nav.style.display === 'none' || nav.style.display === '') {
            nav.style.display = 'flex';
            nav.style.flexDirection = 'column';
        } else {
            nav.style.display = 'none';
        }
    });

    // Smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});