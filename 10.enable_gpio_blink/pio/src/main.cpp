#include <Arduino.h>

void setup(){
	Serial.begin();

	for(byte i=0; i<27; i++)
		pinMode(i, OUTPUT);
}

int loop(){
	Serial.println("Hello Microapp!");

	for(byte i=0; i<27; i++)
		digitalWrite(i, HIGH);

	delay(1000);

	for(byte i=0; i<27; i++)
		digitalWrite(i, LOW);

	delay(1000);
	return 0;
}
