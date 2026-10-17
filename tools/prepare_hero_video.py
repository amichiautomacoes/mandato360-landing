"""Prepara vídeos H.264 silenciosos e capas WebP, preservando o original.

Usa o encoder H.264 do Chromium via MediaRecorder, sem dependências de produção.
Por padrão, atualiza apenas o desktop. A emenda do loop é preparada no próprio
arquivo, com uma fusão curta entre o final e o início, sem escurecer a imagem.
"""

import argparse
import base64
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


LANDING_DIR = Path(__file__).resolve().parents[1]
SOURCE = LANDING_DIR.parent / "assets" / "download.mp4"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--target", choices=("desktop", "mobile", "both"), default="desktop")
    parser.add_argument("--trim-start", type=float, default=0.5,
                        help="Segundos descartados da abertura (padrão: 0.5).")
    parser.add_argument("--crossfade", type=float, default=0.6,
                        help="Duração da fusão no loop (padrão: 0.6 segundo).")
    args = parser.parse_args()
    if args.trim_start < 0 or args.crossfade <= 0:
        parser.error("Use --trim-start >= 0 e --crossfade > 0.")

    browsers = Path(sys.prefix) / "ms-playwright"
    if browsers.is_dir():
        os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(browsers))
    encoded = base64.b64encode(args.source.read_bytes()).decode("ascii")
    specs = []
    if args.target in ("desktop", "both"):
        specs.append({"name": "hero-desktop.mp4", "width": 1920,
                      "bitrate": 3000000, "posterName": "hero-video-poster-desktop.webp"})
    if args.target in ("mobile", "both"):
        specs.append({"name": "hero-mobile.mp4", "width": 540,
                      "bitrate": 900000, "posterName": "hero-video-poster-540.webp"})
    print(f"Preparando {args.target}: {args.source}", flush=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.set_default_timeout(60000)
            page.set_content('<video muted playsinline></video>')
            result = page.evaluate(
                """async ({encoded, specs, trimStart, crossfade}) => {
                    const type = 'video/mp4;codecs=avc1.64001f';
                    const fps = 24;
                    if (!MediaRecorder.isTypeSupported(type)) throw new Error('Encoder H.264 indisponível.');
                    const video = document.querySelector('video');
                    video.muted = true;
                    video.src = 'data:video/mp4;base64,' + encoded;
                    await new Promise((resolve, reject) => {
                        video.addEventListener('loadeddata', resolve, {once:true});
                        video.addEventListener('error', () => reject(new Error('Falha ao ler o vídeo.')), {once:true});
                    });
                    if (video.duration <= trimStart + crossfade * 2) {
                        throw new Error('O vídeo é curto demais para os cortes e a fusão configurados.');
                    }
                    const seek = time => new Promise(resolve => {
                        video.addEventListener('seeked', resolve, {once:true});
                        video.currentTime = time;
                    });
                    // A duração do MP4 pode avançar além do último quadro real.
                    // Usa o timestamp decodificado para completar a fusão antes do loop.
                    const fadeEnd = await new Promise(resolve => {
                        video.requestVideoFrameCallback((_now, metadata) => resolve(metadata.mediaTime));
                        video.currentTime = video.duration - 0.001;
                    });
                    // Guarda a abertura visível para sobrepô-la à cauda do vídeo.
                    // A fusão fica no arquivo; a página precisa de apenas um player.
                    const fadeFrames = [];
                    const fadeCount = Math.ceil(crossfade * fps);
                    for (let i = 0; i <= fadeCount; i++) {
                        await seek(trimStart + crossfade * i / fadeCount);
                        fadeFrames.push(await createImageBitmap(video));
                    }
                    // O último quadro da fusão desemboca exatamente neste início.
                    const start = trimStart + crossfade;
                    await seek(start);
                    const records = specs.map(spec => {
                        const canvas = document.createElement('canvas');
                        canvas.width = Math.max(2, Math.floor(Math.min(spec.width, video.videoWidth) / 2) * 2);
                        canvas.height = Math.max(2, Math.round(canvas.width * video.videoHeight / video.videoWidth / 2) * 2);
                        const context = canvas.getContext('2d', {alpha:false});
                        context.imageSmoothingQuality = 'high';
                        context.drawImage(fadeFrames[fadeCount],0,0,canvas.width,canvas.height);
                        const poster = canvas.toDataURL('image/webp',0.86).split(',')[1];
                        // Entrega cada quadro explicitamente, inclusive os extremos.
                        const stream = canvas.captureStream(0);
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
                    const draw = (_now, metadata) => {
                        if (finished) return;
                        const progress = Math.max(0, Math.min(1,
                            (metadata.mediaTime - (fadeEnd - crossfade)) / crossfade));
                        const frame = fadeFrames[Math.min(fadeCount, Math.round(progress * fadeCount))];
                        records.forEach(({context, canvas, stream}) => {
                            context.globalAlpha = 1;
                            context.drawImage(video,0,0,canvas.width,canvas.height);
                            if (progress > 0) {
                                context.globalAlpha = progress * progress * (3 - 2 * progress);
                                context.drawImage(frame,0,0,canvas.width,canvas.height);
                                context.globalAlpha = 1;
                            }
                            stream.getVideoTracks()[0].requestFrame();
                        });
                        video.requestVideoFrameCallback(draw);
                    };
                    const ended = new Promise(resolve => video.addEventListener('ended', resolve, {once:true}));
                    records.forEach(record => record.recorder.start(1000));
                    records.forEach(record => record.stream.getVideoTracks()[0].requestFrame());
                    await new Promise(resolve => setTimeout(resolve, 2000 / fps));
                    video.requestVideoFrameCallback(draw);
                    await video.play();
                    await ended;
                    finished = true;
                    // Entrega o quadro de fechamento ao encoder antes de parar.
                    // Ele coincide com o primeiro quadro, evitando um salto na volta.
                    records.forEach(({context, canvas, stream}) => {
                        context.globalAlpha = 1;
                        context.drawImage(fadeFrames[fadeCount],0,0,canvas.width,canvas.height);
                        stream.getVideoTracks()[0].requestFrame();
                    });
                    await new Promise(resolve => setTimeout(resolve, 2000 / fps));
                    records.forEach(record => record.recorder.stop());
                    fadeFrames.forEach(frame => frame.close());
                    return await Promise.all(records.map(async record => {
                        const blob = await record.done;
                        record.stream.getTracks().forEach(track => track.stop());
                        const bytes = new Uint8Array(await blob.arrayBuffer());
                        let binary = '';
                        for (let offset=0; offset<bytes.length; offset+=32768) {
                            binary += String.fromCharCode(...bytes.subarray(offset,offset+32768));
                        }
                        return {name:record.name,width:record.canvas.width,height:record.canvas.height,
                            duration:video.duration-start,video:btoa(binary),
                            posterName:record.posterName,poster:record.poster};
                    }));
                }""",
                {"encoded": encoded, "specs": specs, "trimStart": args.trim_start,
                 "crossfade": args.crossfade},
            )
            for item in result:
                target = LANDING_DIR / "static" / "video" / item["name"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(base64.b64decode(item["video"]))
                poster = LANDING_DIR / "static" / "img" / "responsive" / item["posterName"]
                poster.parent.mkdir(parents=True, exist_ok=True)
                poster.write_bytes(base64.b64decode(item["poster"]))
                print(f"{target.name}: {item['width']}x{item['height']}, "
                      f"{item['duration']:.2f}s, {target.stat().st_size:,} bytes", flush=True)
                print(f"{poster.name}: {poster.stat().st_size:,} bytes", flush=True)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
