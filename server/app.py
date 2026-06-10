#!/usr/bin/env python3
import http.server, json, os, sys, time, urllib.parse
from datetime import datetime
P=3001
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SD=os.path.dirname(os.path.abspath(__file__))
DBPATH=os.path.join(SD,"database","data.json")
MIME={".html":"text/html; charset=utf-8",".css":"text/css; charset=utf-8",".js":"application/javascript; charset=utf-8",".json":"application/json; charset=utf-8"}
def ld():
    try:
        with open(DBPATH,"r",encoding="utf-8") as f: return json.load(f)
    except:
        d={"registrations":[],"trials":[],"contacts":[],"courses":[]}
        os.makedirs(os.path.dirname(DBPATH),exist_ok=True)
        with open(DBPATH,"w",encoding="utf-8") as f: json.dump(d,f,ensure_ascii=False,indent=2)
        return d
def sv(d):
    with open(DBPATH,"w",encoding="utf-8") as f: json.dump(d,f,ensure_ascii=False,indent=2)
def tsx():
    return datetime.fromtimestamp(time.time()+8*3600).strftime("%Y-%m-%d %H:%M:%S")
def sj(h,s,d):
    h.send_response(s)
    h.send_header("Content-Type","application/json; charset=utf-8")
    h.send_header("Access-Control-Allow-Origin","*")
    h.send_header("Access-Control-Allow-Methods","GET, POST, PUT, DELETE, OPTIONS")
    h.send_header("Access-Control-Allow-Headers","Content-Type")
    h.end_headers()
    h.wfile.write(json.dumps(d,ensure_ascii=False).encode("utf-8"))
def ss(h,pa):
    if pa in ("/",""): fp=os.path.join(ROOT,"index.html")
    elif pa in ("/admin/","/admin"): fp=os.path.join(SD,"public","index.html")
    else:
        fp=os.path.normpath(os.path.join(ROOT,pa.lstrip("/")))
        if not fp.startswith(ROOT): return sj(h,403,{"error":"Forbidden"})
    if os.path.isfile(fp):
        ext=os.path.splitext(fp)[1].lower()
        ct=MIME.get(ext,"application/octet-stream")
        with open(fp,"rb") as f: data=f.read()
        h.send_response(200); h.send_header("Content-Type",ct); h.send_header("Content-Length",str(len(data))); h.send_header("Cache-Control","no-cache, no-store, must-revalidate"); h.end_headers(); h.wfile.write(data)
    else:
        hp=fp+".html"
        if os.path.isfile(hp):
            with open(hp,"rb") as f: data=f.read()
            h.send_response(200); h.send_header("Content-Type","text/html; charset=utf-8"); h.send_header("Content-Length",str(len(data))); h.end_headers(); h.wfile.write(data)
        else: sj(h,404,{"error":"Not Found"})
def rb(h):
    l=int(h.headers.get("Content-Length",0))
    if l==0: return {}
    try: return json.loads(h.rfile.read(l))
    except: return {}
class H(http.server.BaseHTTPRequestHandler):
    rt={"GET":[],"POST":[],"PUT":[],"DELETE":[]}
    @classmethod
    def ra(cls,m,p,h): cls.rt[m].append({"parts":p.strip("/").split("/"),"handler":h})
    def rs(self,m,pa):
        pp=pa.strip("/").split("/")
        for r in self.rt.get(m,[]):
            if len(r["parts"])!=len(pp): continue
            p={}; ok=True
            for a,b in zip(pp,r["parts"]):
                if b.startswith(":"): p[b[1:]]=a
                elif a!=b: ok=False; break
            if ok: return r["handler"],p
        return None,None
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.end_headers()
    def do_GET(self):
        pa=urllib.parse.urlparse(self.path)
        if pa.path.startswith("/api/"):
            h,p=self.rs("GET",pa.path)
            if h: h(self,{},p or {})
            else: sj(self,404,{"success":False,"message":"not found"})
        else: ss(self,pa.path)
    def do_POST(self):
        b=rb(self); h,p=self.rs("POST",self.path)
        if h: h(self,b,p or {})
        else: sj(self,404,{"success":False,"message":"not found"})
    def do_PUT(self):
        b=rb(self); h,p=self.rs("PUT",self.path)
        if h: h(self,b,p or {})
        else: sj(self,404,{"success":False,"message":"not found"})
    def do_DELETE(self):
        h,p=self.rs("DELETE",self.path)
        if h: h(self,{},p or {})
        else: sj(self,404,{"success":False,"message":"not found"})
# API Handlers
def h_reg(h,b,p):
    n=b.get("name",""); ph=b.get("phone",""); co=b.get("course","")
    if not n or not ph or not co: return sj(h,400,{"success":False,"message":"required"})
    d=ld(); d["registrations"].insert(0,{"id":len(d["registrations"])+1,"name":n,"phone":ph,"course":co,"status":"pending","created_at":tsx()}); sv(d)
    sj(h,200,{"success":True,"message":"ok"})
def l_reg(h,b,p): d=ld(); sj(h,200,d["registrations"])
def u_reg(h,b,p):
    d=ld()
    for r in d["registrations"]:
        if str(r["id"])==p.get("id"): r["status"]=b.get("status","contacted"); break
    sv(d); sj(h,200,{"success":True})
def h_tri(h,b,p):
    n=b.get("name",""); ph=b.get("phone","")
    if not n or not ph: return sj(h,400,{"success":False,"message":"required"})
    d=ld(); d["trials"].insert(0,{"id":len(d["trials"])+1,"name":n,"phone":ph,"date":b.get("date",""),"time":b.get("time",""),"status":"pending","created_at":tsx()}); sv(d)
    sj(h,200,{"success":True,"message":"ok"})
def l_tri(h,b,p): d=ld(); sj(h,200,d["trials"])
def h_con(h,b,p):
    n=b.get("name",""); co=b.get("contact",""); m=b.get("message","")
    if not n or not co or not m: return sj(h,400,{"success":False,"message":"required"})
    d=ld(); d["contacts"].insert(0,{"id":len(d["contacts"])+1,"name":n,"contact":co,"message":m,"status":"unread","created_at":tsx()}); sv(d)
    sj(h,200,{"success":True,"message":"ok"})
def l_con(h,b,p): d=ld(); sj(h,200,d["contacts"])
def m_con(h,b,p):
    d=ld()
    for c in d["contacts"]:
        if str(c["id"])==p.get("id"): c["status"]="read"; break
    sv(d); sj(h,200,{"success":True})
def a_sta(h,b,p):
    d=ld()
    sj(h,200,{"registrations":len(d["registrations"]),"pendingRegistrations":sum(1 for r in d["registrations"] if r.get("status")=="pending"),"trials":len(d["trials"]),"unreadMessages":sum(1 for c in d["contacts"] if c.get("status")=="unread"),"recentRegistrations":d["registrations"][:5],"recentTrials":d["trials"][:5],"recentMessages":d["contacts"][:5]})
def d_reg(h,b,p): d=ld(); d["registrations"]=[r for r in d["registrations"] if str(r.get("id"))!=p.get("id")]; sv(d); sj(h,200,{"success":True})
def d_tri(h,b,p): d=ld(); d["trials"]=[r for r in d["trials"] if str(r.get("id"))!=p.get("id")]; sv(d); sj(h,200,{"success":True})
def d_con(h,b,p): d=ld(); d["contacts"]=[c for c in d["contacts"] if str(c.get("id"))!=p.get("id")]; sv(d); sj(h,200,{"success":True})
# Routes
H.ra("POST","/api/register",h_reg); H.ra("GET","/api/register",l_reg); H.ra("PUT","/api/register/:id",u_reg)
H.ra("POST","/api/trial",h_tri); H.ra("GET","/api/trial",l_tri)
H.ra("POST","/api/contact",h_con); H.ra("GET","/api/contact",l_con); H.ra("PUT","/api/contact/:id",m_con)
H.ra("GET","/api/admin/stats",a_sta)
H.ra("DELETE","/api/admin/registrations/:id",d_reg)
H.ra("DELETE","/api/admin/trials/:id",d_tri)
H.ra("DELETE","/api/admin/contacts/:id",d_con)

if __name__=="__main__":
    s=http.server.HTTPServer(("0.0.0.0",P),H)
    print("CAAC Server at http://localhost:"+str(P))
    print("Admin: http://localhost:"+str(P)+"/admin/")
    print("Static: http://localhost:"+str(P)+"/")
    s.serve_forever()
