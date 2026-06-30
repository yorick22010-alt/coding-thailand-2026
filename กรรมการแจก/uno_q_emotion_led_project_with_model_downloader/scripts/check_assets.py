#!/usr/bin/env python3
from pathlib import Path

required = [
    "assets/libs/face-api.min.js",
    "assets/models/tiny_face_detector_model-weights_manifest.json",
    "assets/models/tiny_face_detector_model-shard1",
    "assets/models/face_expression_model-weights_manifest.json",
    "assets/models/face_expression_model-shard1",
]
root = Path(__file__).resolve().parents[1]
ok = True
for rel in required:
    p = root / rel
    if p.exists() and p.stat().st_size > 100:
        print(f"OK      {rel}  {p.stat().st_size} bytes")
    else:
        print(f"MISSING {rel}")
        ok = False
raise SystemExit(0 if ok else 1)
