all:
	pdflatex report.tex
	pdflatex report.tex
clean:
	rm -f report.aux report.log report.out report.bbl report.blg
open:
	xdg-open report.pdf 
