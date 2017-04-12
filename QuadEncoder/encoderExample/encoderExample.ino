#include <QuadEncoder.h>

#define EncoderPinA 0
#define EncoderPinB 1
int Position = 0;

QuadEncoder Enc0(EncoderPinA,EncoderPinB);

void setup() {
  SerialUSB.begin();
}

void loop() {
  if(Enc0.pos()==Position){
  }
  else{
    Position = Enc0.pos();
    SerialUSB.println(Position);
  } 
}

