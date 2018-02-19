//
// Created by demeuren on 26/01/18.
//

#ifndef COMPENSATIONS_SCHRODINGER_H
#define COMPENSATIONS_SCHRODINGER_H

#include <vector>
#include "../shaman/shaman/Shaman.h"
#include "tests.h"

/*
 * timing on Nestor's ubuntu with g++5.4 and clang++5.0 :
 * double : 0.5s
 * S : 3.5s
 * => 7x slower
 * note : the computation is rich in multiplications and divisions, it takes 110s without the FMA flag enabled (!)
 *
 * on TERATEC's desktop + inline
 * double : 0.46s
 * S : 1.6s
 * => 3.5 slower
 * # 3.1ss with numerical debugger
 */

/*
 * Solving the Schrödinger Equation using the Numerov algorithm
 */
class Schrodinger
{
private:
    // constants
    std::vector<real> psi;
    real ECurrent;
    real EMin = 1.490;
    real xMin = -15.;
    real xMax = 15.;
    real hZero;
    real EDelta = 1e-7;
    real maxPsi = 1e-8;
    int numberDivisions = 200;

    // computations
    real calculateKSSquared(int n);
    real calculateNextPsi(int n);

public:
    // initialisation
    Schrodinger();

    // computations
    void calculate();
};


#endif //COMPENSATIONS_SCHRODINGER_H
