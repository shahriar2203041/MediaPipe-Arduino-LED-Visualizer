// FINAL ARDUINO CODE FOR A NON-BLOCKING LED BAR GRAPH

// Array to hold the pin numbers for our LEDs. This makes the code cleaner.
const int ledPins[] = {7, 8, 9, 10};
const int numLeds = 4; // The total number of LEDs we are using

char input;

// --- Variables for the non-blocking timer ---
bool ledsAreOn = false;           // A flag to check if the LEDs are currently lit
unsigned long timeLedsTurnedOn;   // Stores the time when the LEDs were lit
const long ledOnDuration = 1000;  // How long the LEDs should stay on (1000ms = 1s)


void setup() {
  Serial.begin(9600); // Start serial communication

  // Use a loop to set all our LED pins to OUTPUT mode
  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop() {
  // --- PART 1: Check for a new command from Python ---
  if (Serial.available() > 0) {
    input = Serial.read();

    // Check if the input is a number from '1' to '4'
    if (input >= '1' && input <= '4') {
      // Convert the character ('1', '2', etc.) to an actual number (1, 2, etc.)
      int numToLight = input - '0'; 
      setLedBarGraph(numToLight);
    }
  }

  // --- PART 2: Always check if the LEDs need to be turned off ---
  // This runs continuously, without blocking the code.
  if (ledsAreOn && (millis() - timeLedsTurnedOn >= ledOnDuration)) {
    clearLeds(); // If 1 second has passed, turn them off
  }
}

// Function to turn on the correct number of LEDs
void setLedBarGraph(int count) {
  clearLeds(); // Start by turning all LEDs off

  // Turn on the LEDs from the beginning of the array up to the count
  for (int i = 0; i < count; i++) {
    digitalWrite(ledPins[i], HIGH);
  }

  ledsAreOn = true; // Set our flag to true
  timeLedsTurnedOn = millis(); // Record the current time to start the 1-second timer
}

// Function to turn all LEDs off
void clearLeds() {
  for (int i = 0; i < numLeds; i++) {
    digitalWrite(ledPins[i], LOW);
  }
  ledsAreOn = false; // Reset our flag
}
