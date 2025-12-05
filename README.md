# ESP32 Therapy Keypad & Tracker

**A Bluetooth-enabled interactive keyboard system designed to assist individuals with communication disorders through gamified motor-planning exercises.**

## Overview
Children and adults with communication disorders often struggle with timely responses, consistent gesture patterns, and coordinated motor actions. This project bridges the gap between manual therapy and digital tracking by creating an affordable, data-driven device.

The system consists of an **ESP32-based hardware module** with two physical keys and a **Python-based desktop application**. It gamifies therapy sessions (based on the "Tap Hero Adventure" concept) while recording critical metrics like response time and pattern accuracy.

## Key Features
* **Real-Time Tracking:** Monitors key presses and calculates the exact time interval (in milliseconds) between inputs.
* **Bluetooth Connectivity:** Wirelessly transmits data from the ESP32 to a Windows PC using Serial Bluetooth communication.
* **Interactive Dashboard:** A Python (Kivy) application that visualizes performance data instantly.
* **Immediate Feedback:** Provides visual cues ("Fast", "Consistent", "Slow") to help users improve reaction speed.
* **Session Logging:** Automatically saves all session data to a .csv file for therapist review.
* **Pattern Recognition:** Tracks specific key sequences (e.g., "Left, Left, Right") required for cognitive training.

## Tech Stack
* **Hardware:** ESP32 Microcontroller, Push Buttons, Status LED.
* **Firmware:** C++ (Arduino IDE) using BluetoothSerial.
* **Software:** Python 3.x.
* **Libraries:** pyserial, kivy.

## Hardware Setup
| Component | ESP32 Pin |
| :--- | :--- |
| **Left Key** | GPIO 16 |
| **Right Key** | GPIO 17 |
| **Status LED** | GPIO 5 |

## Installation & Usage

### 1. Firmware (ESP32)
1.  Open the `TherapyDevice` folder in Arduino IDE.
2.  Install the **ESP32 Board Manager**.
3.  Upload the code to your ESP32.
4.  Open the Serial Monitor (115200 baud) to verify buttons are working.

### 2. Software (Python)
1.  Ensure Python is installed on your PC.
2.  Install the required dependencies:
    ```bash
    pip install pyserial kivy
    ```
3.  Pair your computer with the ESP32 via Bluetooth (Device Name: `Therapy_Tracker_ESP32`).
4.  Run the application:
    ```bash
    python TherapyApp.py
    ```

## How It Works
1.  **Connect:** The Python app automatically scans COM ports (e.g., COM16/COM17) to find the device.
2.  **Interact:** The user presses the physical buttons based on therapist instructions.
3.  **Analyze:** The app displays the count and response time in real-time.
4.  **Log:** Upon closing, a `session_log.csv` file is generated with a timestamped history of every interaction.

## Future Enhancements
* Mobile app integration (Android/iOS).
* Haptic feedback for non-visual reinforcement.
* Cloud database integration for long-term patient tracking.

## References
* Project Guidelines: Bluetooth-enabled interactive keyboard system.
* ESP32 Tutorials: Random Nerd Tutorials.
* Python Kivy Docs: Kivy Tutorials.
