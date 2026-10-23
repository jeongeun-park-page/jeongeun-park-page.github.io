Publication content lives in this directory. Each HTML file contains one original publication card, including its authors, media, and links.

Edit `publications.json` to change the year, `tags` (zero to three per paper; use an empty list to omit a paper from the tag view), or `selected` flag. Papers appear in every matching tag section. The record order determines the order within each group and on the home page. Tag labels are defined in `scripts/build_publications.py`.

After editing cards, metadata, or `templates/home.html`, run from the repository root:

```sh
python3 scripts/build_publications.py
```

Commit the generated `index.html`, `publications.html`, and `publications-by-topic.html` as well as the source changes. GitHub Pages serves these static files directly; no build dependencies or client-side rendering are needed.

Open Source projects are listed in `open-source.json`. Add a project name, GitHub `owner/repository`, description, topics, optional local `image` path and `image_alt`, then run the same generator to update `open-source.html` and the shared navigation.

Open Source cards are sorted by `date` (YYYY-MM-DD), newest first, starting at the top left. Use the project release date; the initial two entries use their GitHub repository creation dates.
