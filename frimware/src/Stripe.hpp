//
// Created by Adam Makswiej on 29/10/2023.
//

#ifndef __TINYPIXEL___SRC_STRIPE____
#define __TINYPIXEL___SRC_STRIPE____

#include <Adafruit_NeoPixel.h>

class Stripe {
private:
    Adafruit_NeoPixel _impl;
    bool _has_white{};
protected:
    volatile uint8_t _shouldShow = 0;
public:
    explicit Stripe(uint8_t pin);

    void setup();
    void init(uint8_t count = 0, uint8_t type = 0);
    void loop();

    bool hasWhite() const;

    void set(uint16_t n, uint8_t r, uint8_t g, uint8_t b, uint8_t w = 0);
    void fill(uint8_t r, uint8_t g, uint8_t b, uint8_t w = 0);

    void show();

    void _setHelperLEDs();
};


#endif // __TINYPIXEL___SRC_STRIPE____
