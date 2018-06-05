//
// Created by nestor on 18/05/18.
//

#ifndef SHAMAN_DEMO_H
#define SHAMAN_DEMO_H

#include "../shaman/Shaman.h"

/*
 * computing sqrt(x) using Heron's algorithm
 */
void sqrtHeron()
{
    Sdouble x = 2;
    Sdouble r = x/2;

    while(1e-15 < abs(r*r - x))
    {
        r = (r + x/r) / 2;
        printf("sqrt=%.15e error=%.15e\n", r.number, r.error);
    }
}

#endif //SHAMAN_DEMO_H
