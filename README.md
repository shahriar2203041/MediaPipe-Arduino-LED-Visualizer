# CV-LED-Bar-Graph-Control

A real-time system that uses computer vision to count fingers and visualize the result as a bar graph on physical LEDs connected to an Arduino.

![Project Demo GIF]video_2025-07-03_21-57-38.gif

---

## Project Overview

This project demonstrates a seamless integration between high-level computer vision running on a PC and low-level hardware control on a microcontroller. The Python script uses a webcam to detect hands and count the number of fingers being held up. This number is then sent via serial communication to an Arduino, which lights up a corresponding number of LEDs to create a live, physical bar graph.

## Key Features

-   **Real-Time Hand Tracking:** Utilizes the **MediaPipe** library for robust, multi-hand landmark detection.
-   **Accurate Finger Counting:** Logic to count fingers on one or two hands, recognizing numbers 1 through 10.
-   **Serial Communication:** The Python script sends the finger count (`'1'`, `'2'`, etc.) to the Arduino.
-   **LED Bar Graph Visualization:** The Arduino receives the number and lights up that many LEDs (up to 4).
-   **Non-Blocking Arduino Code:** The Arduino sketch uses the `millis()` function for timing, ensuring the system remains responsive and can receive new commands even while the LEDs are lit.

## Technologies & Hardware

### Software & Libraries
-   **Language:** Python 3, C++ (Arduino)
-   **Python Libraries:** `OpenCV`, `MediaPipe`, `PySerial`
-   **IDE:** Visual Studio Code

### Hardware
-   Arduino Uno (or compatible board)
-   4x LEDs (any color)
-   4x 220Ω Resistors
-   Webcam
-   Breadboard and Jumper Wires

---

## How to Set Up and Run

### 1. Hardware Setup

-   Connect the four LEDs to Arduino digital pins 7, 8, 9, and 10, each with a 220Ω current-limiting resistor connected in series.
-   Connect the other leg of each LED to a common GND pin on the Arduino.
-   Connect the Arduino to your computer via USB.

### 2. Arduino
-   Open the `led_bar_graph.ino` sketch in the Arduino IDE.
-   Select your board and COM port.
-   Upload the sketch to your Arduino.

### 3. Python
-   Make sure you have the required libraries installed:
    ```bash
    pip install opencv-python mediapipe pyserial
    ```
-   Open the `cv_controller.py` script.
-   **Important:** Update the `PORT_NAME` variable at the top of the script to match your Arduino's COM port (e.g., `'COM5'`).
-   Run the script from your terminal:
    ```bash
    python cv_controller.py
    ```
-   Show 1 to 4 fingers to the camera and watch the LEDs light up!
