"""Generate the static site: python3 scripts/build_publications.py."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
TAGS = {
    'efficient': 'Efficient Learning',
    'safety': 'Safety and Robustness',
    'hri': 'Human-Robot Interaction',
    'foundation': 'Robot Foundation Model',
    'manipulation': 'Manipulation',
    'navigation': 'Navigation',
    'humanoids': 'Humanoids',
}
records = json.loads((ROOT / 'data/publications.json').read_text())
template = (ROOT / 'templates/home.html').read_text()
for record in records:
    assert 0 <= len(record['tags']) <= 3, record['id']
    assert len(record['tags']) == len(set(record['tags'])), record['id']
    assert all(tag in TAGS for tag in record['tags']), record['id']

def navigation(active):
    links = [('home', 'index.html', 'Home'), ('year', 'publications.html', 'By year'), ('topic', 'publications-by-topic.html', 'By tag')]
    items = []
    for key, url, label in links:
        current = ' aria-current="page"' if key == active else ''
        if key == 'year':
            items.append('<span class="nav-label">Publications</span>')
        items.append(f'<a href="{url}"{current}>{label}</a>')
    return '<a class="skip-link" href="#main-content">Skip to content</a><header class="site-header"><a class="site-name" href="index.html">Jeongeun Park</a><nav aria-label="Main navigation">' + ''.join(items) + '</nav></header>'

def card(record, group=None, show_tags=True):
    ident = f"{group}-{record['id']}" if group else record['id']
    html = (ROOT / f'data/{record["id"]}.html').read_text().replace('<div class="publication-block columns">', f'<div id="{ident}" class="publication-block columns">', 1)
    if not show_tags or not record['tags']:
        return html
    tags = '<div class="publication-tags" aria-label="Research tags">' + ''.join(
        f'<a href="publications-by-topic.html#group-{tag}">{TAGS[tag]}</a>'
        for tag in TAGS if tag in record['tags']
    ) + '</div>'
    marker = '<div class="publication-venue">'
    return html.replace(marker, tags + '\n' + marker, 1)

def tabs(active):
    return '<nav class="publication-tabs" aria-label="Publication views">' + ''.join(f'<a href="{url}"' + (' aria-current="page"' if key == active else '') + f'>{label}</a>' for key, url, label in [('year', 'publications.html', 'By year'), ('topic', 'publications-by-topic.html', 'By tag')]) + '</nav>'

selected = '<div class="section-heading"><h2 class="title is-3" id="publications">Selected Publications</h2><a href="publications.html">All publications &rarr;</a></div>\n' + ''.join(card(r, show_tags=False) for r in records if r['selected'])
(ROOT / 'index.html').write_text(template.replace('{{NAVIGATION}}', navigation('home')).replace('{{PUBLICATIONS}}', selected))
head = template.split('<body>')[0]
footer = template[template.index('  <footer class="footer">'):template.index('  <script>')]
for mode, filename in [('year', 'publications.html'), ('topic', 'publications-by-topic.html')]:
    groups = [(str(y), str(y)) for y in sorted({r['year'] for r in records}, reverse=True)] if mode == 'year' else list(TAGS.items())
    jumps = '<nav class="publication-jumps" aria-label="Jump to a section">' + ''.join(f'<a href="#group-{key}">{label}</a>' for key,label in groups) + '</nav>'
    content = ''
    for key,label in groups:
        group = [r for r in records if (str(r['year']) == key if mode == 'year' else key in r['tags'])]
        content += f'<section aria-labelledby="group-{key}"><h2 class="title is-4 publication-group" id="group-{key}">{label} <span class="group-count">({len(group)})</span></h2>' + ''.join(card(r, key) for r in group) + '</section>'
    page = head.replace('<title>Jeongeun Park</title>', f'<title>Publications by {"tag" if mode == "topic" else mode} | Jeongeun Park</title>') + '<body>\n' + navigation(mode) + '<main id="main-content" class="site-main"><section class="section"><div class="container is-max-desktop"><h1 class="title is-2">Publications</h1><p class="publication-intro">Browse all publications by year or research tag.</p>' + tabs(mode) + jumps + content + '</div></section></main>\n' + footer + '</body>\n</html>\n'
    (ROOT / filename).write_text(page)
print(f'Generated home and two publication pages from {len(records)} publications.')
