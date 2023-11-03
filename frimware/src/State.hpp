//
// Created by Adam Makswiej on 29/10/2023.
//

#ifndef __TINYPIXEL___SRC_STATE____
#define __TINYPIXEL___SRC_STATE____

#include <stdint.h>

class State {
public:
    enum class Type : uint8_t {
        IDLE,
        SUCCESS,
        ERROR
    };

private:
    uint8_t _pinLed;
    Type _type;
    Type _type_once;
    uint8_t _value;

    void _setType(Type type, uint8_t value = 0);
    void _countDown();
public:
    explicit State(uint8_t led);
    Type once();

    void setup() const;
    void loop();

    void idle();
    void error();
    void success();

    bool isIdle();
};


#endif // __TINYPIXEL___SRC_STATE____
