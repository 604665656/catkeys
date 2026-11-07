#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 TOY 上架包：把内嵌 base64 图片外置到 dist/assets/，使 index.html 解压后 ≤ 1MB。"""
import io, os, re, base64, sys

SRC = r"C:/Users/60466/WorkBuddy/2026-11-07-09-39-46/catkeys/index.html"
DIST = r"C:/Users/60466/WorkBuddy/2026-11-07-09-39-46/ckeys_dist"

with io.open(SRC, "r", encoding="utf-8") as f:
    t = f.read()

os.makedirs(os.path.join(DIST, "assets"), exist_ok=True)
counter = {"n": 0}
missing = []

def repl(m):
    quote, ext, b64 = m.group(1), m.group(2), m.group(3)
    i = counter["n"]; counter["n"] += 1
    ext2 = "jpg" if ext == "jpeg" else ext
    fname = "assets/img%d.%s" % (i, ext2)
    try:
        data = base64.b64decode(b64)
        with io.open(os.path.join(DIST, fname), "wb") as fp:
            fp.write(data)
    except Exception as e:
        missing.append((fname, str(e)))
    return quote + ("assets/img%d.%s" % (i, ext2)) + quote

# 仅替换被引号包裹的 data URI（保留引号），避免误伤 CSS 内联
t2 = re.sub(r'(["\'])data:image/([a-zA-Z0-9]+);base64,([A-Za-z0-9+/=]+)\1', repl, t)

with io.open(os.path.join(DIST, "index.html"), "w", encoding="utf-8") as f:
    f.write(t2)

print("外置图片数:", counter["n"], "失败:", missing)
size = os.path.getsize(os.path.join(DIST, "index.html"))
print("dist/index.html 字节:", size, "=> KB", round(size/1024))
if size > 1048576:
    print("仍超过 1MB 限制！"); sys.exit(1)
print("OK")
