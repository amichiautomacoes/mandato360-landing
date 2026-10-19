"""Reduz metadados dos MP4 sem recodificar e verifica todos os quadros.

Somente aplica um arquivo menor quando pixels, tempos e descrição da faixa
permanecem idênticos. Os arquivos anteriores e a prova framemd5 são preservados.
"""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from prepare_hero_video import find_ffmpeg


LANDING_DIR = Path(__file__).resolve().parents[1]


def run(executable, *arguments, binary=False):
    result = subprocess.run(
        [str(executable), "-hide_banner", *map(str, arguments)],
        capture_output=True, timeout=300,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace")[-4000:])
    return result if binary else (
        result.stdout.decode("utf-8"), result.stderr.decode("utf-8", errors="replace")
    )


def encoder_sei_only(executable, source):
    """Autoriza remover SEI apenas quando contém a identificação do x264."""
    raw = run(
        executable, "-loglevel", "error", "-i", source, "-map", "0:v:0",
        "-c:v", "copy", "-bsf:v", "h264_mp4toannexb", "-f", "h264", "-",
        binary=True,
    ).stdout
    messages = []
    for unit in re.split(b"\x00\x00(?:\x00)?\x01", raw):
        if not unit or unit[0] & 31 != 6:
            continue
        data = unit[1:].replace(b"\x00\x00\x03", b"\x00\x00")
        index = 0
        while index < len(data):
            if data[index] == 128 and not any(data[index + 1:]):
                break
            kind = size = 0
            while index < len(data) and data[index] == 255:
                kind += 255
                index += 1
            if index >= len(data):
                return False
            kind += data[index]
            index += 1
            while index < len(data) and data[index] == 255:
                size += 255
                index += 1
            if index >= len(data):
                return False
            size += data[index]
            index += 1
            payload = data[index:index + size]
            if len(payload) != size:
                return False
            messages.append(kind == 5 and b"x264 - core" in payload)
            index += size
    return bool(messages) and all(messages)


def decoded_proof(executable, source):
    stdout, stderr = run(
        executable, "-i", source, "-map", "0:v:0", "-an", "-sn", "-dn",
        "-fps_mode", "passthrough", "-f", "framemd5", "-",
    )
    line = next(line for line in stderr.splitlines() if "Video:" in line)
    # O bitrate diminui quando metadados são removidos; os demais campos
    # incluem codec, resolução, cor, faixa, cadência e base de tempo.
    description = re.sub(r", \d+(?:\.\d+)? kb/s", "", line.split("Video:", 1)[1]).strip()
    frames = sum(bool(line.strip()) and not line.startswith("#") for line in stdout.splitlines())
    return stdout, description, frames


def optimize(executable, source, evidence, apply):
    evidence.mkdir(parents=True, exist_ok=True)
    before = source.read_bytes()
    original_dir = evidence / "originals"
    original_dir.mkdir(exist_ok=True)
    original = original_dir / source.name
    # Não sobrescreve a cópia de uma execução anterior.
    if not original.exists():
        shutil.copyfile(source, original)
    proof_before, description_before, frames = decoded_proof(executable, source)
    (evidence / f"{source.stem}-before.framemd5").write_text(proof_before, encoding="utf-8")
    remove_encoder_sei = encoder_sei_only(executable, source)
    with tempfile.TemporaryDirectory(prefix="video-delivery-", dir=evidence) as temporary:
        candidate = Path(temporary) / source.name
        arguments = [
            "-loglevel", "error", "-y", "-i", source, "-map", "0:v:0", "-an",
            "-c:v", "copy", "-map_metadata", "-1", "-metadata:s:v:0", "encoder=",
            "-fflags", "+bitexact", "-movflags", "+faststart",
        ]
        if remove_encoder_sei:
            arguments += ["-bsf:v", "filter_units=remove_types=6"]
        run(executable, *arguments, candidate)
        proof_after, description_after, frames_after = decoded_proof(executable, candidate)
        (evidence / f"{source.stem}-after.framemd5").write_text(proof_after, encoding="utf-8")
        if proof_before != proof_after or description_before != description_after or frames != frames_after:
            raise RuntimeError(f"Verificação de fidelidade falhou; original preservado: {source.name}")
        output = candidate.read_bytes()
        smaller = len(output) < len(before)
        if apply and smaller:
            shutil.copyfile(candidate, source)
    return {
        "file": source.name, "before_bytes": len(before), "candidate_bytes": len(output),
        "saved_bytes": max(0, len(before) - len(output)), "applied": apply and smaller,
        "decoded_frames": frames, "all_frames_and_timestamps_identical": True,
        "stream_description_identical": True, "stream": description_before,
        "encoder_identification_removed": remove_encoder_sei,
        "before_sha256": hashlib.sha256(before).hexdigest(),
        "candidate_sha256": hashlib.sha256(output).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ffmpeg", type=Path)
    parser.add_argument("--apply", action="store_true", help="Aplica somente candidatos menores e verificados.")
    parser.add_argument("--evidence", type=Path, default=LANDING_DIR / ".impeccable/verification/video-delivery")
    args = parser.parse_args()
    executable = find_ffmpeg(args.ffmpeg)
    if executable is None or not executable.is_file():
        parser.error("Informe --ffmpeg ou instale imageio-ffmpeg no ambiente de preparação.")
    report = []
    for name in ("desktop", "mobile"):
        item = optimize(executable, LANDING_DIR / "static/video" / f"hero-{name}-hq.mp4", args.evidence, args.apply)
        report.append(item)
        print(json.dumps(item, ensure_ascii=False), flush=True)
    (args.evidence / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
