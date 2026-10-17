"""Prepara MP4s silenciosos e posters WebP do vídeo em assets/download.mp4.

Usa o encoder H.264 do Chromium via MediaRecorder, sem dependências de produção.
O original é preservado. A codificação leva aproximadamente a duração do vídeo.
"""

import base64
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


LANDING_DIR = Path(__file__).resolve().parents[1]
SOURCE = LANDING_DIR.parent / "assets" / "download.mp4"


def main():
    browsers = Path(sys.prefix) / "ms-playwright"
    if browsers.is_dir():
        os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(browsers))
    encoded = base64.b64encode(SOURCE.read_bytes()).decode("ascii")
    print("Preparando o vídeo para celular e desktop...", flush=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.set_content('<video muted playsinline style="width:360px"></video>')
            result = page.evaluate(
                """async (encoded) => {
                    const type = 'video/mp4;codecs=avc1.64001f';
                    if (!MediaRecorder.isTypeSupported(type)) throw new Error('Encoder H.264 indisponível.');
                    const video = document.querySelector('video');
                    video.muted = true;
                    video.src = 'data:video/mp4;base64,' + encoded;
                    await new Promise((resolve, reject) => {
                        video.addEventListener('loadeddata', resolve, {once:true});
                        video.addEventListener('error', () => reject(new Error('Falha ao ler o vídeo.')), {once:true});
                    });
                    // Pula apenas a abertura preta para usar um quadro visível como capa.
                    await new Promise(resolve => {
                        video.addEventListener('seeked', resolve, {once:true});
                        video.currentTime = Math.min(0.1,video.duration / 2);
                    });
                    const specs = [
                        {name:'hero-mobile.mp4', width:540, bitrate:900000},
                        {name:'hero-desktop.mp4', width:720, bitrate:1500000}
                    ];
                    const records = specs.map(spec => {
                        const canvas = document.createElement('canvas');
                        canvas.width = spec.width;
                        canvas.height = Math.round(spec.width * video.videoHeight / video.videoWidth);
                        const context = canvas.getContext('2d');
                        context.imageSmoothingQuality = 'high';
                        context.drawImage(video,0,0,canvas.width,canvas.height);
                        const poster = canvas.toDataURL('image/webp',0.86).split(',')[1];
                        const stream = canvas.captureStream(24);
                        const recorder = new MediaRecorder(stream, {mimeType:type,videoBitsPerSecond:spec.bitrate});
                        const chunks = [];
                        recorder.addEventListener('dataavailable', event => {
                            if (event.data.size) chunks.push(event.data);
                        });
                        const done = new Promise((resolve, reject) => {
                            recorder.addEventListener('stop', () => resolve(new Blob(chunks,{type:'video/mp4'})), {once:true});
                            recorder.addEventListener('error', () => reject(new Error('Falha na codificação.')), {once:true});
                        });
                        return {...spec, canvas, context, recorder, stream, done, poster};
                    });
                    let finished = false;
                    const draw = () => {
                        if (finished) return;
                        records.forEach(record => record.context.drawImage(video,0,0,record.canvas.width,record.canvas.height));
                        video.requestVideoFrameCallback(draw);
                    };
                    const ended = new Promise(resolve => video.addEventListener('ended', resolve, {once:true}));
                    records.forEach(record => record.recorder.start(1000));
                    video.requestVideoFrameCallback(draw);
                    await video.play();
                    await ended;
                    finished = true;
                    records.forEach(record => record.recorder.stop());
                    return await Promise.all(records.map(async record => {
                        const blob = await record.done;
                        record.stream.getTracks().forEach(track => track.stop());
                        const bytes = new Uint8Array(await blob.arrayBuffer());
                        let binary = '';
                        for (let offset=0; offset<bytes.length; offset+=32768) {
                            binary += String.fromCharCode(...bytes.subarray(offset,offset+32768));
                        }
                        return {name:record.name,width:record.canvas.width,height:record.canvas.height,video:btoa(binary),poster:record.poster};
                    }));
                }""",
                encoded,
            )
            for item in result:
                target = LANDING_DIR / "static" / "video" / item["name"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(base64.b64decode(item["video"]))
                poster = LANDING_DIR / "static" / "img" / "responsive" / f"hero-video-poster-{item['width']}.webp"
                poster.parent.mkdir(parents=True, exist_ok=True)
                poster.write_bytes(base64.b64decode(item["poster"]))
                print(f"{target.name}: {item['width']}x{item['height']}, {target.stat().st_size:,} bytes", flush=True)
                print(f"{poster.name}: {poster.stat().st_size:,} bytes", flush=True)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
