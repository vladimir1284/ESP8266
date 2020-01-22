#include <ArduinoOTA.h>
#include <ESPAsyncWebServer.h>

AsyncEventSource events("/events");

const char *hostName = "esp-async";

//Send OTA events to the browser
void setupOTA()
{
    ArduinoOTA.onStart([]() { events.send("Update Start", "ota"); });
    ArduinoOTA.onEnd([]() { events.send("Update End", "ota"); });
    ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
        char p[32];
        sprintf(p, "Progress: %u%%\n", (progress / (total / 100)));
        events.send(p, "ota");
    });
    ArduinoOTA.onError([](ota_error_t error) {
        if (error == OTA_AUTH_ERROR)
            events.send("Auth Failed", "ota");
        else if (error == OTA_BEGIN_ERROR)
            events.send("Begin Failed", "ota");
        else if (error == OTA_CONNECT_ERROR)
            events.send("Connect Failed", "ota");
        else if (error == OTA_RECEIVE_ERROR)
            events.send("Recieve Failed", "ota");
        else if (error == OTA_END_ERROR)
            events.send("End Failed", "ota");
    });
    ArduinoOTA.setHostname(hostName);
    ArduinoOTA.begin();

    events.onConnect([](AsyncEventSourceClient *client) {
        client->send("hello!", NULL, millis(), 1000);
    });
}