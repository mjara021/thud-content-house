#!/usr/bin/env python3
"""Measure a finished video against the house format, and make pictures to look at.

    python3 tools/measure.py production/ep001/final.mp4

Writes next to the video:
  measure.json        length, size, fps, audio, hard cuts per 10s, pass/fail checks
  contact_sheet.jpg   one frame per second in a grid (look at this!)
  safezone_check.jpg  a mid-video frame with the TikTok / Shorts / Reels button areas shaded red
Python 3.9 compatible. Needs Pillow + ffmpeg/ffprobe.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import shutil

from PIL import Image, ImageDraw

# Approximate areas covered by app buttons/captions on a 1080x1920 frame
# [practitioner, training: re-verify against each app's current layout]
UI_ZONES = [
    ("top bar (tabs, search)", (0, 0, 1080, 190)),
    ("bottom caption + username", (0, 1440, 1080, 1920)),
    ("right-side buttons", (930, 760, 1080, 1440)),
]


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
                       capture_output=True, text=True)
    return json.loads(r.stdout)


def hard_cuts(path, threshold=0.4):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-vf", "select='gt(scene,%s)',showinfo" % threshold,
                        "-f", "null", "-"], capture_output=True, text=True)
    return [float(m) for m in re.findall(r"pts_time:([0-9.]+)", r.stderr)]


def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    i = re.findall(r"I:\s+(-?[0-9.]+|-inf) LUFS", r.stderr)
    p = re.findall(r"Peak:\s+(-?[0-9.]+|-inf) dBFS", r.stderr)
    return (i[-1] if i else None), (p[-1] if p else None)


def frames(path, times, tmp):
    out = []
    for i, t in enumerate(times):
        f = os.path.join(tmp, "f%03d.jpg" % i)
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", "%.3f" % t, "-i", path,
                        "-frames:v", "1", "-q:v", "3", f, "-y"], capture_output=True)
        if os.path.isfile(f):
            out.append((t, Image.open(f).convert("RGB")))
    return out


def main(path):
    path = os.path.abspath(path)
    base = os.path.dirname(path)
    info = probe(path)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), {})
    a = [s for s in info["streams"] if s["codec_type"] == "audio"]
    dur = float(info["format"]["duration"])
    num, den = (v.get("avg_frame_rate", "0/1").split("/") + ["1"])[:2]
    fps = float(num) / float(den or 1) if float(den or 1) else 0
    cuts = hard_cuts(path)
    lufs, peak = loudness(path) if a else (None, None)
    m = {
        "file": path,
        "duration_s": round(dur, 2),
        "width": v.get("width"), "height": v.get("height"),
        "fps": round(fps, 2), "video_codec": v.get("codec_name"), "pix_fmt": v.get("pix_fmt"),
        "audio_tracks": len(a),
        "integrated_lufs": lufs, "true_peak_dbfs": peak,
        "hard_cuts_at_s": [round(c, 2) for c in cuts],
        "hard_cuts_per_10s": round(len(cuts) / dur * 10, 2) if dur else None,
    }
    checks = {
        "length_15_30s": 15 <= dur <= 30.5,
        "size_1080x1920": (v.get("width"), v.get("height")) == (1080, 1920),
        "fps_30": abs(fps - 30) < 0.5,
        "h264_yuv420p": v.get("codec_name") == "h264" and v.get("pix_fmt") == "yuv420p",
        "has_audio_track": len(a) > 0,
        "cuts_0_to_1.2_per_10s": m["hard_cuts_per_10s"] is not None and m["hard_cuts_per_10s"] <= 1.2,
    }
    m["checks"] = checks
    m["all_pass"] = all(checks.values())

    tmp = tempfile.mkdtemp(prefix="measure_")
    try:
        times = [min(dur - 0.05, float(t) + 0.5) for t in range(int(dur))]
        fr = frames(path, times, tmp)
        if fr:
            cols = 5
            tw, th = 216, 384
            rows = (len(fr) + cols - 1) // cols
            sheet = Image.new("RGB", (cols * tw, rows * (th + 28)), (255, 255, 255))
            d = ImageDraw.Draw(sheet)
            for i, (t, im) in enumerate(fr):
                x, y = (i % cols) * tw, (i // cols) * (th + 28)
                sheet.paste(im.resize((tw, th)), (x, y))
                d.text((x + 6, y + th + 6), "%.1fs" % t, fill=(0, 0, 0))
            sheet.save(os.path.join(base, "contact_sheet.jpg"), quality=85)
            mid = fr[len(fr) // 2][1].convert("RGBA")
            ov = Image.new("RGBA", mid.size, (0, 0, 0, 0))
            od = ImageDraw.Draw(ov)
            for name, box in UI_ZONES:
                od.rectangle(box, fill=(255, 0, 0, 90), outline=(255, 0, 0, 255), width=4)
                od.text((box[0] + 12, box[1] + 12), name, fill=(255, 255, 255, 255))
            mid.alpha_composite(ov)
            mid.convert("RGB").resize((540, 960)).save(os.path.join(base, "safezone_check.jpg"), quality=85)
            m["contact_sheet"] = os.path.join(base, "contact_sheet.jpg")
            m["safezone_check"] = os.path.join(base, "safezone_check.jpg")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    with open(os.path.join(base, "measure.json"), "w") as fh:
        json.dump(m, fh, indent=2)
    print(json.dumps(m, indent=2))
    return 0 if m["all_pass"] else 2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
