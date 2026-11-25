#!/usr/bin/env python3
"""Generate the blog sitemap and IndexNow payload from canonical, indexable HTML."""
from __future__ import annotations
import argparse
import json
import re
import subprocess
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HOST = "blog.pangolinfo.com"
BASE = f"https://{HOST}"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
XHTML_NS = "http://www.w3.org/1999/xhtml"
ET.register_namespace("", SITEMAP_NS)
ET.register_namespace("xhtml", XHTML_NS)

class HeadParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.canonical = None; self.noindex = False
    def handle_starttag(self, tag, attrs):
        if tag.lower() != "meta" and tag.lower() != "link": return
        a = {k.lower(): (v or "") for k,v in attrs}
        if tag.lower()=="link" and "canonical" in a.get("rel", "").lower().split():
            self.canonical = a.get("href")
        if tag.lower()=="meta" and a.get("name", "").lower() in ("robots", "googlebot", "bingbot"):
            if re.search(r"\bnoindex\b", a.get("content", ""), re.I): self.noindex = True

def candidates():
    files = [ROOT / "index.html", ROOT / "blog.html", ROOT / "zh/index.html", ROOT / "zh/blog.html"]
    for sub in (ROOT / "articles", ROOT / "zh/articles"):
        if sub.exists(): files.extend(sorted(sub.rglob("*.html")))
    out = {}
    for p in files:
        if not p.is_file() or p.name.lower().endswith((".bak", ".backup")): continue
        rel = p.relative_to(ROOT).as_posix()
        parser=HeadParser(); parser.feed(p.read_text(encoding="utf-8", errors="replace"))
        if parser.noindex: continue
        if parser.canonical:
            u=urlparse(parser.canonical)
            if u.scheme not in ("http", "https") or u.netloc.lower()!=HOST: continue
            url=parser.canonical.rstrip("#")
        else:
            path=rel[:-10] if rel.endswith("/index.html") else rel
            url=BASE + ("/" if path in ("", "index.html") else "/"+path)
        if url.endswith("/index.html"): url=url[:-10]
        url=url.replace("http://", "https://", 1)
        lastmod = subprocess.run(["git","log","-1","--format=%cs","--",rel],cwd=ROOT,text=True,capture_output=True).stdout.strip()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", lastmod): lastmod=date.today().isoformat()
        out[url]={"path":rel,"lastmod":lastmod}
    return dict(sorted(out.items()))

def equivalents(urls):
    bypath={v["path"]:u for u,v in urls.items()}
    groups={}
    for p,u in bypath.items():
        if p=="index.html": key="home"
        elif p=="zh/index.html": key="home"
        elif p=="blog.html": key="archive"
        elif p=="zh/blog.html": key="archive"
        elif p.startswith("articles/"): key="article/"+p.split("/",1)[1]
        elif p.startswith("zh/articles/"): key="article/"+p.split("/",2)[2]
        else: continue
        groups.setdefault(key,{})["zh" if p.startswith("zh/") else "en"]=u
    result={}
    for variants in groups.values():
        if "en" in variants and "zh" in variants:
            result[variants["en"]]={"en":variants["en"],"zh-CN":variants["zh"],"x-default":variants["en"]}
            result[variants["zh"]]={"en":variants["en"],"zh-CN":variants["zh"],"x-default":variants["en"]}
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--changed-files", type=Path)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--changed-url-file", type=Path, default=ROOT/"changed-urls.txt")
    args=ap.parse_args()
    urls=candidates()
    if not urls: raise SystemExit("No indexable pages found")
    alt=equivalents(urls)
    root=ET.Element(f"{{{SITEMAP_NS}}}urlset")
    for loc,meta in urls.items():
        entry=ET.SubElement(root,f"{{{SITEMAP_NS}}}url")
        ET.SubElement(entry,f"{{{SITEMAP_NS}}}loc").text=loc
        ET.SubElement(entry,f"{{{SITEMAP_NS}}}lastmod").text=meta["lastmod"]
        for lang,href in alt.get(loc,{}).items():
            ET.SubElement(entry,f"{{{XHTML_NS}}}link",{"rel":"alternate","hreflang":lang,"href":href})
    ET.indent(root, space="  ")
    (ROOT/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(root,encoding="unicode")+'\n',encoding="utf-8")
    keyfile=next((p for p in ROOT.glob("*.txt") if re.fullmatch(r"[a-f0-9]{32}\.txt",p.name)),None)
    if not keyfile: raise SystemExit("IndexNow key file missing")
    key=keyfile.stem
    if keyfile.read_text(encoding="utf-8").strip()!=key: raise SystemExit("IndexNow key file content does not match filename")
    (ROOT/"indexnow.json").write_text(json.dumps({"host":HOST,"key":key,"keyLocation":f"{BASE}/{key}.txt","urlList":list(urls)},indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    changed=[]
    if args.all or not args.changed_files:
        changed=list(urls)
    else:
        lines=args.changed_files.read_text(encoding="utf-8").splitlines()
        for rel in lines:
            rel=rel.strip().replace("\\","/")
            for url,meta in urls.items():
                if meta["path"]==rel: changed.append(url)
    changed=sorted(set(changed))
    args.changed_url_file.write_text("".join(u+"\n" for u in changed),encoding="utf-8")
    print(json.dumps({"sitemap_count":len(urls),"changed_url_count":len(changed),"changed_urls":changed},ensure_ascii=False))
if __name__=="__main__": main()
