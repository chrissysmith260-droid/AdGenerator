"""Build shareable campaign drafts and a static book page without network calls."""

import json
from html import escape
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
SITE_DIR = ROOT / "docs"
SITE_URL = "https://chrissysmith260-droid.github.io/AdGenerator/"
AMAZON_AUTHOR_URL = "https://www.amazon.com/Chrissi-D-Smith/e/B0DHYQ67JM"
INDEXNOW_KEY = "a27e5c82fa314d67be98ac125daf4031"

BOOKS = [
    {
        "slug": "book-b0hlfx1ykt",
    "title": (
          "Monogenic Obesity, Metabolic Malnourishment, and Cellular Death:: "
          "A Comprehensive Review of cellular stress and destress in all "
          "forms leading to disease and disorder in all areas"
    ),
    "description": (
      "Rev. Chrissi D. Smith's review presents the author's perspective "
      "on obesity and metabolic illness through cellular biology, "
      "genetics, immune function, and chronic stress. It challenges "
      "calorie-centered models and discusses the author's proposed "
      "explanations and approaches. This is the author's perspective, "
      "not individual medical guidance."
    ),
    "hook": (
      "Explore a review challenging calorie-centered models of obesity "
      "and examining genetic, cellular, immune, and stress-related factors."
    ),
    "tags": ["metabolic health", "cellular biology", "nonfiction"],
    "match_terms": ["obesity", "metabolic illness", "genetics", "chronic stress"],
    "published_on": "2026-09-29",
    "cover": "https://m.media-amazon.com/images/I/51s0ty+r+kL._SY342_.jpg",
        "url": "https://www.amazon.com/dp/B0HLFX1YKT",
    },
    {
        "slug": "the-thrum-of-the-bull-spirit",
        "title": "The Thrum of the Bull Spirit",
    "description": (
      "After surviving a massacre, Obigdewa travels from the Mississippi "
      "River toward British Columbia. There, a bond with B'gihw and the "
      "family they build together offers hope as they face grief and a "
      "violent past. A short story of survival, love, and resilience."
    ),
    "hook": (
      "Read a story of survival, love, and a chosen family in the "
      "wilderness of British Columbia."
    ),
    "tags": ["fiction", "survival", "chosen family"],
    "published_on": "2026-09-28",
    "cover": "https://m.media-amazon.com/images/I/51wzdvpIyrL._SY342_.jpg",
        "url": "https://www.amazon.com/dp/B0HL989S11",
    },
  {
    "slug": "the-great-uric-acid-debacle",
    "title": "The Great Uric Acid Debacle",
    "description": (
      "Rev. Chrissi D. Smith draws on lived experience to question "
      "common explanations of uric acid and gout, and to discuss "
      "connections the author sees among chronic inflammation, metabolic "
      "dysfunction, trauma, and healthcare. This is the author's account "
      "and perspective, not individual medical guidance."
    ),
    "hook": (
      "A personal account examining uric acid, chronic illness, and "
      "the experience of navigating healthcare."
    ),
    "tags": ["personal narrative", "health", "nonfiction"],
    "match_terms": ["uric acid", "gout", "chronic inflammation", "metabolic dysfunction"],
    "published_on": "2026-08-23",
    "isbn": "9798240841606",
    "publication_note": "Print edition published through IngramSpark.",
    "cover": "https://m.media-amazon.com/images/I/71V-yXM2fxL._SY342_.jpg",
    "url": "https://www.amazon.com/dp/B0HG8531WW",
  },
  {
    "slug": "the-neurodivergent-soul",
    "title": "The Neurodivergent Soul: Embracing Faith with AuDHD",
    "description": (
      "Rev. Chrissi D. Smith writes for readers navigating AuDHD, "
      "connecting neurodivergence with faith and lived experience. "
      "The book presents the author's view that neurodivergent "
      "wiring can be understood as part of a person's identity."
    ),
    "hook": (
      "A faith-centered reflection on navigating life with AuDHD."
    ),
    "tags": ["faith", "neurodiversity", "personal reflection"],
    "published_on": "2026-03-09",
    "review_count": 0,
    "cover": "https://m.media-amazon.com/images/I/915sVSBE7fL._SY342_.jpg",
    "url": "https://www.amazon.com/dp/B0GHVCTWVP",
  },
  {
    "slug": "theodore",
    "title": "Theodore",
    "description": "See the full description on the Amazon listing.",
    "hook": "Discover Theodore by Chrissi Smith.",
    "tags": ["fiction"],
    "cover": "https://m.media-amazon.com/images/I/81TrAXTl+WL._SY342_.jpg",
    "url": "https://www.amazon.com/dp/B0FWPW1CLW",
  },
  {
    "slug": "forgiving-yourself",
    "title": "Forgiving Yourself: 10 Steps To Living in God's Truth",
    "description": (
      "A faith-based guide to self-forgiveness, with ten scripture-rooted "
      "steps focused on releasing guilt and shame, reflecting, praying, "
      "and finding spiritual renewal through God's grace."
    ),
    "hook": (
      "Explore ten scripture-rooted steps toward self-forgiveness and "
      "spiritual renewal."
    ),
    "tags": ["Christian living", "faith", "self-forgiveness"],
    "cover": "https://m.media-amazon.com/images/I/71T53aBYs0L._SY342_.jpg",
    "url": "https://www.amazon.com/dp/B0F1DT1M39",
  },
  {
    "slug": "love",
    "title": "Love",
    "description": (
      "A faith-centered reflection on love, drawing on biblical insight "
      "and personal reflections to explore loving God, giving and "
      "receiving love, and putting love into action through service."
    ),
    "hook": "A short reflection on faith, love, and putting care into action.",
    "tags": ["Christian living", "faith", "love"],
    "cover": "https://m.media-amazon.com/images/I/615te67azXL._SY342_.jpg",
    "url": "https://www.amazon.com/dp/B0DNY99FD6",
  },
  {
    "slug": "my-journey-to-good-health",
    "title": "My Journey To Good Health",
    "description": (
      "A personal account of the author's journey to good health, "
      "covering nutrition, healthcare, exercise, and mental health."
    ),
    "hook": "Read a personal account of a journey through health and wellness.",
    "tags": ["personal narrative", "health", "wellness"],
    "cover": "https://m.media-amazon.com/images/I/51TLVNDNKzL._SY342_.jpg",
    "url": "https://www.amazon.com/dp/B0DHR9GX8V",
  },
  {
    "slug": "on-gods-green-earth",
    "title": "On God's Green Earth",
    "description": (
      "A faith-centered reflection on God's creation, surrender, and "
      "finding peace, shaped by the author's memories of growing up on "
      "a family farm and watching her grandfathers care for the land."
    ),
    "hook": "A reflection on faith, family, and care for God's creation.",
    "tags": ["Christian living", "faith", "creation"],
    "cover": "https://m.media-amazon.com/images/I/71O4n9hHszL._SY342_.jpg",
    "url": "https://www.amazon.com/dp/B0DJV7G49T",
  },
  {
    "slug": "the-jesus-i-know",
    "title": "The Jesus I Know",
    "description": "See the full description on the Amazon listing.",
    "hook": "Discover The Jesus I Know by Chrissi D. Smith.",
    "tags": ["Christian living", "faith"],
    "cover": "https://m.media-amazon.com/images/I/61MgDdive0L._SY342_.jpg",
    "url": "https://www.amazon.com/dp/B0DHV4PPWT",
  },
]

SITE_DESCRIPTION = (
  "Explore fiction, faith, and personal writing by Chrissi D. Smith."
)


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
        if parsed_url.scheme != "https" or not parsed_url.hostname:
          raise ValueError(f"Book URL must use HTTPS: {book['url']}")
        for retailer in book.get("additional_links", []):
          retailer_url = urlparse(retailer.get("url", ""))
          if (
            not retailer.get("label", "").strip()
            or retailer_url.scheme != "https"
            or not retailer_url.hostname
          ):
            raise ValueError("Additional retailer links need a label and HTTPS URL.")


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


def render_rss(books):
    """Build an RSS 2.0 catalog feed with stable IDs for feed readers."""
    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "Books by Chrissi D. Smith"
    ET.SubElement(channel, "link").text = SITE_URL
    ET.SubElement(channel, "description").text = SITE_DESCRIPTION
    ET.SubElement(channel, "language").text = "en-us"

    for book in books:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = book["title"]
        ET.SubElement(item, "link").text = f"{SITE_URL}#{book['slug']}"
        ET.SubElement(item, "guid", {"isPermaLink": "false"}).text = book["slug"]
        ET.SubElement(item, "description").text = (
            f"{book['description']} Read more: {book['url']}"
        )
        for tag in book.get("tags", []):
            ET.SubElement(item, "category").text = tag

    xml = ET.tostring(rss, encoding="unicode")
    return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml}\n'


def render_indexnow_payload():
    """Return an IndexNow notification for URLs hosted by this project."""
    return json.dumps(
        {
            "host": urlparse(SITE_URL).hostname,
            "key": INDEXNOW_KEY,
            "keyLocation": f"{SITE_URL}{INDEXNOW_KEY}.txt",
            "urlList": [
                SITE_URL,
                f"{SITE_URL}feed.xml",
                f"{SITE_URL}sitemap.xml",
                f"{SITE_URL}book-discovery.js",
            ],
        }
    )


def render_widget(books):
    """Build a self-contained contextual widget that links directly to books."""
    catalog = [
        {
            "title": book["title"],
            "description": book["description"],
            "tags": book.get("tags", []),
            "matchTerms": book.get("match_terms", []),
            "publishedOn": book.get("published_on"),
            "reviewCount": book.get("review_count"),
            "url": book["url"],
        }
        for book in books
    ]
    catalog_json = json.dumps(catalog, ensure_ascii=True).replace("</", "<\\/")
    return f"""(() => {{
  const books = {catalog_json};
  const slots = document.querySelectorAll('[data-book-discovery]');
  if (!slots.length) return;

  const pageText = [
    document.title,
    document.querySelector('meta[name="description"]')?.content || '',
    document.querySelector('main')?.innerText || document.querySelector('article')?.innerText || ''
  ].join(' ').toLowerCase();

  const matches = books.map((book) => {{
    const terms = [...book.tags, ...book.matchTerms];
    const score = terms.filter((term) =>
      term.length > 2 && pageText.includes(term.toLowerCase())
    ).length;
    const ageMs = book.publishedOn ? Date.now() - Date.parse(book.publishedOn) : Infinity;
    const newUnreviewed = book.reviewCount === 0 && ageMs >= 0 && ageMs <= 365 * 24 * 60 * 60 * 1000;
    return {{ book, score, newUnreviewed }};
  }}).filter((result) => result.score > 0)
    .sort((left, right) => Number(right.newUnreviewed) - Number(left.newUnreviewed) || right.score - left.score);

  const match = matches[0];
  if (!match) return;

  for (const slot of slots) {{
    const ad = document.createElement('aside');
    ad.setAttribute('aria-label', 'Sponsored book');
    ad.style.cssText = 'border:1px solid #d8ddd4;border-left:4px solid #b94935;padding:16px;margin:16px 0;background:#fff;color:#172b2b;font:16px/1.5 Georgia,serif;max-width:540px';

    const label = document.createElement('p');
    label.textContent = match.newUnreviewed
      ? 'Sponsored book · new release with no reviews yet'
      : 'Sponsored book';
    label.style.cssText = 'margin:0 0 8px;color:#506360;font:600 12px/1.4 system-ui,sans-serif;text-transform:uppercase';

    const title = document.createElement('a');
    title.textContent = match.book.title;
    title.href = match.book.url;
    title.target = '_blank';
    title.rel = 'noopener noreferrer';
    title.style.cssText = 'color:#165c4a;font-size:20px;font-weight:bold';

    const description = document.createElement('p');
    description.textContent = match.book.description;
    description.style.cssText = 'margin:8px 0 0';

    ad.append(label, title, description);
    slot.replaceChildren(ad);
  }}
}})();
"""


def render_site(books):
    book_sections = []
    topics = sorted({tag for book in books for tag in book.get("tags", [])})
    topic_options = "".join(
      f'<option value="{escape(topic, quote=True)}">{escape(topic)}</option>'
      for topic in topics
    )
    for book in books:
        tags = " ".join(
            f'<span class="topic">{escape(tag)}</span>'
            for tag in book.get("tags", [])
        )
        publication_details = " ".join(
            escape(detail)
            for detail in (book.get("publication_note"), book.get("isbn"))
            if detail
        )
        publication_markup = (
            f'\n    <p class="publication-details">{publication_details}</p>'
            if publication_details
            else ""
        )
        searchable_text = " ".join(
            [book["title"], book["description"], *book.get("tags", [])]
        ).lower()
        cover_markup = (
            f'<img src="{escape(book["cover"], quote=True)}" '
            f'alt="Cover of {escape(book["title"], quote=True)}" '
            'loading="lazy" decoding="async">'
            if book.get("cover")
            else '<span class="book-mark" aria-hidden="true">BOOK</span>'
        )
        book_links = [
          (book.get("store_name", "Amazon"), book["url"]),
          *[
            (retailer["label"], retailer["url"])
            for retailer in book.get("additional_links", [])
          ],
        ]
        links_markup = "".join(
          f'<a class="buy-link" href="{escape(url, quote=True)}" '
          f'target="_blank" rel="noopener noreferrer">View on '
          f'{escape(label)} <span aria-hidden="true">&#8599;</span></a>'
          for label, url in book_links
        )
        book_sections.append(
            f"""<article class="book" id="{escape(book['slug'], quote=True)}" data-tags="{escape(','.join(book.get('tags', [])), quote=True)}" data-search="{escape(searchable_text, quote=True)}">
  <a class="book-cover" href="{escape(book['url'], quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="View {escape(book['title'], quote=True)} on Amazon">
    {cover_markup}
  </a>
  <div class="book-copy">
    <p class="eyebrow">{tags}</p>
    <h2>{escape(book['title'])}</h2>
    <p>{escape(book['description'])}</p>{publication_markup}
    <div class="book-actions">{links_markup}</div>
  </div>
</article>"""
        )

    cover_image = next((book.get("cover") for book in books if book.get("cover")), "")
    structured_data = {
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "Books by Chrissi D. Smith",
      "url": SITE_URL,
      "mainEntity": {
        "@type": "ItemList",
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": position,
            "item": {
              "@type": "Book",
              "name": book["title"],
              "description": book["description"],
              "url": book["url"],
              **({"isbn": book["isbn"]} if book.get("isbn") else {}),
              "author": {"@type": "Person", "name": "Chrissi D. Smith"},
            },
          }
          for position, book in enumerate(books, start=1)
        ],
      },
    }
    structured_data_json = json.dumps(structured_data).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(SITE_DESCRIPTION, quote=True)}">
  <link rel="canonical" href="{SITE_URL}">
  <link rel="alternate" type="application/rss+xml" title="Books by Chrissi D. Smith" href="{SITE_URL}feed.xml">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Books by Chrissi D. Smith">
  <meta property="og:description" content="{escape(SITE_DESCRIPTION, quote=True)}">
  <meta property="og:url" content="{SITE_URL}">
  <meta property="og:image" content="{escape(cover_image, quote=True)}">
  <meta name="twitter:card" content="summary_large_image">
  <title>Books by Chrissi D. Smith</title>
  <script type="application/ld+json">{structured_data_json}</script>
  <style>
    :root {{ color-scheme: light; --ink: #172b2b; --muted: #506360; --paper: #f5f7f2; --line: #cbd5ca; --green: #165c4a; --lime: #d6e67d; --coral: #b94935; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--paper); color: var(--ink); font: 17px/1.6 Georgia, "Times New Roman", serif; }}
    header {{ padding: 3rem max(1.25rem, calc((100vw - 1120px) / 2)); background: var(--green); color: #fff; border-bottom: 8px solid var(--lime); }}
    .header-inner {{ display: flex; align-items: end; justify-content: space-between; gap: 2rem; }}
    header p {{ max-width: 38rem; margin: 0; color: #e0eee4; font: 1rem/1.6 system-ui, sans-serif; }}
    h1 {{ max-width: 15ch; margin: 0 0 1rem; font-size: 4rem; line-height: 1.02; font-weight: 500; }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 1.5rem 1.25rem 3rem; }}
    .library-tools {{ display: grid; grid-template-columns: minmax(240px, 1fr) minmax(180px, 240px) auto; align-items: end; gap: 1rem; margin-bottom: 1.5rem; padding: 1rem 0; border-bottom: 1px solid var(--line); }}
    .library-tools label {{ display: grid; gap: .35rem; color: var(--muted); font: 600 .8rem/1.4 system-ui, sans-serif; }}
    .library-tools input, .library-tools select {{ width: 100%; min-height: 44px; padding: .55rem .7rem; border: 1px solid var(--line); border-radius: 3px; background: #fff; color: var(--ink); font: 1rem system-ui, sans-serif; }}
    .library-count {{ margin: 0; color: var(--muted); font: .9rem system-ui, sans-serif; white-space: nowrap; }}
    .book-list {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 1rem; }}
    .book {{ min-width: 0; overflow: hidden; background: #fff; border: 1px solid var(--line); border-radius: 4px; }}
    .book[hidden] {{ display: none; }}
    .book-cover {{ display: grid; place-items: center; aspect-ratio: 3 / 2; overflow: hidden; background: #e7ecdf; border-bottom: 1px solid var(--line); }}
    .book-cover img {{ display: block; width: 100%; height: 100%; object-fit: contain; }}
    .book-mark {{ display: grid; place-items: center; width: 100%; height: 100%; color: var(--green); font: 700 .85rem/1 system-ui, sans-serif; }}
    .book-copy {{ display: flex; flex-direction: column; align-items: start; padding: 1rem; }}
    h2 {{ margin: .15rem 0 .5rem; font-size: 1.45rem; line-height: 1.2; font-weight: 500; }}
    .book-copy > p:not(.eyebrow) {{ color: var(--muted); }}
    .eyebrow {{ display: flex; flex-wrap: wrap; gap: .4rem; margin: 0 0 .8rem; font: .78rem/1.4 system-ui, sans-serif; }}
    .topic {{ padding: .15rem .45rem; border: 1px solid var(--line); border-radius: 3px; }}
    .publication-details {{ font: .78rem/1.5 system-ui, sans-serif; }}
    .book-actions {{ display: flex; flex-wrap: wrap; gap: .5rem; margin-top: auto; padding-top: .75rem; }}
    .buy-link {{ display: inline-block; padding: .65rem .9rem; background: var(--coral); color: #fff; text-decoration: none; font: 600 .95rem system-ui, sans-serif; }}
    .buy-link:hover, .buy-link:focus-visible {{ background: var(--green); outline: 3px solid var(--lime); outline-offset: 2px; }}
    .share-button {{ flex: 0 0 auto; padding: .7rem .9rem; border: 1px solid var(--lime); border-radius: 3px; background: var(--lime); color: var(--ink); font: 600 .95rem system-ui, sans-serif; cursor: pointer; }}
    .share-button:hover, .share-button:focus-visible {{ outline: 3px solid #fff; outline-offset: 2px; }}
    .author-link {{ display: inline-block; margin-top: 1rem; color: #fff; font: 600 .95rem system-ui, sans-serif; }}
    .header-actions {{ display: flex; align-items: center; gap: 1rem; }}
    .share-status {{ min-height: 1.5em; margin: .4rem 0 0; color: #e0eee4; font: .85rem system-ui, sans-serif; }}
    .empty-state {{ padding: 2rem 0; color: var(--muted); }}
    .personalized {{ margin: 0 auto 2rem; max-width: 980px; padding: 1.5rem 1.25rem 0; }}
    .personalized h2 {{ font-size: 1.2rem; margin: 0 0 .5rem; text-transform: uppercase; letter-spacing: .08em; }}
    .personalized p {{ margin: 0 0 1rem; color: var(--muted); }}
    .personalized-picks {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }}
    .pick {{ display: block; padding: 1rem; border: 1px solid var(--line); background: #fff; text-decoration: none; color: var(--ink); }}
    .pick strong {{ display: block; margin-bottom: .35rem; }}
    .pick small {{ color: var(--muted); }}
    footer {{ padding: 1.5rem 1.25rem; color: var(--muted); border-top: 1px solid var(--line); text-align: center; font: .85rem system-ui, sans-serif; }}
    @media (max-width: 700px) {{ .header-inner {{ align-items: start; flex-direction: column; gap: 1rem; }} .header-actions {{ align-items: start; flex-wrap: wrap; }} h1 {{ font-size: 3rem; }} .library-tools {{ grid-template-columns: 1fr; }} .book-list {{ grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); }} }}
    @media (max-width: 520px) {{ header {{ padding-top: 2.25rem; }} .book-list {{ grid-template-columns: 1fr; }} .book {{ display: grid; grid-template-columns: 112px minmax(0, 1fr); }} .book-cover {{ grid-row: 1 / span 2; height: 100%; min-height: 170px; aspect-ratio: auto; border-right: 1px solid var(--line); border-bottom: 0; }} .book-copy {{ padding: .8rem; }} h2 {{ font-size: 1.25rem; }} }}
  </style>
</head>
<body>
  <header>
    <div class="header-inner">
      <div>
        <h1>Books by Chrissi D. Smith</h1>
        <p>Fiction, faith, health, and personal reflections. Browse the library and follow a title to its listing.</p>
        <p class="share-status" id="share-status" role="status" aria-live="polite"></p>
      </div>
      <div class="header-actions">
        <a class="author-link" href="{AMAZON_AUTHOR_URL}" target="_blank" rel="noopener noreferrer">Follow on Amazon <span aria-hidden="true">&#8599;</span></a>
        <a class="author-link" href="{SITE_URL}feed.xml">Subscribe to updates (RSS)</a>
        <button class="share-button" id="share-library" type="button">Share this library</button>
      </div>
    </div>
  </header>
  <main>
    <section aria-label="Book library">
      <div class="library-tools">
        <label for="book-search">Search books
          <input id="book-search" type="search" placeholder="Title, topic, or keyword">
        </label>
        <label for="topic-filter">Topic
          <select id="topic-filter">
            <option value="">All topics</option>
            {topic_options}
          </select>
        </label>
        <p class="library-count" id="library-count" aria-live="polite">{len(books)} books</p>
      </div>
      <div class="book-list" id="book-list">
        {''.join(book_sections)}
      </div>
      <p class="empty-state" id="empty-state" hidden>No books match those filters.</p>
    </section>
  </main>
  <footer>Thank you for reading and sharing independent books.</footer>
  <script>
    (() => {{
      const search = document.getElementById('book-search');
      const topicFilter = document.getElementById('topic-filter');
      const count = document.getElementById('library-count');
      const emptyState = document.getElementById('empty-state');
      const books = [...document.querySelectorAll('.book')];

      const filterBooks = () => {{
        const query = search.value.trim().toLowerCase();
        const topic = topicFilter.value.toLowerCase();
        let visibleCount = 0;

        for (const book of books) {{
          const matchesQuery = book.dataset.search.includes(query);
          const matchesTopic = !topic || book.dataset.tags.toLowerCase().split(',').includes(topic);
          book.hidden = !(matchesQuery && matchesTopic);
          if (!book.hidden) visibleCount += 1;
        }}

        count.textContent = `${{visibleCount}} ${{visibleCount === 1 ? 'book' : 'books'}}`;
        emptyState.hidden = visibleCount > 0;
      }};

      search.addEventListener('input', filterBooks);
      topicFilter.addEventListener('change', filterBooks);

      document.getElementById('share-library').addEventListener('click', async () => {{
        const shareData = {{
          title: document.title,
          text: 'Explore books by Chrissi D. Smith',
          url: window.location.href
        }};
        const status = document.getElementById('share-status');

        try {{
          if (navigator.share) {{
            await navigator.share(shareData);
            status.textContent = 'Thanks for sharing.';
          }} else if (navigator.clipboard) {{
            await navigator.clipboard.writeText(shareData.url);
            status.textContent = 'Library link copied.';
          }} else {{
            status.textContent = shareData.url;
          }}
        }} catch (error) {{
          if (error.name !== 'AbortError') status.textContent = 'Unable to share from this browser.';
        }}
      }});
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
    (SITE_DIR / "feed.xml").write_text(render_rss(BOOKS), encoding="utf-8")
    (SITE_DIR / "book-discovery.js").write_text(render_widget(BOOKS), encoding="utf-8")
    (SITE_DIR / f"{INDEXNOW_KEY}.txt").write_text(f"{INDEXNOW_KEY}\n", encoding="utf-8")
    (SITE_DIR / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n",
        encoding="utf-8",
    )
    sitemap = ET.Element(
        "urlset",
        {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"},
    )
    url = ET.SubElement(sitemap, "url")
    ET.SubElement(url, "loc").text = SITE_URL
    sitemap_xml = ET.tostring(sitemap, encoding="unicode")
    (SITE_DIR / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n{sitemap_xml}\n',
        encoding="utf-8",
    )
    print("Generated campaign drafts, author library, RSS feed, contextual widget, and search files")


if __name__ == "__main__":
    main()