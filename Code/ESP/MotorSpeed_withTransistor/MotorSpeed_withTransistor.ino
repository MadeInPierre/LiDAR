/*
Type an int in the serial monitor and it will drive the motor speed.
Using transistor "BC558C W0 E"
*/

String inString = "";
int value = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(500000);
  pinMode(D7, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() > 0) {
    int inChar = Serial.read();
    if (isDigit(inChar)) {
      // convert the incoming byte to a char
      // and add it to the string:
      inString += (char)inChar;
    }
    // if you get a newline, print the string,
    // then the string's value:
    if (inChar == '\n') {
      Serial.print("Value:");
      Serial.println(inString.toInt());
      Serial.print("String: ");
      Serial.println(inString);

      value = inString.toInt();
      // clear the string for new input:
      inString = "";
    }
  }


  analogWrite(D7, 1023 - value);
}
