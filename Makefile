all:
	pdflatex Project_Report.tex
	bibtex Project_Report
	pdflatex Project_Report.tex
	pdflatex Project_Report.tex
clean:
	rm -f Project_Report.aux Project_Report.log Project_Report.out Project_Report.bbl Project_Report.blg Project_Report.pdf
open:
	xdg-open Project_Report.pdf 
