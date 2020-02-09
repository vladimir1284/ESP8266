#ifndef modbusslave_h
#define modbusslave_h

#include "Configs.h"
#include <ModbusMaster485.h>

#define SLAVE_BUF_SIZE 64
#define MAX_REQUEST_SIZE 25

enum slave_status
{
    NEW_SLAVE,
    OK_SLAVE,
    ERROR_SLAVE,
};

class ModbusSlave
{
public:
    ModbusSlave(ModbusMaster485 *node);

    void init(int setupsAdr, int setupsCount,
              int variablesAdr, int variablesCount, int mbSpeed);

    int run(),
        getSlaveValue(int address);

private:
    int updateVariables(),
        getConfigs(),
        getModbus(int address, int nRegisters);

    int setups_adr,
        setups_count,
        variables_adr,
        variables_count,
        slave_id,
        status;

    uint16 slave_buffer[SLAVE_BUF_SIZE];

    ModbusMaster485 *_node;
};

#endif // modbusslave_h