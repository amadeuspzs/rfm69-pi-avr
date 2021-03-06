#define debug true
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

int numRetries = 3; // default is 2
int timeout = 255; // ms to wait for ACK, default is 30

int TRANSMITPERIOD = 5000; //transmit a packet to gateway so often (in ms)

typedef struct {
  bool state;
} Payload;
Payload theData;

void setup() {
  if (debug) Serial.begin(SERIAL_BAUD);
  radio.initialize(FREQUENCY,NODEID,NETWORKID);
  #ifdef IS_RFM69HW_HCW
    radio.setHighPower(); //must include this only for RFM69HW/HCW!
  #endif
  #ifdef ENABLE_ATC
    radio.enableAutoPower(ATC_RSSI); // set the target RSSI
  #endif
  //radio.encrypt(ENCRYPTKEY);
  if (debug) Serial.print("Transmitting at ");
  if (debug) Serial.print(FREQUENCY==RF69_433MHZ ? 433 : FREQUENCY==RF69_868MHZ ? 868 : 915);
  if (debug) Serial.println(" MHz");
}

void loop() {
  theData.state = (theData.state == 0) ? 1 : 0;
  
  if (debug) Serial.print("Sending struct (");
  if (debug) Serial.print(sizeof(theData));
  if (debug) Serial.print(" bytes): ");
  if (debug) Serial.print(theData.state);
  if (debug) Serial.print(" ... ");
  if (radio.sendWithRetry(GATEWAYID, (const void*)(&theData), sizeof(theData), numRetries, timeout)) {
    if (debug) Serial.print(" ok!");
  } else { 
    if (debug) Serial.print(" nothing...");
  }
  delay(TRANSMITPERIOD);
  if (debug) Serial.println();
}
