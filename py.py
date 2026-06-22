# Smart Parking & Obstacle Monitor - Python side
# Python side: WebUI + REST API + RouterBridge to the MCU.
#
# Data flow:
# Browser Webcam -> Detection -> /api/status?data=warning
# -> Python receives status -> Bridge.call("set_status", status)
# -> Arduino C/C++ sketch updates the LED matrix.

from arduino.app_utils import App, Bridge
from arduino.app_bricks.web_ui import WebUI
from fastapi import Request
import os
import time

# ค้นหาตำแหน่งโฟลเดอร์ assets เพื่อดึงไฟล์ index.html ขึ้นมาแสดงผล
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ASSETS_DIR = os.path.join(APP_DIR, "assets")
ui = WebUI(assets_dir_path=ASSETS_DIR)

# กำหนดสถานะความปลอดภัยที่ระบบยอมรับ
VALID_STATUSES = {
    "normal",   # ปลอดภัย/ปกติ
    "warning",  # เริ่มเตือนภัย (ตรวจเจอวัตถุ/รถ)
    "danger",   # อันตรายร้ายแรง (จอดแช่เกินเวลา)
}

latest_state = {
    "status": "normal",
    "updated_at": time.time(),
    "bridge_ok": False,
    "bridge_result": None,
    "error": None,
}

def send_status_to_mcu(status_string: str):
    """เรียกใช้งานฟังก์ชัน set_status ที่ถูกเขียนไว้บนฝั่งบอร์ด Arduino"""
    try:
        # สั่งยิงข้อมูลข้ามฝั่งผ่านระบบ RouterBridge 
        result = Bridge.call("set_status", status_string)
        return True, str(result), None
    except Exception as exc:
        print(f"[Bridge] ไม่สามารถส่งสถานะไปที่บอร์ดได้: {exc}")
        return False, None, str(exc)

def api_status_info():
    """ส่งคืนสถานะล่าสุดของระบบ"""
    return latest_state

def api_status_update(request: Request):
    """
    GET API endpoint สำหรับรับข้อมูลสถานะความปลอดภัยจากหน้าเว็บ
    ตัวอย่างการเรียกใช้งานจาก JavaScript:
       /api/status?data=warning
       /api/status?data=danger
    """
    raw_status = request.query_params.get("data", "normal").strip().lower()

    # ตรวจสอบความถูกต้องของสถานะ
    status = raw_status if raw_status in VALID_STATUSES else "normal"

    # ส่งสถานะข้ามไปสั่งงานหน้าตาไฟ LED Matrix บนบอร์ด Arduino
    bridge_ok, bridge_result, error = send_status_to_mcu(status)

    # บันทึกสถานะลงในระบบตัวกลาง
    latest_state["status"] = status
    latest_state["updated_at"] = time.time()
    latest_state["bridge_ok"] = bridge_ok
    latest_state["bridge_result"] = bridge_result
    latest_state["error"] = error

    print(f"[Security Status] ปรับเปลี่ยนเป็นสถานะ: {status}, สั่งงานบอร์ดสำเร็จหรือไม่={bridge_ok}")

    return {
        "ok": bridge_ok,
        "status": status,
        "bridge_ok": bridge_ok,
        "bridge_result": bridge_result,
        "error": error,
    }

# ลงทะเบียนช่องทาง API (Endpoints) ให้หน้าเว็บเรียกใช้งานได้
ui.expose_api("GET", "/api/status/info", api_status_info)
ui.expose_api("GET", "/api/status", api_status_update)

# เริ่มต้นระบบให้บอร์ดขึ้นหน้าตาปกติก่อน
send_status_to_mcu("normal")

# รันระบบเฟรมเวิร์กของ App Lab
App.run()