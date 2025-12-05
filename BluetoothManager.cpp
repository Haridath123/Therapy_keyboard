#include "BluetoothManager.h"
#include "Settings.h"
#include "BluetoothSerial.h"

BluetoothSerial SerialBT;

void setupBluetooth() {
  SerialBT.begin(DEVICE_NAME); 
}

void sendMetrics(int keyID, unsigned long interval, int totalCount) {
  if (SerialBT.hasClient()) {
    // Format: "KEY:1,INTERVAL:1500,COUNT:10"
    SerialBT.print("KEY:");
    SerialBT.print(keyID);
    SerialBT.print(",INTERVAL:");
    SerialBT.print(interval);
    SerialBT.print(",COUNT:");
    SerialBT.println(totalCount);
  }
}