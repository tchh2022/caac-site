import os, re
base = os.environ["USERPROFILE"] + "\\Documents\\CAAC考证报名网站"
p = base + "\\index.html"

d = open(p, "r", encoding="utf-8").read()
count_before = d.count("teacher-card")
print("Before:", count_before, "teacher cards")

# 1. Remove leftover </div> (8 spaces) before teacher 4
# The leftover is a </div> with 8 spaces indent followed by 12 spaces <div class="teacher-card">
d = re.sub(
    r'(\n            </div>\n)        </div>\n            <div class="teacher-card">\n                <div class="teacher-avatar" style="background-image:url\(images/teacher-liu.jpg\)">',
    r'\1            <div class="teacher-card">\n                <div class="teacher-avatar" style="background-image:url(images/teacher-liu.jpg)">',
    d, count=1
)
print("Fix 1 done - teacher cards:", d.count("teacher-card"))

# 2. Add teachers 5-8 after teacher 4's closing </div>
# Find: </div> (teacher 4 close) followed by </div> (track close) followed by button
# Insert teachers 5-8 between them
teachers_new = (
    '\n            <div class="teacher-card"><div class="teacher-avatar" style="background-image:url(images/teacher-chen.jpg)">\u9648</div><h4>\u9648\u96c5\u6587</h4><div class="title">\u6a21\u62df\u5668\u8bad\u7ec3\u6559\u5458</div><div class="desc">6\u5e74\u65e0\u4eba\u673a\u6559\u5b66\u7ecf\u9a8c<br>\u64c5\u957f\u6a21\u62df\u5668\u6559\u5b66\u4e0e\u8003\u6838<br>\u5f00\u53d1\u591a\u5957\u6a21\u62df\u8bad\u7ec3\u8bfe\u7a0b</div></div>\n' +
    '            <div class="teacher-card"><div class="teacher-avatar" style="background-image:url(images/teacher-zhao.jpg)">\u8d75</div><h4>\u8d75\u5929\u7ffc</h4><div class="title">\u56fa\u5b9a\u7ffc\u4e13\u9879\u6559\u5458</div><div class="desc">12\u5e74\u56fa\u5b9a\u7ffc\u98de\u884c\u7ecf\u9a8c<br>\u6301\u6709CAAC\u56fa\u5b9a\u7ffc\u6559\u5458\u6267\u7167<br>\u56fa\u5b9a\u7ffc\u98de\u884c\u6280\u672f\u4e00\u6d41</div></div>\n' +
    '            <div class="teacher-card"><div class="teacher-avatar" style="background-image:url(images/teacher-sun.jpg)">\u5b59</div><h4>\u5b59\u6d69\u7136</h4><div class="title">\u8003\u8bd5\u8f85\u5bfc\u4e13\u5458</div><div class="desc">\u6df1\u7814CAAC\u8003\u8bd5\u4f53\u7cfb<br>\u7406\u8bba\u8003\u8bd5\u8f85\u5bfc\u901a\u8fc7\u738799%<br>\u7cbe\u51c6\u628a\u63e1\u8003\u70b9\u96be\u70b9</div></div>\n' +
    '            <div class="teacher-card"><div class="teacher-avatar" style="background-image:url(images/teacher-zhou.jpg)">\u5468</div><h4>\u5468\u7acb\u65b0</h4><div class="title">\u884c\u4e1a\u5e94\u7528\u987e\u95ee</div><div class="desc">\u8d44\u6df1\u65e0\u4eba\u673a\u884c\u4e1a\u5e94\u7528\u4e13\u5bb6<br>\u53c2\u4e0e\u5236\u5b9a\u591a\u9879\u884c\u4e1a\u6807\u51c6<br>\u4e3a\u5b66\u5458\u63d0\u4f9b\u5c31\u4e1a\u6307\u5bfc</div></div>\n'
)

# Add teachers 5-8 before the TRACK closing </div> + button
d = re.sub(
    r'(\n            </div>\n        </div>\n        <button class="carousel-btn carousel-next" id="carouselNext">)',
    teachers_new + r'\1',
    d, count=1
)
print("Fix 2 done - teacher cards:", d.count("teacher-card"))

# 3. Clear slider-controls
d = re.sub(r'<div class="slider-controls">\s*<button.*?</div>', '<div class="slider-controls">\n        </div>', d, flags=re.DOTALL)
print("Fix 3 done")

with open(p, "w", encoding="utf-8") as f:
    f.write(d)
print("Final teacher cards:", d.count("teacher-card"))
