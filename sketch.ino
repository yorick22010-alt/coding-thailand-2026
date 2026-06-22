#include <Arduino.h>
#include <ArduinoGraphics.h>
#include <Arduino_LED_Matrix.h>
#include <Arduino_RouterBridge.h>

Arduino_LED_Matrix matrix;


const uint8_t ICON_NORMAL[104] = {
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,7,7,7,7,7,7,7,7,7,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0
};


const uint8_t ICON_WARNING[104] = {
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,7,7,7,7,7,0,0,0,0,
    0,0,0,7,0,0,0,0,0,7,0,0,0,
    0,0,0,0,7,7,7,7,7,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0
};


const uint8_t ICON_DANGER[104] = {
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,7,7,0,0,0,0,0,0,0,7,7,0,
    0,0,0,7,7,0,0,0,7,7,0,0,0,
    0,0,7,7,0,0,0,0,0,7,7,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,7,7,7,7,7,7,7,0,0,0,
    0,0,7,0,0,0,0,0,0,0,7,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0
};

void show_icon(const uint8_t icon[104]) {
  matrix.draw(icon);
}


String set_status(String current_status) {
  current_status.toLowerCase();

  if (current_status == "normal") {
    show_icon(ICON_NORMAL);
  } else if (current_status == "warning") {
    show_icon(ICON_WARNING);
  } else if (current_status == "danger") {
    show_icon(ICON_DANGER);
  } else {
    show_icon(ICON_NORMAL);
  }

  return "ok:" + current_status;
}

void setup() {
  matrix.begin();
  matrix.clear();
  show_icon(ICON_NORMAL); 

  Bridge.begin();
 
  Bridge.provide_safe("set_status", set_status);
}

void loop() {
  
}