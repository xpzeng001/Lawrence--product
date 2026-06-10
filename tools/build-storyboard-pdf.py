from __future__ import annotations

import math
import subprocess
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
VIDEO = ROOT / "renders" / "Lawrence-销售演示视频_2026-06-02_17-17-01.mp4"
OUT_DIR = ROOT / "outputs" / "storyboard-complete-frames"
FRAMES_DIR = OUT_DIR / "frames"
PDF_PATH = OUT_DIR / "Lawrence-分镜完整画面整理.pdf"


SEGMENTS = [
    {"id": "s01-opening", "title": "S1 开场：Lawrence 亮相", "start": 0.0, "end": 15.1, "count": 4},
    {"id": "s02-digital-worker", "title": "S2 不是聊天框，是数字员工", "start": 15.1, "end": 36.1, "count": 6},
    {"id": "s03-identity-access", "title": "S3 企业身份与入口接入", "start": 36.25, "end": 54.0, "count": 6},
    {"id": "s04-task-brief", "title": "S4 任务交代：语音、文件、文字", "start": 56.95, "end": 73.15, "count": 6},
    {"id": "s05-task-flow", "title": "S5 任务拆解与可审核交付", "start": 72.15, "end": 87.75, "count": 6},
    {"id": "s06-workstation", "title": "S6 数字工位：工具与记忆连接", "start": 87.15, "end": 99.15, "count": 4},
    {"id": "s07-secure-workspace", "title": "S7 安全工作区与企业内运行", "start": 100.15, "end": 134.15, "count": 6},
    {"id": "s08-capability-bridge", "title": "S8 专业技能承接：从法律到管理", "start": 135.15, "end": 161.25, "count": 6},
    {"id": "s09-capability-intro", "title": "S9 专业技能章节开场", "start": 162.25, "end": 167.25, "count": 3},
    {"id": "s10-legal-compliance", "title": "S10 法律合规能力", "start": 167.25, "end": 192.25, "count": 6},
    {"id": "s11-management-marketing", "title": "S11 管理执行与营销增长", "start": 192.25, "end": 234.25, "count": 6},
    {"id": "s12-capability-closing", "title": "S12 专业能力章节收尾", "start": 234.25, "end": 240.25, "count": 3},
    {"id": "s13-global-expansion", "title": "S13 企业出海 / 资源连接", "start": 240.25, "end": 255.25, "count": 5},
    {"id": "s14-wiseskill-hub", "title": "S14 WiseSkill Hub", "start": 255.25, "end": 272.25, "count": 6},
    {"id": "s15-enablement", "title": "S15 课程培训与场景陪跑", "start": 273.65, "end": 296.15, "count": 6},
]


def register_font() -> str:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            pdfmetrics.registerFont(TTFont("CJK", path))
            return "CJK"
    return "Helvetica"


def sample_times(start: float, end: float, count: int) -> list[float]:
    duration = end - start
    if count <= 1:
        return [start + duration * 0.5]
    padding = min(0.75, max(0.18, duration * 0.08))
    inner_start = start + padding
    inner_end = end - padding
    if inner_end <= inner_start:
        inner_start, inner_end = start, end
    return [inner_start + (inner_end - inner_start) * i / (count - 1) for i in range(count)]


def extract_frame(time_s: float, output: Path) -> None:
    if output.exists() and output.stat().st_size > 0:
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            f"{time_s:.3f}",
            "-i",
            str(VIDEO),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(output),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def draw_cover(pdf: canvas.Canvas, font: str, page_w: float, page_h: float) -> None:
    pdf.setFillColor(colors.HexColor("#f6f1ea"))
    pdf.rect(0, 0, page_w, page_h, stroke=0, fill=1)
    pdf.setFillColor(colors.HexColor("#261f1b"))
    pdf.setFont(font, 28)
    pdf.drawString(28 * mm, page_h - 48 * mm, "Lawrence 销售演示视频")
    pdf.setFont(font, 18)
    pdf.drawString(28 * mm, page_h - 62 * mm, "分镜完整画面整理")
    pdf.setStrokeColor(colors.HexColor("#d3422e"))
    pdf.setLineWidth(2)
    pdf.line(28 * mm, page_h - 72 * mm, page_w - 28 * mm, page_h - 72 * mm)
    pdf.setFillColor(colors.HexColor("#6d625c"))
    pdf.setFont(font, 11)
    pdf.drawString(28 * mm, page_h - 86 * mm, f"来源：{VIDEO.relative_to(ROOT)}")
    pdf.drawString(28 * mm, page_h - 94 * mm, f"视频规格：1920×1080 / 30fps / 299.7s")
    pdf.drawString(28 * mm, page_h - 102 * mm, f"分镜页数：{len(SEGMENTS)}")
    pdf.showPage()


def draw_segment_page(
    pdf: canvas.Canvas,
    font: str,
    page_w: float,
    page_h: float,
    segment: dict,
    frame_paths: list[Path],
    times: list[float],
    page_num: int,
) -> None:
    margin_x = 16 * mm
    margin_top = 13 * mm
    margin_bottom = 12 * mm
    header_h = 18 * mm
    gap = 4 * mm

    pdf.setFillColor(colors.white)
    pdf.rect(0, 0, page_w, page_h, stroke=0, fill=1)

    pdf.setFillColor(colors.HexColor("#241f1a"))
    pdf.setFont(font, 15)
    pdf.drawString(margin_x, page_h - margin_top, segment["title"])
    pdf.setFillColor(colors.HexColor("#786d66"))
    pdf.setFont(font, 8.5)
    pdf.drawRightString(
        page_w - margin_x,
        page_h - margin_top,
        f'{segment["start"]:.2f}s - {segment["end"]:.2f}s',
    )
    pdf.setStrokeColor(colors.HexColor("#d9cfc5"))
    pdf.setLineWidth(0.7)
    pdf.line(margin_x, page_h - margin_top - 6 * mm, page_w - margin_x, page_h - margin_top - 6 * mm)

    count = len(frame_paths)
    cols = 3 if count > 4 else 2
    rows = math.ceil(count / cols)
    grid_top = page_h - margin_top - header_h
    grid_h = grid_top - margin_bottom
    cell_w = (page_w - 2 * margin_x - (cols - 1) * gap) / cols
    cell_h = (grid_h - (rows - 1) * gap) / rows

    for i, frame_path in enumerate(frame_paths):
        row = i // cols
        col = i % cols
        x = margin_x + col * (cell_w + gap)
        y = margin_bottom + (rows - 1 - row) * (cell_h + gap)

        with Image.open(frame_path) as img:
            img_w, img_h = img.size
        label_h = 5 * mm
        available_h = cell_h - label_h
        scale = min(cell_w / img_w, available_h / img_h)
        draw_w = img_w * scale
        draw_h = img_h * scale
        img_x = x + (cell_w - draw_w) / 2
        img_y = y + label_h + (available_h - draw_h) / 2

        pdf.setFillColor(colors.HexColor("#f4efe8"))
        pdf.roundRect(x, y, cell_w, cell_h, 2.2 * mm, stroke=0, fill=1)
        pdf.drawImage(str(frame_path), img_x, img_y, draw_w, draw_h, preserveAspectRatio=True, anchor="c")
        pdf.setFillColor(colors.HexColor("#4f4640"))
        pdf.setFont(font, 7.3)
        pdf.drawString(x + 2 * mm, y + 1.8 * mm, f"Frame {i + 1} · {times[i]:.2f}s")

    pdf.setFillColor(colors.HexColor("#9a8e84"))
    pdf.setFont(font, 7)
    pdf.drawRightString(page_w - margin_x, 7 * mm, f"{page_num:02d}")
    pdf.showPage()


def main() -> None:
    if not VIDEO.exists():
        raise FileNotFoundError(VIDEO)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)

    font = register_font()
    page_w, page_h = landscape(A4)

    frame_manifest: list[tuple[dict, list[Path], list[float]]] = []
    for segment in SEGMENTS:
        times = sample_times(segment["start"], segment["end"], segment["count"])
        frame_paths = []
        for idx, time_s in enumerate(times, start=1):
            frame_path = FRAMES_DIR / f'{segment["id"]}_{idx:02d}_{time_s:07.3f}s.jpg'
            extract_frame(time_s, frame_path)
            frame_paths.append(frame_path)
        frame_manifest.append((segment, frame_paths, times))

    pdf = canvas.Canvas(str(PDF_PATH), pagesize=(page_w, page_h))
    pdf.setTitle("Lawrence 分镜完整画面整理")
    draw_cover(pdf, font, page_w, page_h)

    for page_num, (segment, frame_paths, times) in enumerate(frame_manifest, start=1):
        draw_segment_page(pdf, font, page_w, page_h, segment, frame_paths, times, page_num)

    pdf.save()

    print(PDF_PATH)


if __name__ == "__main__":
    main()
