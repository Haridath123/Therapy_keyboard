#ifndef BLUETOOTH_MANAGER_H
#define BLUETOOTH_MANAGER_H
#include <Arduino.h>

void setupBluetooth();
void sendMetrics(int keyID, unsigned long interval, int totalCount);

#endif