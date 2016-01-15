default: plots.png stats.png

plots.png: aalog plots.gnuplot
	gnuplot plots.gnuplot

aalog: main.py
	pypy3 main.py -l aalog odleglosci.csv

stats: make_stats.sh main.py
	bash make_stats.sh

stats.png: stats stats.gnuplot
	gnuplot stats.gnuplot
