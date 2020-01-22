#include "MsgProcessor.h"

MsgProcessor::MsgProcessor()
{
}

void MsgProcessor::processWsMessage(String msg, AsyncWebSocketClient *client)
{
    currentClient = client;
    // Deserialize the JSON document
    DeserializationError error = deserializeJson(doc, msg);
    // Test if parsing succeeds.
    if (error)
    {
        String response = "deserializeJson() failed: " + String(error.c_str());
        Serial.println(response);
        currentClient->text(response);
        return;
    }
    if (doc["cmd"] == "fs")
    {
        handleFileOperation();
        return;
    }
    if (doc["cmd"] == "get")
    {
        handleGetOperation();
        return;
    }
    if (doc["cmd"] == "set")
    {
        handleSetOperation();
        return;
    }
}

void MsgProcessor::handleSetOperation()
{
}

void MsgProcessor::handleGetOperation()
{
    StaticJsonDocument<RESPONSE_SIZE> response;
    String buffer;

    if (doc["type"] == "setup")
    {
        response["UT_HEIGTH"] = mbPumpData[ADR_UT_HEIGTH];
        response["UT_GAP"] = mbPumpData[ADR_UT_GAP];
        response["UT_MIN"] = mbPumpData[ADR_UT_MIN];
        response["UT_RESTART"] = mbPumpData[ADR_UT_RESTART];
        response["LT_HEIGTH"] = mbPumpData[ADR_LT_HEIGTH];
        response["LT_GAP"] = mbPumpData[ADR_LT_GAP];
        response["LT_MIN"] = mbPumpData[ADR_LT_MIN];
        response["LT_RESTART"] = mbPumpData[ADR_LT_RESTART];

        response["type"] = doc["type"];
        response["slave"] = doc["slave"];

        serializeJson(response, buffer);
        currentClient->text(buffer);
        //Serial.println(buffer);
        return;
    }

    if (doc["type"] == "variables")
    {
        response["UT_LEVEL"] = mbPumpData[ADR_UT_LEVEL];
        response["LT_LEVEL"] = mbPumpData[ADR_LT_LEVEL];
        response["PC_STATE"] = mbPumpData[ADR_PC_STATE];

        response["type"] = doc["type"];
        response["slave"] = doc["slave"];

        serializeJson(response, buffer);
        currentClient->text(buffer);
        //Serial.println(buffer);
        return;
        return;
    }
}

String MsgProcessor::fixFileName(String str)
{
    const char *txt = doc[str];
    String filename = String(txt);
    if (!filename.startsWith("/"))
    {
        filename = "/" + filename;
    }
    return filename;
}

void MsgProcessor::handleFileOperation()
{
    String response = "";
    if (doc["operation"] == "remove")
    {
        String filename = fixFileName("filename");
        if (SPIFFS.remove(filename))
        {
            response = "deleted: " + filename;
        }
        else
        {
            response = "Not found: " + filename;
        }
        Serial.println(response);
        currentClient->text(response);
        return;
    }
    if (doc["operation"] == "rename")
    {
        String ifilename = fixFileName("ifile");
        String ofilename = fixFileName("ofile");
        if (SPIFFS.rename(ifilename, ofilename))
        {
            response = "Moved: " + ifilename + "->" + ofilename;
        }
        else
        {
            response = "Can't move: " + ifilename + "->" + ofilename;
        }
        Serial.println(response);
        currentClient->text(response);
        return;
    }
}