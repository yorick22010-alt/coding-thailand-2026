"""
Arduino UNO Q Dimmer
Python side: WebUI + Socket.IO + Bridge

Main idea:
- WebUI selects the mode: WEB or POT.
- WebUI sends slider value to Python using Socket.IO.
- Python calls MCU functions using Bridge.
- MCU only handles hardware: PWM LED and potentiometer reading.

Communication path:

Browser
  -> socket.emit(...)
  -> Python ui.on_message(...)
  -> Bridge.call(...)
  -> MCU sketch
  -> LED / potentiometer
"""

from arduino.app_utils import App, Bridge
from arduino.app_bricks.web_ui import WebUI
import time


# ============================================================
# Create WebUI object
# ============================================================
# WebUI serves assets/index.html and provides the Socket.IO channel.
ui = WebUI()


# ============================================================
# Application state
# ============================================================
# Mode is selected from the webpage only.
#
# WEB:
#   The webpage slider controls the real LED.
#
# POT:
#   The webpage slider is disabled.
#   Python reads the potentiometer from MCU.
#   Python sends the potentiometer value back to MCU as LED brightness.
current_mode = "WEB"


# Brightness command from webpage slider.
# Range: 0 to 100
web_brightness = 50


# Last brightness value actually sent to the real LED.
# This is used to update the webpage display.
output_brightness = 50


# Latest potentiometer brightness.
# This is useful in POT mode.
pot_brightness = 0


# ============================================================
# Helper functions
# ============================================================
def clamp_percent(value):
    """
    Convert a value to integer and keep it inside 0 to 100.

    This protects the hardware from invalid values from the webpage.
    """
    try:
        value = int(value)
    except Exception:
        value = 0

    if value < 0:
        value = 0

    if value > 100:
        value = 100

    return value


def bridge_call_int(function_name, default_value=0):
    """
    Call an MCU Bridge function and try to convert the result to int.

    Some Bridge calls may return numbers directly.
    Some may return text depending on the environment.
    This helper keeps the Python code safer for teaching.
    """
    try:
        result = Bridge.call(function_name)
        return int(result)
    except Exception:
        return default_value


def set_real_led(percent):
    """
    Send brightness command to the MCU.

    The MCU will convert 0-100% brightness to PWM.
    """
    percent = clamp_percent(percent)

    try:
        Bridge.call("set_led_brightness", percent)
    except Exception:
        # In a teaching demo, this prevents the app from crashing
        # if the MCU sketch is not running yet.
        pass


def read_real_pot():
    """
    Ask the MCU to read the potentiometer.

    Return:
        potentiometer brightness from 0 to 100
    """
    value = bridge_call_int("read_pot_percent", default_value=0)
    return clamp_percent(value)


def make_state():
    """
    Build the current state package for the webpage.

    This dictionary is sent to the browser through Socket.IO.
    """
    return {
        "mode": current_mode,
        "web_brightness": web_brightness,
        "pot_brightness": pot_brightness,
        "output_brightness": output_brightness,
        "slider_enabled": current_mode == "WEB",
    }


def send_state(room=None):
    """
    Send current state to the webpage.

    If room is None:
        broadcast to all connected browsers.

    If room is given:
        send only to one browser client.
    """
    state = make_state()

    if room is None:
        ui.send_message("state_update", message=state)
    else:
        ui.send_message("state_update", message=state, room=room)


# ============================================================
# Socket.IO event: browser connected
# ============================================================
def on_connect(sid):
    """
    Called when a browser opens the WebUI.

    sid is the browser client ID.
    We immediately send the current state to this browser.
    """
    send_state(room=sid)


# ============================================================
# Socket.IO event: set mode
# ============================================================
def on_set_mode(sid, data):
    """
    Called when the user clicks WEB Mode or POT Mode.

    Expected data from browser:
        {"mode": "WEB"}

    or:
        {"mode": "POT"}
    """
    global current_mode
    global output_brightness
    global pot_brightness

    mode = data.get("mode", "WEB")

    if mode not in ["WEB", "POT"]:
        return

    current_mode = mode

    if current_mode == "WEB":
        # When entering WEB mode, immediately apply the current slider value.
        output_brightness = web_brightness
        set_real_led(output_brightness)

    elif current_mode == "POT":
        # When entering POT mode, read the real potentiometer immediately.
        pot_brightness = read_real_pot()
        output_brightness = pot_brightness
        set_real_led(output_brightness)

    # Send updated state to all browsers.
    send_state()


# ============================================================
# Socket.IO event: set web brightness
# ============================================================
def on_set_brightness(sid, data):
    """
    Called when the user moves the webpage slider.

    Expected data from browser:
        {"brightness": 75}

    Important rule:
    - The slider value is stored every time.
    - But it controls the real LED only when current_mode == "WEB".
    """
    global web_brightness
    global output_brightness

    brightness = data.get("brightness", 0)
    web_brightness = clamp_percent(brightness)

    if current_mode == "WEB":
        output_brightness = web_brightness
        set_real_led(output_brightness)

    # Send updated state to all browsers.
    send_state()


# ============================================================
# Socket.IO event: browser asks for current state
# ============================================================
def on_get_state(sid, data=None):
    """
    Called when the browser asks for the latest state.

    The browser may call:
        socket.emit("get_state", {})
    """
    send_state(room=sid)


# ============================================================
# Register WebUI Socket.IO event handlers
# ============================================================
# Browser event name      Python function
# ------------------------------------------------------------
# "set_mode"          ->  on_set_mode
# "set_brightness"    ->  on_set_brightness
# "get_state"         ->  on_get_state
ui.on_connect(on_connect)
ui.on_message("set_mode", on_set_mode)
ui.on_message("set_brightness", on_set_brightness)
ui.on_message("get_state", on_get_state)


# ============================================================
# Main loop
# ============================================================
def loop():
    """
    Main application loop.

    In WEB mode:
        The LED is updated when the slider sends a Socket.IO event.

    In POT mode:
        Python repeatedly reads the potentiometer from the MCU.
        Then Python sends that value back to the MCU as LED brightness.
        Then Python updates the webpage lamp display.
    """
    global pot_brightness
    global output_brightness

    if current_mode == "POT":
        pot_brightness = read_real_pot()
        output_brightness = pot_brightness
        set_real_led(output_brightness)

        # Update browser so the webpage lamp follows the real potentiometer.
        send_state()

    time.sleep(0.10)


# ============================================================
# Start the App Lab application
# ============================================================
# App.run() starts the Python application and the App Lab runtime.
App.run(user_loop=loop)