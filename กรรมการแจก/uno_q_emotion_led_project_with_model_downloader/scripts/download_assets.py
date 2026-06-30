#!/usr/bin/env python3
"""Download local face-api.js library and required model files.
Run from the project root:
    python scripts/download_assets.py
"""
from pathlib import Path
from urllib.request import urlretrieve

FILES = {
    "assets/libs/face-api.min.js": "https://cdn.jsdelivr.net/gh/justadudewhohacks/face-api.js@0.22.2/dist/face-api.min.js",
    "assets/models/tiny_face_detector_model-weights_manifest.json": "https://cdn.jsdelivr.net/gh/justadudewhohacks/face-api.js@0.22.2/weights/tiny_face_detector_model-weights_manifest.json",
    "assets/models/tiny_face_detector_model-shard1": "https://cdn.jsdelivr.net/gh/justadudewhohacks/face-api.js@0.22.2/weights/tiny_face_detector_model-shard1",
    "assets/models/face_expression_model-weights_manifest.json": "https://cdn.jsdelivr.net/gh/justadudewhohacks/face-api.js@0.22.2/weights/face_expression_model-weights_manifest.json",
    "assets/models/face_expression_model-shard1": "https://cdn.jsdelivr.net/gh/justadudewhohacks/face-api.js@0.22.2/weights/face_expression_model-shard1",
}

root = Path(__file__).resolve().parents[1]
for rel, url in FILES.items():
    out = root / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {rel}")
    print(f"  from {url}")
    urlretrieve(url, out)
    print(f"  saved {out} ({out.stat().st_size} bytes)")

print("Done. You can now run the Arduino App Lab project.")
