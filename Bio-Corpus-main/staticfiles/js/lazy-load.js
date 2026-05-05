// Lazy Loading Images avec Intersection Observer
document.addEventListener('DOMContentLoaded', function() {
  const images = document.querySelectorAll('img[data-src]');
  
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.classList.add('loaded');
          observer.unobserve(img);
        }
      });
    }, {
      rootMargin: '50px'
    });
    
    images.forEach(img => imageObserver.observe(img));
  } else {
    // Fallback pour les anciens navigateurs
    images.forEach(img => {
      img.src = img.dataset.src;
    });
  }
});

// Optimisation: Preload les images critiques
function preloadCriticalImages() {
  const criticalImages = document.querySelectorAll('img.critical');
  criticalImages.forEach(img => {
    if (img.dataset.src) {
      img.src = img.dataset.src;
    }
  });
}

// Exécuter après le chargement complet
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', preloadCriticalImages);
} else {
  preloadCriticalImages();
}
