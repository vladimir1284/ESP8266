#include "module.h"

// ------- Constructor --------------
Module::Module()
{
}

// -------------------------------------------------------------------------
void Module::init(String id, ModbusSlave *slave, int setupsAdr, int variablesAdr)
{
    module_id = id;
    _slave = slave;
    setups_adr = setupsAdr;
    variables_adr = variablesAdr;
}

// -------------------------------------------------------------------------
String Module::getConfigs()
{
    return "Response from the base class!";
}

// -------------------------------------------------------------------------
String Module::getVariables()
{
    return "Response from the base class!";
}

// -------------------------------------------------------------------------
String Module::setConfigs(StaticJsonDocument<512> rq_doc)
{
    return "Response from the base class!";
}

/*
=========================== PumpControlModule ===================================== 
*/

// -------------------------------------------------------------------------
String PumpControlModule::getConfigs()
{
    StaticJsonDocument<RESPONSE_SIZE> response;

    int index = setups_adr;

    response["UT_HEIGTH"] = _slave->getSlaveValue(index++);
    response["UT_GAP"] = _slave->getSlaveValue(index++);
    response["UT_MIN"] = _slave->getSlaveValue(index++);
    response["UT_RESTART"] = _slave->getSlaveValue(index++);
    response["LT_HEIGTH"] = _slave->getSlaveValue(index++);
    response["LT_GAP"] = _slave->getSlaveValue(index++);
    response["LT_MIN"] = _slave->getSlaveValue(index++);
    response["LT_RESTART"] = _slave->getSlaveValue(index++);
    response["PUMP_START_CAP"] = _slave->getSlaveValue(index++);
    response["PUMP_ON"] = _slave->getSlaveValue(index++);
    response["FULL_TANK"] = _slave->getSlaveValue(index++);

    String responseBuffer;
    serializeJson(response, responseBuffer);
    Serial.println(responseBuffer);
    return responseBuffer;
}

// -------------------------------------------------------------------------
String PumpControlModule::getVariables()
{
    StaticJsonDocument<RESPONSE_SIZE> response;

    int index = variables_adr;

    response["UT_LEVEL"] = _slave->getSlaveValue(index++);
    response["LT_LEVEL"] = _slave->getSlaveValue(index++);
    response["PC_STATE"] = _slave->getSlaveValue(index++);

    String responseBuffer;
    serializeJson(response, responseBuffer);
    Serial.println(responseBuffer);
    return responseBuffer;
}

// -------------------------------------------------------------------------
String PumpControlModule::setConfigs(StaticJsonDocument<512> rq_doc)
{
    StaticJsonDocument<RESPONSE_SIZE> response;

    int index = variables_adr;

    response["status"] = "test";
    response["cmd"] = "set";
    response["type"] = "setup";
    response["module"] = rq_doc["module"];

    String responseBuffer;
    serializeJson(response, responseBuffer);
    Serial.println(responseBuffer);
    return responseBuffer;
}

/*
=========================== LightControlModule ===================================== 
*/

// -------------------------------------------------------------------------
String LightControlModule::getConfigs()
{
    StaticJsonDocument<RESPONSE_SIZE> response;

    int index = setups_adr;

    response["LIGHT_MODE"] = _slave->getSlaveValue(index++);
    response["LIGHT_SLEEP_TIME"] = _slave->getSlaveValue(index++);
    response["LIGHT_SMART"] = _slave->getSlaveValue(index++);
    response["LIGHT_SMART_DELAY"] = _slave->getSlaveValue(index++);
    response["LIGHT_INIT_DELAY"] = _slave->getSlaveValue(index++);
    response["LIGHT_DELAY_INCREMENT"] = _slave->getSlaveValue(index++);
    response["LIGHT_TRESHOLD"] = _slave->getSlaveValue(index++);

    String responseBuffer;
    serializeJson(response, responseBuffer);
    Serial.println(responseBuffer);
    return responseBuffer;
}

// -------------------------------------------------------------------------
String LightControlModule::getVariables()
{
    StaticJsonDocument<RESPONSE_SIZE> response;

    int index = variables_adr;

    response["LUMINOSITY"] = _slave->getSlaveValue(index++);
    response["PIR_STATE"] = _slave->getSlaveValue(index++);
    response["LIGHT_STATE"] = _slave->getSlaveValue(index++);

    String responseBuffer;
    serializeJson(response, responseBuffer);
    Serial.println(responseBuffer);
    return responseBuffer;
}

// -------------------------------------------------------------------------
String LightControlModule::setConfigs(StaticJsonDocument<512> rq_doc)
{
    StaticJsonDocument<RESPONSE_SIZE> response;

    int index = variables_adr;

    response["status"] = "test";
    response["cmd"] = "set";
    response["type"] = "setup";
    response["module"] = rq_doc["module"];

    String responseBuffer;
    serializeJson(response, responseBuffer);
    Serial.println(responseBuffer);
    return responseBuffer;
}