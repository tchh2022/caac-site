import os, re
base = os.environ["USERPROFILE"] + "\\Documents\\CAAC考证报名网站"

# ===== 1. Update index.html =====
hp = base + "\\index.html"
html = open(hp, "r", encoding="utf-8").read()

# Teacher data for all 8 teachers
teachers = [
    ("teacher-wang.jpg", "\u738b", "\u738b\u5efa\u56fd", "\u9996\u5e2d\u6559\u5458 / \u6c11\u822a\u5c40\u59d4\u4efb\u4ee3\u8868", "15\u5e74\u822a\u7a7a\u4ece\u4e1a\u7ecf\u9a8c<br>\u6301\u6709CAAC\u591a\u65cb\u7ffc+\u56fa\u5b9a\u7ffc\u6559\u5458\u6267\u7167<br>\u7d2f\u8ba1\u57f9\u8bad\u5b66\u5458800+\u4eba"),
    ("teacher-li.jpg", "\u674e", "\u674e\u660e\u8fbe", "\u9ad8\u7ea7\u6559\u5458 / \u65e0\u4eba\u673a\u7cfb\u7edf\u5de5\u7a0b\u5e08", "10\u5e74\u65e0\u4eba\u673a\u884c\u4e1a\u7ecf\u9a8c<br>\u7cbe\u901a\u98de\u63a7\u7cfb\u7edf\u8c03\u8bd5\u4e0e\u6545\u969c\u6392\u67e5<br>\u591a\u6b21\u53c2\u4e0e\u56fd\u5bb6\u7ea7\u65e0\u4eba\u673a\u9879\u76ee"),
    ("teacher-zhang.jpg", "\u5f20", "\u5f20\u96ea\u5cf0", "\u7406\u8bba\u6559\u5b66\u8d1f\u8d23\u4eba", "\u822a\u7a7a\u9662\u6821\u5ba2\u5ea7\u6559\u6388<br>\u6c11\u822a\u6cd5\u89c4\u4e0e\u6c14\u8c61\u5b66\u4e13\u5bb6<br>\u7f16\u8457\u591a\u672c\u65e0\u4eba\u673a\u57f9\u8bad\u6559\u6750"),
    ("teacher-liu.jpg", "\u5218", "\u5218\u9e4f\u98de", "\u9ad8\u7ea7\u5b9e\u64cd\u6559\u5458", "8\u5e74\u65e0\u4eba\u673a\u5b9e\u64cd\u98de\u884c\u7ecf\u9a8c<br>\u5404\u7c7b\u673a\u578b\u7d2f\u8ba1\u98de\u884c5000+\u5c0f\u65f6<br>\u64c5\u957f\u7279\u60c5\u5904\u7f6e\u4e0e\u98de\u884c\u6280\u5de7"),
    ("teacher-chen.jpg", "\u9648", "\u9648\u96c5\u6587", "\u6a21\u62df\u5668\u8bad\u7ec3\u6559\u5458", "6\u5e74\u65e0\u4eba\u673a\u6559\u5b66\u7ecf\u9a8c<br>\u64c5\u957f\u6a21\u62df\u5668\u6559\u5b66\u4e0e\u8003\u6838<br>\u5f00\u53d1\u591a\u5957\u6a21\u62df\u8bad\u7ec3\u8bfe\u7a0b"),
    ("teacher-zhao.jpg", "\u8d75", "\u8d75\u5929\u7ffc", "\u56fa\u5b9a\u7ffc\u4e13\u9879\u6559\u5458", "12\u5e74\u56fa\u5b9a\u7ffc\u98de\u884c\u7ecf\u9a8c<br>\u6301\u6709CAAC\u56fa\u5b9a\u7ffc\u6559\u5458\u6267\u7167<br>\u56fa\u5b9a\u7ffc\u98de\u884c\u6280\u672f\u4e00\u6d41"),
    ("teacher-sun.jpg", "\u5b59", "\u5b59\u6d69\u7136", "\u8003\u8bd5\u8f85\u5bfc\u4e13\u5458", "\u6df1\u7814CAAC\u8003\u8bd5\u4f53\u7cfb<br>\u7406\u8bba\u8003\u8bd5\u8f85\u5bfc\u901a\u8fc7\u738799%<br>\u7cbe\u51c6\u628a\u63e1\u8003\u70b9\u96be\u70b9"),
    ("teacher-zhou.jpg", "\u5468", "\u5468\u7acb\u65b0", "\u884c\u4e1a\u5e94\u7528\u987e\u95ee", "\u8d44\u6df1\u65e0\u4eba\u673a\u884c\u4e1a\u5e94\u7528\u4e13\u5bb6<br>\u53c2\u4e0e\u5236\u5b9a\u591a\u9879\u884c\u4e1a\u6807\u51c6<br>\u4e3a\u5b66\u5458\u63d0\u4f9b\u5c31\u4e1a\u6307\u5bfc"),
]

# Build teacher card HTML
card_tpl = """            <div class="teacher-card">
                <div class="teacher-avatar" style="background-image:url(images/{img})">{initial}</div>
                <h4>{name}</h4>
                <div class="title">{title}</div>
                <div class="desc">{desc}</div>
            </div>"""

all_cards = ""
for t in teachers:
    all_cards += card_tpl.format(img=t[0], initial=t[1], name=t[2], title=t[3], desc=t[4]) + "\n"

# Find carousel-track and replace its content
track_start = html.index('id="carouselTrack">') + len('id="carouselTrack">')
track_end = html.index("</div>", track_start)
# Find the actual </div> that closes carousel-track (should be after all teacher cards)
# We need to find the </div> that's right before the next button
next_btn = html.index('carousel-next')
# Go backwards from next_btn to find the closing </div> of carousel-track
track_close = html.rindex("</div>", track_start, next_btn)

html = html[:track_start] + "\n" + all_cards + html[track_close:]

# Update slider controls - clear dots, JS will create them dynamically
ctrl_start = html.index("slider-controls")
ctrl_tag_end = html.index(">", ctrl_start) + 1
ctrl_end = html.index("</div>", ctrl_tag_end)
html = html[:ctrl_tag_end] + "\n" + html[ctrl_end:]

open(hp, "w", encoding="utf-8").write(html)
print("index.html: 8 teachers added, dots cleared")

# ===== 2. Update main.js carousel logic =====
mp = base + "\\js\\main.js"
js = open(mp, "r", encoding="utf-8").read()

# Replace carousel section with new version
new_carousel = """
    // --- Teacher carousel ---
    var track = document.getElementById('carouselTrack');
    if (track) {
      var cards = track.querySelectorAll('.teacher-card');
      var ctrl = document.querySelector('.slider-controls');
      var timer;
      var cardsPerPage = window.innerWidth >= 768 ? 3 : 1;
      var totalPages = Math.ceil(cards.length / cardsPerPage);
      var curPage = 0;

      function getPageWidth() {
        return cards[0].offsetWidth + 30;
      }

      function goToPage(p, anim) {
        curPage = Math.max(0, Math.min(p, totalPages - 1));
        track.scrollTo({ left: curPage * cardsPerPage * getPageWidth(), behavior: anim ? 'smooth' : 'instant' });
        // Update dots
        var ds = ctrl.querySelectorAll('.slider-dot');
        for (var d = 0; d < ds.length; d++) ds[d].classList.toggle('active', d === curPage);
      }

      function nextP() { goToPage(curPage + 1, true); }
      function prevP() { goToPage(curPage - 1, true); }
      function startT() { clearInterval(timer); timer = setInterval(nextP, 4000); }
      function stopT() { clearInterval(timer); }

      // Create dots dynamically
      ctrl.innerHTML = '';
      for (var d = 0; d < totalPages; d++) {
        var dot = document.createElement('button');
        dot.className = 'slider-dot' + (d === 0 ? ' active' : '');
        dot.onclick = function(i) { return function() { goToPage(i, true); startT(); }; }(d);
        ctrl.appendChild(dot);
      }

      // Event listeners
      var prev_btn = document.getElementById('carouselPrev');
      var next_btn = document.getElementById('carouselNext');
      if (prev_btn) prev_btn.onclick = function() { prevP(); startT(); };
      if (next_btn) next_btn.onclick = function() { nextP(); startT(); };
      track.onmouseenter = stopT;
      track.onmouseleave = startT;

      // Handle resize
      window.addEventListener('resize', function() {
        var newCpp = window.innerWidth >= 768 ? 3 : 1;
        if (newCpp !== cardsPerPage) {
          cardsPerPage = newCpp;
          totalPages = Math.ceil(cards.length / cardsPerPage);
          curPage = Math.min(curPage, totalPages - 1);
          // Recreate dots
          ctrl.innerHTML = '';
          for (var d2 = 0; d2 < totalPages; d2++) {
            var dot2 = document.createElement('button');
            dot2.className = 'slider-dot' + (d2 === curPage ? ' active' : '');
            dot2.onclick = function(j) { return function() { goToPage(j, true); startT(); }; }(d2);
            ctrl.appendChild(dot2);
          }
          goToPage(curPage, false);
        }
      });

      goToPage(0, false);
      startT();
    }
"""

# Find the existing carousel section and replace it
js_start = js.index("    // --- Teacher carousel ---")
# Find the end - look for the next top-level comment or the end of the DOMContentLoaded
# The carousel section ends before "console.log('CAAC site ready');"
# Find the line after the carousel code that starts with "    console.log"
console_line = js.index("\n    console.log('CAAC site ready')")
js = js[:js_start] + new_carousel + js[console_line:]

open(mp, "w", encoding="utf-8").write(js)
print("main.js: carousel logic rewritten")
print("Done!")
