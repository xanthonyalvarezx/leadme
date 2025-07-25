// Hamburger Menu Functionality
document.addEventListener("DOMContentLoaded", function () {
    const hamburgerMenu = document.querySelector(".hamburger-menu");
    const navLinks = document.querySelector(".nav-links");
    const mobileOverlay = document.querySelector(".mobile-overlay");
    const body = document.body;

    // Toggle menu when hamburger is clicked
    hamburgerMenu.addEventListener("click", function () {
        hamburgerMenu.classList.toggle("active");
        navLinks.classList.toggle("active");
        mobileOverlay.classList.toggle("active");
        body.style.overflow = navLinks.classList.contains("active")
            ? "hidden"
            : "";
    });

    // Close menu when clicking on a link
    const navLinksItems = navLinks.querySelectorAll("a, button");
    navLinksItems.forEach((item) => {
        item.addEventListener("click", function () {
            hamburgerMenu.classList.remove("active");
            navLinks.classList.remove("active");
            mobileOverlay.classList.remove("active");
            body.style.overflow = "";
        });
    });

    // Close menu when clicking outside
    document.addEventListener("click", function (event) {
        if (
            !hamburgerMenu.contains(event.target) &&
            !navLinks.contains(event.target)
        ) {
            hamburgerMenu.classList.remove("active");
            navLinks.classList.remove("active");
            mobileOverlay.classList.remove("active");
            body.style.overflow = "";
        }
    });

    // Close menu on window resize (if screen becomes larger)
    window.addEventListener("resize", function () {
        if (window.innerWidth > 768) {
            hamburgerMenu.classList.remove("active");
            navLinks.classList.remove("active");
            mobileOverlay.classList.remove("active");
            body.style.overflow = "";
        }
    });

    // Prevent body scroll when menu is open
    navLinks.addEventListener(
        "touchmove",
        function (e) {
            if (navLinks.classList.contains("active")) {
                e.preventDefault();
            }
        },
        { passive: false }
    );
});
