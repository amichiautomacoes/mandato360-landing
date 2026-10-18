"""Prepara vídeos H.264 de alta qualidade e capas WebP, preservando os originais.

Usa FFmpeg/libx264 com qualidade constante, sem dependência no container de produção.
O corte e a fusão são calculados por quadro para manter a cadência e a emenda do loop.
Informe --ffmpeg ou instale imageio-ffmpeg somente no ambiente de preparação.
"""

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


LANDING_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = LANDING_DIR.parent / "assets"
SPECS = {
    "desktop": {"source": "download.mp4", "max_width": 1920},
    "mobile": {"source": "fundocel.mp4", "max_width": 1080},
}


def find_ffmpeg(explicit):
    """Aceita um binário local ou o executável incluído no pacote de preparação."""
    if explicit:
        return explicit.resolve()
    installed = shutil.which("ffmpeg")
    if installed:
        return Path(installed)
    try:
        import imageio_ffmpeg
    except ImportError:
        return None
    return Path(imageio_ffmpeg.get_ffmpeg_exe())


def run_ffmpeg(executable, *arguments):
    result = subprocess.run(
        [str(executable), "-hide_banner", *map(str, arguments)],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300,
    )
    if result.returncode:
        raise RuntimeError(f"Falha no FFmpeg:\n{result.stderr[-4000:]}")
    return result


def probe_video(executable, source):
    """Decodifica a faixa de vídeo para contar os quadros reais, sem incluir áudio."""
    result = run_ffmpeg(
        executable, "-i", source, "-map", "0:v:0", "-an", "-sn", "-dn",
        "-fps_mode", "passthrough", "-progress", "pipe:1", "-nostats", "-f", "null", "-",
    )
    stream = next((line for line in result.stderr.splitlines() if "Video:" in line), "")
    dimensions = re.search(r"\b(\d{2,5})x(\d{2,5})\b", stream)
    rate = re.search(r"\b(\d+(?:\.\d+)?) fps\b", stream)
    frames = re.findall(r"^frame=(\d+)", result.stdout, re.MULTILINE)
    if not dimensions or not rate or not frames:
        raise RuntimeError(f"Não foi possível inspecionar os quadros de {source}.")
    return {
        "width": int(dimensions[1]), "height": int(dimensions[2]),
        "fps": float(rate[1]), "frames": int(frames[-1]),
    }


def prepare_video(executable, name, source, trim_start, crossfade, crf, preset):
    info = probe_video(executable, source)
    fps = info["fps"]
    trim_frames = round(trim_start * fps)
    fade_frames = max(2, round(crossfade * fps))
    body_frames = info["frames"] - trim_frames - fade_frames
    if body_frames <= fade_frames:
        raise ValueError("O vídeo é curto demais para os cortes e a fusão configurados.")
    width = max(2, min(SPECS[name]["max_width"], info["width"]) // 2 * 2)
    height = max(2, round(width * info["height"] / info["width"] / 2) * 2)
    rate = f"{fps:g}"
    # A abertura termina no quadro imediatamente anterior ao reinício do corpo.
    # Os dois ramos mantêm a mesma cadência e base de tempo antes da fusão.
    filters = (
        "[0:v:0]split=2[body0][head0];"
        f"[body0]trim=start_frame={trim_frames + fade_frames}:end_frame={info['frames']},"
        f"setpts=PTS-STARTPTS,fps={rate},settb=AVTB[body];"
        f"[head0]trim=start_frame={trim_frames}:end_frame={trim_frames + fade_frames},"
        f"setpts=PTS-STARTPTS,fps={rate},settb=AVTB[head];"
        f"[body][head]xfade=transition=fade:duration={fade_frames / fps:.9f}:"
        f"offset={(body_frames - fade_frames) / fps:.9f},"
        f"scale={width}:{height}:flags=lanczos,format=yuv420p[video]"
    )
    video_dir = LANDING_DIR / "static" / "video"
    poster_dir = LANDING_DIR / "static" / "img" / "responsive"
    video_dir.mkdir(parents=True, exist_ok=True)
    poster_dir.mkdir(parents=True, exist_ok=True)
    video_path = video_dir / f"hero-{name}-hq.mp4"
    poster_path = poster_dir / f"hero-video-poster-{name}-hq.webp"
    # Os arquivos finais só são trocados depois que vídeo e capa estiverem prontos.
    with tempfile.TemporaryDirectory(prefix=".hero-hq-", dir=video_dir) as temporary:
        temporary_video = Path(temporary) / "video.mp4"
        temporary_poster = Path(temporary) / "poster.webp"
        run_ffmpeg(
            executable, "-loglevel", "error", "-y", "-i", source,
            "-filter_complex", filters, "-map", "[video]", "-an",
            "-c:v", "libx264", "-preset", preset, "-crf", crf, "-pix_fmt", "yuv420p",
            "-frames:v", body_frames, "-r", rate, "-fps_mode", "cfr",
            "-movflags", "+faststart", temporary_video,
        )
        run_ffmpeg(
            executable, "-loglevel", "error", "-y", "-i", temporary_video,
            "-frames:v", "1", "-an", "-c:v", "libwebp", "-quality", "96",
            "-compression_level", "6", temporary_poster,
        )
        # A cópia herda as permissões de static/, em vez das permissões privadas
        # da pasta temporária no Windows, permitindo leitura pelo Git e servidor.
        shutil.copyfile(temporary_video, video_path)
        shutil.copyfile(temporary_poster, poster_path)
    print(
        f"{video_path.name}: {width}x{height}, {rate} fps, "
        f"{body_frames / fps:.2f}s, {video_path.stat().st_size:,} bytes", flush=True,
    )
    print(f"{poster_path.name}: {poster_path.stat().st_size:,} bytes", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, help="Substitui o original do destino selecionado.")
    parser.add_argument("--target", choices=("desktop", "mobile", "both"), default="desktop")
    parser.add_argument("--ffmpeg", type=Path, help="Caminho do executável FFmpeg com libx264 e libwebp.")
    parser.add_argument("--trim-start", type=float, default=0.5)
    parser.add_argument("--crossfade", type=float, default=0.6)
    parser.add_argument("--crf", type=int, default=16, help="Qualidade constante; menor preserva mais detalhes.")
    parser.add_argument("--preset", choices=("fast", "medium", "slow", "slower", "veryslow"), default="slow")
    args = parser.parse_args()
    if args.trim_start < 0 or args.crossfade <= 0 or not 0 <= args.crf <= 51:
        parser.error("Use --trim-start >= 0, --crossfade > 0 e --crf entre 0 e 51.")
    if args.target == "both" and args.source:
        parser.error("Use --source com --target desktop ou mobile; both usa os dois originais próprios.")
    executable = find_ffmpeg(args.ffmpeg)
    if executable is None or not executable.is_file():
        parser.error("Informe --ffmpeg ou instale imageio-ffmpeg na venv de preparação.")
    for name in (SPECS if args.target == "both" else (args.target,)):
        source = (args.source or ASSETS_DIR / SPECS[name]["source"]).resolve()
        if not source.is_file():
            parser.error(f"Original não encontrado: {source}")
        print(f"Preparando {name}: {source}", flush=True)
        prepare_video(executable, name, source, args.trim_start, args.crossfade, args.crf, args.preset)


if __name__ == "__main__":
    main()
