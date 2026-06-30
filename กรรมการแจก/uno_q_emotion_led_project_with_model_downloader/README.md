# UNO Q Emotion LED Matrix

โปรเจกต์นี้ใช้เว็บเบราว์เซอร์ถ่ายภาพ/ใช้กล้อง ตรวจจับอารมณ์ด้วย `face-api.js` แล้วส่งผลลัพธ์ไปยัง Arduino UNO Q เพื่อแสดงไอคอนบน LED Matrix ขนาด 13×8

## โครงสร้างไฟล์

```text
uno_q_emotion_led_project_with_model_downloader/
├─ app.yaml
├─ assets/
│  ├─ index.html
│  ├─ libs/
│  │  └─ face-api.min.js                      ← ต้องดาวน์โหลด
│  └─ models/
│     ├─ tiny_face_detector_model-weights_manifest.json  ← ต้องดาวน์โหลด
│     ├─ tiny_face_detector_model-shard1                 ← ต้องดาวน์โหลด
│     ├─ face_expression_model-weights_manifest.json      ← ต้องดาวน์โหลด
│     └─ face_expression_model-shard1                     ← ต้องดาวน์โหลด
├─ python/
│  └─ main.py
├─ sketch/
│  └─ sketch.ino
└─ scripts/
   ├─ download_assets.py
   ├─ download_assets.bat
   ├─ download_assets.sh
   └─ check_assets.py
```

## ขั้นตอนใช้งาน

### 1) ดาวน์โหลด library และ model files

ถ้าใช้ Windows ให้เปิด Command Prompt ใน project folder แล้วรัน:

```bat
scripts\download_assets.bat
```

ถ้าใช้ macOS, Linux หรือ terminal บน UNO Q:

```bash
python3 scripts/download_assets.py
```

ตรวจสอบไฟล์:

```bash
python3 scripts/check_assets.py
```

### 2) เปิดโปรเจกต์ใน Arduino App Lab

ตรวจสอบว่า `app.yaml` มี WebUI brick:

```yaml
bricks:
  - arduino:web_ui: {}
```

### 3) Run app

App Lab จะรันทั้ง:

- `python/main.py` บน Linux side
- `sketch/sketch.ino` บน STM32 MCU side
- `assets/index.html` เป็นหน้าเว็บ

### 4) เปิดหน้าเว็บ

```text
http://<UNO-Q-IP>:7000/
```

ทดสอบ API โดยตรง:

```text
http://<UNO-Q-IP>:7000/api/emotion?data=happy
http://<UNO-Q-IP>:7000/api/status
```

## หมายเหตุเรื่องกล้อง

เบราว์เซอร์บางตัวไม่อนุญาตให้ใช้กล้องผ่าน `http://<UNO-Q-IP>:7000` เพราะไม่ใช่ HTTPS ถ้าใช้กล้องไม่ได้ ให้ลอง:

1. เปิดจาก browser บน UNO Q โดยตรงที่ `http://localhost:7000`
2. ใช้ปุ่ม Upload image แทนกล้อง
3. ใช้ปุ่ม manual emotion เพื่อทดสอบ LED Matrix ก่อน

## อารมณ์ที่รองรับ

- neutral
- happy
- sad
- angry
- fearful
- disgusted
- surprised

## การไหลของข้อมูล

```text
Camera / uploaded image
→ face-api.js in browser
→ /api/emotion?data=<emotion>
→ Python WebUI API
→ Bridge.call("set_emotion", emotion)
→ C/C++ sketch
→ UNO Q LED Matrix
```

## Troubleshooting

ถ้า AI detect แล้ว LED Matrix ไม่เปลี่ยน:

1. เปิด `http://<UNO-Q-IP>:7000/api/emotion?data=happy`
2. ถ้ายังไม่เปลี่ยน ให้เช็คว่า sketch อัปโหลดแล้วหรือยัง
3. เช็คว่า C/C++ มีบรรทัดนี้:

```cpp
Bridge.provide_safe("set_emotion", set_emotion);
```

4. เช็คว่า Python เรียกชื่อเดียวกัน:

```python
Bridge.call("set_emotion", emotion)
```
