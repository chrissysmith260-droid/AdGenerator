"""Build shareable campaign drafts and a static book page without network calls."""

import json
from html import escape
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
SITE_DIR = ROOT / "docs"

# Replace the first book's placeholder title and description before publishing.
BOOKS = [
    {
        "slug": "book-b0hlfx1ykt",
        "title": "Edit this title for B0HLFX1YKT",
        "description": "Add a short, accurate description of this book.",
        "hook": "Discover this book and see whether it is right for you.",
        "tags": ["independent publishing"],
        "url": "https://www.amazon.com/dp/B0HLFX1YKT",
    },
    {
        "slug": "the-thrum-of-the-bull-spirit",
        "title": "The Thrum of the Bull Spirit",
        "description": "Uncover the raw mechanics behind modern obscurity and independent creation.",
        "hook": "Uncover the raw mechanics behind modern obscurity and independent creation.",
        "tags": ["indie publishing", "creative philosophy"],
        "url": "https://www.amazon.com/dp/B0HL989S11",
    },
]


def validate_books(books):
    """Reject incomplete entries and links outside Amazon's public domain."""
    slugs = set()
    for book in books:
        for field in ("slug", "title", "description", "hook", "url"):
            if not book.get(field, "").strip():
                raise ValueError(f"Book entry is missing {field!r}.")
        if book["slug"] in slugs:
            raise ValueError(f"Duplicate book slug: {book['slug']}")
        slugs.add(book["slug"])

        parsed_url = urlparse(book["url"])
        if parsed_url.scheme != "https" or parsed_url.hostname not in {
            "amazon.com",
            "www.amazon.com",
        }:
            raise ValueError(f"Book URL must be an HTTPS Amazon.com link: {book['url']}")


def render_campaign_pack(books):
    sections = [
        "# Book promotion drafts",
        "",
        "These are drafts for manual sharing, not automated posts. Adapt each one to the audience and follow the community's promotion rules. Send the email draft only to people who opted in.",
    ]
    for book in books:
        tags = ", ".join(f"`{tag}`" for tag in book.get("tags", [])) or "None configured"
        sections.extend(
            [
                "",
                f"## {book['title']}",
                "",
                f"**Book link:** {book['url']}",
                f"**Topics:** {tags}",
                "",
                "### Short social post",
                "",
                f"{book['hook']} Read more: {book['url']}",
                "",
                "### Community post (use only where promotion is allowed)",
                "",
                f"I wrote {book['title']}. {book['description']} If book recommendations are welcome here, details are available at {book['url']}",
                "",
                "### Opt-in email draft",
                "",
                f"**Subject:** A book for readers interested in {', '.join(book.get('tags', [])) or 'independent books'}",
                "",
                f"{book['hook']}\n\nMore details: {book['url']}",
            ]
        )
    return "\n".join(sections) + "\n"


def render_site(books):
    book_sections = []
    catalog = []
    for book in books:
        tags = " ".join(
            f'<span class="topic">{escape(tag)}</span>'
            for tag in book.get("tags", [])
        )
        catalog.append({
            "slug": book["slug"],
            "title": book["title"],
            "url": book["url"],
        })
        book_sections.append(
            f"""<article class="book" id="{escape(book['slug'], quote=True)}">
  <div class="book-mark" aria-hidden="true">BOOK</div>
  <div class="book-copy">
    <p class="eyebrow">{tags}</p>
    <h2>{escape(book['title'])}</h2>
    <p>{escape(book['description'])}</p>
    <a class="buy-link" data-book-slug="{escape(book['slug'], quote=True)}" data-book-title="{escape(book['title'], quote=True)}" data-book-url="{escape(book['url'], quote=True)}" href="{escape(book['url'], quote=True)}" target="_blank" rel="noopener noreferrer">View on Amazon <span aria-hidden="true">&#8599;</span></a>
  </div>
</article>"""
        )

    catalog_json = escape(json.dumps(catalog), quote=True)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Books by Chrissi Smith. Explore the books and visit their Amazon listings.">
  <title>Books by Chrissi Smith</title>
  <style>
    :root {{ color-scheme: light; --ink: #172b2b; --muted: #506360; --paper: #f5f7f2; --line: #cbd5ca; --green: #165c4a; --lime: #d6e67d; --coral: #b94935; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--paper); color: var(--ink); font: 17px/1.6 Georgia, "Times New Roman", serif; }}
    header {{ padding: 3.5rem max(1.25rem, calc((100vw - 980px) / 2)) 2.5rem; background: var(--green); color: #fff; border-bottom: 8px solid var(--lime); }}
    header p {{ max-width: 38rem; margin: 0; color: #e0eee4; font: 1rem/1.6 system-ui, sans-serif; }}
    h1 {{ max-width: 12ch; margin: 0 0 1rem; font-size: 4.5rem; line-height: 1.02; font-weight: 500; }}
    main {{ max-width: 980px; margin: 0 auto; padding: 1rem 1.25rem 3rem; }}
    .book {{ display: grid; grid-template-columns: minmax(100px, 170px) 1fr; gap: clamp(1.25rem, 5vw, 3.5rem); align-items: center; padding: 2.5rem 0; border-bottom: 1px solid var(--line); }}
    .book-mark {{ min-height: 220px; display: grid; place-items: center; padding: 1rem; background: var(--lime); color: var(--green); border: 1px solid var(--green); box-shadow: 8px 8px 0 var(--coral); font: 700 .85rem/1 system-ui, sans-serif; }}
    .book-copy {{ max-width: 650px; }}
    h2 {{ margin: .15rem 0 .5rem; font-size: 2.5rem; line-height: 1.1; font-weight: 500; }}
    .book-copy > p:not(.eyebrow) {{ color: var(--muted); }}
    .eyebrow {{ display: flex; flex-wrap: wrap; gap: .4rem; margin: 0 0 .8rem; font: .78rem/1.4 system-ui, sans-serif; }}
    .topic {{ padding: .15rem .45rem; border: 1px solid var(--line); border-radius: 3px; }}
    .buy-link {{ display: inline-block; margin-top: .55rem; padding: .65rem .9rem; background: var(--coral); color: #fff; text-decoration: none; font: 600 .95rem system-ui, sans-serif; }}
    .buy-link:hover, .buy-link:focus-visible {{ background: var(--green); outline: 3px solid var(--lime); outline-offset: 2px; }}
    .personalized {{ margin: 0 auto 2rem; max-width: 980px; padding: 1.5rem 1.25rem 0; }}
    .personalized h2 {{ font-size: 1.2rem; margin: 0 0 .5rem; text-transform: uppercase; letter-spacing: .08em; }}
    .personalized p {{ margin: 0 0 1rem; color: var(--muted); }}
    .personalized-picks {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }}
    .pick {{ display: block; padding: 1rem; border: 1px solid var(--line); background: #fff; text-decoration: none; color: var(--ink); }}
    .pick strong {{ display: block; margin-bottom: .35rem; }}
    .pick small {{ color: var(--muted); }}
    footer {{ padding: 1.5rem 1.25rem; color: var(--muted); border-top: 1px solid var(--line); text-align: center; font: .85rem system-ui, sans-serif; }}
    @media (max-width: 700px) {{ h1 {{ font-size: 3.25rem; }} h2 {{ font-size: 1.8rem; }} }}
    @media (max-width: 520px) {{ header {{ padding-top: 2.5rem; }} .book {{ grid-template-columns: 86px 1fr; gap: 1.1rem; align-items: start; }} .book-mark {{ min-height: 130px; padding: .5rem; box-shadow: 5px 5px 0 var(--coral); font-size: .7rem; }} }}
  </style>
</head>
<body data-track-endpoint="" data-book-catalog='{catalog_json}'>
  <header>
    <h1>Books by Chrissi Smith</h1>
    <p>Explore the books, find one that speaks to you, and visit its listing for details.</p>
  </header>
  <main>
    <section class="personalized" aria-live="polite">
      <h2>Personalized picks</h2>
      <p>Browsing history stays on this device when a remote tracking endpoint is unavailable, and it can sync to a network endpoint when one is configured.</p>
      <div class="personalized-picks" id="personalized-picks"></div>
    </section>
    {''.join(book_sections)}
  </main>
  <footer>Thank you for supporting independent publishing.</footer>
  <script>
    (() => {{
      const STORAGE_KEY = 'ad-generator-personalization';
      const catalog = JSON.parse(document.body.dataset.bookCatalog || '[]');
      const endpoint = document.body.dataset.trackEndpoint || '';

      const readState = () => {{
        try {{
          const raw = window.localStorage.getItem(STORAGE_KEY);
          return raw ? JSON.parse(raw) : {{ events: [], lastSeen: null }};
        }} catch (error) {{
          return {{ events: [], lastSeen: null }};
        }}
      }};

      const saveState = (state) => {{
        try {{
          window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        }} catch (error) {{
          // Ignore storage failures.
        }}
      }};

      const syncToNetwork = (payload) => {{
        if (!endpoint) {{
          return;
        }}

        const data = JSON.stringify(payload);
        try {{
          if (navigator.sendBeacon) {{
            navigator.sendBeacon(endpoint, new Blob([data], {{ type: 'application/json' }}));
            return;
          }}
          if (window.fetch) {{
            fetch(endpoint, {{
              method: 'POST',
              headers: {{ 'Content-Type': 'application/json' }},
              body: data,
              keepalive: true
            }}).catch(() => {{}});
          }}
        }} catch (error) {{
          // Keep the local state as the reliable fallback.
        }}
      }};

      const renderPicks = (state) => {{
        const container = document.getElementById('personalized-picks');
        if (!container) {{
          return;
        }}

        const events = Array.isArray(state.events) ? state.events : [];
        const ranked = [];
        const seen = new Map();

        for (const event of [...events].reverse()) {{
          if (!event || !event.slug) {{
            continue;
          }}
          if (!seen.has(event.slug)) {{
            seen.set(event.slug, event);
            ranked.push(event);
          }}
        }}

        let picks = ranked.length ? ranked : catalog.map((book) => ({{ slug: book.slug, title: book.title, url: book.url }}));
        picks = picks.slice(0, 3).map((book) => {{
          const href = book.url || (catalog.find((item) => item.slug === book.slug) || {{}}).url || '#';
          return '<a class="pick" href="' + href + '" target="_blank" rel="noopener noreferrer"><strong>' + (book.title || 'Recommended title') + '</strong><small>Based on local personalization</small></a>';
        }}).join('');

        container.innerHTML = picks || '<p>No picks yet. Visit a book and we will personalize the next list.</p>';
      }};

      const recordEvent = (type, slug, title, url) => {{
        const state = readState();
        const event = {{ type, slug, title, url, timestamp: Date.now() }};
        const timeWindowMs = 1000 * 60 * 60 * 24 * 30;
        const nextEvents = Array.isArray(state.events) ? state.events : [];

        state.events = nextEvents.concat([event]).filter((item) => item && item.timestamp && Date.now() - item.timestamp <= timeWindowMs);
        state.lastSeen = event.timestamp;
        saveState(state);
        syncToNetwork({{ host: window.location.host, path: window.location.pathname, event }});
        renderPicks(state);
      }};

      const init = () => {{
        const state = readState();
        renderPicks(state);

        document.querySelectorAll('[data-book-slug]').forEach((link) => {{
          const currentSlug = link.dataset.bookSlug;
          const title = link.dataset.bookTitle || 'Book recommendation';
          const url = link.dataset.bookUrl || '#';
          recordEvent('impression', currentSlug, title, url);

          link.addEventListener('click', () => {{
            recordEvent('click', currentSlug, title, url);
          }});
        }});
      }};

      if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', init);
      }} else {{
        init();
      }}
    }})();
  </script>
</body>
</html>
"""


def main():
    validate_books(BOOKS)
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "campaign_pack.md").write_text(render_campaign_pack(BOOKS), encoding="utf-8")
    (SITE_DIR / "index.html").write_text(render_site(BOOKS), encoding="utf-8")
    print("Generated campaign_pack.md and docs/index.html")
    if "Edit this title" in BOOKS[0]["title"]:
        print("Before publishing, replace the first book's placeholder title and description in this script.")


if __name__ == "__main__":
    main()