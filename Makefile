all:
	pdflatex main
	bibtex main
	pdflatex main
	pdflatex main


clean:
	rm *.aux *.lof *.log *.lot *.fls *.out *.toc *.fmt *.fot *.cb *.cb2 .*.lb *.lol