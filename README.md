# AdGenerator

## Free promotion pipeline

The generator does not send ads or make network requests. It creates optional
promotion drafts, a static author library, and an RSS feed that updates whenever
the catalog is regenerated. Feed readers can subscribe and check for updates
automatically; this reaches subscribers, not people who have not opted in. The
page does not transmit visitor browsing activity; book-cover images are loaded
from Amazon's image host.

Run it with Python 3:

```sh
python3 zero_cost_ad_pipeline.py
```

It generates:

- `campaign_pack.md`: short social posts, community-post drafts, and an opt-in
	email draft for each book. Share only where promotion is allowed, and send
	emails only to people who opted in.
- `docs/index.html`: a searchable author library with book listings and a
	visitor-initiated share button.
- `docs/feed.xml`: an RSS feed for readers who subscribe through their feed app.
- `docs/book-discovery.js`: a contextual widget for participating websites.
- `docs/<IndexNow key>.txt`: public ownership verification for search crawling.
- `docs/robots.txt` and `docs/sitemap.xml`: basic search-engine discovery files.

### Contextual network prototype

The widget does not need a separate page for each book. A participating site
owner can place this where a contextual book recommendation may appear:

```html
<div data-book-discovery></div>
<script defer src="https://chrissysmith260-droid.github.io/AdGenerator/book-discovery.js"></script>
```

It compares the current page's title, description, and main/article text against
catalog topics, then shows at most one clearly labeled sponsored book linking
directly to its retailer. Matching happens in the visitor's browser; the widget
does not read or transfer browsing history, keep an identifier, or send page
text to the catalog. Loading the script does make a normal request to GitHub
Pages; a host can instead copy and serve the script locally. A recent book gets
priority only when its publication date is known, its review count is explicitly
zero, and its topics match the page. Unknown review counts are never treated as
zero. Site owners must choose to install the widget; it cannot add itself to
unrelated sites or search results.

To preview locally, run `python3 -m http.server 8080 --bind 0.0.0.0 --directory docs`
or start **Book page: local preview** from VS Code's Run and Debug panel. For a
public forwarded URL, start **Book page: public HTTPS preview** and paste the
HTTPS URL for port 8080 when prompted. The preview server speaks HTTP inside
the workspace; the forwarded-port service provides HTTPS externally.

### Before publishing

Edit the `BOOKS` entries in `zero_cost_ad_pipeline.py` to add or correct books,
descriptions, topics, cover images, ISBNs, and retailer links. The current catalog
contains ten Kindle titles found on the public Amazon author page and author
search; it may not include every print, IngramSpark, or other retailer edition.
Review the entries and add any missing titles before publishing. Two Amazon
listings did not expose their descriptions to the catalog builder, so those
entries link readers to Amazon for the full descriptions.

The included GitHub Actions workflow regenerates and publishes the author library
and RSS feed when its source or `docs/` changes on `main`. After deployment, it
submits only this site's library, feed, sitemap, and widget URLs to IndexNow,
which notifies participating search engines to crawl them. This does not submit
Amazon product URLs, guarantee indexing, or improve ranking by itself. Google
Search Console remains a separate, free verification and sitemap-submission step.
Social networks are not
connected yet: automatic posts require authorization for accounts you control
and each platform's supported API. Credentials must be stored as repository
secrets, never in this repository or chat. In the repository's **Settings >
Pages**, set the build and deployment source to **GitHub Actions**. Then push to
`main` or run **Deploy book page** from the Actions tab. The public page will be available at
https://chrissysmith260-droid.github.io/AdGenerator/ after the workflow
completes. Publishing makes the library accessible; it does not guarantee feed
placement or automatically send promotional messages.