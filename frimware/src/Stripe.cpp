//
// Created by Adam Makswiej on 29/10/2023.
//

#include "Stripe.hpp"

#define MODE NEO_KHZ800

Stripe::Stripe(uint8_t pin): _impl(0, pin, NEO_GRB + MODE) {

}

void Stripe::setup() {
    _impl.begin();
}

void Stripe::init(uint8_t count, uint8_t type) {
    _impl.updateLength(count + 2);
    _impl.updateType(type + MODE);

    uint8_t wOffset = (type >> 6) & 0b11;
    uint8_t rOffset = (type >> 4) & 0b11;
    _has_white = wOffset != rOffset;
    _setHelperLEDs();
}


void Stripe::loop() {
    if (_shouldShow > 0) {
        _shouldShow--;
        _impl.show();
    }
}

void Stripe::show() {
    _shouldShow = 2;
}

bool Stripe::hasWhite() const {
    return _has_white;
}

void Stripe::set(uint16_t n, uint8_t r, uint8_t g, uint8_t b, uint8_t w) {
    _impl.setPixelColor(n + 1, Adafruit_NeoPixel::Color(r, g, b, w));
}

void Stripe::fill(uint8_t r, uint8_t g, uint8_t b, uint8_t w) {
    _impl.fill(Adafruit_NeoPixel::Color(r, g, b, w));
    _setHelperLEDs();
}

void Stripe::_setHelperLEDs() {
    if (_impl.getPin() % 2) {
        _impl.setPixelColor(0, Adafruit_NeoPixel::Color(15, 0, 0, 0));
    } else {
        _impl.setPixelColor(0, Adafruit_NeoPixel::Color(0, 15, 0, 0));
    }
    _impl.setPixelColor(_impl.numPixels() - 1, Adafruit_NeoPixel::Color(0, 0, 0, 0));
}
