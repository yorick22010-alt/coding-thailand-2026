#include <Arduino_RouterBridge.h>
#include <Arduino_Modulino.h>

const int LED_PWM_PIN = LED_BUILTIN; //9;

ModulinoKnob volumeKnob;

void setup() {
    pinMode(LED_PWM_PIN, OUTPUT);
    analogWrite(LED_PWM_PIN, 0);

    Modulino.begin();
    volumeKnob.begin();
    volumeKnob.set(50);

    Bridge.begin();

    Bridge.provide_safe("set_led_brightness", set_led_brightness);

    /*
        Keep the same Bridge function name.

        Python does not need to change.
        main.py still calls:
            Bridge.call("read_pot_percent")
    */
    Bridge.provide_safe("read_pot_percent", read_pot_percent);

    Bridge.provide_safe("led_off", led_off);
}

void loop() {
}

/*
    Same function name as before.

    But now it reads from Modulino Volume / Knob,
    not from A0.
*/
int read_pot_percent() {
    int value = volumeKnob.get();

    int percent = constrain(value, 0, 100);

    if (value != percent) {
        volumeKnob.set(percent);
    }

    return percent;
}

void set_led_brightness(int percent) {
    percent = constrain(percent, 0, 100);

    int pwmValue = map(percent, 0, 100, 0, 255);

    analogWrite(LED_PWM_PIN, pwmValue);
}

void led_off() {
    analogWrite(LED_PWM_PIN, 0);
}