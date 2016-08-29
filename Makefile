build/usage.html: src/usage.md
	stitch src/usage.md -o build/usage.html


index.html: src/usage.md build/usage.html
	python make_page.py

