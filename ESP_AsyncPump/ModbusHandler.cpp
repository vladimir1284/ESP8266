#include "ModbusHandler.h"

// ------- Constructor -------------------
ModbusHandler::ModbusHandler()
{
    nSlaves = 0;
    lastUpdate = 0;
}

// ----------------------------------------------
void ModbusHandler::append(ModbusSlave *slave)
{
    slaves[nSlaves++] = slave;
    _slave = slave;
}

// ----------------------------------------------
void ModbusHandler::run()
{
    int i;
    if (millis() - lastUpdate > REQUEST_DELAY)
    {
        // Update info from slaves
        for (i = 0; i < nSlaves; i++)
        {
            slaves[i]->run();
            //_slave->run();
        }
        lastUpdate = millis();
    }
}