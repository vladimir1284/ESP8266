#include <ESP8266mDNS.h>
#include "ota_setup.h"
#include "ws_setup.h"
#include "server_setup.h"
#include <ModbusMaster485.h>

#define REQUEST_DELAY 2000

unsigned int lastRequest;
int val = 0;

const int EnTxPin = 5;          // HIGH:TX y LOW:RX
SoftwareSerial mySerial(4, 14); // RX, TX
ModbusMaster485 node(1, EnTxPin, &mySerial);

void setup()
{
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  WiFi.mode(WIFI_AP);
  WiFi.softAP(hostName);

  setupOTA();

  MDNS.addService("http", "tcp", 80);

  SPIFFS.begin();

  ws.onEvent(onWsEvent);
  server.addHandler(&ws);

  server.addHandler(&events);

  setupServer();

  // Modbus
  node.begin(19200);
  lastRequest = 0;
}

void loop()
{
  ArduinoOTA.handle();
  ws.cleanupClients();

  if (millis() - lastRequest > REQUEST_DELAY)
  {
    uint8_t j, result;
    lastRequest = millis();
    // slave: read (11) 16-bit registers starting at register 0 to RX buffer
    result = node.readHoldingRegisters(0, 11);

    // do something with data if read is successful
    if (result == node.ku8MBSuccess)
    {
      for (j = 0; j < 11; j++)
      {
        Serial.print(node.getResponseBuffer(j));
        mp.mbPumpData[j] = node.getResponseBuffer(j);
        Serial.print(",");
      }
        Serial.println();
    } else {
      Serial.println("Modbus Error!");
    }
  }
}
