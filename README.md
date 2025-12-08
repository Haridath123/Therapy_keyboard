# Therapy Keypad & Dashboard

**A comprehensive hardware-software system designed for motor-planning therapy, reaction time training, and cognitive rehabilitation.**

![Project Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Platform](https://img.shields.io/badge/Platform-ESP32%20%7C%20Windows-blue)
![Language](https://img.shields.io/badge/Language-C%2B%2B%20%7C%20Python-orange)

## Overview

**NeuroTrack Medical** is a therapeutic tool that gamifies and tracks motor-speech and hand-eye coordination exercises. It consists of a custom **ESP32-based keypad** (Hardware) and a professional **Clinical Dashboard** (Software).

The system tracks user inputs, recognizes complex rhythmic patterns (e.g., "Left-Right-Left"), measures precise reaction times, and logs all data for therapist review.

---

## Key Features

### Clinical Dashboard (Software)
* **Medical-Grade GUI:** Clean, split-screen interface designed for clinical environments (White/Teal theme).
* **Real-Time Metrics:** Displays total session counts and precise response intervals (in milliseconds).
* **Live Session Log:** A scrollable sidebar history of every action performed during the session.
* **Automated Feedback:** Analyzes response time to provide immediate feedback:
    * **< 1100ms:** "Excellent Reflexes"
    * **< 2000ms:** "Normal Pace"
    * **> 2000ms:** "Delayed Response".
* **Data Export:** Automatically saves all session data to `session_log.csv` with timestamps.

### Therapy Keypad (Hardware)
* **Pattern Recognition:** Smart firmware detects single presses, simultaneous "Duo" presses, and complex sequences (up to 37 unique patterns).
* **Wireless Connectivity:** Transmits data via Bluetooth Serial (RFCOMM) to remove cable clutter.
* **Debouncing & Noise Filtering:** Advanced input handling to prevent accidental double-clicks.
* **Visual Feedback:** On-board Status LED provides immediate confirmation of input registration.

---

## System Architecture

### Hardware Logic
The firmware operates on a **1.2-second timeout window**.
1.  **Input:** User presses buttons (Left, Right, or Both).
2.  **Buffering:** The ESP32 records the sequence into a buffer (e.g., "L", "L", "R").
3.  **Processing:** Once the user stops pressing for 1.2s, the system matches the buffer string to a **Pattern ID**.
4.  **Transmission:** The Pattern ID and elapsed time are sent to the PC via Bluetooth.

### Supported Inputs
The system uses a smart `InputHandler` that waits 50ms upon detecting a press to see if the second button is also pressed, allowing for accurate **"Simultaneous (Duo)"** detection.

---

## Hardware Setup

### Components
* **Microcontroller:** ESP32 Development Board
* **Inputs:** 2x Tactile Push Buttons
* **Output:** 1x LED (Built-in or External)

### Wiring Diagram (Configuration)
Defined in `Settings.h`:

| Component | ESP32 GPIO Pin | Type |
| :--- | :--- | :--- |
| **Left Key** | GPIO 16 | Input (Pull-up) |
| **Right Key** | GPIO 17 | Input (Pull-up) |
| **Status LED** | GPIO 5 | Output |

---

## Installation & Usage

### Prerequisite: Firmware Setup
1.  Open the project folder in **Arduino IDE**.
2.  Ensure all header files (`.h`) and source files (`.cpp`) are in the same directory as `TherapyKeypad.ino`.
3.  Select your board (ESP32 Dev Module) and upload the code.
4.  **Note:** The device Bluetooth name is set to `"Therapy_Tracker_ESP32"`.

### Prerequisite: Software Setup
1.  Install **Python 3.x**.
2.  Install the required dependencies:
    ```bash
    pip install pyserial kivy
    ```
3.  **Bluetooth Pairing:**
    * Go to Windows Bluetooth Settings.
    * Pair with **Therapy_Tracker_ESP32**.
    * Check Device Manager (Ports) to find your COM port numbers (Standard Serial over Bluetooth).
4.  **Configure Ports:**
    * Open `TherapyApp.py`.
    * Update line 15 with your specific COM ports:
        ```python
        TARGET_PORTS = ['COM16', 'COM17'] # Change these to match your PC
        ```

### Running the Application
Run the Python script:
```bash
python TherapyApp.py
