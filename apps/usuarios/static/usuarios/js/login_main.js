// main.js - Versión sin jQuery
document.addEventListener('DOMContentLoaded', function() {
    // Full height function
    function setFullHeight() {
        const elements = document.querySelectorAll('.js-fullheight');
        elements.forEach(function(element) {
            element.style.height = window.innerHeight + 'px';
        });
    }

    // Set initial height and update on resize
    setFullHeight();
    window.addEventListener('resize', setFullHeight);

    // Toggle password visibility
    const togglePassword = document.querySelector('.toggle-password');
    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
            const input = document.querySelector(this.getAttribute('toggle'));
            if (input.getAttribute('type') === 'password') {
                input.setAttribute('type', 'text');
            } else {
                input.setAttribute('type', 'password');
            }
        });
    }
});