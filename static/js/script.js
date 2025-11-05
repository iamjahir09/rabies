document.addEventListener('DOMContentLoaded', () => {
    
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            const username = document.getElementById('username').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const signupButton = signupForm.querySelector('.signup-button');

            if (username.length < 3) {
                alert('Username must be at least 3 characters long.');
                e.preventDefault();
            }
            if (!email.includes('@')) {
                alert('Please enter a valid email address.');
                e.preventDefault();
            }
            if (password.length < 6) {
                alert('Password must be at least 6 characters long.');
                e.preventDefault();
            }

            if (!e.defaultPrevented) {
                signupButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Creating Account...</span>';
                signupButton.disabled = true;
            }
        });
    }

    
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const loginButton = loginForm.querySelector('.login-button');

            if (!email.includes('@')) {
                alert('Please enter a valid email address.');
                e.preventDefault();
            }
            if (password.length < 6) {
                alert('Password must be at least 6 characters long.');
                e.preventDefault();
            }

            if (!e.defaultPrevented) {
                loginButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Logging in...</span>';
                loginButton.disabled = true;
            }
        });
    }

    
    const predictForm = document.getElementById('predict-form');
    if (predictForm) {
        predictForm.addEventListener('submit', (e) => {
            const age = document.getElementById('age').value;
            const timeSinceExposure = document.getElementById('time_since_exposure').value;
            const selects = ['location_risk', 'animal_type', 'bite_severity', 'vaccination_status', 'pep', 'wound_location', 'animal_vaccination'];
            const predictButton = predictForm.querySelector('.predict-button');

            for (let selectId of selects) {
                const select = document.getElementById(selectId);
                if (!select.value) {
                    alert(`Please select an option for ${selectId.replace('_', ' ')}.`);
                    e.preventDefault();
                    return;
                }
            }

            if (age < 0 || age > 100) {
                alert('Age must be between 0 and 100.');
                e.preventDefault();
            }
            if (timeSinceExposure < 0 || timeSinceExposure > 720) {
                alert('Time since exposure must be between 0 and 720 hours.');
                e.preventDefault();
            }

            if (!e.defaultPrevented) {
                predictButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Analyzing...</span>';
                predictButton.disabled = true;
            }
        });
    }

    
    const togglePassword = document.getElementById('togglePassword');
    const password = document.getElementById('password');
    if (togglePassword && password) {
        togglePassword.addEventListener('click', function() {
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    }

    
    if (password) {
        const strengthFill = document.querySelector('.strength-fill');
        const strengthText = document.querySelector('.strength-text');
        password.addEventListener('input', function() {
            const passwordVal = this.value;
            let strength = 0;

            if (passwordVal.length >= 8) strength++;
            if (passwordVal.match(/[a-z]/) && passwordVal.match(/[A-Z]/)) strength++;
            if (passwordVal.match(/\d/)) strength++;
            if (passwordVal.match(/[^a-zA-Z\d]/)) strength++;

            if (passwordVal.length === 0) {
                strengthFill.className = 'strength-fill';
                strengthFill.style.width = '0%';
                strengthText.textContent = '';
            } else if (strength <= 2) {
                strengthFill.className = 'strength-fill strength-weak';
                strengthText.textContent = 'Weak password';
            } else if (strength === 3) {
                strengthFill.className = 'strength-fill strength-medium';
                strengthText.textContent = 'Medium strength';
            } else {
                strengthFill.className = 'strength-fill strength-strong';
                strengthText.textContent = 'Strong password';
            }
        });
    }

    
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach((row, index) => {
        row.style.opacity = '0';
        row.style.transform = 'translateY(20px)';
        setTimeout(() => {
            row.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            row.style.opacity = '1';
            row.style.transform = 'translateY(0)';
        }, index * 100);
    });
});