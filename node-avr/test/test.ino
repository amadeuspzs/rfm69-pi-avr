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
#define SERIAL_BAUD 115200

#ifdef ENABLE_ATC
  RFM69_ATC radio;
#else
  RFM69 radio;
#endif

int numRetries = 3; // default is 2
int timeout = 100; // ms to wait for ACK, default is 30

int TRANSMITPERIOD = 5000; //transmit a packet to gateway so often (in ms)

typedef struct {
  bool state;
} Payload;
Payload theData;

void setup() {
  Serial.begin(SERIAL_BAUD);
  radio.initialize(FREQUENCY,NODEID,NETWORKID);
#ifdef IS_RFM69HW_HCW
  radio.setHighPower(); //must include this only for RFM69HW/HCW!
#endif
  //radio.encrypt(ENCRYPTKEY);
  Serial.print("Transmitting at ");
  Serial.print(FREQUENCY==RF69_433MHZ ? 433 : FREQUENCY==RF69_868MHZ ? 868 : 915);
  Serial.println(" MHz");
}

void loop() {
  theData.state = (theData.state == 0) ? 1 : 0;
  
  Serial.print("Sending struct (");
  Serial.print(sizeof(theData));
  Serial.print(" bytes): ");
  Serial.print(theData.state);
  Serial.print(" ... ");
  if (radio.sendWithRetry(GATEWAYID, (const void*)(&theData), sizeof(theData), numRetries, timeout)) {
    Serial.print(" ok!");
  } else { 
    Serial.print(" nothing...");
  }
  delay(TRANSMITPERIOD);
  Serial.println();
}
