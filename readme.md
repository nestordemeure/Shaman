# SHAMAN : A library that bridges the gap between humans and the invisible world of numerical errors

## What is Shaman ?

Shaman is a library that can be used to evaluate the numerical accuracy of an application but also to locate and reduce numerical unstabilities.

## How to use Shaman ?

Shaman is meant to be used with a test suite (usual recommendations such as having a good coverage apply), for all tests :

- Instrument the code with Shaman (see the `doc/how_to_instrument.md` file).
- Stabilize meaninful branches (unstable branches can be detected with the numerical debugger, see the `doc/how_to_debug.md` file).
- Get the number of significant digits over a specified threshold (by default Shaman will only output digits it considers significant).

Once your branches are stable and your error is low enough, your code is verified.

## Give me an example !

See the `examples` folder.

## How to install Shaman ?

Run `cmake -DCMAKE_INSTALL_PREFIX=path/to/installation/folder .` followed by `make install`.

## How to link a project with Shaman ?

Add `find_package(shaman)` to the CMakeLists.txt file (and set the shaman_DIR variable with the path to shaman's cmake files).

Add `PUBLIC shaman::shaman` the `target_link_libraries` line in your CMakeLists.txt.

## How does Shaman works ?

Shaman lets you do a computation while running a model of the propagation of numerical error in your code.
Having both the result and a good approximation of its numerical error, we can deduce the number of significant digits and numerical unstabilities such as unstable tests.

The error is deduced using Error Free Transformationss and higher precision arithmetic, detailled explainations and further references are included in a paper that will soon be published.

It is important to note that we don't take the impact of the control flow of the code into account.
In other words, if your code had taken a different branch (due to an unstable test) its numerical error might have been vastly different
(this will usually lead to Shaman underestimating the stability of codes that have been designed to be resilient to numerical error in intermediate steps).
Hence you need to be sure that meaningful branches are stable before starting to trust the number of significant digits that is displayed by Shaman.

