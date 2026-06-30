// UNO Q Emotion LED Matrix - MCU side
// Receives emotion labels from Python through Arduino_RouterBridge
// and displays a matching 13 x 8 icon on the built-in LED matrix.

#include <Arduino.h>
#include <ArduinoGraphics.h>
#include <Arduino_LED_Matrix.h>
#include <Arduino_RouterBridge.h>

Arduino_LED_Matrix matrix;

const uint8_t ICON_HAPPY[104] = {
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,7,0,0,0,0,0,0,0,0,0,7,0,
    0,0,7,0,0,0,0,0,0,0,7,0,0,
    0,0,0,7,7,7,7,7,7,7,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0
};

const uint8_t ICON_SAD[104] = {
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,7,7,7,7,7,7,7,0,0,0,
    0,0,7,0,0,0,0,0,0,0,7,0,0,
    0,7,0,0,0,0,0,0,0,0,0,7,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0
};

const uint8_t ICON_ANGRY[104] = {
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,7,7,0,0,0,0,0,0,0,7,7,0,
    0,0,0,7,7,0,0,0,7,7,0,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,7,7,7,7,7,7,7,0,0,0,
    0,0,7,0,0,0,0,0,0,0,7,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0
};

const uint8_t ICON_SURPRISED[104] = {
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,7,7,7,7,7,0,0,0,0,
    0,0,0,7,0,0,0,0,0,7,0,0,0,
    0,0,0,0,7,7,7,7,7,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0
};

const uint8_t ICON_NEUTRAL[104] = {
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,7,7,7,7,7,7,7,7,7,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0
};

const uint8_t ICON_FEARFUL[104] = {
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,7,0,0,7,7,7,7,7,0,0,7,0,
    0,0,7,0,0,0,0,0,0,0,7,0,0,
    0,0,0,7,7,7,7,7,7,7,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0
};

const uint8_t ICON_DISGUSTED[104] = {
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,7,7,7,7,7,7,0,0,0,0,
    0,0,7,0,0,0,0,0,7,7,0,0,0,
    0,7,0,0,0,0,0,0,0,0,7,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0
};


void show_icon(const uint8_t icon[104]) {
  matrix.draw(icon);
}

String set_emotion(String emotion) {
  emotion.toLowerCase();

  if (emotion == "happy") {
    show_icon(ICON_HAPPY);
  } else if (emotion == "sad") {
    show_icon(ICON_SAD);
  } else if (emotion == "angry") {
    show_icon(ICON_ANGRY);
  } else if (emotion == "surprised") {
    show_icon(ICON_SURPRISED);
  } else if (emotion == "fearful") {
    show_icon(ICON_FEARFUL);
  } else if (emotion == "disgusted") {
    show_icon(ICON_DISGUSTED);
  } else {
    emotion = "neutral";
    show_icon(ICON_NEUTRAL);
  }

  return "ok:" + emotion;
}

void setup() {
  matrix.begin();
  matrix.clear();
  show_icon(ICON_NEUTRAL);

  Bridge.begin();
  Bridge.provide_safe("set_emotion", set_emotion);
}

void loop() {
  // Nothing needed. Python calls set_emotion() through the Bridge.
}
