plots.png: aalog plots.gnuplot
	gnuplot plots.gnuplot

aalog: main.py
	pypy3 main.py
