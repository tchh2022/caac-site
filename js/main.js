// ===== Shared Site Scripts =====

// --- Mobile nav toggle ---
document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.querySelector('.hamburger');
    const nav = document.querySelector('.nav');
    if (hamburger && nav) {
        hamburger.addEventListener('click', () => nav.classList.toggle('open'));
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.header-inner')) nav.classList.remove('open');
        });
    }

    // --- Header scroll effect ---
    const header = document.querySelector('.header');
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const y = window.scrollY;
        if (header) header.classList.toggle('scrolled', y > 50);
        lastScroll = y;
    });

    // --- Back to top ---
    const backTop = document.querySelector('.back-top');
    if (backTop) {
        window.addEventListener('scroll', () => {
            backTop.classList.toggle('visible', window.scrollY > 400);
        });
        backTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    // --- Active nav link ---
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav a').forEach(a => {
        const href = a.getAttribute('href').split('/').pop();
        if (href === currentPath) a.classList.add('active');
    });

    // --- FAQ accordion ---
    document.querySelectorAll('.faq-question').forEach(q => {
        q.addEventListener('click', () => {
            const item = q.parentElement;
            item.classList.toggle('open');
        });
    });

    // --- Course filter ---
    const filterBtns = document.querySelectorAll('.course-filter button');
    const courseCards = document.querySelectorAll('.course-card');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const filter = btn.dataset.filter || 'all';
            courseCards.forEach(card => {
                if (filter === 'all' || card.dataset.category === filter) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    // --- Payment method selection ---
    document.querySelectorAll('.payment-method').forEach(m => {
        m.addEventListener('click', () => {
            document.querySelectorAll('.payment-method').forEach(x => x.classList.remove('selected'));
            m.classList.add('selected');
        });
    });

    // --- Toast system ---
    window.showToast = function (message, type = 'success') {
        let toast = document.querySelector('.toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.className = 'toast';
            document.body.appendChild(toast);
        }
        toast.textContent = message;
        toast.className = `toast ${type} show`;
        setTimeout(() => toast.classList.remove('show'), 3000);
    };

    // --- Form submission ---
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const btn = form.querySelector('.btn');
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<span class="loading-spinner"></span> 鎻愪氦涓?..';
            }
                        const formData = new FormData(form);
            var data = {};
            for (var eli = 0; eli < form.elements.length; eli++) {
              var el = form.elements[eli];
              if (el.name && el.type !== 'submit' && el.type !== 'button') {
                data[el.name] = el.value;
              }
            }

            let endpoint = '/api/register';
            const formId = form.id;
            if (formId === 'trialForm') endpoint = '/api/trial';
            else if (formId === 'contactForm') endpoint = '/api/contact';
            if (form.getAttribute('action')) endpoint = form.getAttribute('action');

            try {
                const res = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data),
                });
                const result = await res.json();
                if (result.success) {
                    showToast(result.message, 'success');
                    form.reset();
                } else {
                    showToast(result.message || '提交失败，请重试', 'error');
                }
            } catch (err) {
                showToast('网络异常，请稍后重试', 'error');
            } finally {
                if (btn) {
                    btn.disabled = false;
                    btn.textContent = btn.dataset.originalText || '提交';
                }
            }
        });
    });

    // --- Counter animation ---
    function animateCounters() {
        document.querySelectorAll('.number-item .num, .hero-stat .num').forEach(el => {
            const target = parseInt(el.textContent.replace(/[+,]/g, ''), 10);
            if (isNaN(target) || el.dataset.animated) return;
            el.dataset.animated = 'true';
            const suffix = el.textContent.includes('+') ? '+' : '';
            const duration = 1500;
            const start = performance.now();
            function update(now) {
                const progress = Math.min((now - start) / duration, 1);
                const current = Math.floor(progress * target);
                el.textContent = current.toLocaleString() + suffix;
                if (progress < 1) requestAnimationFrame(update);
            }
            requestAnimationFrame(update);
        });
    }

    // --- Intersection Observer for counters ---
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });
    const numbersSection = document.querySelector('.numbers, .hero-stats');
    if (numbersSection) observer.observe(numbersSection);

    // --- Smooth scroll for anchor links ---
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', (e) => {
            const target = document.querySelector(a.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    console.log('CAAC site ready');
});
