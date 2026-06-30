# Required face-api.js files for UNO Q Emotion LED Matrix

This project uses browser-side AI inference with `face-api.js`.
You must place the JavaScript library and model weights in `assets/`.

## Exact files to download

| Destination in this project | Direct download URL |
|---|---|
| `assets/libs/face-api.min.js` | `https://cdn.jsdelivr.net/gh/justadudewhohacks/face-api.js@0.22.2/dist/face-api.min.js` |
| `assets/models/tiny_face_detector_model-weights_manifest.json` | `https://cdn.jsdelivr.net/gh/justadudewhohacks/face-api.js@0.22.2/weights/tiny_face_detector_model-weights_manifest.json` |
| `assets/models/tiny_face_detector_model-shard1` | `https://cdn.jsdelivr.net/gh/justadudewhohacks/face-api.js@0.22.2/weights/tiny_face_detector_model-shard1` |
| `assets/models/face_expression_model-weights_manifest.json` | `https://cdn.jsdelivr.net/gh/justadudewhohacks/face-api.js@0.22.2/weights/face_expression_model-weights_manifest.json` |
| `assets/models/face_expression_model-shard1` | `https://cdn.jsdelivr.net/gh/justadudewhohacks/face-api.js@0.22.2/weights/face_expression_model-shard1` |

## Automatic download

From the project root, run one of these commands:

### Windows

```bat
scripts\download_assets.bat
```

or:

```bat
python scripts\download_assets.py
```

### macOS / Linux / UNO Q terminal

```bash
python3 scripts/download_assets.py
```

Then check the files:

```bash
python3 scripts/check_assets.py
```

## Why these files?

- `face-api.min.js` is the browser-side face-api.js library.
- `tiny_face_detector_*` detects the face location.
- `face_expression_model_*` classifies the expression/emotion.

The project sends only the final emotion label to the UNO Q Python API.
The face image is processed inside the browser.
