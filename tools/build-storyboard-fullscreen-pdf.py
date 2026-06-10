from __future__ import annotations

from pathlib import Path

from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
FRAMES_DIR = ROOT / "outputs" / "storyboard-complete-frames" / "frames"
OUT_DIR = ROOT / "outputs" / "storyboard-fullscreen-pages"
PDF_PATH = OUT_DIR / "Lawrence-分镜完整画面_16x9逐页版.pdf"

PAGE_W = 1920
PAGE_H = 1080


def main() -> None:
    frames = sorted(FRAMES_DIR.glob("*.jpg"))
    if not frames:
        raise FileNotFoundError(f"No storyboard frames found in {FRAMES_DIR}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(PDF_PATH), pagesize=(PAGE_W, PAGE_H))
    pdf.setTitle("Lawrence 分镜完整画面 16x9 逐页版")

    for frame in frames:
        pdf.drawImage(str(frame), 0, 0, PAGE_W, PAGE_H, preserveAspectRatio=True, anchor="c")
        pdf.showPage()

    pdf.save()
    print(PDF_PATH)
    print(f"{len(frames)} pages")


if __name__ == "__main__":
    main()
