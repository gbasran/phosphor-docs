// Phosphor Docs — Search Engine
// Search index is injected at build time
var SEARCH_INDEX = {{SEARCH_INDEX}};

// Search logic — returns scored + filtered results (max 8)
function searchDocs(query) {
  if (!query || !query.trim()) return [];

  var q = query.toLowerCase().trim();
  var words = q.split(/\s+/).filter(function(w) { return w.length >= 2; });
  if (words.length === 0) return [];

  var scored = [];

  for (var i = 0; i < SEARCH_INDEX.length; i++) {
    var entry = SEARCH_INDEX[i];
    var title = entry.title.toLowerCase();
    var keywords = entry.keywords.toLowerCase();
    var section = entry.section.toLowerCase();
    var all = title + ' ' + keywords + ' ' + section;
    var score = 0;

    // Full-query matching against title
    if (title === q) {
      score += 100;
    } else if (title.indexOf(q) === 0) {
      score += 80;
    } else if (title.indexOf(q) !== -1) {
      score += 60;
    }

    // Full-query matching against keywords
    if (keywords.indexOf(q) !== -1) {
      score += 30;
    }

    // Per-word matching
    var wordHits = 0;
    for (var j = 0; j < words.length; j++) {
      var w = words[j];
      var hit = false;

      if (title.indexOf(w) !== -1) {
        score += 20;
        hit = true;
      }
      if (keywords.indexOf(w) !== -1) {
        score += 10;
        hit = true;
      }
      if (section.indexOf(w) !== -1) {
        score += 5;
        hit = true;
      }

      // Prefix matching
      if (!hit) {
        var parts = all.split(/[\s/.\-_]+/);
        for (var k = 0; k < parts.length; k++) {
          if (parts[k].indexOf(w) === 0 && w.length >= 3) {
            score += 6;
            hit = true;
            break;
          }
        }
      }

      if (hit) wordHits++;
    }

    // Bonus for matching ALL query words
    if (words.length > 1 && wordHits === words.length) {
      score += 25;
    }

    if (score > 0) {
      scored.push({ entry: entry, score: score });
    }
  }

  scored.sort(function(a, b) { return b.score - a.score; });
  return scored.slice(0, 8);
}

// Highlight matching text in title
function highlightMatch(title, query) {
  if (!query || !query.trim()) return title;
  var words = query.trim().split(/\s+/).filter(function(w) { return w.length >= 2; });
  if (words.length === 0) return title;

  var q = query.trim();
  var idx = title.toLowerCase().indexOf(q.toLowerCase());
  if (idx !== -1) {
    return escapeHtml(title.substring(0, idx)) +
      '<mark>' + escapeHtml(title.substring(idx, idx + q.length)) + '</mark>' +
      escapeHtml(title.substring(idx + q.length));
  }

  var result = title;
  for (var i = 0; i < words.length; i++) {
    var w = words[i];
    var regex = new RegExp('(' + w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
    result = result.replace(regex, '<mark>$1</mark>');
  }
  return result;
}

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// DOM setup
(function() {
  var input = document.querySelector('.search-input');
  var resultsBox = document.querySelector('.search-results');
  if (!input || !resultsBox) return;

  var activeIndex = -1;

  function render(results, query) {
    if (results.length === 0 && query && query.trim().length >= 2) {
      resultsBox.innerHTML = '<div class="search-no-results">No results for "' + escapeHtml(query.trim()) + '"</div>';
      resultsBox.classList.add('visible');
      activeIndex = -1;
      return;
    }
    if (results.length === 0) {
      resultsBox.innerHTML = '';
      resultsBox.classList.remove('visible');
      activeIndex = -1;
      return;
    }

    var html = '';
    for (var i = 0; i < results.length; i++) {
      var r = results[i].entry;
      html += '<a class="search-result" href="' + r.url + '" data-index="' + i + '">' +
        '<div class="search-result-title">' + highlightMatch(r.title, query) + '</div>' +
        '<div class="search-result-section">' + escapeHtml(r.section) + '</div>' +
        '</a>';
    }
    resultsBox.innerHTML = html;
    resultsBox.classList.add('visible');
    activeIndex = -1;
  }

  function setActive(index) {
    var items = resultsBox.querySelectorAll('.search-result');
    if (items.length === 0) return;

    for (var i = 0; i < items.length; i++) {
      items[i].classList.remove('active');
    }

    if (index < 0) index = items.length - 1;
    if (index >= items.length) index = 0;
    activeIndex = index;

    items[activeIndex].classList.add('active');
    items[activeIndex].scrollIntoView({ block: 'nearest' });
  }

  function close() {
    resultsBox.innerHTML = '';
    resultsBox.classList.remove('visible');
    activeIndex = -1;
  }

  input.addEventListener('input', function() {
    var results = searchDocs(input.value);
    render(results, input.value);
  });

  input.addEventListener('keydown', function(e) {
    var items = resultsBox.querySelectorAll('.search-result');

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (items.length > 0) setActive(activeIndex + 1);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (items.length > 0) setActive(activeIndex - 1);
    } else if (e.key === 'Enter') {
      e.preventDefault();
      var target = activeIndex >= 0 ? items[activeIndex] : items[0];
      if (target) {
        var sidebar = document.querySelector('.sidebar');
        if (sidebar) sidebar.classList.remove('open');
        window.location.href = target.href;
      }
    } else if (e.key === 'Escape') {
      close();
      input.blur();
    }
  });

  document.addEventListener('click', function(e) {
    if (!e.target.closest('.sidebar-search')) {
      close();
    }
  });

  resultsBox.addEventListener('click', function(e) {
    var link = e.target.closest('.search-result');
    if (link) {
      var sidebar = document.querySelector('.sidebar');
      if (sidebar) sidebar.classList.remove('open');
    }
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === '/' && !e.ctrlKey && !e.metaKey && !e.altKey) {
      var tag = (e.target.tagName || '').toLowerCase();
      if (tag === 'input' || tag === 'textarea' || e.target.isContentEditable) return;
      e.preventDefault();
      input.focus();
    }
  });
})();
