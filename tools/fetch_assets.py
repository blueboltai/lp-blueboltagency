#!/usr/bin/env python3
"""Descarrega para assets/ tudo o que a pagina referenciava no WordPress.

Percorre o export do Elementor (imagens, video de fundo, icones SVG) e a lista
de videos Presto (posters), guarda cada ficheiro em assets/img e escreve
tools/source/asset-map.json, o mapa URL remoto -> caminho local que o conversor
usa para reescrever as referencias.

Tambem descarrega as fontes do Google Fonts para assets/fonts, para a pagina
ficar sem qualquer dependencia externa.

    python3 tools/fetch_assets.py
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "tools", "source", "elementor-export.json")
VIDEOS = os.path.join(ROOT, "tools", "source", "presto-videos.json")
ASSET_MAP = os.path.join(ROOT, "tools", "source", "asset-map.json")
IMG_DIR = os.path.join(ROOT, "assets", "img")
FONT_DIR = os.path.join(ROOT, "assets", "fonts")
FONT_CSS = os.path.join(ROOT, "assets", "css", "fonts.css")

HOST = "agencia.bluebolt.pt"

FONT_FAMILIES = [
    ("DM+Sans:wght@400;500;600;700;800", "dm-sans"),
    ("Instrument+Serif:ital@0;1", "instrument-serif"),
]
# User agent moderno para o Google Fonts devolver woff2.
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"


def curl(url, dest=None, text=False):
    cmd = ["curl", "-sSL", "--max-time", "120", "-A", UA]
    if text:
        cmd.append(url)
        result = subprocess.run(cmd, capture_output=True)
        return result.stdout.decode("utf-8", "replace") if result.returncode == 0 else None
    cmd += ["-o", dest, "-w", "%{http_code}", url]
    result = subprocess.run(cmd, capture_output=True)
    return result.stdout.decode().strip()


def collect_urls():
    with open(SOURCE, encoding="utf-8") as fh:
        data = json.load(fh)
    urls = set()

    def visit(node):
        settings = node.get("settings", {})
        for value in settings.values():
            for url in find_urls(value):
                urls.add(url)
        for child in node.get("elements", []):
            visit(child)

    def find_urls(value):
        found = []
        if isinstance(value, str):
            if value.startswith(f"https://{HOST}/"):
                found.append(value)
        elif isinstance(value, dict):
            for sub in value.values():
                found.extend(find_urls(sub))
        elif isinstance(value, list):
            for sub in value:
                found.extend(find_urls(sub))
        return found

    for section in data["content"]:
        visit(section)

    with open(VIDEOS, encoding="utf-8") as fh:
        for video in json.load(fh):
            if (video.get("poster") or "").startswith(f"https://{HOST}/"):
                urls.add(video["poster"])
    return sorted(urls)


def local_name(url, taken):
    name = os.path.basename(urlparse(url).path)
    name = re.sub(r"[^A-Za-z0-9._-]", "-", name) or "asset"
    base, ext = os.path.splitext(name)
    candidate, counter = name, 2
    while candidate in taken and taken[candidate] != url:
        candidate = f"{base}-{counter}{ext}"
        counter += 1
    taken[candidate] = url
    return candidate


def fetch_images():
    os.makedirs(IMG_DIR, exist_ok=True)
    mapping, taken, failed = {}, {}, []
    urls = collect_urls()
    print(f"{len(urls)} ficheiros a descarregar de {HOST}")
    for url in urls:
        name = local_name(url, taken)
        dest = os.path.join(IMG_DIR, name)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            mapping[url] = f"assets/img/{name}"
            continue
        code = curl(url, dest)
        if code == "200" and os.path.getsize(dest) > 0:
            mapping[url] = f"assets/img/{name}"
            print(f"  ok   {name} ({os.path.getsize(dest):,} B)")
        else:
            failed.append((url, code))
            if os.path.exists(dest):
                os.remove(dest)
            print(f"  FALHA {url} -> {code}", file=sys.stderr)
    return mapping, failed


def fetch_fonts():
    """Descarrega os woff2 do Google Fonts e gera assets/css/fonts.css."""
    os.makedirs(FONT_DIR, exist_ok=True)
    blocks = []
    for spec, slug in FONT_FAMILIES:
        css = curl(f"https://fonts.googleapis.com/css2?family={spec}&display=swap", text=True)
        if not css:
            print(f"  FALHA css de {spec}", file=sys.stderr)
            continue
        counter = 0
        for match in re.finditer(r"@font-face\s*\{[^}]*\}", css):
            face = match.group(0)
            src = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", face)
            if not src:
                continue
            # Ficamos so com o subconjunto latino (o CSS lista varios unicode-range).
            unicode_range = re.search(r"unicode-range:\s*([^;]+);", face)
            if unicode_range and not unicode_range.group(1).startswith("U+0000"):
                if "U+0100" not in unicode_range.group(1):
                    continue
            counter += 1
            name = f"{slug}-{counter}.woff2"
            code = curl(src.group(1), os.path.join(FONT_DIR, name))
            if code != "200":
                print(f"  FALHA fonte {name} -> {code}", file=sys.stderr)
                continue
            face = face.replace(src.group(1), f"../fonts/{name}")
            blocks.append(face.strip())
            print(f"  ok   {name}")
    if blocks:
        header = "/* Fontes auto-alojadas (Google Fonts, licença SIL OFL). */\n\n"
        with open(FONT_CSS, "w", encoding="utf-8") as fh:
            fh.write(header + "\n\n".join(blocks) + "\n")


def main():
    mapping, failed = fetch_images()
    print("\nFontes:")
    fetch_fonts()
    with open(ASSET_MAP, "w", encoding="utf-8") as fh:
        json.dump(mapping, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"\nasset-map.json: {len(mapping)} entradas")
    if failed:
        print(f"{len(failed)} falhas:", file=sys.stderr)
        for url, code in failed:
            print(f"  {code} {url}", file=sys.stderr)


if __name__ == "__main__":
    main()
