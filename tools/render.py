#!/usr/bin/env python3
"""Turn a build_spec.json into a finished vertical video (1080x1920, 30fps, H.264).

    python3 tools/render.py production/ep001/build_spec.json            # render video
    python3 tools/render.py production/ep001/build_spec.json --check    # only validate the spec
    python3 tools/render.py production/ep001/build_spec.json --frames 0,6.5,18
                                                     # write preview PNGs at those times (fast)

Everything the video needs comes from the spec. If something is missing or
risky, it is reported as an ERROR (render refuses) or WARNING (render goes on).
All file paths inside the spec are relative to the spec's own folder.
See tools/README.md for the spec format, and tools/sample_spec.json for an example.
Python 3.9 compatible. Needs Pillow + ffmpeg.
"""
import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import thud as thudlib  # noqa: E402

TOOLS = os.path.dirname(os.path.abspath(__file__))
FONT_TITLE = os.path.join(TOOLS, "fonts", "anton", "Anton-Regular.ttf")
FONT_TEXT = os.path.join(TOOLS, "fonts", "archivoblack", "ArchivoBlack-Regular.ttf")

# Brand defaults (a spec may override any of these under "brand")
BRAND = {
    "title_bg": [18, 22, 27, 232],
    "title_fg": [255, 255, 255],
    "accent": [255, 178, 56],
    "caption_fg": [255, 255, 255],
    "caption_active": [255, 178, 56],
    "caption_stroke": [11, 13, 16],
    "credit_fg": [235, 230, 220],
}

# Layout that keeps text away from TikTok / Shorts / Reels buttons and captions.
# Content-safe box: x 60..900, y 200..1440 (on a 1080x1920 frame).
LAYOUT = {
    "safe_left": 60, "safe_right": 900, "safe_top": 200, "safe_bottom": 1440,
    "title_top": 220, "title_max_w": 820,
    "caption_y": 860, "caption_max_w": 760, "caption_cx": 500,
    "thud_x": 70, "thud_bottom": 1405, "thud_height": 330,
    "verdict_xy": [640, 1180],
    "credit_right": 900, "credit_bottom": 1430,
}
CONTAIN_TOP, CONTAIN_H = 500, 900   # where a 'contain' picture sits
POSES = set(thudlib.POSES)
BLINK_SECONDS = 0.15


# ----------------------------------------------------------------- helpers
def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def rgb(c):
    return tuple(int(v) for v in c[:3])


def rgba(c):
    c = list(c)
    return tuple(int(v) for v in (c + [255])[:4])


def font(path, size):
    return ImageFont.truetype(path, int(size))


def text_w(f, s):
    return f.getlength(s)


def wrap(words, f, max_w):
    lines, cur = [], []
    for w in words:
        trial = " ".join(cur + [w])
        if cur and text_w(f, trial) > max_w:
            lines.append(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------ validation
def validate(spec, base):
    errors, warnings = [], []
    dur = spec.get("duration")
    if not isinstance(dur, (int, float)) or dur <= 0:
        errors.append("duration missing or not a positive number")
        dur = 0
    elif not (15 <= dur <= 30):
        warnings.append("duration %.1fs is outside the 15-30s target" % dur)

    bgs = spec.get("backgrounds") or []
    if not bgs:
        errors.append("no backgrounds")
    for i, b in enumerate(bgs):
        p = os.path.join(base, b.get("image", ""))
        if not b.get("image") or not os.path.isfile(p):
            errors.append("backgrounds[%d].image not found: %s" % (i, b.get("image")))
        if b.get("start", -1) < 0 or b.get("end", 0) <= b.get("start", 0):
            errors.append("backgrounds[%d] has bad start/end" % i)
        if b.get("fit", "cover") not in ("cover", "contain"):
            errors.append("backgrounds[%d].fit must be cover or contain" % i)
        if b.get("grade", "archival") not in ("archival", "bw", "none"):
            errors.append("backgrounds[%d].grade must be archival, bw or none" % i)
    if bgs and dur:
        if abs(bgs[0].get("start", 0)) > 1e-6 or abs(bgs[-1].get("end", 0) - dur) > 0.05:
            errors.append("backgrounds must cover 0..duration with no gaps")
        for a, b in zip(bgs, bgs[1:]):
            if abs(a.get("end", 0) - b.get("start", 0)) > 0.05:
                errors.append("gap/overlap between backgrounds at %.2fs" % a.get("end", 0))
        cuts = sum(1 for b in bgs[1:] if b.get("transition", "cut") == "cut")
        per10 = cuts / dur * 10 if dur else 0
        if per10 > 1.2:
            warnings.append("%.2f hard cuts per 10s; research target is 0.5-1" % per10)

    tc = spec.get("title_card") or {}
    if not tc.get("text"):
        errors.append("title_card.text missing")
    elif len(tc["text"].split()) > 6:
        warnings.append("title card has %d words; rule is 6 or fewer" % len(tc["text"].split()))

    caps = spec.get("captions") or []
    if not caps:
        errors.append("no captions (videos must work on mute)")
    prev_end = 0.0
    for i, c in enumerate(caps):
        words = c.get("words") or []
        if not words:
            errors.append("captions[%d] has no words" % i)
            continue
        s, e = c.get("start", 0), c.get("end", 0)
        if e <= s:
            errors.append("captions[%d] end <= start" % i)
        if s < prev_end - 1e-6:
            warnings.append("captions[%d] overlaps the previous caption" % i)
        prev_end = e
        wt = c.get("word_times")
        if wt is not None and len(wt) != len(words):
            errors.append("captions[%d].word_times length != words length" % i)
        chars = len(" ".join(words))
        if e > s and chars / (e - s) > 20:
            warnings.append("captions[%d] reads at %.0f chars/sec (>20 is hard to read)" % (i, chars / (e - s)))
        if dur and e > dur + 1e-6:
            errors.append("captions[%d] ends after the video" % i)
    if caps and caps[0].get("start", 99) > 0.5:
        warnings.append("first caption starts after 0.5s; the hook must be readable in 0-3s")

    th = spec.get("thud")
    if not th:
        warnings.append("no thud section; Thud will not appear")
    else:
        for i, ev in enumerate(th.get("track") or []):
            if ev.get("pose") not in POSES:
                errors.append("thud.track[%d].pose %r unknown (use %s)" % (i, ev.get("pose"), ", ".join(sorted(POSES))))
    if not spec.get("verdict"):
        warnings.append("no verdict stamp")
    if not spec.get("credits"):
        warnings.append("no on-screen source credit")
    m = spec.get("music")
    if m and not os.path.isfile(os.path.join(base, m.get("file", ""))):
        errors.append("music.file not found")
    if m and not m.get("license"):
        errors.append("music.license missing (no license = not used)")
    return errors, warnings


# ------------------------------------------------------------ backgrounds
def grade(img, mode):
    if mode == "none":
        return img.convert("RGB")
    g = ImageOps.autocontrast(img.convert("L"), cutoff=1)
    if mode == "bw":
        return g.convert("RGB")
    return ImageOps.colorize(g, black=(26, 19, 12), white=(243, 227, 195), mid=(150, 122, 86))


class Background:
    def __init__(self, seg, base, W, H, warnings):
        self.seg = seg
        self.fit = seg.get("fit", "cover")
        src = Image.open(os.path.join(base, seg["image"]))
        src = grade(ImageOps.exif_transpose(src), seg.get("grade", "archival"))
        mv = seg.get("move") or {}
        z = max((mv.get("from") or {}).get("zoom", 1.0), (mv.get("to") or {}).get("zoom", 1.0), 1.0)
        if self.fit == "cover":
            need = max(W / src.width, H / src.height) * z
        else:
            need = min((W - 80) / src.width, CONTAIN_H / src.height) * z
        if need > 1.6:
            warnings.append("%s is small: upscaled %.1fx, may look blurry" % (seg["image"], need))
        if need < 0.9:  # shrink very large images once, for speed
            src = src.resize((max(1, int(src.width * need * 1.1)), max(1, int(src.height * need * 1.1))), Image.LANCZOS)
        self.src = src
        self.W, self.H = W, H
        if self.fit == "contain":
            # blurred, darkened cover version as backdrop
            s = max(W / src.width, H / src.height)
            bd = src.resize((int(src.width * s) + 2, int(src.height * s) + 2), Image.BILINEAR)
            bd = bd.crop(((bd.width - W) // 2, (bd.height - H) // 2, (bd.width - W) // 2 + W, (bd.height - H) // 2 + H))
            bd = bd.filter(ImageFilter.GaussianBlur(28))
            self.backdrop = Image.blend(bd, Image.new("RGB", (W, H), (0, 0, 0)), 0.45)

    def _params(self, t):
        s, e = self.seg["start"], self.seg["end"]
        k = ease((t - s) / (e - s)) if e > s else 0
        mv = self.seg.get("move") or {}
        a = {"zoom": 1.0, "x": 0.5, "y": 0.5}
        a.update(mv.get("from") or {})
        b = dict(a)
        b.update(mv.get("to") or {})
        return tuple(a[n] + (b[n] - a[n]) * k for n in ("zoom", "x", "y"))

    def frame(self, t):
        z, cx, cy = self._params(t)
        W, H, src = self.W, self.H, self.src
        if self.fit == "cover":
            s = max(W / src.width, H / src.height) * z
            cw, ch = W / s, H / s
            x0 = min(max(cx * src.width - cw / 2, 0), src.width - cw)
            y0 = min(max(cy * src.height - ch / 2, 0), src.height - ch)
            return src.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BICUBIC)
        s = min((W - 80) / src.width, CONTAIN_H / src.height) * z
        w, h = src.width * s, src.height * s
        # in contain mode x/y pan the whole picture slightly (0.5 = centered);
        # the picture sits between the title card and the bottom app buttons
        ox = (W - w) / 2 + (cx - 0.5) * 120
        oy = CONTAIN_TOP + (CONTAIN_H - h) / 2 + (cy - 0.5) * 120
        img = src.transform((int(round(w)), int(round(h))), Image.EXTENT, (0, 0, src.width, src.height), Image.BICUBIC)
        out = self.backdrop.copy()
        out.paste(img, (int(round(ox)), int(round(oy))))
        return out


# ------------------------------------------------------------ static layers
def make_shade(W, H, caption_y):
    small = Image.new("L", (108, 192), 0)
    px = small.load()
    for y in range(192):
        for x in range(108):
            dx, dy = (x - 54) / 54.0, (y - 96) / 96.0
            v = max(0.0, math.hypot(dx, dy) - 0.55) / 0.85
            band = math.exp(-((y * 10 - caption_y) / 230.0) ** 2)
            px[x, y] = int(min(1.0, v) * 120 + band * 95)
    a = small.resize((W, H), Image.BICUBIC)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.putalpha(a)
    return layer


def make_title(spec, brand, W):
    tc = spec["title_card"]
    text = tc["text"].upper()
    tag = (spec.get("series_tag") or "").upper()
    max_w = LAYOUT["title_max_w"]
    size = 104
    while True:
        f = font(FONT_TITLE, size)
        lines = wrap(text.split(), f, max_w)
        if len(lines) <= 2 or size <= 60:
            break
        size -= 6
    tagf = font(FONT_TEXT, 30)
    line_h = int(size * 1.12)
    pad_x, pad_y = 34, 26
    tag_h = 44 if tag else 0
    widest = max([text_w(f, " ".join(l)) for l in lines] + ([text_w(tagf, tag)] if tag else []))
    bw = int(widest + pad_x * 2)
    bh = int(pad_y * 2 + tag_h + line_h * len(lines))
    layer = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((0, 0, bw - 1, bh - 1), radius=22, fill=rgba(brand["title_bg"]))
    d.rounded_rectangle((0, 0, 10, bh - 1), radius=5, fill=rgba(brand["accent"]))
    y = pad_y
    if tag:
        d.text((bw / 2, y), tag, font=tagf, fill=rgb(brand["accent"]), anchor="ma")
        y += tag_h
    for l in lines:
        d.text((bw / 2, y), " ".join(l), font=f, fill=rgb(brand["title_fg"]), anchor="ma")
        y += line_h
    x = (W - bw) // 2
    return layer, (x, LAYOUT["title_top"])


class Captions:
    def __init__(self, caps, brand, warnings):
        self.caps = caps
        self.brand = brand
        self.cache = {}
        self.warnings = warnings
        self.layouts = [self._layout(c) for c in caps]

    def _layout(self, c):
        words = c["words"]
        size = 72
        while True:
            f = font(FONT_TEXT, size)
            lines = wrap(words, f, LAYOUT["caption_max_w"])
            if len(lines) <= 2 or size <= 52:
                break
            size -= 4
        if len(lines) > 2:
            self.warnings.append("caption at %.1fs needs %d lines; split it into two captions" % (c["start"], len(lines)))
        wt = c.get("word_times")
        if wt is None:  # spread words over the caption by length
            s, e = c["start"], c["start"] + (c["end"] - c["start"]) * 0.85
            weights = [len(w) + 2 for w in words]
            tot = float(sum(weights))
            acc, wt = 0.0, []
            for w in weights:
                wt.append(s + (e - s) * acc / tot)
                acc += w
        return f, lines, wt

    def layer(self, t):
        for i, c in enumerate(self.caps):
            if c["start"] <= t < c["end"]:
                f, lines, wt = self.layouts[i]
                active = max([k for k, w in enumerate(wt) if w <= t] or [0])
                key = (i, active)
                if key not in self.cache:
                    if len(self.cache) > 40:
                        self.cache.clear()
                    self.cache[key] = self._render(f, lines, active)
                return self.cache[key]
        return None

    def _render(self, f, lines, active):
        b = self.brand
        line_h = int(f.size * 1.25)
        stroke = max(4, f.size // 11)
        W = 1080
        layer = Image.new("RGBA", (W, line_h * len(lines) + stroke * 4), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        k = 0
        y = stroke * 2
        space = text_w(f, " ")
        for l in lines:
            total = text_w(f, " ".join(l))
            x = LAYOUT["caption_cx"] - total / 2
            for w in l:
                col = rgb(b["caption_active"]) if k == active else rgb(b["caption_fg"])
                d.text((x, y), w, font=f, fill=col, stroke_width=stroke, stroke_fill=rgb(b["caption_stroke"]))
                x += text_w(f, w) + space
                k += 1
            y += line_h
        top = LAYOUT["caption_y"] - layer.height // 2
        return layer, (0, top)


def make_credit(text, brand):
    """Small source credit, right-aligned, kept clear of Thud (max 520px wide, 2 lines)."""
    max_w = 520
    for size in (28, 26, 24, 22):
        f = font(FONT_TEXT, size)
        lines = [" ".join(l) for l in wrap(text.split(), f, max_w)]
        if len(lines) <= 2:
            break
    line_h = int(f.size * 1.3)
    w = int(max(text_w(f, l) for l in lines)) + 16
    h = line_h * len(lines) + 12
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i, l in enumerate(lines):
        d.text((w - 8, 6 + i * line_h), l, font=f, fill=rgb(brand["credit_fg"]), stroke_width=3,
               stroke_fill=(0, 0, 0), anchor="ra")
    return layer, (LAYOUT["credit_right"] - w, LAYOUT["credit_bottom"] - h)


def make_verdict(text, brand):
    f = font(FONT_TITLE, 118)
    tw = int(text_w(f, text))
    pad = 30
    w, h = tw + pad * 2, 118 + pad * 2
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((20, 20, 20 + w, 20 + h), radius=18, outline=rgb(brand["accent"]), width=9, fill=(18, 22, 27, 170))
    d.text((20 + w / 2, 20 + h / 2), text, font=f, fill=rgb(brand["accent"]), anchor="mm",
           stroke_width=4, stroke_fill=(11, 13, 16))
    return layer.rotate(5, resample=Image.BICUBIC, expand=True)


# ------------------------------------------------------------ the frame
class Renderer:
    def __init__(self, spec, base):
        self.spec, self.base = spec, base
        self.W, self.H = spec.get("width", 1080), spec.get("height", 1920)
        self.fps = spec.get("fps", 30)
        self.dur = float(spec["duration"])
        self.brand = dict(BRAND, **(spec.get("brand") or {}))
        self.warnings = []
        self.bgs = [Background(b, base, self.W, self.H, self.warnings) for b in spec["backgrounds"]]
        self.shade = make_shade(self.W, self.H, LAYOUT["caption_y"])
        self.title = make_title(spec, self.brand, self.W)
        self.caps = Captions(spec["captions"], self.brand, self.warnings)
        self.credits = [(c, make_credit(c["text"], self.brand)) for c in (spec.get("credits") or [])]
        v = spec.get("verdict")
        self.verdict = (v, make_verdict(v["text"], self.brand)) if v else None
        th = spec.get("thud") or None
        self.thud = th
        if th:
            self.thud_h = th.get("height", LAYOUT["thud_height"])
            self.track = sorted(th.get("track") or [{"t": 0, "pose": "idle"}], key=lambda e: e["t"])
        self.loop_fade = float((spec.get("loop") or {}).get("fade_seconds", 0.4))
        self.frame0 = None

    def _bg(self, t):
        for i, b in enumerate(self.bgs):
            s, e = b.seg["start"], b.seg["end"]
            if s <= t < e or (i == len(self.bgs) - 1 and t >= s):
                fr = b.frame(t)
                tr = b.seg.get("transition", "cut")
                if i > 0 and tr == "fade" and t - s < 0.35:
                    prev = self.bgs[i - 1].frame(t)
                    fr = Image.blend(prev, fr, ease((t - s) / 0.35))
                return fr
        return self.bgs[-1].frame(t)

    def _pose(self, t):
        pose = "idle"
        for ev in self.track:
            if ev["t"] <= t:
                if ev["pose"] == "blink":
                    if t - ev["t"] < BLINK_SECONDS:
                        return "blink"
                else:
                    pose = ev["pose"]
        return pose

    def compose(self, t, loop=True):
        W, H = self.W, self.H
        frame = self._bg(t).convert("RGBA")
        frame.alpha_composite(self.shade)
        tl, tpos = self.title
        tc = self.spec["title_card"]
        if tc.get("start", 0) <= t <= tc.get("end", self.dur):
            frame.alpha_composite(tl, tpos)
        for c, (cl, cpos) in self.credits:
            if c.get("start", 0) <= t <= c.get("end", self.dur):
                frame.alpha_composite(cl, cpos)
        if self.thud:
            img = thudlib.draw(self._pose(t), self.thud_h)
            bob = int(round(2 * math.sin(2 * math.pi * t / 3.2)))
            if self.thud.get("position", "lower_left") == "lower_right":
                x = LAYOUT["safe_right"] - img.width
            else:
                x = LAYOUT["thud_x"]
            frame.alpha_composite(img, (x, LAYOUT["thud_bottom"] - img.height + bob))
        cap = self.caps.layer(t)
        if cap:
            frame.alpha_composite(cap[0], cap[1])
        shake = (0, 0)
        if self.verdict:
            v, vl = self.verdict
            if v["start"] <= t <= v.get("end", self.dur):
                k = ease((t - v["start"]) / 0.12)
                sc = 1.35 - 0.35 * k
                img = vl.resize((max(1, int(vl.width * sc)), max(1, int(vl.height * sc))), Image.BICUBIC)
                if k < 1:
                    a = img.getchannel("A").point(lambda p: int(p * k))
                    img.putalpha(a)
                cx, cy = v.get("xy", LAYOUT["verdict_xy"])
                frame.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))
                dt = t - v["start"]
                if 0.10 <= dt < 0.25:
                    shake = ((6, -4), (-5, 5), (4, 3), (-2, -2))[int((dt - 0.10) * self.fps) % 4]
        out = frame.convert("RGB")
        if shake != (0, 0):
            out = ImageChops.offset(out, shake[0], shake[1])
        if loop and self.loop_fade > 0 and t > self.dur - self.loop_fade:
            if self.frame0 is None:
                self.frame0 = self.compose(0.0, loop=False)
            out = Image.blend(out, self.frame0, ease((t - (self.dur - self.loop_fade)) / self.loop_fade))
        return out


# ------------------------------------------------------------ audio + encode
def run(cmd):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise SystemExit("ffmpeg failed:\n" + p.stderr.decode(errors="ignore")[-2000:])


def thud_sfx(path):
    """Our own synthesized 'stone thud': a falling low tone + a short filtered noise hit."""
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
         "-f", "lavfi", "-i", "aevalsrc='0.95*sin(2*PI*(78*t-60*t*t))*exp(-7*t)':s=48000:d=0.55",
         "-f", "lavfi", "-i", "anoisesrc=d=0.55:c=brown:a=0.9:r=48000",
         "-filter_complex",
         "[1]lowpass=f=220,afade=t=out:st=0:d=0.18,volume=0.8[n];"
         "[0][n]amix=inputs=2:normalize=0,alimiter=limit=0.7,aformat=sample_rates=48000:channel_layouts=stereo",
         path])


def build_audio(spec, base, dur, tmp):
    out = os.path.join(tmp, "audio.wav")
    inputs = ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo:d=%.3f" % dur]
    chains, labels = [], ["[0]"]
    sfx = spec.get("sfx") or []
    if sfx:
        tp = os.path.join(tmp, "thud.wav")
        thud_sfx(tp)
        for i, s in enumerate(sfx):
            inputs += ["-i", tp]
            ms = int(float(s["t"]) * 1000)
            vol = float(s.get("volume", 1.0))
            chains.append("[%d]adelay=%d|%d,volume=%.2f[s%d]" % (i + 1, ms, ms, vol, i))
            labels.append("[s%d]" % i)
    m = spec.get("music")
    if m:
        inputs += ["-i", os.path.join(base, m["file"])]
        idx = len(labels)
        db = float(m.get("volume_db", -20))
        chains.append("[%d]atrim=0:%.3f,volume=%.1fdB,afade=t=out:st=%.3f:d=1.0,aformat=sample_rates=48000:channel_layouts=stereo[m]"
                      % (idx, dur, db, max(0.0, dur - 1.0)))
        labels.append("[m]")
    graph = ";".join(chains + ["%samix=inputs=%d:normalize=0:duration=first,atrim=0:%.3f[out]" % ("".join(labels), len(labels), dur)])
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + inputs +
        ["-filter_complex", graph, "-map", "[out]", "-ar", "48000", "-ac", "2", out])
    return out


def render(spec_path, frames_at=None, check_only=False):
    spec_path = os.path.abspath(spec_path)
    base = os.path.dirname(spec_path)
    with open(spec_path) as fh:
        spec = json.load(fh)
    errors, warnings = validate(spec, base)
    report = {"spec": spec_path, "errors": errors, "warnings": warnings}
    if errors or check_only:
        print(json.dumps(report, indent=2))
        return 1 if errors else 0
    t0 = time.time()
    r = Renderer(spec, base)
    report["warnings"] += r.warnings
    if frames_at is not None:
        outs = []
        for t in frames_at:
            p = os.path.join(base, "preview_%06.2fs.png" % t)
            r.compose(t).save(p)
            outs.append(p)
        report["previews"] = outs
        print(json.dumps(report, indent=2))
        return 0
    out = os.path.join(base, spec.get("output", "final.mp4"))
    n = int(round(r.dur * r.fps))
    tmp = tempfile.mkdtemp(prefix="render_")
    try:
        audio = build_audio(spec, base, r.dur, tmp)
        cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
               "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (r.W, r.H), "-r", str(r.fps), "-i", "pipe:0",
               "-i", audio,
               "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
               "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
               "-movflags", "+faststart", "-shortest", out]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        for i in range(n):
            t = i / float(r.fps)
            p.stdin.write(r.compose(t).tobytes())
        p.stdin.close()
        err = p.stderr.read().decode(errors="ignore")
        if p.wait() != 0:
            raise SystemExit("ffmpeg encode failed:\n" + err[-2000:])
        cover_t = float(spec.get("cover_time", 0.6))
        cover = os.path.join(base, spec.get("cover", "cover.jpg"))
        r.compose(cover_t, loop=False).save(cover, quality=92)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    report.update({"output": out, "cover": cover, "frames": n, "seconds_to_render": round(time.time() - t0, 1)})
    with open(os.path.join(base, "render_report.json"), "w") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Render a build_spec.json into a vertical MP4")
    ap.add_argument("spec")
    ap.add_argument("--check", action="store_true", help="validate only")
    ap.add_argument("--frames", help="comma-separated times (seconds) to write preview PNGs instead of a video")
    a = ap.parse_args()
    fr = [float(x) for x in a.frames.split(",")] if a.frames else None
    sys.exit(render(a.spec, frames_at=fr, check_only=a.check))
