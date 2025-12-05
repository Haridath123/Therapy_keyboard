#include "InputHandler.h"
#include "Settings.h"

int lastLeft = HIGH;
int lastRight = HIGH;
unsigned long lastDebounce = 0;

void setupInputs() {
  pinMode(PIN_LEFT_KEY, INPUT_PULLUP);
  pinMode(PIN_RIGHT_KEY, INPUT_PULLUP);
}

int checkButtons() {
  int readLeft = digitalRead(PIN_LEFT_KEY);
  int readRight = digitalRead(PIN_RIGHT_KEY);
  int pressed = 0;

  if ((millis() - lastDebounce) > DEBOUNCE_DELAY) {
    if (readLeft == LOW && lastLeft == HIGH) {
      pressed = 1;
      lastDebounce = millis();
    }
    else if (readRight == LOW && lastRight == HIGH) {
      pressed = 2;
      lastDebounce = millis();
    }
  }
  lastLeft = readLeft;
  lastRight = readRight;
  return pressed;
}