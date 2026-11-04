#!/usr/bin/env python3
"""
roadmap_render.py — Render a swimlane roadmap (SVG / HTML / PNG) from a TOML file.

Produces a swimlane roadmap: one swimlane per direction, one bar per work
package, laid over a weekly grid, with a today line, a shaded projection zone,
completion fill inside each bar, a per-issue progress sparkline, and milestone
markers.

Outputs, named after the `week` field in the data file:
  roadmap-<week>.svg   vector, for the vault and for embedding
  roadmap-<week>.html  standalone page: the same SVG plus a detail table
  roadmap-<week>.png   raster, for Slack (Slack does not preview SVG)

Usage:
  python3 _tools/roadmap_render.py \
      --data 03-projects/<project>/roadmap.toml \
      --out 10-reports/assets

  python3 _tools/roadmap_render.py --data <file> --formats svg,html
  python3 _tools/roadmap_render.py --data <file> --check

PNG rasterisation uses the first available of: rsvg-convert, magick, Chrome
or Chromium (headless). Pass --formats svg,html to skip it entirely.

Data format: see _templates/roadmap.toml.
"""

import argparse
import datetime as dt
import html
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

# ---------------------------------------------------------------- constants

STATUS = {
    "done": ("#1F7A4D", "#D6EFE0", "Done"),
    "active": ("#1F5FA8", "#D9E7F7", "In progress"),
    "planned": ("#6B7280", "#E7E9ED", "Planned"),
    "at-risk": ("#B45309", "#FBECD5", "At risk"),
    "paused": ("#6D28D9", "#E9E2FB", "Paused"),
}

INK = "#111827"
MUTED = "#4B5563"
FAINT = "#9CA3AF"
GRID = "#E5E7EB"
BAND = "#F3F4F6"
PROJECTION_BG = "#FAFAFA"
TODAY = "#DC2626"

FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"

PAD = 24
LEFT = 300          # name column
CW = 54             # week column
RIGHT = 156         # now% + sparkline column
MONTH_H = 22
WEEK_H = 30
MILESTONE_H = 50
ROW_H = 32
LANE_H = 30
LANE_GAP = 10
LEGEND_H = 64

CHART_TITLE_H = 54

# ------------------------------------------------------------------ helpers

WEEK_RE = re.compile(r"^(\d{4})-W(\d{1,2})$")


class DataError(Exception):
    pass


def parse_week(value, field):
    """'2026-W35' -> date of that ISO week's Monday."""
    if isinstance(value, dt.date):
        return iso_monday(value)
    m = WEEK_RE.match(str(value).strip())
    if not m:
        raise DataError(f"{field}: expected a week like '2026-W35', got {value!r}")
    year, week = int(m.group(1)), int(m.group(2))
    try:
        return dt.date.fromisocalendar(year, week, 1)
    except ValueError as exc:
        raise DataError(f"{field}: {value!r} is not a valid ISO week ({exc})") from exc


def parse_date(value, field):
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value).strip())
    except ValueError as exc:
        raise DataError(f"{field}: expected YYYY-MM-DD, got {value!r}") from exc


def iso_monday(d):
    return d - dt.timedelta(days=d.weekday())


def week_label(d):
    return f"W{d.isocalendar().week:02d}"


def fmt_day(d):
    """'5 Aug': day without zero padding, portable to Windows."""
    return f"{d.day} {d.strftime('%b')}"


def truncate(text, limit):
    text = str(text)
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def esc(text):
    return html.escape(str(text), quote=True)


# --------------------------------------------------------------- data model


class Package:
    def __init__(self, raw, lane_name, index):
        where = f"lane '{lane_name}' package #{index}"
        if "name" not in raw:
            raise DataError(f"{where}: missing 'name'")
        self.name = str(raw["name"])
        where = f"package '{self.name}'"
        self.start = parse_week(raw.get("start"), f"{where}.start")
        self.end = parse_week(raw.get("end"), f"{where}.end")
        if self.end < self.start:
            raise DataError(f"{where}: end {raw['end']} is before start {raw['start']}")
        self.status = str(raw.get("status", "planned"))
        if self.status not in STATUS:
            raise DataError(
                f"{where}: status {self.status!r} is not one of {', '.join(STATUS)}"
            )
        self.percent = max(0, min(100, int(raw.get("percent", 0))))
        self.done = raw.get("done")
        self.total = raw.get("total")
        self.note = str(raw.get("note", ""))
        self.projection = str(raw.get("projection", ""))
        self.history = [
            max(0, min(100, int(point.get("percent", 0))))
            for point in raw.get("history", [])
        ]

    @property
    def counts(self):
        if self.done is None or self.total is None:
            return ""
        return f"{self.done}/{self.total}"

    @property
    def now_label(self):
        counts = self.counts
        return f"{self.percent}%" + (f" ({counts})" if counts else "")


class Lane:
    def __init__(self, raw, index):
        if "name" not in raw:
            raise DataError(f"lane #{index}: missing 'name'")
        self.name = str(raw["name"])
        self.note = str(raw.get("note", ""))
        packages = raw.get("packages", [])
        if not packages:
            raise DataError(f"lane '{self.name}': has no [[lanes.packages]] entries")
        self.packages = [Package(p, self.name, i + 1) for i, p in enumerate(packages)]


class Roadmap:
    def __init__(self, raw):
        self.title = str(raw.get("title", "Roadmap"))
        self.subtitle = str(raw.get("subtitle", ""))
        self.week = str(raw.get("week", "")).strip()
        if not WEEK_RE.match(self.week):
            raise DataError("top level: 'week' is required, e.g. week = \"2026-W35\"")
        self.issue = raw.get("issue")
        self.epic = str(raw.get("epic", ""))
        self.epic_label = str(raw.get("epic_label", "Tracking epic"))
        horizon = raw.get("horizon")
        if not horizon or len(horizon) != 2:
            raise DataError(
                'top level: horizon = ["2026-W27", "2026-W40"] is required'
            )
        self.first = parse_week(horizon[0], "horizon[0]")
        self.last = parse_week(horizon[1], "horizon[1]")
        if self.last < self.first:
            raise DataError("horizon: second week is before the first")
        self.today = (
            parse_date(raw["today"], "today") if "today" in raw else dt.date.today()
        )
        self.lanes = [Lane(l, i + 1) for i, l in enumerate(raw.get("lanes", []))]
        if not self.lanes:
            raise DataError("no [[lanes]] found in the data file")
        self.milestones = [
            (str(m.get("name", "milestone")), parse_date(m.get("date"), "milestone.date"))
            for m in raw.get("milestones", [])
        ]
        self.weeks = []
        cur = self.first
        while cur <= self.last:
            self.weeks.append(cur)
            cur += dt.timedelta(days=7)

    def week_index(self, d):
        """Fractional column position of a date within the horizon."""
        monday = iso_monday(d)
        idx = (monday - self.first).days // 7
        return idx + d.weekday() / 7.0

    def clamp_index(self, value):
        return max(0.0, min(float(len(self.weeks)), value))


# ------------------------------------------------------------------- render


class SVG:
    def __init__(self):
        self.parts = []

    def add(self, markup):
        self.parts.append(markup)

    def rect(self, x, y, w, h, fill, rx=0, stroke=None, sw=1, opacity=None, extra=""):
        s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        o = f' opacity="{opacity}"' if opacity is not None else ""
        self.add(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w, 0):.1f}" '
            f'height="{h:.1f}" rx="{rx}" fill="{fill}"{s}{o}{extra}/>'
        )

    def line(self, x1, y1, x2, y2, stroke, sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}/>'
        )

    def text(self, x, y, content, size=12, fill=INK, weight="normal", anchor="start"):
        self.add(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">'
            f"{esc(content)}</text>"
        )


def render_svg(rm):
    n_weeks = len(rm.weeks)
    grid_w = n_weeks * CW
    width = PAD * 2 + LEFT + grid_w + RIGHT

    header_top = PAD + CHART_TITLE_H
    grid_top = header_top + MONTH_H + WEEK_H
    milestone_band = MILESTONE_H if rm.milestones else 0
    rows_top = grid_top + milestone_band

    # vertical layout of lanes and rows
    y = rows_top
    layout = []
    for lane in rm.lanes:
        lane_y = y
        y += LANE_H
        rows = []
        for pkg in lane.packages:
            rows.append((pkg, y))
            y += ROW_H
        layout.append((lane, lane_y, rows))
        y += LANE_GAP
    grid_bottom = y - LANE_GAP
    height = grid_bottom + LEGEND_H + PAD

    s = SVG()
    s.add(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height:.0f}" '
        f'viewBox="0 0 {width} {height:.0f}" role="img">'
    )
    s.add(
        '<defs><pattern id="proj" width="7" height="7" patternUnits="userSpaceOnUse" '
        'patternTransform="rotate(45)">'
        '<rect width="7" height="7" fill="#FFFFFF" fill-opacity="0"/>'
        '<line x1="0" y1="0" x2="0" y2="7" stroke="#FFFFFF" stroke-width="3.2" '
        'stroke-opacity="0.55"/></pattern></defs>'
    )
    s.rect(0, 0, width, height, "#FFFFFF")

    gx = PAD + LEFT
    today_x = gx + rm.clamp_index(rm.week_index(rm.today)) * CW

    # title block
    s.text(PAD, PAD + 18, rm.title, size=17, weight="bold")
    sub = rm.subtitle or (
        f"Issue #{rm.issue} · {rm.week}" if rm.issue else rm.week
    )
    s.text(PAD, PAD + 38, sub, size=12, fill=MUTED)

    # projection zone
    if today_x < gx + grid_w:
        s.rect(today_x, grid_top, gx + grid_w - today_x, grid_bottom - grid_top,
               PROJECTION_BG)

    # month band
    s.rect(gx, header_top, grid_w, MONTH_H, BAND)
    month_start = 0
    for i in range(n_weeks + 1):
        boundary = i == n_weeks or (
            i > 0 and rm.weeks[i].strftime("%b") != rm.weeks[month_start].strftime("%b")
        )
        if boundary:
            x0 = gx + month_start * CW
            x1 = gx + i * CW
            s.text((x0 + x1) / 2, header_top + 15,
                   rm.weeks[month_start].strftime("%B %Y"), size=11, fill=MUTED,
                   weight="bold", anchor="middle")
            if i < n_weeks:
                s.line(x1, header_top, x1, grid_bottom, "#D1D5DB", 1)
            month_start = i

    # week headers
    for i, monday in enumerate(rm.weeks):
        x = gx + i * CW
        s.text(x + CW / 2, header_top + MONTH_H + 13, week_label(monday), size=11,
               fill=INK, weight="bold", anchor="middle")
        s.text(x + CW / 2, header_top + MONTH_H + 25, fmt_day(monday),
               size=9, fill=FAINT, anchor="middle")
        s.line(x, header_top, x, grid_bottom, GRID, 1)
    s.line(gx + grid_w, header_top, gx + grid_w, grid_bottom, GRID, 1)
    s.line(gx, grid_top, gx + grid_w, grid_top, "#D1D5DB", 1)

    # milestones, labels staggered over two levels so neighbouring dates stay readable
    if rm.milestones:
        visible = [
            (n, d)
            for n, d in rm.milestones
            if rm.first <= d <= rm.last + dt.timedelta(days=6)
        ]
        visible.sort(key=lambda item: item[1])
        for i, (name, date) in enumerate(visible):
            mx = gx + rm.clamp_index(rm.week_index(date)) * CW
            my = grid_top + 13
            s.add(
                f'<path d="M {mx:.1f} {my - 7:.1f} L {mx + 7:.1f} {my:.1f} '
                f'L {mx:.1f} {my + 7:.1f} L {mx - 7:.1f} {my:.1f} Z" '
                f'fill="#111827"/>'
            )
            s.line(mx, my + 9, mx, grid_bottom, "#111827", 1, dash="2 4")
            label = f"{name} · {fmt_day(date)}"
            half = len(label) * 2.9
            anchor, tx = "middle", mx
            if mx - half < gx:
                anchor, tx = "start", gx + 2
            elif mx + half > gx + grid_w:
                anchor, tx = "end", gx + grid_w - 2
            s.text(tx, my + (22 if i % 2 == 0 else 36), label, size=10, fill=INK,
                   anchor=anchor)

    # lanes and bars
    for lane, lane_y, rows in layout:
        s.rect(PAD, lane_y, LEFT + grid_w + RIGHT, LANE_H - 4, BAND, rx=4)
        s.text(PAD + 10, lane_y + 18, lane.name.upper(), size=11, weight="bold",
               fill=INK)
        if lane.note:
            s.text(PAD + 10 + len(lane.name) * 7.6 + 14, lane_y + 18,
                   truncate(lane.note, 46), size=10, fill=MUTED)

        for pkg, row_y in rows:
            cy = row_y + ROW_H / 2
            s.line(PAD, row_y + ROW_H, PAD + LEFT + grid_w + RIGHT, row_y + ROW_H,
                   "#F3F4F6", 1)
            s.text(PAD + 18, cy + 4, truncate(pkg.name, 38), size=12, fill=INK)

            strong, light, _ = STATUS[pkg.status]
            i0 = (pkg.start - rm.first).days / 7.0
            i1 = (pkg.end - rm.first).days / 7.0 + 1
            x0 = gx + rm.clamp_index(i0) * CW + 3
            x1 = gx + rm.clamp_index(i1) * CW - 3
            bw = max(x1 - x0, 6)
            by, bh = cy - 9, 18

            s.rect(x0, by, bw, bh, light, rx=5, stroke=strong, sw=1, opacity=0.9)
            fill_end = x0 + bw * pkg.percent / 100.0
            if pkg.percent > 0:
                s.rect(x0, by, fill_end - x0, bh, strong, rx=5)
            # hatch what is both undone and in the future, never a completed stretch
            hatch_from = max(fill_end, today_x)
            if hatch_from < x1:
                s.rect(hatch_from, by, x1 - hatch_from, bh, "url(#proj)", rx=5)

            fill_w = bw * pkg.percent / 100.0
            if bw > 52:
                inside = fill_w > 52
                s.text(x0 + 9 if inside else x1 - 9, cy + 4, f"{pkg.percent}%",
                       size=10, fill="#FFFFFF" if inside else strong, weight="bold",
                       anchor="start" if inside else "end")

            # right column: now label + sparkline
            rx0 = gx + grid_w + 14
            s.text(rx0, cy + 4, pkg.now_label, size=11, weight="bold", fill=INK)
            if len(pkg.history) >= 2:
                sw, sh = 62, 14
                sx = rx0 + 74
                sy = cy - sh / 2
                step = sw / (len(pkg.history) - 1)
                pts = " ".join(
                    f"{sx + i * step:.1f},{sy + sh - (v / 100.0) * sh:.1f}"
                    for i, v in enumerate(pkg.history)
                )
                s.line(sx, sy + sh, sx + sw, sy + sh, GRID, 1)
                s.add(
                    f'<polyline points="{pts}" fill="none" stroke="{strong}" '
                    f'stroke-width="1.6" stroke-linejoin="round"/>'
                )
                last_v = pkg.history[-1]
                s.add(
                    f'<circle cx="{sx + sw:.1f}" '
                    f'cy="{sy + sh - (last_v / 100.0) * sh:.1f}" r="2.2" '
                    f'fill="{strong}"/>'
                )

    # today line, pill parked above the month band so it clears the week headers
    s.line(today_x, header_top - 6, today_x, grid_bottom, TODAY, 2)
    pill_x = min(max(today_x, gx + 26), gx + grid_w - 26)
    s.rect(pill_x - 26, header_top - 21, 52, 16, TODAY, rx=8)
    s.text(pill_x, header_top - 9, "today", size=10, fill="#FFFFFF", weight="bold",
           anchor="middle")

    # legend
    ly = grid_bottom + 26
    lx = PAD
    for key in ("done", "active", "planned", "at-risk", "paused"):
        strong, light, label = STATUS[key]
        s.rect(lx, ly - 9, 22, 12, light, rx=3, stroke=strong, sw=1)
        s.rect(lx, ly - 9, 13, 12, strong, rx=3)
        s.text(lx + 28, ly + 1, label, size=11, fill=MUTED)
        lx += 34 + len(label) * 6.6
    s.rect(lx, ly - 9, 22, 12, "#9CA3AF", rx=3)
    s.rect(lx, ly - 9, 22, 12, "url(#proj)", rx=3)
    s.text(lx + 28, ly + 1, "projected", size=11, fill=MUTED)
    lx += 34 + len("projected") * 6.6
    s.line(lx + 6, ly - 10, lx + 6, ly + 3, TODAY, 2)
    s.text(lx + 14, ly + 1, "today", size=11, fill=MUTED)

    s.text(PAD, ly + 22,
           "Bar spans the weeks the work package is scheduled for. Fill is completion. "
           "Hatched is not yet done. Sparkline is completion per snapshot.",
           size=10, fill=FAINT)

    s.add("</svg>")
    return "\n".join(s.parts)


def render_html(rm, svg):
    rows = []
    for lane in rm.lanes:
        rows.append(
            f'<tr class="lane"><th colspan="6">{esc(lane.name)}'
            + (f' <span>{esc(lane.note)}</span>' if lane.note else "")
            + "</th></tr>"
        )
        for p in lane.packages:
            strong, light, label = STATUS[p.status]
            window = (
                f"{week_label(p.start)}–{week_label(p.end)} "
                f"({fmt_day(p.start)} – "
                f"{fmt_day(p.end + dt.timedelta(days=6))})"
            )
            rows.append(
                "<tr>"
                f"<td>{esc(p.name)}</td>"
                f'<td><span class="pill" style="background:{light};color:{strong};'
                f'border-color:{strong}">{esc(label)}</span></td>'
                f"<td>{esc(window)}</td>"
                f'<td class="num">{esc(p.now_label)}</td>'
                f"<td>{esc(p.projection)}</td>"
                f"<td>{esc(p.note)}</td>"
                "</tr>"
            )
    milestones = "".join(
        f"<li><b>{esc(n)}</b> · {fmt_day(d) + f' {d.year}'}</li>" for n, d in rm.milestones
    )
    epic = (
        f'<p class="epic">📋 <a href="{esc(rm.epic)}">{esc(rm.epic_label)}</a></p>'
        if rm.epic
        else ""
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(rm.title)} · {esc(rm.week)}</title>
<style>
  :root {{ color-scheme: light; }}
  body {{ margin:0; padding:28px; background:#F9FAFB; color:{INK};
         font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
  .wrap {{ max-width:1400px; margin:0 auto; }}
  .card {{ background:#fff; border:1px solid {GRID}; border-radius:10px;
           padding:18px; margin-bottom:20px; overflow-x:auto; }}
  h1 {{ font-size:20px; margin:0 0 4px; }}
  h2 {{ font-size:14px; margin:0 0 14px; font-weight:600; color:{MUTED}; }}
  .epic {{ margin:0 0 16px; font-size:13px; }}
  a {{ color:#1F5FA8; }}
  table {{ border-collapse:collapse; width:100%; font-size:13px; }}
  th, td {{ text-align:left; padding:8px 10px; border-bottom:1px solid #F3F4F6;
            vertical-align:top; }}
  tr.lane th {{ background:{BAND}; font-size:11px; letter-spacing:.06em;
                text-transform:uppercase; border-bottom:1px solid {GRID}; }}
  tr.lane th span {{ text-transform:none; letter-spacing:0; font-weight:400;
                     color:{MUTED}; }}
  td.num {{ font-variant-numeric:tabular-nums; white-space:nowrap; }}
  .pill {{ display:inline-block; padding:1px 8px; border-radius:10px;
           border:1px solid; font-size:11px; font-weight:600; white-space:nowrap; }}
  ul {{ margin:0; padding-left:18px; font-size:13px; }}
  footer {{ font-size:11px; color:{FAINT}; }}
</style></head>
<body><div class="wrap">
  <h1>{esc(rm.title)}</h1>
  <h2>{esc(rm.subtitle or (f"Issue #{rm.issue} · {rm.week}" if rm.issue else rm.week))}
      · rendered {fmt_day(rm.today) + f' {rm.today.year}'}</h2>
  {epic}
  <div class="card">{svg}</div>
  <div class="card"><table>
    <tr><th>Work package</th><th>Status</th><th>Window</th><th>Now</th>
        <th>Projection</th><th>Note</th></tr>
    {''.join(rows)}
  </table></div>
  {f'<div class="card"><h2>Milestones</h2><ul>{milestones}</ul></div>' if milestones else ''}
  <footer>Generated by _tools/roadmap_render.py</footer>
</div></body></html>
"""


def write_png(svg_path, png_path, width):
    """Rasterise with whatever is installed. Returns the tool used, or None."""
    if shutil.which("rsvg-convert"):
        cmd = ["rsvg-convert", "-w", str(width * 2), "-b", "white",
               "-o", str(png_path), str(svg_path)]
        tool = "rsvg-convert"
    elif shutil.which("magick"):
        cmd = ["magick", "-density", "220", "-background", "white",
               str(svg_path), str(png_path)]
        tool = "magick"
    else:
        chrome = next(
            (
                c
                for c in (
                    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    shutil.which("google-chrome"),
                    shutil.which("chromium"),
                    shutil.which("chromium-browser"),
                )
                if c and Path(c).exists()
            ),
            None,
        )
        if chrome is None:
            return None
        cmd = [chrome, "--headless", "--disable-gpu", "--force-device-scale-factor=2",
               f"--screenshot={png_path}", f"--window-size={width},2000",
               str(svg_path)]
        tool = "chrome"
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"{tool} failed: {result.stderr.strip()[:400]}")
    return tool


# --------------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", required=True, help="roadmap TOML file")
    ap.add_argument("--out", default=".", help="output directory (default: cwd)")
    ap.add_argument("--name", help="output basename (default: roadmap-<week>)")
    ap.add_argument("--formats", default="svg,html,png",
                    help="comma list of svg,html,png (default: all)")
    ap.add_argument("--check", action="store_true",
                    help="validate the data file and print a summary, write nothing")
    args = ap.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        sys.exit(f"error: {data_path} not found")
    try:
        raw = tomllib.loads(data_path.read_text(encoding="utf-8"))
        rm = Roadmap(raw)
    except tomllib.TOMLDecodeError as exc:
        sys.exit(f"error: {data_path} is not valid TOML: {exc}")
    except DataError as exc:
        sys.exit(f"error: {exc}")

    n_pkgs = sum(len(l.packages) for l in rm.lanes)
    print(f"{rm.title}: {len(rm.lanes)} lanes, {n_pkgs} work packages, "
          f"{len(rm.weeks)} weeks {week_label(rm.first)}–{week_label(rm.last)}, "
          f"today {rm.today}")
    for lane in rm.lanes:
        for p in lane.packages:
            if p.end < rm.today and p.percent < 100:
                print(f"  warning: '{p.name}' ends {week_label(p.end)}, in the past, "
                      f"still at {p.percent}%")
            if p.percent == 100 and p.status != "done":
                print(f"  warning: '{p.name}' is at 100% but status is {p.status!r}")
    if args.check:
        return

    formats = {f.strip() for f in args.formats.split(",") if f.strip()}
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    base = args.name or f"roadmap-{rm.week}"

    svg = render_svg(rm)
    svg_path = out_dir / f"{base}.svg"
    width = PAD * 2 + LEFT + len(rm.weeks) * CW + RIGHT

    if "svg" in formats or "png" in formats:
        svg_path.write_text(svg, encoding="utf-8")
        if "svg" in formats:
            print(f"wrote {svg_path}")
    if "html" in formats:
        html_path = out_dir / f"{base}.html"
        html_path.write_text(render_html(rm, svg), encoding="utf-8")
        print(f"wrote {html_path}")
    if "png" in formats:
        png_path = out_dir / f"{base}.png"
        tool = write_png(svg_path, png_path, width)
        if tool is None:
            print("warning: no rasteriser found (rsvg-convert, magick, Chrome/Chromium), "
                  "skipped PNG")
        else:
            print(f"wrote {png_path} (via {tool})")
        if "svg" not in formats:
            svg_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
