//
// Created by demeuren on 04/06/18.
//

#ifndef SHAMAN_ERRORSUM_H
#define SHAMAN_ERRORSUM_H

#include <unordered_map>
#include <algorithm>
#include <numeric>
#include <sstream>
#include <iomanip>
#include <iostream>
#include "Tagger.h"

template<typename errorType> class ErrorSum
{
public:
    // contains the error decomposed in composants (one per block encountered)
    // errors[tag] = error // if tag is out or range, error is 0
    std::vector<errorType> errors;

    //-------------------------------------------------------------------------
    // CONSTRUCTORS

    /*
     * empty constructor : currently no error
     */
    explicit ErrorSum(): errors() {}

    /*
     * returns an errorSum with a single element (singleton)
     */
    explicit ErrorSum(Tag tag, errorType error): errors()
    {
        errors.resize(tag+1);
        errors[tag] = error;
    }

    /*
     * returns an errorSum with a single element (singleton)
     * uses the current tag
     */
    explicit ErrorSum(errorType error): errors()
    {
        Tag tag = Block::currentBlock();
        errors.resize(tag+1);
        errors[tag] = error;
    }

    //-------------------------------------------------------------------------
    // OPERATIONS

    /*
     * ~-
     */
    void unaryNeg()
    {
        for(auto& error : errors)
        {
            error = -error;
        }
    }

    /*
     * *= scalar
     */
    void multByScalar(errorType scalar)
    {
        for(auto& error : errors)
        {
            error *= scalar;
        }
    }

    /*
     * /= scalar
     */
    void divByScalar(errorType scalar)
    {
        for(auto& error : errors)
        {
            error /= scalar;
        }
    }

    /*
     * += error
     */
    void addError(errorType error)
    {
        Tag tag = Block::currentBlock();

        // insures that errors is big enough to store the results
        if (tag >= errors.size())
        {
            errors.resize(tag+1);
        }

        errors[tag] += error;
    }

    /*
     * += errorComposants
     */
    void addErrors(const ErrorSum& errors2)
    {
        addMap(errors2, [](errorType e){return e;});
    }

    /*
     * -= errorComposants
     */
    void subErrors(const ErrorSum& errors2)
    {
        addMap(errors2, [](errorType e){return -e;});
    }

    /*
     * += scalar * errorComposants
     */
    void addErrorsTimeScalar(const ErrorSum& errors2, errorType scalar)
    {
        addMap(errors2, [scalar](errorType e){return e*scalar;});
    }

    /*
     * -= scalar * errorComposants
     */
    void subErrorsTimeScalar(const ErrorSum& errors2, errorType scalar)
    {
        addMap(errors2, [scalar](errorType e){return -e*scalar;});
    }

    //-------------------------------------------------------------------------

    /*
     * applies a function f to the elements of errors2 and add them to errors
     */
    template<typename FUN>
    inline void addMap(const ErrorSum& errorSum2, FUN f)
    {
        auto& errors2 = errorSum2.errors;

        // insures that errors is big enough to store the results
        if (errors2.size() > errors.size())
        {
            errors.resize(errors2.size());
        }

        // adds the values from errors2 to errors
        for(int tag = 0; tag < errors2.size(); tag++)
        {
            errors[tag] += f(errors2[tag]);
        }
    }

    //-------------------------------------------------------------------------
    // DISPLAY

    /*
     * produces a readable string representation of the error terms
     * the error terms are sorted from larger to smaller
     * displays only the maxElementNumberDisplayed first elements with an amplitude big enough to matter given the type (10^-19 doesn't matter for a float
     */
    explicit operator std::string() const
    {
        std::ostringstream output;
        output << std::scientific << std::setprecision(2) << '[';
        int maxElementNumberDisplayed = 5;

        if(errors.empty())
        {
            output << "no-error";
        }
        else
        {
            // collect the relevant data the data
            std::vector<std::pair<Tag, errorType>> data;
            for(int tag = 0; tag < errors.size(); tag++)
            {
                errorType error = errors[tag];
                if(error != 0.)
                {
                    data.push_back(std::make_pair(tag, error));
                }
            }

            // sorts the vector by abs(error) descending
            auto compare = [](const std::pair<Tag, errorType>& p1, const std::pair<Tag, errorType>& p2){return std::abs(p1.second) > std::abs(p2.second);};
            std::sort(data.begin(), data.end(), compare);

            // functions that returns only if the error is big enough to have an impact given the type
            int nbDigitsMax = std::numeric_limits<errorType>::digits10 + 1;
            auto significant = [nbDigitsMax](const std::pair<Tag, errorType>& p){return -std::log10(std::abs(p.second)) < nbDigitsMax;};

            // displays the first element
            int i = 0;
            auto kv = data[0];
            output << Block::nameOfTag(kv.first) << ':' << kv.second;
            i++;

            // displays each other element prefixed by a ", " separator
            while((i < maxElementNumberDisplayed) && (i < data.size()) && (significant(data[i])))
            {
                kv = data[i];
                output << ", " << Block::nameOfTag(kv.first) << ':' << kv.second;
                i++;
            }

            // adds a reminder that we are not displaying all error terms
            if(i < data.size())
            {
                output << "…";
            }
        }

        output << ']';
        return output.str();
    }
};

#endif //SHAMAN_ERRORSUM_H
