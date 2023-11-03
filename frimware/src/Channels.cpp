//
// Created by Adam Makswiej on 29/10/2023.
//

#include "Channels.hpp"

Channels::Channels(uint8_t pin0, uint8_t pin1) : ch0( pin0), ch1(pin1) {

}

Stripe *Channels::get(uint8_t channel) {
    switch (channel) {
        case 0:
            return &ch0;
        case 1:
            return &ch1;
        default:
            return nullptr;
    }
}

void Channels::setup() {
    ch0.setup();
    ch1.setup();
}

void Channels::loop() {
    ch0.loop();
    ch1.loop();
}
