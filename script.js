const cube = document.querySelector(".cube");

cube.addEventListener("mouseenter", () => {

    cube.style.animationDuration = "3s";

});

cube.addEventListener("mouseleave", () => {

    cube.style.animationDuration = "18s";

});

cube.addEventListener("click", () => {

    cube.classList.toggle("explode");

});
const cube = document.querySelector(".cube");

const faces = document.querySelectorAll(".face");

const logos = [
    "images/logo-blue.jpeg",
    "images/logo-green.jpeg",
    "images/logo-violet.jpeg"
];

cube.addEventListener("click", () => {

    const randomLogo =
        logos[Math.floor(Math.random() * logos.length)];

    faces.forEach(face => {

        face.style.backgroundImage =
            `url('${randomLogo}')`;

    });

});


// ========== HAMBURGER MENU - COMPLETE FIX ==========
const hamburger = document.getElementById('hamburgerBtn');
const navLinks = document.getElementById('navLinks');

function toggleMenu() {
    hamburger.classList.toggle('active');
    navLinks.classList.toggle('active');
    
    // Prevent body scroll when menu is open
    if (navLinks.classList.contains('active')) {
        document.body.style.overflow = 'hidden';
    } else {
        document.body.style.overflow = '';
    }
}

// Toggle menu on hamburger click
if (hamburger) {
    hamburger.addEventListener('click', toggleMenu);
}

// Close menu when a link is clicked
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', (e) => {
        if (navLinks.classList.contains('active')) {
            toggleMenu();
        }
        // Smooth scroll to section
        const targetId = link.getAttribute('href');
        if(targetId && targetId !== '#') {
            e.preventDefault();
            const targetSection = document.querySelector(targetId);
            if(targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
});

// Close menu when window is resized above mobile breakpoint
window.addEventListener('resize', () => {
    if (window.innerWidth > 900 && navLinks.classList.contains('active')) {
        toggleMenu();
    }
});