//
// Created by Adam Makswiej on 29/10/2023.
//

#ifndef __TINYPIXEL___SRC_TYPES____
#define __TINYPIXEL___SRC_TYPES____

#include <stdint.h>

enum class Command : uint8_t {
    SETUP = 0xF,
    OFF = 0x0,
    FILL = 0x1,
    SET = 0x2,
    SHOW = 0xE,
};

#endif // __TINYPIXEL___SRC_TYPES____
