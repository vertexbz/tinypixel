//
// Created by Adam Makswiej on 29/10/2023.
//

#ifndef __TINYPIXEL___SRC_CHANNELS____
#define __TINYPIXEL___SRC_CHANNELS____

#include <stdint.h>
#include "Stripe.hpp"

class Channels {
protected:
    Stripe ch0;
    Stripe ch1;

public:
    Channels(uint8_t pin0, uint8_t pin1);
    void setup();
    void loop();
    Stripe *get(uint8_t channel);
};


#endif // __TINYPIXEL___SRC_CHANNELS____
