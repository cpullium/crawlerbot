#ifndef QuadEncoder_h
#define QuadEncoder_h

#include "Arduino-compatibles.h"
#include "wirish.h"

class QuadEncoder
{
 public:
     QuadEncoder(byte PinA, byte PinB);
     int pos();

 private:	
	static void TurnSensed_A();
	static void TurnSensed_B();
};

#endif
