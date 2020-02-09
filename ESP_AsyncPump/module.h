#ifndef module_h
#define module_h

#include "ModbusSlave.h"
#include <ArduinoJson.h>

class Module
{
public:
    Module();
    void init(String id, ModbusSlave *slave, int setups_adr, int variables_adr);
    virtual String getConfigs(),
        getVariables(),
        setConfigs(StaticJsonDocument<512> rq_doc);

    String module_id;

protected:
    int setups_adr,
        variables_adr;

    ModbusSlave *_slave;

};

class PumpControlModule : public Module
{
public:
    virtual String getConfigs(),
        getVariables(),
        setConfigs(StaticJsonDocument<512> rq_doc);
};

class LightControlModule : public Module
{
public:
    virtual String getConfigs(),
        getVariables(),
        setConfigs(StaticJsonDocument<512> rq_doc);
};

#endif // module_h
