//
// Created by Adam Makswiej on 29/10/2023.
//

#include "State.hpp"
#include <Arduino.h>

State::State(uint8_t led) {
    _pinLed = led;
    _type = State::Type::IDLE;
    _type_once = State::Type::IDLE;
    _value = 0;
}

void State::setup() const {
    pinMode(_pinLed, OUTPUT);
    digitalWrite(_pinLed, LOW);
}

void State::loop() {
    switch (_type) {
        case Type::IDLE:
            digitalWrite(_pinLed, HIGH);
            break;
        case Type::ERROR:
            digitalWrite(_pinLed, LOW);
            _countDown();
            break;
        case Type::SUCCESS:
            digitalWrite(_pinLed, HIGH);
            _countDown();
            break;
    }
}

void State::idle() {
    _type_once = State::Type::ERROR;
}

void State::error() {
    _setType(State::Type::ERROR, 5);
}

void State::success() {
    _setType(State::Type::SUCCESS, 5);
}

State::Type State::once() {
    State::Type last = _type_once;
    idle();
    return last;
}

bool State::isIdle() {
    return _type == Type::IDLE;
}

void State::_setType(State::Type type, uint8_t value) {
    _type = type;
    _type_once = type;
    _value = value;
}

void State::_countDown() {
    if (_value > 0) {
        _value--;
    } else {
        _setType(State::Type::IDLE);
    }
}
