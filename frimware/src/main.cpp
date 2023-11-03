#include <Arduino.h>
#include <Wire.h>
#include <avr/power.h>

#include "Channels.hpp"
#include "State.hpp"
#include "types.hpp"

const uint8_t LAP_MS = 100;
const uint8_t STEP_MS = 10;

State state(1);
Channels channels(3, 4);


inline bool handleCommand(Command command, Stripe *channel, uint8_t input) {
#define checksum(a) if ((uint8_t)(input ^ a) != (uint8_t)Wire.read()) { return false; } else
    switch (command) {
        case Command::SETUP: {
            uint8_t length = Wire.read();
            uint8_t type = Wire.read();

            checksum(length ^ type) {
                channel->init(length, type);
            }
        }   break;
        case Command::OFF: {
            checksum(0xff) {
                channel->fill(0, 0, 0);
                channel->show();
            }
        }   break;
        case Command::SHOW: {
            checksum(0xff) {
                channel->show();
            }
        }   break;
        case Command::FILL: {
            uint8_t r = Wire.read();
            uint8_t g = Wire.read();
            uint8_t b = Wire.read();
            if (channel->hasWhite()) {
                uint8_t w = Wire.read();
                checksum(r ^ g ^ b ^ w) {
                    channel->fill(r, g, b, w);
                }
            } else {
                checksum(r ^ g ^ b) {
                    channel->fill(r, g, b);
                }
            }
        }   break;
        case Command::SET: {
            uint8_t index = Wire.read();
            uint8_t r = Wire.read();
            uint8_t g = Wire.read();
            uint8_t b = Wire.read();

            if (channel->hasWhite()) {
                uint8_t w = Wire.read();
                checksum(index ^ r ^ g ^ b ^ w) {
                    channel->set(index, r, g, b, w);
                }
            } else {
                checksum(index ^ r ^ g ^ b) {
                    channel->set(index, r, g, b);
                }
            }
        }   break;
        default: return false;
    }
    return true;
}

void I2C_TxHandler() {
    switch (state.once()) {
        case State::Type::IDLE:
            Wire.write(0x00);
            break;
        case State::Type::SUCCESS:
            Wire.write(0x42);
            break;
        case State::Type::ERROR:
            Wire.write(0xFF);
            break;
    }
}

void I2C_RxHandler(int _) {
    while(Wire.available()) {
        uint8_t input = Wire.read();
        Stripe *channel = channels.get(input & 0x0F);

        if (channel != nullptr) {
            state.idle();
            if (handleCommand(Command(input >> 4), channel, input)) {
                state.success();
                continue;
            }
        }

        state.error();
    }
}
void setup() {
#if defined(__AVR_ATtiny85__) && (F_CPU == 8000000)
    clock_prescale_set(clock_div_1);
#endif

    state.setup();
    channels.setup();
    Wire.begin(0x69);
    Wire.onReceive(I2C_RxHandler);
    Wire.onRequest(I2C_TxHandler);
}

void loop() {
    state.loop();
    if (!state.isIdle()) {
        delay(LAP_MS);
        return;
    }
    for (uint8_t i = 0; i < LAP_MS / STEP_MS; ++i) {
        channels.loop();
        delay(STEP_MS);
    }
}