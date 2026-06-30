# UNO Q Emotion LED Matrix
# Python side: WebUI + REST API + RouterBridge to the STM32 MCU.
#
# Data flow:
# Browser camera/image -> browser AI emotion detection -> /api/emotion?data=happy
# -> Python receives emotion -> Bridge.call("set_emotion", emotion)
# -> Arduino C/C++ sketch updates the 13x8 LED matrix.
#
# Important privacy note:
# This Python code receives only the emotion label and confidence score.
# It does not receive or save the face image.

from arduino.app_utils import App, Bridge
from arduino.app_bricks.web_ui import WebUI
from fastapi import Request
import os
import time

# Serve static website files from the app-level assets/ folder.
# In Arduino App Lab, HTML/CSS/JavaScript and local model/library files
# should be placed in assets/, while Python code stays in python/.
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ASSETS_DIR = os.path.join(APP_DIR, "assets")
ui = WebUI(assets_dir_path=ASSETS_DIR)

VALID_EMOTIONS = {
    "neutral",
    "happy",
    "sad",
    "angry",
    "fearful",
    "disgusted",
    "surprised",
    "no_face",
    "unknown",
}

latest_state = {
    "emotion": "neutral",
    "confidence": None,
    "updated_at": time.time(),
    "bridge_ok": False,
    "bridge_result": None,
    "error": None,
}


def normalize_emotion(value: str) -> str:
    """Normalize labels from the browser before sending them to the MCU."""
    if value is None:
        return "unknown"

    value = str(value).strip().lower()

    # Common aliases from emotion models or student code.
    aliases = {
        "fear": "fearful",
        "scared": "fearful",
        "surprise": "surprised",
        "none": "no_face",
        "noface": "no_face",
        "no-face": "no_face",
    }

    value = aliases.get(value, value)
    return value if value in VALID_EMOTIONS else "unknown"


def send_emotion_to_mcu(emotion: str):
    """Call the C/C++ function set_emotion(emotion) registered on the MCU."""
    try:
        # The sketch provides this RPC function:
        #   Bridge.provide_safe("set_emotion", set_emotion);
        result = Bridge.call("set_emotion", emotion)
        return True, str(result), None
    except Exception as exc:
        print(f"[Bridge] Could not send emotion to MCU: {exc}")
        return False, None, str(exc)


def api_status():
    """Return the latest emotion state for testing in the browser."""
    return latest_state


def api_emotion_get(request: Request):
    """
    GET endpoint for simple student-friendly testing.

    Examples:
      /api/emotion?data=happy
      /api/emotion?data=sad&confidence=0.91
      /api/emotion?data=sad&score=0.91       # score is also accepted as an alias
    """
    raw_emotion = request.query_params.get("data", "unknown")
    raw_confidence = request.query_params.get(
        "confidence",
        request.query_params.get("score", None),
    )

    emotion = normalize_emotion(raw_emotion)

    try:
        confidence = None if raw_confidence is None else float(raw_confidence)
    except ValueError:
        confidence = None

    bridge_ok, bridge_result, error = send_emotion_to_mcu(emotion)

    latest_state["emotion"] = emotion
    latest_state["confidence"] = confidence
    latest_state["updated_at"] = time.time()
    latest_state["bridge_ok"] = bridge_ok
    latest_state["bridge_result"] = bridge_result
    latest_state["error"] = error

    print(f"[Emotion] {emotion}, confidence={confidence}, bridge_ok={bridge_ok}")

    return {
        "ok": bridge_ok,
        "emotion": emotion,
        "confidence": confidence,
        "bridge_ok": bridge_ok,
        "bridge_result": bridge_result,
        "error": error,
    }


# Register REST endpoints exposed by the WebUI brick.
ui.expose_api("GET", "/api/status", api_status)
ui.expose_api("GET", "/api/emotion", api_emotion_get)

# Set a startup face on the LED matrix.
send_emotion_to_mcu("neutral")

App.run()
