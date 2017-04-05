
#include "Arduino-compatibles.h"
#include "wirish.h"
#include "QuadEncoder.h"

volatile int _ENCPosition = 0;//Keeps track of encoder _ENCPosition(ticks)
byte _PinA;
byte _PinB;

QuadEncoder::QuadEncoder(byte PinA, byte PinB)
{	
	attachInterrupt(PinA,TurnSensed_A, CHANGE);
	attachInterrupt(PinB,TurnSensed_B, CHANGE);	
	_PinA = PinA;
	_PinB = PinB;
	pinMode(_PinA, INPUT); 
	pinMode(_PinB, INPUT);
}

//Returns current _ENCPosition of the encoder
int QuadEncoder::pos(){
	return _ENCPosition;
}

void QuadEncoder::TurnSensed_A(){
   
  // look for a low-to-high on channel A
  if (digitalRead(_PinA) == HIGH) { 
    // check channel B to see which way encoder is turning
    if (digitalRead(_PinB) == LOW) {  
      _ENCPosition = _ENCPosition + 1;         // CW
    } 
    else {
      _ENCPosition = _ENCPosition - 1;         // CCW
    }
  }
  else   // must be a high-to-low edge on channel A                                       
  { 
    // check channel B to see which way encoder is turning  
    if (digitalRead(_PinB) == HIGH) {   
      _ENCPosition = _ENCPosition + 1;          // CW
    } 
    else {
      _ENCPosition = _ENCPosition - 1;          // CCW
    }
  }
}

void QuadEncoder::TurnSensed_B(){
  // look for a low-to-high on channel B
  if (digitalRead(_PinB) == HIGH) {   
   // check channel A to see which way encoder is turning
    if (digitalRead(_PinA) == HIGH) {  
      _ENCPosition = _ENCPosition + 1;         // CW
    } 
    else {
      _ENCPosition = _ENCPosition - 1;         // CCW
    }
  }
  // Look for a high-to-low on channel B
  else { 
    // check channel B to see which way encoder is turning  
    if (digitalRead(_PinA) == LOW) {   
      _ENCPosition = _ENCPosition + 1;          // CW
    } 
    else {
      _ENCPosition = _ENCPosition - 1;          // CCW
    }
  }
}