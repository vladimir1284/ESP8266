#include "Configs.h"
#include <ArduinoJson.h>
#include <FS.h> // Include the SPIFFS library
#include <ESPAsyncWebServer.h>
#include "module.h"

#define NMODULES 5

class MsgProcessor
{
public:
    MsgProcessor();

    void processWsMessage(String msg, AsyncWebSocketClient *client),
        appendModule(Module *module);

    uint16_t mbPumpData[ADR_PC_STATE + 1];

private:
    String getVariables(String id),
        getSetups(String id),
        updateSetups(StaticJsonDocument<512> rq_doc);

    AsyncWebSocketClient *currentClient;

    StaticJsonDocument<512> doc;

    void handleFileOperation(),
        handleGetOperation(),
        handleSetOperation();

    String fixFileName(String str);

    Module *modules[NMODULES];
    int modules_count;
};