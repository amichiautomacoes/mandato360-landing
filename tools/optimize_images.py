"""Gera as versões WebP de content.json sem alterar as imagens originais.

Execute com o Python da venv que contém Playwright, a partir de qualquer pasta.
A conversão usa o encoder WebP do Chromium e mantém a proporção das imagens.
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


LANDING_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = LANDING_DIR / "static"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    targets = parser.add_mutually_exclusive_group()
    targets.add_argument("--mobile-only", action="store_true", help="Gera apenas as imagens verticais dos módulos.")
    targets.add_argument("--desktop-only", action="store_true", help="Gera apenas as imagens horizontais dos módulos.")
    args = parser.parse_args()
    browsers = Path(sys.prefix) / "ms-playwright"
    if browsers.is_dir():
        os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(browsers))

    content = json.loads((LANDING_DIR / "content.json").read_text(encoding="utf-8"))
    images = []
    if not args.mobile_only and not args.desktop_only:
        images = [
            content["hero"]["image"],
            content["solution"]["card_background"],
            content["section_background"],
            content["audience"]["background"],
        ]
    for module in content["solution"]["modules"]:
        gallery = module.get("gallery", {})
        if not args.mobile_only:
            images.extend(slide["image"] for slide in gallery.get("slides", []))
        if not args.desktop_only:
            images.extend(slide["image"] for slide in gallery.get("mobile", {}).get("slides", []))
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            for image in images:
                original = STATIC_DIR / image["path"]
                encoded = base64.b64encode(original.read_bytes()).decode("ascii")
                for source in image.get("sources", []):
                    data_url = page.evaluate(
                        """async ({encoded, width, quality}) => {
                            const image = new Image();
                            image.src = 'data:image/png;base64,' + encoded;
                            await image.decode();
                            const canvas = document.createElement('canvas');
                            canvas.width = Math.min(width, image.naturalWidth);
                            canvas.height = Math.round(canvas.width * image.naturalHeight / image.naturalWidth);
                            const context = canvas.getContext('2d');
                            context.imageSmoothingQuality = 'high';
                            context.drawImage(image, 0, 0, canvas.width, canvas.height);
                            return canvas.toDataURL('image/webp', quality);
                        }""",
                        {"encoded": encoded, "width": source["width"], "quality": image.get("quality", 0.86)},
                    )
                    if not data_url.startswith("data:image/webp;base64,"):
                        raise RuntimeError("O navegador não gerou uma imagem WebP.")
                    target = STATIC_DIR / source["path"]
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(base64.b64decode(data_url.split(",", 1)[1]))
                    print(f"{target.name}: {target.stat().st_size:,} bytes")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
