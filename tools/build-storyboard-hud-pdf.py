from __future__ import annotations

from pathlib import Path

from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
FRAMES_DIR = ROOT / "outputs" / "storyboard-complete-frames" / "frames"
OUT_DIR = ROOT / "outputs" / "storyboard-hud-full-frames"
PDF_PATH = OUT_DIR / "Lawrence-分镜完整画面_16x9带HUD完成态版.pdf"

PAGE_W = 1920
PAGE_H = 1080

# 1-based positions in the sorted extracted-frame list.
# Keep only fully composed frames that retain the on-screen HUD/chapter chrome.
KEEP_INDEXES = [
    6, 7, 8,
    12, 14,
    18, 20, 21, 24, 25, 26, 27,
    30, 31,
    34, 35, 36, 37,
    39, 40, 41, 42, 43,
    46, 47,
    52, 53, 55, 56, 58, 59,
    61, 62,
    65, 66, 67,
    69, 70, 71, 72,
    75, 76, 77,
]


def main() -> None:
    frames = sorted(FRAMES_DIR.glob("*.jpg"))
    if not frames:
        raise FileNotFoundError(f"No storyboard frames found in {FRAMES_DIR}")

    selected = []
    for index in KEEP_INDEXES:
        if index < 1 or index > len(frames):
            raise IndexError(f"Frame index out of range: {index}")
        selected.append(frames[index - 1])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "selected-frames.txt").write_text(
        "\n".join(frame.name for frame in selected) + "\n",
        encoding="utf-8",
    )

    pdf = canvas.Canvas(str(PDF_PATH), pagesize=(PAGE_W, PAGE_H))
    pdf.setTitle("Lawrence 分镜完整画面 16x9 带HUD完成态版")
    for frame in selected:
        pdf.drawImage(str(frame), 0, 0, PAGE_W, PAGE_H, preserveAspectRatio=True, anchor="c")
        pdf.showPage()
    pdf.save()

    print(PDF_PATH)
    print(f"{len(selected)} pages")


if __name__ == "__main__":
    main()
