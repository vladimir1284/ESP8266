#include "MsgProcessor.h"

MsgProcessor::MsgProcessor()
{
    modules_count = 0;
}

// ---------------------------------------------------------------------------
void MsgProcessor::appendModule(Module *module)
{
    modules[modules_count++] = module;
}

// ---------------------------------------------------------------------------
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

// ---------------------------------------------------------------------------
void MsgProcessor::handleSetOperation()
{
    StaticJsonDocument<RESPONSE_SIZE> response;
    String buffer;

    if (doc["type"] == "setup")
    {
        Serial.println("Setup");
        buffer = updateSetups(doc);
        currentClient->text(buffer);
        Serial.println(buffer);
        return;
    }
}

// ---------------------------------------------------------------------------
void MsgProcessor::handleGetOperation()
{
    StaticJsonDocument<RESPONSE_SIZE> response;
    String buffer;

    if (doc["type"] == "setup")
    {
        Serial.println("Setup");
        buffer = getSetups(doc["module"]);
        currentClient->text(buffer);
        Serial.println(buffer);
        return;
    }

    if (doc["type"] == "variables")
    {
        Serial.println("Variable");
        buffer = getVariables(doc["module"]);
        currentClient->text(buffer);
        Serial.println(buffer);
        return;
    }
}

// ---------------------------------------------------------------------------
String MsgProcessor::getVariables(String id)
{
    int i;
    for (i = 0; i < modules_count; i++)
    {
        if (modules[i]->module_id.equals(id))
        {
            return modules[i]->getVariables();
        }
    }
    return "No se encuentra el modulo " + id + "!";
}

// ---------------------------------------------------------------------------
String MsgProcessor::getSetups(String id)
{
    int i;
    for (i = 0; i < modules_count; i++)
    {
        if (modules[i]->module_id.equals(id))
        {
            return modules[i]->getConfigs();
        }
    }
    return "No se encuentra el modulo " + id + "!";
}

// ---------------------------------------------------------------------------
String MsgProcessor::updateSetups(StaticJsonDocument<512> rq_doc)
{
    int i;
    const char* id = rq_doc["module"];
    for (i = 0; i < modules_count; i++)
    {
        if (modules[i]->module_id.equals(id))
        {
            return modules[i]->setConfigs(rq_doc);
        }
    }
    return "No se encuentra el modulo " + String(id) + "!";
}

// ---------------------------------------------------------------------------
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

// ---------------------------------------------------------------------------
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