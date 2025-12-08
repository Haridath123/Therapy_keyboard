#include "Settings.h"
#include "BluetoothManager.h"
#include "InputHandler.h"

// Metrics
int sessionCount = 0;

// LED Variables
bool ledActive = false;
unsigned long ledTimer = 0;

// Pattern Recognition Variables
String patternBuffer = "";       
unsigned long lastInputTime = 0; 
unsigned long lastReportTime = 0; // NEW: Tracks when we last sent data

void setup() {
  Serial.begin(115200); // <--- REQUIRED for Serial Monitor
  
  pinMode(PIN_STATUS_LED, OUTPUT);
  digitalWrite(PIN_STATUS_LED, HIGH); 
  
  setupInputs();
  setupBluetooth();
  
  Serial.println("System Ready.");
}

void loop() {
  // 1. Check for raw clicks (1=Left, 2=Right, 3=Both)
  int key = checkButtons();

  if (key != 0) {
    // Blink LED for visual feedback of a click
    digitalWrite(PIN_STATUS_LED, LOW);
    ledActive = true;
    ledTimer = millis();

    // Add to our pattern buffer
    if (key == 1) patternBuffer += "L";
    if (key == 2) patternBuffer += "R";
    if (key == 3) patternBuffer += "B";
    
    // Reset the timer so we wait for more inputs
    lastInputTime = millis();
  }

  // 2. TIMEOUT CHECK: Has the user stopped pressing buttons?
  // If buffer has data AND time is up... analyze the pattern!
  if (patternBuffer.length() > 0 && (millis() - lastInputTime > SEQUENCE_TIMEOUT)) {
    
    int actionID = 0;

    // --- YOUR CUSTOM RULES ---
    if (patternBuffer == "L")           actionID = 1;
    else if (patternBuffer == "R")      actionID = 2;
    else if (patternBuffer == "B")      actionID = 3;
    else if (patternBuffer == "LRR")    actionID = 4;
    else if (patternBuffer == "RLL")    actionID = 5;
    else if (patternBuffer == "BB")     actionID = 6;
    else if (patternBuffer == "LLR")    actionID = 7;
    else if (patternBuffer == "RRL")    actionID = 8;
    else if (patternBuffer == "RL")     actionID = 9;
    else if (patternBuffer == "LR")     actionID = 10;
    else if (patternBuffer == "LLRR")   actionID = 11;
    else if (patternBuffer == "LLLRR")  actionID = 12;
    else if (patternBuffer == "RLRL")   actionID = 13;
    else if (patternBuffer == "LRL")    actionID = 14;
    else if (patternBuffer == "RLR")    actionID = 15;
    else if (patternBuffer == "LLL")    actionID = 16;
    else if (patternBuffer == "RRR")    actionID = 17;
    else if (patternBuffer == "LLLL")   actionID = 18;
    else if (patternBuffer == "RRRR")   actionID = 19;
    else if (patternBuffer == "LBL")    actionID = 20;
    else if (patternBuffer == "RBR")    actionID = 21;
    else if (patternBuffer == "BL")     actionID = 22;
    else if (patternBuffer == "BR")     actionID = 23;
    else if (patternBuffer == "BBB")    actionID = 24;
    else if (patternBuffer == "LRLR")   actionID = 25;
    else if (patternBuffer == "RRLL")   actionID = 26;
    else if (patternBuffer == "LLRL")   actionID = 27;
    else if (patternBuffer == "RRLR")   actionID = 28;
    else if (patternBuffer == "RLRLR")  actionID = 29;
    else if (patternBuffer == "LLLR")   actionID = 30;
    else if (patternBuffer == "RRRL")   actionID = 31;
    else if (patternBuffer == "LLBR")   actionID = 32;
    else if (patternBuffer == "RRBL")   actionID = 33;
    else if (patternBuffer == "LLLB")   actionID = 34;
    else if (patternBuffer == "RRRB")   actionID = 35;
    else if (patternBuffer == "LL")     actionID = 36;
    else if (patternBuffer == "RR")     actionID = 37;


    
    else actionID = 99; // Unknown pattern (Error)

    // --- NEW INTERVAL CALCULATION ---
    unsigned long now = millis();
    unsigned long duration = now - lastReportTime;
    
    // If it's the very first action, set interval to 0
    if (sessionCount == 0) duration = 0;
    
    lastReportTime = now;
    // --------------------------------

    sessionCount++;
    sendMetrics(actionID, duration, sessionCount);

    patternBuffer = "";
  }

  if (ledActive && (millis() - ledTimer > 100)) {
    digitalWrite(PIN_STATUS_LED, HIGH);
    ledActive = false;
  }
  
  delay(10);
}