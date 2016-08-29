import bs4
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
    pairs = [{"source": s, "rendered": r} for s, r in zip(source, rendered)]
    tpl = Template('''
    <html>
    <head>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
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
    </body>
    </html>
    ''')
    result = tpl.render(pairs=pairs)
    with open('index.html', 'w') as f:
        f.write(result)


def main():
    source = source_pairs("src/usage.md")
    rendered = rendered_pairs("build/usage.html")
    render(source, rendered)

if __name__ == '__main__':
    main()
