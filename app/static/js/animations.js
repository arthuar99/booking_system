/**
 * Animated Statistics Counter & Testimonial Carousel
 * Creates impressive visual effects for the homepage
 */

// Counting animation using Intersection Observer
class StatCounter {
    constructor(element) {
        this.element = element;
        this.target = parseInt(element.dataset.target, 10);
        this.suffix = element.dataset.suffix || '';
        this.prefix = element.dataset.prefix || '';
        this.duration = 2000;
        this.hasAnimated = false;
    }

    animate() {
        if (this.hasAnimated) return;
        this.hasAnimated = true;

        const startTime = performance.now();
        const startValue = 0;

        const updateCount = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / this.duration, 1);
            
            // Easing function for smooth deceleration
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const currentValue = Math.floor(startValue + (this.target - startValue) * easeOutQuart);
            
            this.element.textContent = this.prefix + currentValue.toLocaleString() + this.suffix;

            if (progress < 1) {
                requestAnimationFrame(updateCount);
            }
        };

        requestAnimationFrame(updateCount);
    }
}

// Initialize all stat counters with Intersection Observer
function initStatCounters() {
    const counters = document.querySelectorAll('[data-counter]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = new StatCounter(entry.target);
                counter.animate();
            }
        });
    }, { threshold: 0.3 });

    counters.forEach(el => observer.observe(el));
}

// Testimonial Carousel
class TestimonialCarousel {
    constructor(container) {
        this.container = container;
        this.slides = container.querySelectorAll('.testimonial-slide');
        this.currentIndex = 0;
        this.autoPlayInterval = null;
        this.init();
    }

    init() {
        if (this.slides.length === 0) return;
        this.showSlide(0);
        this.startAutoPlay();
        
        // Pause on hover
        this.container.addEventListener('mouseenter', () => this.stopAutoPlay());
        this.container.addEventListener('mouseleave', () => this.startAutoPlay());
    }

    showSlide(index) {
        this.slides.forEach((slide, i) => {
            slide.classList.remove('active', 'prev');
            if (i === index) {
                slide.classList.add('active');
            } else if (i === this.currentIndex) {
                slide.classList.add('prev');
            }
        });
        this.currentIndex = index;

        // Update dots
        const dots = this.container.querySelectorAll('.carousel-dot');
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
    }

    next() {
        const nextIndex = (this.currentIndex + 1) % this.slides.length;
        this.showSlide(nextIndex);
    }

    startAutoPlay() {
        this.stopAutoPlay();
        this.autoPlayInterval = setInterval(() => this.next(), 5000);
    }

    stopAutoPlay() {
        if (this.autoPlayInterval) {
            clearInterval(this.autoPlayInterval);
            this.autoPlayInterval = null;
        }
    }
}

// Smooth reveal animation for sections
function initScrollReveal() {
    const revealElements = document.querySelectorAll('[data-reveal]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    revealElements.forEach(el => observer.observe(el));
}

// Floating animation for decorative elements
function initFloatingElements() {
    const floaters = document.querySelectorAll('.float-element');
    floaters.forEach((el, i) => {
        el.style.animationDelay = `${i * 0.5}s`;
    });
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initStatCounters();
    initScrollReveal();
    initFloatingElements();
    
    const carouselContainer = document.querySelector('.testimonial-carousel');
    if (carouselContainer) {
        new TestimonialCarousel(carouselContainer);
    }
});
