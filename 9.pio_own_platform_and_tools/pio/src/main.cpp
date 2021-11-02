#include <Arduino.h>

void setup(){
	Serial.begin();

	for(byte i=0; i<27; i++)
		pinMode(i, OUTPUT);
}

int loop(){
	Serial.println("Hello Microapp!");

	delay(1000);
	return 0;
}
