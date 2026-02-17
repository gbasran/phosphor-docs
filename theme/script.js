// ── Generate IDs for h3 headings ──
document.querySelectorAll('.content h3').forEach(function(h3) {
  if (!h3.id) {
    h3.id = h3.textContent.trim().toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '');
  }
});

// ── Build Table of Contents ──
var toc = document.querySelector('.toc');
if (toc) {
  var headings = document.querySelectorAll('.content h2, .content h3');
  if (headings.length > 1) {
    var html = '<div class="toc-label">On this page</div>';
    headings.forEach(function(h) {
      var level = h.tagName.toLowerCase();
      var targetId;
      if (h.tagName === 'H2') {
        var section = h.closest('.section[id]');
        targetId = section ? section.id : h.id;
      } else {
        targetId = h.id;
      }
      html += '<a href="#' + targetId + '" class="toc-' + level + '">' + h.textContent.trim() + '</a>';
    });
    toc.innerHTML = html;
  }
}

// ── Scroll spy — highlight active sidebar link + TOC link ──
var sections = document.querySelectorAll('.section[id]');
var navLinks = document.querySelectorAll('.sidebar-nav a');
var tocAnchors = toc ? toc.querySelectorAll('a') : [];
var backToTop = document.querySelector('.back-to-top');

function onScroll() {
  var scrollY = window.scrollY + 120;

  // Back to top visibility
  if (window.scrollY > 400) {
    backToTop.classList.add('visible');
  } else {
    backToTop.classList.remove('visible');
  }

  // Sidebar scroll spy
  var current = '';
  sections.forEach(function(section) {
    if (section.offsetTop <= scrollY) {
      current = section.id;
    }
  });

  navLinks.forEach(function(link) {
    link.classList.remove('active');
    var href = link.getAttribute('href');
    if (href === '#' + current || href.endsWith('#' + current)) {
      link.classList.add('active');
    }
  });

  // TOC scroll spy
  if (tocAnchors.length > 0) {
    var currentToc = '';
    tocAnchors.forEach(function(a) {
      var id = a.getAttribute('href').slice(1);
      var el = document.getElementById(id);
      if (el && el.offsetTop <= scrollY) {
        currentToc = id;
      }
    });
    tocAnchors.forEach(function(a) {
      a.classList.remove('active');
      if (a.getAttribute('href') === '#' + currentToc) {
        a.classList.add('active');
      }
    });
  }
}

window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// ── Close mobile sidebar on nav click ──
navLinks.forEach(function(link) {
  link.addEventListener('click', function() {
    document.querySelector('.sidebar').classList.remove('open');
  });
});