#include <ESP8266mDNS.h>
#include "ota_setup.h"
#include "ws_setup.h"
#include "server_setup.h"
#include "ModbusHandler.h"
#include "ModbusSlave.h"

int val = 0;

// Creating slaves
SoftwareSerial mySerial(RxPin, TxPin); // RX, TX
ModbusMaster485 node(1, EnTxPin, &mySerial);
ModbusSlave mbSlave1 = ModbusSlave(&node);

// Creating the ModbusHandler
ModbusHandler mbHandler = ModbusHandler();

// Create modules
PumpControlModule pump = PumpControlModule();
LightControlModule light0 = LightControlModule();


void setup()
{
  if (DEBUG)
  {
    Serial.begin(115200);
    Serial.setDebugOutput(true);
  }

  WiFi.mode(WIFI_AP);
  WiFi.softAP(hostName);

  setupOTA();

  MDNS.addService("http", "tcp", 80);

  SPIFFS.begin();

  ws.onEvent(onWsEvent);
  server.addHandler(&ws);
  // Append modules
  pump.init("PumpCtrl0", &mbSlave1, ADR_UT_HEIGTH, ADR_UT_LEVEL);
  mp.appendModule(&pump);

  light0.init("Light0", &mbSlave1, ADR_LIGHT_MODE_0, ADR_LUMINOSITY_0);
  mp.appendModule(&light0);

  server.addHandler(&events);

  setupServer();

  // Modbus
  mbSlave1.init(ADR_UT_HEIGTH, 18, ADR_UT_LEVEL, 7, MB_SPEED);
  mbHandler.append(&mbSlave1);
}

void loop()
{
  ArduinoOTA.handle();
  ws.cleanupClients();
  mbHandler.run();
}
