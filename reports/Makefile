LATEXMK ?= latexmk
REPORT_NAME ?= report
REPORT_MAIN ?= main

.PHONY: all pdf clean

all: pdf

pdf:
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build "$(REPORT_MAIN).tex"
	mkdir -p output/pdf
	cp "build/$(REPORT_MAIN).pdf" "output/pdf/$(REPORT_NAME).pdf"

clean:
	$(LATEXMK) -c -outdir=build "$(REPORT_MAIN).tex"
