/* ============================================================
   SCROLL REVEAL (IntersectionObserver)
   ============================================================ */
const revealTargets = document.querySelectorAll('.section-head, .section-desc, .card, .platform-card');
revealTargets.forEach(el => el.classList.add('reveal'));

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('in-view');
      revealObserver.unobserve(entry.target); // Animates once per session
    }
  });
}, { threshold: 0.15 });

revealTargets.forEach(el => revealObserver.observe(el));