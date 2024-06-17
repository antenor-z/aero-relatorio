all:
	pdflatex  --shell-escape main
	bibtex main
	pdflatex  --shell-escape main
	pdflatex  --shell-escape main


clean:
	rm -f *.aux *.lof *.log *.lot *.fls *.out *.toc *.fmt *.fot *.cb *.cb2 .*.lb *.lol *.bbl