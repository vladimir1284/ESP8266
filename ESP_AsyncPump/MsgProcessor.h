#include <Arduino.h>
#include <ArduinoJson.h>
#include <FS.h> // Include the SPIFFS library
#include <ESPAsyncWebServer.h>

#define RESPONSE_SIZE 200


enum reg_addresses
{
    ADR_UT_LEVEL,
    ADR_UT_HEIGTH,
    ADR_UT_GAP,
    ADR_UT_MIN,
    ADR_UT_RESTART,
    ADR_LT_LEVEL,
    ADR_LT_HEIGTH,
    ADR_LT_GAP,
    ADR_LT_MIN,
    ADR_LT_RESTART,
    ADR_PC_STATE,
};

class MsgProcessor
{
public:
    MsgProcessor();
    void processWsMessage(String msg, AsyncWebSocketClient *client);
    uint16_t mbPumpData[ADR_PC_STATE+1] = {49, 120, 10, 20, 65, 52, 120, 10, 20, 80, 1};

private:
    AsyncWebSocketClient *currentClient;
    StaticJsonDocument<512> doc;
    void handleFileOperation(),
        handleGetOperation(),
        handleSetOperation();
    String fixFileName(String str);
};