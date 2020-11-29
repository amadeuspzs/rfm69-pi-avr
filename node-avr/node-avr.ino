#define debug true // true for serial output

#include <avr/sleep.h>
#include "PinChangeInterrupt.h" // for PCINTX
#include <RFM69.h>         //get it here: https://github.com/amadeuspzs/RFM69
#include <RFM69_ATC.h>     //get it here: https://github.com/amadeuspzs/RFM69
#include <SPI.h>           //included with Arduino IDE install (www.arduino.cc)

#define NODEID      2
#define NETWORKID   1
#define GATEWAYID   1
#define FREQUENCY     RF69_433MHZ
//#define ENCRYPTKEY    "sampleEncryptKey" //has to be same 16 characters/bytes on all nodes, not more not less!
//#define IS_RFM69HW_HCW  //uncomment only for RFM69HW/HCW! Leave out if you have RFM69W/CW!
#define ENABLE_ATC    //comment out this line to disable AUTO TRANSMISSION CONTROL
#define ATC_RSSI      -80 // target RSSI (dBm)  
#define SERIAL_BAUD 9600

#ifdef ENABLE_ATC
  RFM69_ATC radio;
#else
  RFM69 radio;
#endif

int sensor = 7; // Reed switch attached to D7=PIN6=PA7=PCINT7

int numRetries = 3; // default is 2
int timeout = 255; // ms to wait for ACK, default is 30

typedef struct {
  bool state;
} Payload;
Payload theData;

void setup() {
  pinMode(sensor,INPUT_PULLUP);
  delay(2000); // allow debounce cap to charge

  if (debug) {
    Serial.begin(SERIAL_BAUD);
    while (!Serial) ;
  }
  
  radio.initialize(FREQUENCY,NODEID,NETWORKID);
  #ifdef IS_RFM69HW_HCW
    radio.setHighPower(); //must include this only for RFM69HW/HCW!
  #endif
  #ifdef ENABLE_ATC
    radio.enableAutoPower(ATC_RSSI); // set the target RSSI
  #endif

  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  
  //radio.encrypt(ENCRYPTKEY);
  if (debug) {
    Serial.print("Transmitting at ");
    Serial.print(FREQUENCY==RF69_433MHZ ? 433 : FREQUENCY==RF69_868MHZ ? 868 : 915);
    Serial.println(" MHz");
  }
}

void loop() {
  
  theData.state = digitalRead(sensor);

  if (debug) {
    Serial.print("Sending struct (");
    Serial.print(sizeof(theData));
    Serial.print(" bytes): ");
    Serial.print(theData.state);
    Serial.print(" ... ");
  }
  
  if (radio.sendWithRetry(GATEWAYID, (const void*)(&theData), sizeof(theData), numRetries, timeout)) {
    if (debug) Serial.print(" ok!");
  } else { 
    if (debug) Serial.print(" nothing...");
  }

  if (debug) {
    Serial.println();
    Serial.println("Dropping into sleep");
    Serial.flush();
  }
  
  attachPCINT(digitalPinToPCINT(sensor), wake, CHANGE);

  sleep_enable(); // enable sleep
  sleep_cpu();   // go to sleep
}

void wake()
{
  detachPCINT(digitalPinToPCINT(sensor));
  sleep_disable();
  // this will then go back into the loop() function
} //end of wake
