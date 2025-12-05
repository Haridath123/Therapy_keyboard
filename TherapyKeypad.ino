#include "Settings.h"
#include "BluetoothManager.h"
#include "InputHandler.h"

// Metrics Variables
unsigned long lastPressTime = 0;
int sessionCount = 0;

// LED Variables
bool ledActive = false;
unsigned long ledTimer = 0;

void setup() {
  pinMode(PIN_STATUS_LED, OUTPUT);
  digitalWrite(PIN_STATUS_LED, HIGH); // OFF
  
  setupInputs();
  setupBluetooth();
}

void loop() {
  int key = checkButtons();

  if (key != 0) {
    // 1. Calculate Timing
    unsigned long now = millis();
    unsigned long interval = now - lastPressTime;
    
    // Ignore the interval for the very first press of the session
    if (sessionCount == 0) interval = 0; 
    
    lastPressTime = now;
    sessionCount++;

    // 2. Send Data to PC
    sendMetrics(key, interval, sessionCount);

    // 3. Blink LED (Visual Feedback)
    digitalWrite(PIN_STATUS_LED, LOW);
    ledActive = true;
    ledTimer = millis();
  }

  // Turn off LED after 100ms
  if (ledActive && (millis() - ledTimer > 100)) {
    digitalWrite(PIN_STATUS_LED, HIGH);
    ledActive = false;
  }
  
  delay(10);
}