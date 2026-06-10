import os, re
base = os.environ["USERPROFILE"] + "\\Documents\\CAAC考证报名网站"
p = base + "\\index.html"
d = open(p, "r", encoding="utf-8").read()

# Build 8 teacher cards (one-liner each to avoid nesting issues)
cards_html = ""
teachers = [
    ("teacher-wang.jpg", "\u738b", "\u738b\u5efa\u56fd", "\u9996\u5e2d\u6559\u5458 / \u6c11\u822a\u5c40\u59d4\u4efb\u4ee3\u8868",
     "15\u5e74\u822a\u7a7a\u4ece\u4e1a\u7ecf\u9a8c<br>\u6301\u6709CAAC\u591a\u65cb\u7ffc+\u56fa\u5b9a\u7ffc\u6559\u5458\u6267\u7167<br>\u7d2f\u8ba1\u57f9\u8bad\u5b66\u5458800+\u4eba"),
    ("teacher-li.jpg", "\u674e", "\u674e\u660e\u8fbe", "\u9ad8\u7ea7\u6559\u5458 / \u65e0\u4eba\u673a\u7cfb\u7edf\u5de5\u7a0b\u5e08",
     "10\u5e74\u65e0\u4eba\u673a\u884c\u4e1a\u7ecf\u9a8c<br>\u7cbe\u901a\u98de\u63a7\u7cfb\u7edf\u8c03\u8bd5\u4e0e\u6545\u969c\u6392\u67e5<br>\u591a\u6b21\u53c2\u4e0e\u56fd\u5bb6\u7ea7\u65e0\u4eba\u673a\u9879\u76ee"),
    ("teacher-zhang.jpg", "\u5f20", "\u5f20\u96ea\u5cf0", "\u7406\u8bba\u6559\u5b66\u8d1f\u8d23\u4eba",
     "\u822a\u7a7a\u9662\u6821\u5ba2\u5ea7\u6559\u6388<br>\u6c11\u822a\u6cd5\u89c4\u4e0e\u6c14\u8c61\u5b66\u4e13\u5bb6<br>\u7f16\u8457\u591a\u672c\u65e0\u4eba\u673a\u57f9\u8bad\u6559\u6750"),
    ("teacher-liu.jpg", "\u5218", "\u5218\u9e4f\u98de", "\u9ad8\u7ea7\u5b9e\u64cd\u6559\u5458",
     "8\u5e74\u65e0\u4eba\u673a\u5b9e\u64cd\u98de\u884c\u7ecf\u9a8c<br>\u5404\u7c7b\u673a\u578b\u7d2f\u8ba1\u98de\u884c5000+\u5c0f\u65f6<br>\u64c5\u957f\u7279\u60c5\u5904\u7f6e\u4e0e\u98de\u884c\u6280\u5de7"),
    ("teacher-chen.jpg", "\u9648", "\u9648\u96c5\u6587", "\u6a21\u62df\u5668\u8bad\u7ec3\u6559\u5458",
     "6\u5e74\u65e0\u4eba\u673a\u6559\u5b66\u7ecf\u9a8c<br>\u64c5\u957f\u6a21\u62df\u5668\u6559\u5b66\u4e0e\u8003\u6838<br>\u5f00\u53d1\u591a\u5957\u6a21\u62df\u8bad\u7ec3\u8bfe\u7a0b"),
    ("teacher-zhao.jpg", "\u8d75", "\u8d75\u5929\u7ffc", "\u56fa\u5b9a\u7ffc\u4e13\u9879\u6559\u5458",
     "12\u5e74\u56fa\u5b9a\u7ffc\u98de\u884c\u7ecf\u9a8c<br>\u6301\u6709CAAC\u56fa\u5b9a\u7ffc\u6559\u5458\u6267\u7167<br>\u56fa\u5b9a\u7ffc\u98de\u884c\u6280\u672f\u4e00\u6d41"),
    ("teacher-sun.jpg", "\u5b59", "\u5b59\u6d69\u7136", "\u8003\u8bd5\u8f85\u5bfc\u4e13\u5458",
     "\u6df1\u7814CAAC\u8003\u8bd5\u4f53\u7cfb<br>\u7406\u8bba\u8003\u8bd5\u8f85\u5bfc\u901a\u8fc7\u738799%<br>\u7cbe\u51c6\u628a\u63e1\u8003\u70b9\u96be\u70b9"),
    ("teacher-zhou.jpg", "\u5468", "\u5468\u7acb\u65b0", "\u884c\u4e1a\u5e94\u7528\u987e\u95ee",
     "\u8d44\u6df1\u65e0\u4eba\u673a\u884c\u4e1a\u5e94\u7528\u4e13\u5bb6<br>\u53c2\u4e0e\u5236\u5b9a\u591a\u9879\u884c\u4e1a\u6807\u51c6<br>\u4e3a\u5b66\u5458\u63d0\u4f9b\u5c31\u4e1a\u6307\u5bfc"),
]
for t in teachers:
    cards_html += '            <div class="teacher-card"><div class="teacher-avatar" style="background-image:url(images/%s)">%s</div><h4>%s</h4><div class="title">%s</div><div class="desc">%s</div></div>\n' % t

# New section HTML
new_section = """        <div class="teacher-slider" id="teacherSlider">
            <button class="carousel-btn carousel-prev" id="carouselPrev">&#10094;</button>
            <div class="carousel-track" id="carouselTrack">
""" + cards_html + """            </div>
            <button class="carousel-btn carousel-next" id="carouselNext">&#10095;</button>
        </div>
        <div class="slider-controls">
        </div>"""

# Find and replace the teacher section
# Match from <section class="teachers"> to next section start
start = d.index('<section class="teachers">')
# Find the NEXT section start after the teachers section
# The next section is "开课通知" or classes
next_section = d.index('<section class="classes">', start)
# The section text to replace
old_section_text = d[start:next_section]

# Build replacement
replace_with = """<section class="teachers">
    <div class="container">
        <h2 class="section-title">\u5e08\u8d44\u529b\u91cf</h2>
        <p class="section-subtitle">\u884c\u4e1a\u8d44\u6df1\u6559\u7ec3\u56e2\u961f\uff0c\u7406\u8bba\u4e0e\u5b9e\u64cd\u7ecf\u9a8c\u4e30\u5bcc</p>
""" + new_section + """
    </div>
</section>
"""

d = d[:start] + replace_with + d[next_section:]

with open(p, "w", encoding="utf-8") as f:
    f.write(d)
print("Done! Teacher cards:", d.count("teacher-card"))
