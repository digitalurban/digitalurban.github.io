#!/usr/bin/env python3
"""Pre-cutover checks for pointing digitalurban.org at the new site.

Run from the site directory:

    python3 precutover_check.py

Reports, and writes precutover-report.txt:

  1. Post bodies still pointing at the WordPress host - these break the moment
     the domain moves, or keep serving from the old box if it stays up.
  2. Local asset references that have no matching file in ../assets - broken
     images regardless of DNS.
  3. Absolute internal links that should be relative.
  4. Whether redirects.json (from the dedupe) is wired into the build.
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict

POSTS = "src/posts"
ASSETS = "../assets"
SITE_OUT = "_site"

HOSTS = re.compile(
    r"https?://(?:www\.)?digitalurban\.(?:org|com)(/[^\s\"'<>)\]]*)?", re.I
)
SRCS = re.compile(r"(?:src|href)\s*=\s*[\"']([^\"']+)[\"']", re.I)
MD_IMG = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")


def walk_posts():
    for root, _dirs, files in os.walk(POSTS):
        for name in sorted(files):
            if name.endswith(".md"):
                path = os.path.join(root, name)
                with open(path, encoding="utf-8", errors="replace") as fh:
                    yield path, fh.read()


def main():
    if not os.path.isdir(POSTS):
        sys.exit("run this from the site directory (no %s here)" % POSTS)

    out = []
    host_hits = defaultdict(list)
    host_kinds = Counter()
    local_refs = defaultdict(list)
    total = 0

    for path, text in walk_posts():
        total += 1
        for m in HOSTS.finditer(text):
            url = m.group(0)
            host_hits[path].append(url)
            if "/wp-content/" in url:
                host_kinds["wp-content asset"] += 1
            elif re.search(r"\.(jpg|jpeg|png|gif|webp|svg|pdf|mp4|mov)$", url, re.I):
                host_kinds["other asset"] += 1
            else:
                host_kinds["internal link"] += 1

        for ref in list(SRCS.findall(text)) + list(MD_IMG.findall(text)):
            if ref.startswith("/assets/"):
                local_refs[ref].append(path)

    # --- 1. old host references
    out.append("=" * 70)
    out.append("1. REFERENCES TO THE OLD WORDPRESS HOST")
    out.append("=" * 70)
    n = sum(len(v) for v in host_hits.values())
    out.append("%d references across %d of %d posts" % (n, len(host_hits), total))
    for kind, c in host_kinds.most_common():
        out.append("  %-18s %d" % (kind, c))
    if host_hits:
        out.append("")
        out.append("First 25 posts affected:")
        for path in list(host_hits)[:25]:
            out.append("  %s" % path)
            for url in host_hits[path][:3]:
                out.append("      %s" % url)
    out.append("")

    # --- 2. missing local assets
    out.append("=" * 70)
    out.append("2. LOCAL ASSET REFERENCES WITH NO FILE ON DISK")
    out.append("=" * 70)
    missing = {}
    if not os.path.isdir(ASSETS):
        out.append("no %s directory found - skipped" % ASSETS)
    else:
        for ref, posts in local_refs.items():
            rel = ref[len("/assets/"):]
            if not os.path.exists(os.path.join(ASSETS, rel)):
                missing[ref] = posts
        out.append(
            "%d distinct local asset refs, %d missing"
            % (len(local_refs), len(missing))
        )
        for ref, posts in list(missing.items())[:40]:
            out.append("  MISSING %s" % ref)
            out.append("          in %s" % posts[0])
        if len(missing) > 40:
            out.append("  ... and %d more" % (len(missing) - 40))
    out.append("")

    # --- 3. redirects wiring
    out.append("=" * 70)
    out.append("3. REDIRECTS FROM THE DEDUPE")
    out.append("=" * 70)
    rpath = "src/_data/redirects.json"
    if not os.path.exists(rpath):
        out.append("no %s - the dedupe was run without --redirects" % rpath)
    else:
        with open(rpath, encoding="utf-8") as fh:
            try:
                red = json.load(fh)
            except ValueError:
                red = {}
        out.append("%d redirects recorded in %s" % (len(red), rpath))
        wired = False
        for root, _dirs, files in os.walk("src"):
            for name in files:
                if name.endswith((".njk", ".js", ".json")) and "redirects" not in name:
                    p = os.path.join(root, name)
                    try:
                        with open(p, encoding="utf-8", errors="replace") as fh:
                            if "redirects" in fh.read():
                                wired = True
                                out.append("  referenced in %s" % p)
                    except OSError:
                        pass
        if not wired:
            out.append("  NOT referenced by any template - the redirects are")
            out.append("  recorded but nothing serves them yet.")
    out.append("")

    # --- 4. built output sanity
    out.append("=" * 70)
    out.append("4. BUILT OUTPUT")
    out.append("=" * 70)
    if not os.path.isdir(SITE_OUT):
        out.append("no %s - run npm run build first" % SITE_OUT)
    else:
        for f, want in [
            ("feed.xml", "<?xml"),
            ("sitemap.xml", "<?xml"),
            ("search.json", "["),
            ("robots.txt", "User-agent"),
            ("CNAME", "digitalurban"),
        ]:
            p = os.path.join(SITE_OUT, f)
            if not os.path.exists(p):
                out.append("  MISSING  %s" % f)
                continue
            with open(p, encoding="utf-8", errors="replace") as fh:
                head = fh.read(200).lstrip()
            out.append("  %-12s %s" % (f, "ok" if head.startswith(want) else "WRONG: starts %r" % head[:60]))
        pages = sum(
            1 for r, _d, fs in os.walk(SITE_OUT) for x in fs if x == "index.html"
        )
        out.append("  %d html pages built" % pages)
    out.append("")

    out.append("=" * 70)
    out.append("WHAT TO DO")
    out.append("=" * 70)
    out.append(
        """
If section 1 shows wp-content assets: those images live on the WordPress box. If
you shut it down they vanish. Either copy them into ../assets and rewrite the
references, or keep the old host serving files. Send me the report and I will
write the rewrite script.

If section 1 shows internal links only: harmless while both hosts answer, but
worth rewriting to relative paths so the pages stop depending on the domain.

If section 2 lists missing files: those are already broken in the new build and
have nothing to do with DNS. Fix before cutover so you are not debugging two
things at once.

Section 3: recorded-but-unwired redirects mean the 576 deleted duplicate URLs
currently 404. Tell me and I will add the redirect pages to the build.
"""
    )

    report = "\n".join(out)
    with open("precutover-report.txt", "w", encoding="utf-8") as fh:
        fh.write(report)
    print(report)
    print("written to precutover-report.txt")


if __name__ == "__main__":
    main()
