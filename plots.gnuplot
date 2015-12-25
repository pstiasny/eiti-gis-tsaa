set term png
set output 'plots.png'
set multiplot layout 2, 1
plot "aalog" using 1:2 title "temp"
plot "aalog" using 1:3 title "length"
