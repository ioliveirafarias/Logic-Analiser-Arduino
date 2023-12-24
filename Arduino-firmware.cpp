/*
RAM:   [=         ]   8.8% (used 181 bytes from 2048 bytes)
Flash: [          ]   4.6% (used 1478 bytes from 32256 bytes)
*/

#include <Arduino.h>

#define PROBES_LEN 5
uint8_t PROBES[] = {A0, A1, A2, A3, A4};

int main() {

  uint8_t i;
  uint8_t responseByte = 0;

  for (i = 0; i < PROBES_LEN; i++) {    
    pinMode( PROBES[i], INPUT );
  }

  Serial.begin(9600);
  while ( true ) {
    responseByte = 0;
    for (i = 0; i < PROBES_LEN; i++) {    
      responseByte += digitalRead( PROBES[i] ) ? int(i*i) : 0;
    } 
    Serial.write( responseByte );    
    _delay_ms(500);
  }
}