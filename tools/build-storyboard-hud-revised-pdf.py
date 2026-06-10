from __future__ import annotations

from pathlib import Path

from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
BASE_FRAMES = ROOT / "outputs" / "storyboard-complete-frames" / "frames"
DENSE_FRAMES = ROOT / "outputs" / "storyboard-hud-full-frames" / "qa-professional"
OUT_DIR = ROOT / "outputs" / "storyboard-hud-revised-full-frames"
PDF_PATH = OUT_DIR / "Lawrence-分镜完整画面_16x9带HUD完成态修订版.pdf"

PAGE_W = 1920
PAGE_H = 1080


FRAME_NAMES = [
    # 01 Professional digital worker
    "base:s02-digital-worker_02_019.750s.jpg",
    "base:s02-digital-worker_03_023.650s.jpg",
    "base:s02-digital-worker_04_027.550s.jpg",
    # 02 Identity & access
    "base:s03-identity-access_01_037.000s.jpg",
    "base:s03-identity-access_02_040.250s.jpg",
    "base:s03-identity-access_04_046.750s.jpg",
    # 03 Task flow, replace partial frames with denser complete states
    "dense:frame_0063.50.jpg",
    "dense:frame_0066.50.jpg",
    "dense:frame_0068.00.jpg",
    "dense:frame_0069.50.jpg",
    "dense:frame_0074.00.jpg",
    "dense:frame_0075.50.jpg",
    "dense:frame_0077.00.jpg",
    "dense:frame_0078.50.jpg",
    "dense:frame_0080.00.jpg",
    "dense:frame_0081.50.jpg",
    "dense:frame_0083.00.jpg",
    "dense:frame_0084.50.jpg",
    # 04 Secure workspace
    "base:s06-workstation_02_091.400s.jpg",
    "base:s06-workstation_03_094.900s.jpg",
    "base:s07-secure-workspace_02_107.400s.jpg",
    "base:s07-secure-workspace_03_113.900s.jpg",
    "base:s07-secure-workspace_04_120.400s.jpg",
    "base:s07-secure-workspace_05_126.900s.jpg",
    "dense:frame_0128.00.jpg",
    "dense:frame_0129.50.jpg",
    "dense:frame_0131.00.jpg",
    # 04/05 bridge
    "base:s08-capability-bridge_01_135.900s.jpg",
    "base:s08-capability-bridge_02_140.820s.jpg",
    "base:s08-capability-bridge_03_145.740s.jpg",
    "base:s08-capability-bridge_04_150.660s.jpg",
    "base:s08-capability-bridge_05_155.580s.jpg",
    # 05 Professional skills intro and legal/compliance
    "dense:frame_0163.50.jpg",
    "dense:frame_0165.00.jpg",
    "dense:frame_0166.50.jpg",
    "dense:frame_0169.50.jpg",
    "dense:frame_0171.00.jpg",
    "dense:frame_0174.00.jpg",
    "dense:frame_0175.50.jpg",
    "dense:frame_0180.00.jpg",
    "dense:frame_0181.50.jpg",
    "dense:frame_0184.50.jpg",
    "dense:frame_0186.00.jpg",
    "dense:frame_0189.00.jpg",
    "dense:frame_0190.50.jpg",
    "dense:frame_0192.00.jpg",
    # 05 Management and marketing
    "dense:frame_0193.50.jpg",
    "dense:frame_0195.00.jpg",
    "dense:frame_0196.50.jpg",
    "dense:frame_0199.50.jpg",
    "dense:frame_0201.00.jpg",
    "dense:frame_0204.00.jpg",
    "dense:frame_0205.50.jpg",
    "dense:frame_0210.00.jpg",
    "dense:frame_0211.50.jpg",
    "dense:frame_0216.00.jpg",
    "dense:frame_0219.00.jpg",
    "dense:frame_0220.50.jpg",
    "dense:frame_0223.50.jpg",
    "dense:frame_0225.00.jpg",
    "dense:frame_0226.50.jpg",
    "dense:frame_0229.50.jpg",
    "dense:frame_0231.00.jpg",
    "dense:frame_0232.50.jpg",
    "dense:frame_0237.00.jpg",
    "dense:frame_0238.50.jpg",
    "dense:frame_0240.00.jpg",
    # 06 Global expansion
    "base:s13-global-expansion_03_247.750s.jpg",
    "base:s13-global-expansion_04_251.125s.jpg",
    "base:s13-global-expansion_05_254.500s.jpg",
    # 07 WiseSkill Hub
    "base:s14-wiseskill-hub_02_259.100s.jpg",
    "base:s14-wiseskill-hub_03_262.200s.jpg",
    "base:s14-wiseskill-hub_04_265.300s.jpg",
    "base:s14-wiseskill-hub_05_268.400s.jpg",
    # 08 Enablement
    "dense:frame_0276.00.jpg",
    "dense:frame_0277.50.jpg",
    "dense:frame_0279.00.jpg",
    "dense:frame_0280.50.jpg",
    "dense:frame_0282.00.jpg",
    "dense:frame_0283.50.jpg",
    "dense:frame_0286.50.jpg",
    "dense:frame_0289.50.jpg",
    "dense:frame_0292.50.jpg",
    "dense:frame_0294.00.jpg",
    "dense:frame_0295.50.jpg",
]


def resolve_frame(name: str) -> Path:
    prefix, filename = name.split(":", 1)
    base = BASE_FRAMES if prefix == "base" else DENSE_FRAMES
    path = base / filename
    if not path.exists():
        raise FileNotFoundError(path)
    return path


def main() -> None:
    frames = [resolve_frame(name) for name in FRAME_NAMES]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "selected-frames.txt").write_text(
        "\n".join(str(frame.relative_to(ROOT)) for frame in frames) + "\n",
        encoding="utf-8",
    )

    pdf = canvas.Canvas(str(PDF_PATH), pagesize=(PAGE_W, PAGE_H))
    pdf.setTitle("Lawrence 分镜完整画面 16x9 带HUD完成态修订版")
    for frame in frames:
        pdf.drawImage(str(frame), 0, 0, PAGE_W, PAGE_H, preserveAspectRatio=True, anchor="c")
        pdf.showPage()
    pdf.save()
    print(PDF_PATH)
    print(f"{len(frames)} pages")


if __name__ == "__main__":
    main()
