.PHONY: all

all: index.html build/tidy.html build/tidy.pdf build/tidy.docx


build/usage.html: src/usage.md
	stitch src/usage.md -o build/usage.html


index.html: src/usage.md build/usage.html
	python make_page.py

build/tidy.html: src/tidy.md
	stitch src/tidy.md -o build/tidy.html

build/tidy.pdf: src/tidy.md
	stitch src/tidy.md -t latex -o build/tidy.pdf

build/tidy.docx: src/tidy.md
	stitch src/tidy.md -o build/tidy.docx
