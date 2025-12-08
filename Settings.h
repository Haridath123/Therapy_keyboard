#ifndef SETTINGS_H
#define SETTINGS_H
#include <Arduino.h>

// --- Hardware Pins ---
#define PIN_LEFT_KEY  16
#define PIN_RIGHT_KEY 17
#define PIN_STATUS_LED 5

// --- Bluetooth Name ---
#define DEVICE_NAME "Therapy_Tracker_ESP32_Haridath"

// --- Tuning ---
#define DEBOUNCE_DELAY 50 
#define SEQUENCE_TIMEOUT 1000 // Wait 1.2 seconds to finish a pattern
#endif