set term png
set output 'stats.png'
set multiplot layout 2, 1
set xlabel "Temperatura początkowa"
set ylabel "Długość cyklu"
plot "stats" using 1:2 smooth unique title "średnia długość cyklu", \
     "stats" using 1:2 title "długości cyklu"
set ylabel "Liczba iteracji"
plot "stats" using 1:3 smooth unique title "średnia liczba iteracji", \
     "stats" using 1:3 title "liczba iteracji"
