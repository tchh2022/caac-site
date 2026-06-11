import os, re
base = os.environ["USERPROFILE"] + "\\Documents\\CAAC考证报名网站"

# SEO data for each page
pages = {
    "index.html": {
        "title": "CAAC\u65e0\u4eba\u673a\u57f9\u8bad\u8003\u8bc1\u62a5\u540d\u7f51\u7ad9 - \u6c11\u7528\u822a\u7a7a\u5c40\u8ba4\u8bc1",
        "desc": "CAAC\u65e0\u4eba\u673a\u57f9\u8bad\u4e2d\u5fc3\uff0c\u63d0\u4f9b\u591a\u65cb\u7ffc\u3001\u56fa\u5b9a\u7ffc\u3001VTOL\u65e0\u4eba\u673a\u9a7e\u9a76\u5458\u6267\u7167\u57f9\u8bad\uff0c\u901a\u8fc7\u738795%+\uff0c\u5317\u4eac\u5b9e\u5730\u57f9\u8bad\u3002",
        "keywords": "CAAC\u65e0\u4eba\u673a\u57f9\u8bad,CAAC\u65e0\u4eba\u673a\u8003\u8bc1,\u65e0\u4eba\u673a\u6267\u7167,\u6c11\u7528\u822a\u7a7a\u5c40\u8ba4\u8bc1,\u5317\u4eac\u65e0\u4eba\u673a\u57f9\u8bad",
        "canonical": "https://caacflying.com/"
    },
    "pages/courses.html": {
        "title": "\u8bfe\u7a0b\u4e2d\u5fc3 - CAAC\u65e0\u4eba\u673a\u57f9\u8bad\u8003\u8bc1",
        "desc": "CAAC\u65e0\u4eba\u673a\u9a7e\u9a76\u5458\u57f9\u8bad\u8bfe\u7a0b\uff0c\u6db5\u76d6\u591a\u65cb\u7ffc\u3001\u56fa\u5b9a\u7ffc\u3001\u5782\u76f4\u8d77\u964d\u56fa\u5b9a\u7ffc\u4e09\u5927\u673a\u578b\uff0c\u89c6\u8ddd\u5185\u3001\u8d85\u89c6\u8ddd\u3001\u6559\u5458\u4e09\u4e2a\u7ea7\u522b\u3002",
        "keywords": "CAAC\u65e0\u4eba\u673a\u8bfe\u7a0b,\u65e0\u4eba\u673a\u57f9\u8bad\u8bfe\u7a0b,\u591a\u65cb\u7ffc\u57f9\u8bad,\u56fa\u5b9a\u7ffc\u57f9\u8bad,\u65e0\u4eba\u673a\u6559\u5458\u57f9\u8bad",
        "canonical": "https://caacflying.com/pages/courses.html"
    },
    "pages/about.html": {
        "title": "\u5173\u4e8e\u6211\u4eec - CAAC\u65e0\u4eba\u673a\u57f9\u8bad\u4e2d\u5fc3",
        "desc": "CAAC\u65e0\u4eba\u673a\u57f9\u8bad\u4e2d\u5fc3\uff0c\u6c11\u7528\u822a\u7a7a\u5c40\u8ba4\u8bc1\u57f9\u8bad\u673a\u6784\uff0c6\u5e74\u57f9\u8bad\u7ecf\u9a8c\uff0c\u7d2f\u8ba1\u57f9\u8bad\u5b66\u54583800+\u4eba\uff0c\u4e3a\u884c\u4e1a\u8f93\u9001\u5927\u6279\u65e0\u4eba\u673a\u4e13\u4e1a\u4eba\u624d\u3002",
        "keywords": "\u5173\u4e8eCAAC\u57f9\u8bad,\u65e0\u4eba\u673a\u57f9\u8bad\u673a\u6784,\u6c11\u822a\u5c40\u57f9\u8bad,\u5317\u4eac\u65e0\u4eba\u673a\u57f9\u8bad\u4e2d\u5fc3",
        "canonical": "https://caacflying.com/pages/about.html"
    },
    "pages/teachers.html": {
        "title": "\u5e08\u8d44\u529b\u91cf - CAAC\u65e0\u4eba\u673a\u57f9\u8bad",
        "desc": "CAAC\u65e0\u4eba\u673a\u57f9\u8bad\u4e2d\u5fc3\u62e5\u6709\u8d44\u6df1\u6559\u5458\u56e2\u961f\uff0c\u5747\u6301\u6709CAAC\u65e0\u4eba\u673a\u6559\u5458\u6267\u7167\uff0c\u5e73\u5747\u884c\u4e1a\u7ecf\u9a8c8\u5e74+\uff0c\u4e3a\u5b66\u5458\u63d0\u4f9b\u4e13\u4e1a\u65e0\u4eba\u673a\u57f9\u8bad\u3002",
        "keywords": "CAAC\u6559\u5458,\u65e0\u4eba\u673a\u6559\u5458,\u65e0\u4eba\u673a\u57f9\u8bad\u5e08\u8d44,\u65e0\u4eba\u673a\u6559\u5b66",
        "canonical": "https://caacflying.com/pages/teachers.html"
    },
    "pages/cases.html": {
        "title": "\u5b66\u5458\u6848\u4f8b - CAAC\u65e0\u4eba\u673a\u57f9\u8bad",
        "desc": "\u770b\u770b\u5386\u5c4a\u5b66\u5458\u5982\u4f55\u901a\u8fc7CAAC\u65e0\u4eba\u673a\u57f9\u8bad\u5b9e\u73b0\u804c\u4e1a\u8f6c\u578b\uff0c\u4ece\u96f6\u57fa\u7840\u5230\u6301\u8bc1\u98de\u884c\uff0c\u4ed6\u4eec\u7684\u6210\u529f\u6545\u4e8b\u53ef\u4ee5\u590d\u5236\u3002",
        "keywords": "CAAC\u5b66\u5458\u6848\u4f8b,\u65e0\u4eba\u673a\u8003\u8bc1\u6848\u4f8b,\u65e0\u4eba\u673a\u804c\u4e1a\u8f6c\u578b",
        "canonical": "https://caacflying.com/pages/cases.html"
    },
    "pages/news.html": {
        "title": "\u65b0\u95fb\u8d44\u8baf - CAAC\u65e0\u4eba\u673a\u57f9\u8bad",
        "desc": "CAAC\u65e0\u4eba\u673a\u57f9\u8bad\u4e2d\u5fc3\u6700\u65b0\u52a8\u6001\u3001\u884c\u4e1a\u65b0\u95fb\u3001\u65e0\u4eba\u673a\u6cd5\u89c4\u66f4\u65b0\uff0c\u5e2e\u52a9\u60a8\u53ca\u65f6\u4e86\u89e3\u65e0\u4eba\u673a\u884c\u4e1a\u524d\u6cbf\u8d44\u8baf\u3002",
        "keywords": "\u65e0\u4eba\u673a\u65b0\u95fb,CAAC\u52a8\u6001,\u65e0\u4eba\u673a\u884c\u4e1a\u8d44\u8baf",
        "canonical": "https://caacflying.com/pages/news.html"
    },
    "pages/contact.html": {
        "title": "\u8054\u7cfb\u6211\u4eec - CAAC\u65e0\u4eba\u673a\u57f9\u8bad\u4e2d\u5fc3",
        "desc": "\u8054\u7cfbCAAC\u65e0\u4eba\u673a\u57f9\u8bad\u4e2d\u5fc3\uff0c\u54a8\u8be2\u65e0\u4eba\u673a\u9a7e\u9a76\u5458\u6267\u7167\u57f9\u8bad\u8bfe\u7a0b\uff0c\u83b7\u53d6\u514d\u8d39\u4f53\u9a8c\u8bfe\u673a\u4f1a\u3002",
        "keywords": "\u8054\u7cfbCAAC\u57f9\u8bad,\u65e0\u4eba\u673a\u57f9\u8bad\u54a8\u8be2,\u5317\u4eac\u65e0\u4eba\u673a\u57f9\u8bad\u8054\u7cfb",
        "canonical": "https://caacflying.com/pages/contact.html"
    },
    "pages/register.html": {
        "title": "\u5728\u7ebf\u62a5\u540d - CAAC\u65e0\u4eba\u673a\u57f9\u8bad\u8003\u8bc1",
        "desc": "\u7acb\u5373\u62a5\u540dCAAC\u65e0\u4eba\u673a\u9a7e\u9a76\u5458\u57f9\u8bad\uff0c\u5728\u7ebf\u7533\u8bf7\u65e0\u4eba\u673a\u6267\u7167\u57f9\u8bad\u8bfe\u7a0b\uff0c\u6211\u4eec\u5c06\u572824\u5c0f\u65f6\u5185\u4e0e\u60a8\u8054\u7cfb\u3002",
        "keywords": "CAAC\u62a5\u540d,\u65e0\u4eba\u673a\u57f9\u8bad\u62a5\u540d,\u65e0\u4eba\u673a\u8003\u8bc1\u62a5\u540d,\u5728\u7ebf\u62a5\u540d",
        "canonical": "https://caacflying.com/pages/register.html"
    },
    "pages/trial.html": {
        "title": "\u514d\u8d39\u4f53\u9a8c\u8bfe - CAAC\u65e0\u4eba\u673a\u57f9\u8bad",
        "desc": "\u9884\u7ea6CAAC\u65e0\u4eba\u673a\u514d\u8d39\u4f53\u9a8c\u8bfe\uff0c\u4eb2\u8eab\u611f\u53d7\u98de\u884c\u4e50\u8da3\uff0c\u4e86\u89e3\u65e0\u4eba\u673a\u884c\u4e1a\u524d\u666f\uff0c\u4e13\u4e1a\u6559\u7ec3\u6307\u5bfc\u3002",
        "keywords": "\u65e0\u4eba\u673a\u514d\u8d39\u4f53\u9a8c,\u65e0\u4eba\u673a\u8bd5\u98de,\u514d\u8d39\u65e0\u4eba\u673a\u57f9\u8bad\u4f53\u9a8c",
        "canonical": "https://caacflying.com/pages/trial.html"
    },
    "pages/course-detail.html": {
        "title": "\u8bfe\u7a0b\u8be6\u60c5 - CAAC\u65e0\u4eba\u673a\u57f9\u8bad",
        "desc": "CAAC\u65e0\u4eba\u673a\u8d85\u89c6\u8ddd\u9a7e\u9a76\u5458\u57f9\u8bad\u8bfe\u7a0b\u8be6\u60c5\uff0c\u5305\u542b\u57f9\u8bad\u5185\u5bb9\u3001\u62a5\u540d\u6761\u4ef6\u3001\u8003\u6838\u65b9\u5f0f\u3001\u5c31\u4e1a\u65b9\u5411\u7b49\u5168\u9762\u4ecb\u7ecd\u3002",
        "keywords": "CAAC\u8bfe\u7a0b\u8be6\u60c5,\u65e0\u4eba\u673a\u57f9\u8bad\u5185\u5bb9,\u65e0\u4eba\u673a\u8003\u6838",
        "canonical": "https://caacflying.com/pages/course-detail.html"
    }
}

# JSON-LD for homepage
jsonld = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "EducationalOrganization",
  "name": "CAAC\u65e0\u4eba\u673a\u57f9\u8bad\u4e2d\u5fc3",
  "description": "CAAC\u6c11\u7528\u822a\u7a7a\u5c40\u8ba4\u8bc1\u65e0\u4eba\u673a\u9a7e\u9a76\u5458\u57f9\u8bad\u673a\u6784\uff0c\u63d0\u4f9b\u591a\u65cb\u7ffc\u3001\u56fa\u5b9a\u7ffc\u3001VTOL\u65e0\u4eba\u673a\u6267\u7167\u57f9\u8bad\u3002",
  "url": "https://caacflying.com",
  "telephone": "138-0000-8888",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "\u5317\u4eac\u5e02\u660c\u5e73\u533a",
    "streetAddress": "\u79d1\u6280\u56ed\u533a\u521b\u65b0\u8def88\u53f7"
  },
  "areaServed": "\u4e2d\u56fd",
  "course": [
    {"@type": "Course", "name": "\u591a\u65cb\u7ffc\u89c6\u8ddd\u5185\u9a7e\u9a76\u5458\u57f9\u8bad"},
    {"@type": "Course", "name": "\u591a\u65cb\u7ffc\u8d85\u89c6\u8ddd\u9a7e\u9a76\u5458\u57f9\u8bad"},
    {"@type": "Course", "name": "\u56fa\u5b9a\u7ffc\u8d85\u89c6\u8ddd\u9a7e\u9a76\u5458\u57f9\u8bad"}
  ]
}
</script>"""

# OG tags template
def make_meta(title, desc, canonical):
    return f'''    <meta name="description" content="{desc}">
    <meta name="keywords" content="{pages[list(pages.keys())[0]]['keywords'] if 'index' in canonical else 'CAAC\u65e0\u4eba\u673a\u57f9\u8bad'}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="CAAC\u65e0\u4eba\u673a\u57f9\u8bad\u4e2d\u5fc3">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="canonical" href="{canonical}">'''

# Process each page
for filepath, seo in pages.items():
    p = os.path.join(base, filepath)
    if not os.path.exists(p):
        print(f"Skipping {filepath}: not found")
        continue
    
    d = open(p, "r", encoding="utf-8").read()
    title = seo["title"]
    desc = seo["desc"]
    keywords = seo["keywords"]
    canonical = seo["canonical"]
    
    # Update title tag
    d = re.sub(r'<title>[^<]*</title>', f'<title>{title}</title>', d)
    
    # Replace existing meta description, or add after charset
    if f'<meta name="description"' in d:
        d = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{desc}">', d)
    else:
        d = d.replace('<meta charset="UTF-8">', f'<meta charset="UTF-8">\n    <meta name="description" content="{desc}">')
    
    # Add OG tags and canonical before </head>
    og_tags = f'''    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="CAAC\u65e0\u4eba\u673a\u57f9\u8bad\u4e2d\u5fc3">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="canonical" href="{canonical}">'''
    
    if '<meta property="og:title"' not in d:
        d = d.replace('</head>', f'    {og_tags}\n</head>')
    
    # Add JSON-LD to homepage only
    if filepath == "index.html" and '<script type="application/ld+json">' not in d:
        d = d.replace('</head>', f'    {jsonld}\n</head>')
    
    # Add html lang if missing
    if 'lang="' not in d[:200]:
        d = d.replace('<html>', '<html lang="zh-CN">')
        d = d.replace('<html ', '<html lang="zh-CN" ')
    
    open(p, "w", encoding="utf-8").write(d)
    print(f"OK: {filepath}")

print("\nSEO update complete!")
