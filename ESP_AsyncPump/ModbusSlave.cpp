#include "ModbusSlave.h"

// ------- Constructor -------------------
ModbusSlave::ModbusSlave(ModbusMaster485 *node)
{
    _node = node;
};

// ------------------------------------------------------------------------
void ModbusSlave::init(int setupsAdr, int setupsCount,
                       int variablesAdr, int variablesCount, int mbSpeed)
{
    setups_adr = setupsAdr;
    setups_count = setupsCount;
    variables_adr = variablesAdr;
    variables_count = variablesCount;

    // init
    _node->begin(mbSpeed);
    status = NEW_SLAVE;
}

// ------------------------------------------------------------------------
int ModbusSlave::run()
{
    if (status != OK_SLAVE)
    {
        getConfigs();
    }
    updateVariables();
}

// ------------------------------------------------------------------------
int ModbusSlave::getSlaveValue(int address)
{
    if (address > 0 && address < SLAVE_BUF_SIZE)
    {
        return slave_buffer[address];
    }
    else
    {
        return -1;
    }
}

// ------------------------------------------------------------------------
int ModbusSlave::getConfigs()
{
    getModbus(setups_adr, setups_count);
}

// ------------------------------------------------------------------------
int ModbusSlave::updateVariables()
{
    getModbus(variables_adr, variables_count);
}

// ------------------------------------------------------------------------
int ModbusSlave::getModbus(int address, int nRegisters)
{
    int request_size;
    int count = 0;
    status = OK_SLAVE;
    do
    {
        request_size = nRegisters - count * MAX_REQUEST_SIZE;
        if (request_size > MAX_REQUEST_SIZE)
        {
            request_size = MAX_REQUEST_SIZE;
        }
        uint8_t j, result;

        // slave: read (request_size) 16-bit registers starting at register 0 to RX buffer
        result = _node->readHoldingRegisters(address + count * MAX_REQUEST_SIZE, request_size);

        // update local buffer if success
        if (result == _node->ku8MBSuccess)
        {
            for (j = 0; j < request_size; j++)
            {
                slave_buffer[address + j + count * MAX_REQUEST_SIZE] = _node->getResponseBuffer(j);
                if (DEBUG)
                {
                    Serial.print(_node->getResponseBuffer(j));
                    Serial.print(",");
                }
            }
            if (DEBUG)
            {
                Serial.println();
            }
        }
        else
        {
            status = ERROR_SLAVE;
            if (DEBUG)
            {
                Serial.print("Modbus Error from Slave: ");
            }
        }
        count++;
    } while (request_size == MAX_REQUEST_SIZE);
}