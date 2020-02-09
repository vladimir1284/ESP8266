#ifndef modbushandler_h
#define modbushandler_h

#include "ModbusSlave.h"

#define MAX_SLAVES 10

class ModbusHandler
{
public:
    ModbusHandler();
    void append(ModbusSlave *slave),
        run();

private:
    int nSlaves;

    ModbusSlave *slaves[MAX_SLAVES];
    ModbusSlave *_slave;
    unsigned int lastUpdate;
};

#endif // modbushandler_h