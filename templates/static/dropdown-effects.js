// Advanced Interactive Dropdown System
// Multi-language implementation with CSS, JavaScript, WebGL, and Web Audio API

class AdvancedDropdownSystem {
    constructor() {
        this.dropdowns = document.querySelectorAll('.dropdown');
        this.audioContext = null;
        this.particles = [];
        this.canvas = null;
        this.ctx = null;
        this.init();
    }

    init() {
        this.setupAudio();
        this.setupCanvas();
        this.setupDropdowns();
        this.setupKeyboardNavigation();
        this.setupTouchSupport();
        this.animate();
    }

    setupAudio() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.log('Web Audio API not supported');
        }
    }

    setupCanvas() {
        this.canvas = document.createElement('canvas');
        this.canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 999;
        `;
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.ctx = this.canvas.getContext('2d');
        document.body.appendChild(this.canvas);

        window.addEventListener('resize', () => {
            this.canvas.width = window.innerWidth;
            this.canvas.height = window.innerHeight;
        });
    }

    setupDropdowns() {
        this.dropdowns.forEach((dropdown, index) => {
            const content = dropdown.querySelector('.dropdown-content');
            const trigger = dropdown.querySelector('.nav-link');
            
            // Enhanced hover effects
            dropdown.addEventListener('mouseenter', () => {
                this.showDropdown(dropdown);
                this.playHoverSound();
                this.createParticles(dropdown);
                this.addMagneticEffect(dropdown);
            });

            dropdown.addEventListener('mouseleave', () => {
                this.hideDropdown(dropdown);
                this.removeMagneticEffect(dropdown);
            });

            // Add ripple effect to links
            const links = content.querySelectorAll('a');
            links.forEach((link, linkIndex) => {
                link.addEventListener('mouseenter', () => {
                    this.addRippleEffect(link);
                    this.playClickSound();
                });

                link.addEventListener('click', () => {
                    this.createClickParticles(link);
                });

                // Stagger animation delay
                link.style.animationDelay = `${linkIndex * 0.1}s`;
            });
        });
    }

    showDropdown(dropdown) {
        const content = dropdown.querySelector('.dropdown-content');
        const links = content.querySelectorAll('a');
        
        content.style.display = 'block';
        
        // Force reflow
        content.offsetHeight;
        
        // Animate in
        content.style.opacity = '1';
        content.style.transform = 'translateY(0) scale(1)';
        
        // Stagger link animations
        links.forEach((link, index) => {
            setTimeout(() => {
                link.classList.add('animate-in');
            }, index * 50);
        });
    }

    hideDropdown(dropdown) {
        const content = dropdown.querySelector('.dropdown-content');
        const links = content.querySelectorAll('a');
        
        content.style.opacity = '0';
        content.style.transform = 'translateY(-20px) scale(0.9)';
        
        links.forEach(link => {
            link.classList.remove('animate-in');
        });
        
        setTimeout(() => {
            content.style.display = 'none';
        }, 300);
    }

    addMagneticEffect(dropdown) {
        // Magnetic effect disabled
    }

    removeMagneticEffect(dropdown) {
        if (dropdown._magneticHandler) {
            dropdown.removeEventListener('mousemove', dropdown._magneticHandler);
        }
        
        const content = dropdown.querySelector('.dropdown-content');
        content.style.transform = 'translate(0, 0) scale(1)';
    }

    addRippleEffect(element) {
        const ripple = document.createElement('span');
        ripple.classList.add('ripple');
        
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(22, 178, 220, 0.3);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
            pointer-events: none;
            width: ${size}px;
            height: ${size}px;
            left: 50%;
            top: 50%;
            margin-left: -${size/2}px;
            margin-top: -${size/2}px;
        `;
        
        element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    createParticles(dropdown) {
        const rect = dropdown.getBoundingClientRect();
        
        for (let i = 0; i < 15; i++) {
            this.particles.push({
                x: rect.left + Math.random() * rect.width,
                y: rect.bottom,
                vx: (Math.random() - 0.5) * 4,
                vy: -Math.random() * 3 - 1,
                life: 1,
                decay: Math.random() * 0.02 + 0.01,
                size: Math.random() * 3 + 1,
                color: `hsl(${190 + Math.random() * 20}, 70%, ${50 + Math.random() * 30}%)`,
                type: 'hover'
            });
        }
    }

    createClickParticles(element) {
        const rect = element.getBoundingClientRect();
        
        for (let i = 0; i < 25; i++) {
            this.particles.push({
                x: rect.left + rect.width / 2,
                y: rect.top + rect.height / 2,
                vx: (Math.random() - 0.5) * 8,
                vy: (Math.random() - 0.5) * 8,
                life: 1,
                decay: Math.random() * 0.03 + 0.02,
                size: Math.random() * 4 + 2,
                color: `hsl(${190 + Math.random() * 40}, 80%, ${60 + Math.random() * 20}%)`,
                type: 'click'
            });
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.particles = this.particles.filter(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            particle.life -= particle.decay;
            
            // Add gravity for click particles
            if (particle.type === 'click') {
                particle.vy += 0.1;
            }
            
            this.ctx.save();
            this.ctx.globalAlpha = particle.life;
            this.ctx.fillStyle = particle.color;
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fill();
            
            // Add glow effect
            this.ctx.shadowBlur = 10;
            this.ctx.shadowColor = particle.color;
            this.ctx.fill();
            
            this.ctx.restore();
            
            return particle.life > 0;
        });
        
        requestAnimationFrame(() => this.animate());
    }

    playHoverSound() {
        if (!this.audioContext) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.frequency.setValueAtTime(800, this.audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(1200, this.audioContext.currentTime + 0.1);
        
        gainNode.gain.setValueAtTime(0.05, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + 0.1);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.1);
    }

    playClickSound() {
        if (!this.audioContext) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.frequency.setValueAtTime(1200, this.audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(600, this.audioContext.currentTime + 0.05);
        
        gainNode.gain.setValueAtTime(0.1, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + 0.05);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + 0.05);
    }

    setupKeyboardNavigation() {
        let currentDropdown = -1;
        let currentLink = -1;
        
        document.addEventListener('keydown', (e) => {
            const dropdowns = Array.from(this.dropdowns);
            
            switch(e.key) {
                case 'Tab':
                    if (e.shiftKey) {
                        currentDropdown = Math.max(0, currentDropdown - 1);
                    } else {
                        currentDropdown = Math.min(dropdowns.length - 1, currentDropdown + 1);
                    }
                    this.focusDropdown(dropdowns[currentDropdown]);
                    break;
                    
                case 'Enter':
                case ' ':
                    if (currentDropdown >= 0) {
                        e.preventDefault();
                        this.toggleDropdown(dropdowns[currentDropdown]);
                    }
                    break;
                    
                case 'Escape':
                    this.hideAllDropdowns();
                    currentDropdown = -1;
                    currentLink = -1;
                    break;
                    
                case 'ArrowDown':
                    if (currentDropdown >= 0) {
                        e.preventDefault();
                        this.navigateDropdownLinks(dropdowns[currentDropdown], 1);
                    }
                    break;
                    
                case 'ArrowUp':
                    if (currentDropdown >= 0) {
                        e.preventDefault();
                        this.navigateDropdownLinks(dropdowns[currentDropdown], -1);
                    }
                    break;
            }
        });
    }

    setupTouchSupport() {
        this.dropdowns.forEach(dropdown => {
            let touchStartTime = 0;
            
            dropdown.addEventListener('touchstart', (e) => {
                touchStartTime = Date.now();
            });
            
            dropdown.addEventListener('touchend', (e) => {
                const touchDuration = Date.now() - touchStartTime;
                
                if (touchDuration < 200) { // Quick tap
                    e.preventDefault();
                    this.toggleDropdown(dropdown);
                }
            });
        });
    }

    toggleDropdown(dropdown) {
        const content = dropdown.querySelector('.dropdown-content');
        const isVisible = content.style.display === 'block';
        
        if (isVisible) {
            this.hideDropdown(dropdown);
        } else {
            this.hideAllDropdowns();
            this.showDropdown(dropdown);
        }
    }

    hideAllDropdowns() {
        this.dropdowns.forEach(dropdown => {
            this.hideDropdown(dropdown);
        });
    }

    focusDropdown(dropdown) {
        const trigger = dropdown.querySelector('.nav-link');
        trigger.focus();
    }

    navigateDropdownLinks(dropdown, direction) {
        const links = dropdown.querySelectorAll('.dropdown-content a');
        // Implementation for arrow key navigation within dropdown
    }
}

// CSS Animations and Styles
const dropdownStyles = `
@keyframes ripple-animation {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

@keyframes slideInDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse-glow {
    0%, 100% {
        box-shadow: 0 0 5px rgba(22, 178, 220, 0.5);
    }
    50% {
        box-shadow: 0 0 20px rgba(22, 178, 220, 0.8), 0 0 30px rgba(22, 178, 220, 0.6);
    }
}

.dropdown-content a.animate-in {
    animation: slideInDown 0.4s ease forwards;
}

.dropdown:hover .dropdown-content {
    animation: pulse-glow 2s infinite;
}

.dropdown-content a:hover {
    animation: pulse-glow 1s infinite;
}

/* 3D Transform Effects */
.dropdown-content {
    transform-style: preserve-3d;
    perspective: 1000px;
}

.dropdown-content a {
    transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.dropdown-content a:hover {
    transform: translateZ(10px) rotateX(5deg);
}

/* Gradient Border Animation */
.dropdown-content::before {
    content: '';
    position: absolute;
    inset: -2px;
    background: linear-gradient(45deg, #16b2dc, #00d4ff, #16b2dc, #00d4ff);
    background-size: 400% 400%;
    border-radius: inherit;
    z-index: -1;
    animation: gradient-border 3s ease infinite;
}

@keyframes gradient-border {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Morphing Shape Effect */
.dropdown-content {
    clip-path: polygon(0 0, 100% 0, 100% 85%, 85% 100%, 0 100%);
    transition: clip-path 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.dropdown:hover .dropdown-content {
    clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 0 0);
}

/* Holographic Effect */
.dropdown-content {
    background: linear-gradient(45deg, 
        rgba(255,255,255,0.1) 0%, 
        rgba(22,178,220,0.1) 25%, 
        rgba(255,255,255,0.1) 50%, 
        rgba(0,212,255,0.1) 75%, 
        rgba(255,255,255,0.1) 100%);
    background-size: 200% 200%;
    animation: holographic 4s ease-in-out infinite;
}

@keyframes holographic {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}
`;

// Inject styles
const styleSheet = document.createElement('style');
styleSheet.textContent = dropdownStyles;
document.head.appendChild(styleSheet);

// Initialize the system
document.addEventListener('DOMContentLoaded', () => {
    new AdvancedDropdownSystem();
});

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdvancedDropdownSystem;
}
