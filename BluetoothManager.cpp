#include "BluetoothManager.h"
#include "Settings.h"
#include "BluetoothSerial.h"

BluetoothSerial SerialBT;

void setupBluetooth() {
  SerialBT.begin(DEVICE_NAME); 
  // We don't need Serial.begin here because it's usually in the main setup()
}

void sendMetrics(int keyID, unsigned long interval, int totalCount) {
  // 1. Send to Python App (Bluetooth)
  if (SerialBT.hasClient()) {
    SerialBT.print("KEY:");
    SerialBT.print(keyID);
    SerialBT.print(",INTERVAL:");
    SerialBT.print(interval);
    SerialBT.print(",COUNT:");
    SerialBT.println(totalCount);
  }

  // 2. Send to Arduino Serial Monitor (USB)
  // This lets you see what's happening without the Python app!
  Serial.print("KEY:");
  Serial.print(keyID);
  Serial.print(", INTERVAL:");
  Serial.print(interval);
  Serial.print(", COUNT:");
  Serial.println(totalCount);
}