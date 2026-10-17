"""Gera as versões WebP de content.json sem alterar as imagens originais.

Execute com o Python da venv que contém Playwright, a partir de qualquer pasta.
A conversão usa o encoder WebP do Chromium e mantém a proporção das imagens.
"""

import base64
import json
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


LANDING_DIR = Path(__file__).resolve().parents[1]
STATIC_DIR = LANDING_DIR / "static"


def main():
    browsers = Path(sys.prefix) / "ms-playwright"
    if browsers.is_dir():
        os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(browsers))

    content = json.loads((LANDING_DIR / "content.json").read_text(encoding="utf-8"))
    images = [content["hero"]["image"]]
    images.extend(module["image"] for module in content["solution"]["modules"])
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            for image in images:
                original = STATIC_DIR / image["path"]
                encoded = base64.b64encode(original.read_bytes()).decode("ascii")
                for source in image.get("sources", []):
                    data_url = page.evaluate(
                        """async ({encoded, width}) => {
                            const image = new Image();
                            image.src = 'data:image/png;base64,' + encoded;
                            await image.decode();
                            const canvas = document.createElement('canvas');
                            canvas.width = Math.min(width, image.naturalWidth);
                            canvas.height = Math.round(canvas.width * image.naturalHeight / image.naturalWidth);
                            const context = canvas.getContext('2d');
                            context.imageSmoothingQuality = 'high';
                            context.drawImage(image, 0, 0, canvas.width, canvas.height);
                            return canvas.toDataURL('image/webp', 0.86);
                        }""",
                        {"encoded": encoded, "width": source["width"]},
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
