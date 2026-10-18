(function(){
  // Footer year
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Mobile menu toggle
  var menuButton = document.querySelector('.navbar5_menu-button');
  var menu = document.querySelector('.navbar5_menu');
  if (menuButton && menu) {
    menuButton.addEventListener('click', function(){
      var isOpen = menu.style.display === 'flex';
      menu.style.display = isOpen ? '' : 'flex';
      menu.style.flexDirection = 'column';
      menu.style.position = 'absolute';
      menu.style.top = '100%';
      menu.style.left = '0';
      menu.style.right = '0';
      menu.style.background = 'var(--color-cream)';
      menu.style.padding = '1rem 5%';
      menu.style.gap = '1rem';
      // The menu's background switches to cream when open, but nav links
      // default to a light color for the transparent/dark hero navbar —
      // without this class they'd be invisible (light text on cream).
      menu.classList.toggle('is-mobile-open', !isOpen);
    });
  }

  // Newsletter: lightweight success message toggle (no backend wired yet)
  var nlForm = document.getElementById('nlForm');
  var nlSuccess = document.getElementById('nlSuccess');
  if (nlForm && nlSuccess) {
    nlForm.addEventListener('submit', function(e){
      e.preventDefault();
      nlSuccess.classList.add('is-visible');
      nlForm.reset();
    });
  }

  // Testimonial5 ticker (only present on pages that include #reviewTicker)
  // Each review fades in while sliding in from the right to center, holds
  // in place long enough to read, then fades out in place — then the next
  // review repeats the same sequence.
  var root = document.getElementById('reviewTicker');
  if (root) {
    var slides = Array.prototype.slice.call(root.querySelectorAll('.testimonial5_slide'));
    var dots = Array.prototype.slice.call(root.querySelectorAll('.testimonial5_dot'));
    var current = 0;
    var timer = null;
    var FADE_MS = 800;   // slide/fade in or out duration
    var HOLD_MS = 4200;  // fully visible, time to read

    function enter(index){
      var slide = slides[index];
      slide.classList.remove('is-leaving');
      slide.classList.add('is-current');
      slide.classList.add('is-entering');
      void slide.offsetWidth; // force reflow so the transition plays
      slide.classList.add('is-visible');
      dots.forEach(function(d, i){ d.classList.toggle('is-active', i === index); });
    }

    function leave(index, callback){
      var slide = slides[index];
      slide.classList.remove('is-entering');
      slide.classList.add('is-leaving');
      slide.classList.remove('is-visible');
      window.setTimeout(function(){
        slide.classList.remove('is-current', 'is-entering', 'is-leaving', 'is-visible');
        if (callback) callback();
      }, FADE_MS);
    }

    function cycle(){
      leave(current, function(){
        current = (current + 1) % slides.length;
        enter(current);
        timer = window.setTimeout(cycle, FADE_MS + HOLD_MS);
      });
    }

    dots.forEach(function(dot, i){
      dot.addEventListener('click', function(){
        if (i === current) return;
        if (timer) window.clearTimeout(timer);
        leave(current, function(){
          current = i;
          enter(current);
          timer = window.setTimeout(cycle, FADE_MS + HOLD_MS);
        });
      });
    });

    enter(current);
    timer = window.setTimeout(cycle, FADE_MS + HOLD_MS);
  }
})();
