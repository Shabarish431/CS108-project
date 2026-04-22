all:
	pdflatex Project_Report.tex
	bibtex Project_Report
	pdflatex Project_Report.tex
	pdflatex Project_Report.tex
.PHONY:
clean:
	rm -f *.aux *.log *.out *.bbl *.blg
open:
	xdg-open Project_Report.pdf 
