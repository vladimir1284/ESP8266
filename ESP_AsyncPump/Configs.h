#ifndef configs_h
#define configs_h

#include <Arduino.h>

#define EnTxPin 5 // HIGH:TX y LOW:RX
#define RxPin 4
#define TxPin 14
#define MB_SPEED 19200

#define RESPONSE_SIZE 200

#define REQUEST_DELAY 2000
#define DEBUG true


enum slave1_addresses
{
    //  ----------- Configs-----------
    // Pump Controller 0
    ADR_UT_HEIGTH,
    ADR_UT_GAP,
    ADR_UT_MIN,
    ADR_UT_RESTART,
    ADR_LT_HEIGTH,
    ADR_LT_GAP,
    ADR_LT_MIN,
    ADR_LT_RESTART,
    ADR_PUMP_START_CAP,
    ADR_PUMP_ON,
    ADR_FULL_TANK,
    // Light 0
    ADR_LIGHT_MODE_0,
    ADR_LIGHT_SLEEP_TIME_0,
    ADR_LIGHT_SMART_0,
    ADR_LIGHT_SMART_DELAY_0,
    ADR_LIGHT_INIT_DELAY_0,
    ADR_LIGHT_DELAY_INCREMENT_0,
    ADR_LIGHT_TRESHOLD_0,
    //  ----------- Vaiables-----------
    // Pump Controller 0
    ADR_UT_LEVEL,
    ADR_LT_LEVEL,
    ADR_PC_STATE,
    ADR_ERROR_ACK, // Coil
    // Light 0
    ADR_LUMINOSITY_0,
    ADR_PIR_STATE_0,
    ADR_LIGHT_STATE_0,
};


#endif // configs_h