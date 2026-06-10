import os
base = os.environ["USERPROFILE"] + "\\Documents\\CAAC考证报名网站"
p = base + "\\index.html"
d = open(p, "r", encoding="utf-8").read()

# Remove single Chinese char inside teacher-avatar divs
import re
d = re.sub(r'(class="teacher-avatar"[^>]*>)[^<]+(</div>)', r'\1\2', d)

with open(p, "w", encoding="utf-8") as f:
    f.write(d)
print("Done - removed avatar text chars")
