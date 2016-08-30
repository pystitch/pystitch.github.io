import bs4
from textwrap import dedent
from markdown import markdown
from itertools import takewhile, dropwhile
from toolz import partitionby
from jinja2 import Template


def rendered_pairs(src):
    with open(src) as f:
        soup = bs4.BeautifulSoup(f.read(), "lxml")

    pairs = []
    for head in soup.find_all('h2'):
        right = head.find_next('h2')
        nodes = (node for node in head.nextSiblingGenerator())
        selected = list(takewhile(lambda node: node != right, nodes))
        pairs.append({'head': head, 'rest': "\n".join(str(x) for x in selected)})
    return pairs


def source_pairs(src):
    with open(src) as f:
        doc = f.read()
    lines = doc.split("\n")
    lines = dropwhile(lambda line: not line.startswith("##"), lines)
    lines = list(partitionby(lambda x: x.startswith("##"), lines))
    headers, rest = lines[::2], lines[1::2]

    pairs = [{"head": h[0], "rest": '\n'.join(r)}
             for h, r in zip(headers, rest)]
    return pairs


def render(source, rendered):
    assert len(source) == len(rendered)
    pairs = [{"source": s, "rendered": r} for s, r in zip(source, rendered)]
    preamble = dedent('''\
    # Stitch

    Stitch is a small python library for writing reproducible reports in
    markdown.
    ''')
    preamble = markdown(preamble)

    tpl = Template('''
    <html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        <link rel="stylesheet" type="text/css" href="style.css">
        <link rel="stylesheet" type="text/css" href="default.css">
    </head>
    <body>

    <header class="nav-down">
    <nav class="navbar navbar-default">
      <ul class="nav navbar-nav">
        <li><a href="src/tidy.md">Markdown</a></li>
        <li><a href="build/tidy.html">HTML</a></li>
        <li><a href="build/tidy.pdf">PDF</a></li>
        <li><a href="build/tidy.docx">docx</a></li>
      </ul>
    </nav>
    </header>

    {{ preamble|safe }}
    <div class="container">
    {% for pair in pairs %}
    <div class="area">
        {{ pair.rendered.head | safe }}

        <div class="source">
            <pre>
                {{ pair.source.rest|safe }}
            </pre>
        </div>
        <div class="rendered">
            {{ pair.rendered.rest|safe }}
        </div>

    </div>
    <hr>
    {% endfor %}
    </div>

    <script src="https://code.jquery.com/jquery-3.1.0.slim.min.js" integrity="sha256-cRpWjoSOw5KcyIOaZNo4i6fZ9tKPhYYb6i5T9RSVJG8=" crossorigin="anonymous"></script>
    <script src="script.js"></script>

    </body>
    </html>
    ''')
    result = tpl.render(pairs=pairs, preamble=preamble)
    with open('index.html', 'w') as f:
        f.write(result)


def main():
    source = source_pairs("src/usage.md")
    rendered = rendered_pairs("build/usage.html")
    render(source, rendered)


if __name__ == '__main__':
    main()
