"""Index the NM Classic archive's directory listings (names, sizes, dates only).

Usage: python3 -I crawl_nmc.py OUT.json
"""
import html, json, re, sys, time, urllib.parse, urllib.request

BASE = "https://electro-music.org"
ROOT = "/nm_classic/"
UA = "g1-patch-atlas-indexer/1.0 (metadata only; links back to source)"
DELAY = 0.35

ROW = re.compile(
    r'<td class="indexcolname"><a href="([^"]+)">(.*?)</a></td>'
    r'<td class="indexcollastmod">([^<]*)</td><td class="indexcolsize">([^<]*)</td>')


def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("latin-1")


def main(out):
    tree = get(ROOT + "tree.php")
    dirs = sorted({h for h in re.findall(r'href="(/nm_classic/[^"]*/)"', tree)} | {ROOT})
    files, pages, failed = [], [], []
    for i, d in enumerate(dirs):
        try:
            body = get(urllib.parse.quote(urllib.parse.unquote(d), safe="/()&'!,+~"))
        except Exception as e:  # noqa: BLE001
            failed.append({"dir": d, "error": str(e)})
            continue
        rows = ROW.findall(body)
        if not rows:
            pages.append(d)
        for href, name, mod, size in rows:
            if href.endswith("/") or href.startswith("?") or href.startswith("/"):
                continue
            files.append({
                "dir": urllib.parse.unquote(d)[len(ROOT):],
                "name": html.unescape(urllib.parse.unquote(href)),
                "modified": mod.strip(),
                "size": size.strip(),
            })
        if i % 50 == 0:
            print(f"{i}/{len(dirs)} dirs, {len(files)} files", flush=True)
        time.sleep(DELAY)
    data = {
        "source": BASE + ROOT,
        "indexed": time.strftime("%Y-%m-%d"),
        "dirs": len(dirs),
        "pages": pages,
        "failed": failed,
        "files": files,
    }
    with open(out, "w") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    print(f"done: {len(dirs)} dirs, {len(files)} files, {len(pages)} non-listing pages, {len(failed)} failed")


if __name__ == "__main__":
    main(sys.argv[1])
