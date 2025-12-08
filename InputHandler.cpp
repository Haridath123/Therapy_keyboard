#include "InputHandler.h"
#include "Settings.h"

int lastLeft = HIGH;
int lastRight = HIGH;
unsigned long lastDebounce = 0;

void setupInputs() {
  pinMode(PIN_LEFT_KEY, INPUT_PULLUP);
  pinMode(PIN_RIGHT_KEY, INPUT_PULLUP);
}

// Returns: 0=None, 1=Left, 2=Right, 3=Both (Duo)
int checkButtons() {
  int readLeft = digitalRead(PIN_LEFT_KEY);
  int readRight = digitalRead(PIN_RIGHT_KEY);
  int result = 0;

  // Check if enough time has passed to ignore noise
  if ((millis() - lastDebounce) > DEBOUNCE_DELAY) {
    
    // Check for button press (LOW is pressed)
    bool leftPressed = (readLeft == LOW && lastLeft == HIGH);
    bool rightPressed = (readRight == LOW && lastRight == HIGH);

    if (leftPressed || rightPressed) {
      // Tiny delay to see if the user meant to press BOTH
      delay(50); 
      readLeft = digitalRead(PIN_LEFT_KEY);
      readRight = digitalRead(PIN_RIGHT_KEY);

      if (readLeft == LOW && readRight == LOW) {
        result = 3; // Duo / Both
      } else if (leftPressed) {
        result = 1; // Left Only
      } else if (rightPressed) {
        result = 2; // Right Only
      }
      
      lastDebounce = millis();
    }
  }

  lastLeft = readLeft;
  lastRight = readRight;
  return result;
}