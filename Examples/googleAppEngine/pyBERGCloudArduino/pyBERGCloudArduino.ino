/*

 */

#include <BERGCloud.h>
#include <SPI.h>

// These values should be edited to reflect your Product setup on bergcloud.com

#define MY_PRODUCT_VERSION 0
const uint8_t MY_PRODUCT_ID[16] = {
  0xA8,0x65,0x07,0x34,0xFF,0x0A,0x56,0x52,0x60,0xB6,0x96,0x09,0xAA,0x8D,0x69,0x2A};

// Define your commands and events here, according to the schema from bergcloud.com

#define EVENT_TESTEVENT 0
#define COMMAND_TESTCOMMAND 0

// time related stuff

//Change the value below responsibly. Need to have some time between sending events and pooling commands, the two things happen with a activityTimeInterval/2 time interval from 
//one to the other. Furthermore, if on Google App Engine, free account has limits on database writing rate. Need to take care of this rate if using the GAE example provided, since there 
//every event is written on a database. 
#define activityTimeInterval 8000


// DO NOT CHANGE DEFINES BELOW THIS LINE

#define nSSEL_PIN 10



void setup()
{
  Serial.begin(115200);
  BERGCloud.begin(&SPI, nSSEL_PIN);
  Serial.println("--- reset ---");

  if (BERGCloud.joinNetwork(MY_PRODUCT_ID, MY_PRODUCT_VERSION))
  {
    Serial.println("Joined/Rejoined network");
  }
  else
  {
    Serial.println("joinNetwork() returned false.");
  }
}

void loop()
{


  uint8_t commandBuffer[20];
  uint16_t commandSize;
  uint8_t commandID;

  uint8_t temp[6];

  delay((unsigned long)activityTimeInterval/2);
  Serial.print("Poll for command... ");
  if (BERGCloud.pollForCommand(commandBuffer, sizeof(commandBuffer), commandSize, commandID))
  {
    Serial.print("Got command 0x");
    Serial.print(commandID, HEX);
    Serial.print(" with data length ");
    Serial.print(commandSize, DEC);
    Serial.println(" bytes.");

    for (int i=0; i<commandSize; i++)
    {
      Serial.print("0x");
      Serial.println(commandBuffer[i], HEX);
    }
  }
  else
  {
    Serial.println("none.");
  }

  delay((unsigned long)activityTimeInterval - (unsigned long)activityTimeInterval/2);


  Serial.print("Sending an event... ");

  // Our event consists of 8 bytes, the first four spell out BERG,
  // and the second 4 make up an int32 counter value we increment
  // inside this main loop

  temp[0] = 'B';
  temp[1] = 'E';
  temp[2] = 'R';
  temp[3] = 'G';

  if (BERGCloud.sendEvent(EVENT_TESTEVENT, temp, 4))
  {
    Serial.println("ok");
  }
  else
  {
    Serial.println("failed/busy");
  }

}


