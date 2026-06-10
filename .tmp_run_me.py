import os, re
base = os.environ["USERPROFILE"] + "\\Documents\\CAAC考证报名网站"
p = base + "\\index.html"

print("Reading", p)
d = open(p, "r", encoding="utf-8").read()

# 1. Remove leftover </div> between teacher 3 and teacher 4
old = ('            </div>\n' +
       '        </div>\n' +
       '            <div class="teacher-card">\n' +
       '                <div class="teacher-avatar" style="background-image:url(images/teacher-liu.jpg)">')
new = ('            </div>\n' +
       '            <div class="teacher-card">\n' +
       '                <div class="teacher-avatar" style="background-image:url(images/teacher-liu.jpg)">')
d = d.replace(old, new)
print("Fix 1 applied: removing leftover </div>")

# 2. Teachers 5-8 data
t5 = ('\n            <div class="teacher-card"><div class="teacher-avatar" style="background-image:url(images/teacher-chen.jpg)">\u9648</div><h4>\u9648\u96c5\u6587</h4><div class="title">\u6a21\u62df\u5668\u8bad\u7ec3\u6559\u5458</div><div class="desc">6\u5e74\u65e0\u4eba\u673a\u6559\u5b66\u7ecf\u9a8c<br>\u64c5\u957f\u6a21\u62df\u5668\u6559\u5b66\u4e0e\u8003\u6838<br>\u5f00\u53d1\u591a\u5957\u6a21\u62df\u8bad\u7ec3\u8bfe\u7a0b</div></div>\n' +
      '            <div class="teacher-card"><div class="teacher-avatar" style="background-image:url(images/teacher-zhao.jpg)">\u8d75</div><h4>\u8d75\u5929\u7ffc</h4><div class="title">\u56fa\u5b9a\u7ffc\u4e13\u9879\u6559\u5458</div><div class="desc">12\u5e74\u56fa\u5b9a\u7ffc\u98de\u884c\u7ecf\u9a8c<br>\u6301\u6709CAAC\u56fa\u5b9a\u7ffc\u6559\u5458\u6267\u7167<br>\u56fa\u5b9a\u7ffc\u98de\u884c\u6280\u672f\u4e00\u6d41</div></div>\n' +
      '            <div class="teacher-card"><div class="teacher-avatar" style="background-image:url(images/teacher-sun.jpg)">\u5b59</div><h4>\u5b59\u6d69\u7136</h4><div class="title">\u8003\u8bd5\u8f85\u5bfc\u4e13\u5458</div><div class="desc">\u6df1\u7814CAAC\u8003\u8bd5\u4f53\u7cfb<br>\u7406\u8bba\u8003\u8bd5\u8f85\u5bfc\u901a\u8fc7\u738799%<br>\u7cbe\u51c6\u628a\u63e1\u8003\u70b9\u96be\u70b9</div></div>\n' +
      '            <div class="teacher-card"><div class="teacher-avatar" style="background-image:url(images/teacher-zhou.jpg)">\u5468</div><h4>\u5468\u7acb\u65b0</h4><div class="title">\u884c\u4e1a\u5e94\u7528\u987e\u95ee</div><div class="desc">\u8d44\u6df1\u65e0\u4eba\u673a\u884c\u4e1a\u5e94\u7528\u4e13\u5bb6<br>\u53c2\u4e0e\u5236\u5b9a\u591a\u9879\u884c\u4e1a\u6807\u51c6<br>\u4e3a\u5b66\u5458\u63d0\u4f9b\u5c31\u4e1a\u6307\u5bfc</div></div>\n')
d = d.replace("\u5218\u9e4f\u98de</div>", "\u5218\u9e4f\u98de</div>" + t5, 1)
print("Fix 2 applied: teachers 5-8 added")

# 3. Clear slider-controls
d = re.sub(r'<div class="slider-controls">\s*<button.*?</div>', '<div class="slider-controls">\n        </div>', d, flags=re.DOTALL)
print("Fix 3 applied: slider-controls cleared")

# Write
with open(p, "w", encoding="utf-8") as f:
    f.write(d)
print("Written OK - teacher cards:", d.count("teacher-card"))
print("All fixes applied! Refresh index.html with Ctrl+F5")
