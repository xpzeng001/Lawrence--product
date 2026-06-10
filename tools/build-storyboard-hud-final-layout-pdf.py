from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs/storyboard-complete-frames/frames"
DENSE = ROOT / "outputs/storyboard-hud-full-frames/qa-professional"
OUT = ROOT / "outputs/storyboard-hud-final-layouts"
PDF = OUT / "Lawrence-分镜完整画面_16x9带HUD最终布局版.pdf"
PAGE_W, PAGE_H = 1920, 1080


FRAMES = [
    # 01 不是软件，是新同事
    "base:s02-digital-worker_02_019.750s.jpg",
    "base:s02-digital-worker_03_023.650s.jpg",
    "base:s02-digital-worker_04_027.550s.jpg",
    # 02 数字员工身份
    "base:s03-identity-access_01_037.000s.jpg",
    "base:s03-identity-access_02_040.250s.jpg",
    "base:s03-identity-access_04_046.750s.jpg",
    # 03 任务接收与执行
    "dense:frame_0069.50.jpg",
    "dense:frame_0080.00.jpg",
    "dense:frame_0081.50.jpg",
    "dense:frame_0084.50.jpg",
    # 04 安全工作区
    "base:s06-workstation_03_094.900s.jpg",
    "base:s07-secure-workspace_02_107.400s.jpg",
    "base:s07-secure-workspace_03_113.900s.jpg",
    "base:s07-secure-workspace_04_120.400s.jpg",
    "base:s07-secure-workspace_05_126.900s.jpg",
    "dense:frame_0131.00.jpg",
    # 04 -> 05 能力承接
    "base:s08-capability-bridge_01_135.900s.jpg",
    "base:s08-capability-bridge_02_140.820s.jpg",
    "base:s08-capability-bridge_03_145.740s.jpg",
    "base:s08-capability-bridge_04_150.660s.jpg",
    "base:s08-capability-bridge_05_155.580s.jpg",
    # 05 专业技能：法律合规
    "dense:frame_0166.50.jpg",
    "dense:frame_0171.00.jpg",
    "dense:frame_0175.50.jpg",
    "dense:frame_0181.50.jpg",
    "dense:frame_0186.00.jpg",
    "dense:frame_0192.00.jpg",
    # 05 专业技能：战略管理 / 管理执行
    "dense:frame_0196.50.jpg",
    "dense:frame_0201.00.jpg",
    "dense:frame_0205.50.jpg",
    "dense:frame_0211.50.jpg",
    # 05 专业技能：营销增长
    "dense:frame_0216.00.jpg",
    "dense:frame_0220.50.jpg",
    "dense:frame_0225.00.jpg",
    "dense:frame_0226.50.jpg",
    "dense:frame_0232.50.jpg",
    "dense:frame_0238.50.jpg",
    # 06 企业出海 / 资源连接
    "base:s13-global-expansion_03_247.750s.jpg",
    "base:s13-global-expansion_04_251.125s.jpg",
    "base:s13-global-expansion_05_254.500s.jpg",
    # 07 WiseSkill Hub
    "base:s14-wiseskill-hub_02_259.100s.jpg",
    "base:s14-wiseskill-hub_03_262.200s.jpg",
    "base:s14-wiseskill-hub_04_265.300s.jpg",
    "base:s14-wiseskill-hub_05_268.400s.jpg",
    # 08 课程与陪跑
    "dense:frame_0277.50.jpg",
    "dense:frame_0280.50.jpg",
    "dense:frame_0283.50.jpg",
    "dense:frame_0286.50.jpg",
    "dense:frame_0289.50.jpg",
    "dense:frame_0292.50.jpg",
    "dense:frame_0295.50.jpg",
]


HUD_OVERRIDES = {
    # These task-flow captures are complete layouts from the rendered video, but
    # the video frame itself does not carry the section HUD. Add it at export.
    6: ("03", "TASK FLOW", "任务接收与执行", "语音任务 · 文件处理 · 结果返回"),
    7: ("03", "TASK FLOW", "任务接收与执行", "语音任务 · 文件处理 · 结果返回"),
    8: ("03", "TASK FLOW", "任务接收与执行", "语音任务 · 文件处理 · 结果返回"),
    9: ("03", "TASK FLOW", "任务接收与执行", "语音任务 · 文件处理 · 结果返回"),
}


def resolve(spec: str) -> Path:
    prefix, name = spec.split(":", 1)
    path = (BASE if prefix == "base" else DENSE) / name
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def draw_hud(pdf: canvas.Canvas, hud: tuple[str, str, str, str]) -> None:
    number, eyebrow, title, subtitle = hud
    try:
        pdf.setFillAlpha(0.92)
        pdf.setStrokeAlpha(0.92)
    except AttributeError:
        pass

    pdf.setFillColor(colors.HexColor("#f7f2ee"))
    pdf.setStrokeColor(colors.HexColor("#dccfc7"))
    pdf.setLineWidth(2)
    pdf.circle(148, 950, 18, stroke=1, fill=1)

    pdf.setFillColor(colors.HexColor("#9b6b5b"))
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawCentredString(148, 945, number)

    pdf.setFillColor(colors.HexColor("#8f6658"))
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(182, 962, eyebrow)

    pdf.setFillColor(colors.HexColor("#1f1c1a"))
    pdf.setFont("STSong-Light", 23)
    pdf.drawString(182, 935, title)

    pdf.setFillColor(colors.HexColor("#6e625c"))
    pdf.setFont("STSong-Light", 11)
    pdf.drawString(182, 912, subtitle)

    pdf.setStrokeColor(colors.HexColor("#9b6b5b"))
    pdf.setLineWidth(2)
    pdf.line(462, 956, 625, 956)
    pdf.setStrokeColor(colors.HexColor("#62b98f"))
    pdf.line(625, 956, 822, 956)
    pdf.setStrokeColor(colors.HexColor("#e8e1dc"))
    pdf.line(822, 956, 955, 956)

    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 33)
    pdf.drawRightString(1745, 935, "WiseLaw")

    try:
        pdf.setFillAlpha(1)
        pdf.setStrokeAlpha(1)
    except AttributeError:
        pass


def main() -> None:
    frames = [resolve(spec) for spec in FRAMES]
    OUT.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    (OUT / "selected-frames.txt").write_text(
        "\n".join(str(frame.relative_to(ROOT)) for frame in frames) + "\n",
        encoding="utf-8",
    )
    pdf = canvas.Canvas(str(PDF), pagesize=(PAGE_W, PAGE_H))
    pdf.setTitle("Lawrence 分镜完整画面 16x9 带HUD最终布局版")
    for index, frame in enumerate(frames):
        pdf.drawImage(str(frame), 0, 0, PAGE_W, PAGE_H, preserveAspectRatio=True, anchor="c")
        if index in HUD_OVERRIDES:
            draw_hud(pdf, HUD_OVERRIDES[index])
        pdf.showPage()
    pdf.save()
    print(PDF)
    print(f"{len(frames)} pages")


if __name__ == "__main__":
    main()
