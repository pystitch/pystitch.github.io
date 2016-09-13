Whatsnew
========

Version 0.3.4
`````````````

- BUG: Fixed a bug in the chunk options-line parser where arguments like ``fig.cap="Figure, captioned"``, quoted strings
  containing a comma, would break the parser (:issue:`42`)
- API: Accept ``fig.cap`` as a chunk option to control the figure caption (:issue:`38`)
- API: Exposed the ``no-self-contained`` command-line option to the stitching
  operation.
- API: Added a ``warning`` option for controling whether stderr is included in the output.
- API: Changed the ``on_error`` option to ``error`` for compatability with knitr and symmytry with the ``warning`` option.

Version 0.3.3
`````````````

- Included ``default.css`` in the source and binary distributions (:issue:`26`).
- Fixed not handling output from IPython's various ``display`` methods (:issue:`27`).
