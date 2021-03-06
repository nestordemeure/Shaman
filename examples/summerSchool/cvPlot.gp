#!/usr/bin/gnuplot

set terminal pngcairo
set output "cvPlot.png"

set xlabel "Nb rectangles"
set format x "%.0e"

set ylabel "Erreur"
set format y "%.0e"
set yrange [1e-09 : *]

set logscale xy
plot "cvPlot.dat" using 1:3 title "Evaluation native", \
     "cvPlot.dat" using 1:4 title "Estimation Shaman"

unset output

set output "cvPlot_raw.png"
plot "cvPlot.dat" using 1:3 title "Evaluation native"
unset output