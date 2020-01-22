#include <ESPAsyncWebServer.h>

File fsUploadFile; // a File object to temporarily store the received file
AsyncWebServer server(80);

void setupServer()
{
    server.on("/heap", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send(200, "text/plain", String(ESP.getFreeHeap()));
    });

    server.serveStatic("/", SPIFFS, "/").setDefaultFile("tanque.html");

    server.onNotFound([](AsyncWebServerRequest *request) {
        Serial.printf("NOT_FOUND: ");
        if (request->method() == HTTP_GET)
            Serial.printf("GET");
        else if (request->method() == HTTP_POST)
            Serial.printf("POST");
        else if (request->method() == HTTP_DELETE)
            Serial.printf("DELETE");
        else if (request->method() == HTTP_PUT)
            Serial.printf("PUT");
        else if (request->method() == HTTP_PATCH)
            Serial.printf("PATCH");
        else if (request->method() == HTTP_HEAD)
            Serial.printf("HEAD");
        else if (request->method() == HTTP_OPTIONS)
            Serial.printf("OPTIONS");
        else
            Serial.printf("UNKNOWN");
        Serial.printf(" http://%s%s\n", request->host().c_str(), request->url().c_str());

        if (request->contentLength())
        {
            Serial.printf("_CONTENT_TYPE: %s\n", request->contentType().c_str());
            Serial.printf("_CONTENT_LENGTH: %u\n", request->contentLength());
        }

        int headers = request->headers();
        int i;
        for (i = 0; i < headers; i++)
        {
            AsyncWebHeader *h = request->getHeader(i);
            Serial.printf("_HEADER[%s]: %s\n", h->name().c_str(), h->value().c_str());
        }

        int params = request->params();
        for (i = 0; i < params; i++)
        {
            AsyncWebParameter *p = request->getParam(i);
            if (p->isFile())
            {
                Serial.printf("_FILE[%s]: %s, size: %u\n", p->name().c_str(), p->value().c_str(), p->size());
            }
            else if (p->isPost())
            {
                Serial.printf("_POST[%s]: %s\n", p->name().c_str(), p->value().c_str());
            }
            else
            {
                Serial.printf("_GET[%s]: %s\n", p->name().c_str(), p->value().c_str());
            }
        }

        request->send(404);
    });


    server.onFileUpload([](AsyncWebServerRequest *request, const String &fname, size_t index, uint8_t *data, size_t len, bool final) {
        String filename = "";
        if (!index)
        {
            filename = fname.c_str();
            if (!filename.startsWith("/"))
            {
                filename = "/" + filename;
            }
            Serial.print("handleFileUpload Name: ");
            Serial.println(filename);
            fsUploadFile = SPIFFS.open(filename, "w"); // Open the file for writing in SPIFFS (create if it doesn't exist)
        }
        if (fsUploadFile)
        {
            fsUploadFile.write(data, len); // Write the received bytes to the file
        }
        if (final)
        {
            if (fsUploadFile)
            {                         // If the file was successfully created
                fsUploadFile.close(); // Close the file again
                Serial.printf("UploadEnd: %s (%u)\n", fname.c_str(), index + len);
                //server.sendHeader("Location", "/upload.html"); // Redirect the client to the success page
                request->send(303);
            }
            else
            {
                request->send(500, "text/plain", "500: couldn't create file");
            }
        }
    });


    server.onRequestBody([](AsyncWebServerRequest *request, uint8_t *data, size_t len, size_t index, size_t total) {
        if (!index)
            Serial.printf("BodyStart: %u\n", total);
        Serial.printf("%s", (const char *)data);
        if (index + len == total)
            Serial.printf("BodyEnd: %u\n", total);
    });

    // ===================
    // ===== Start =======
    // ===================
    server.begin();
}