(() => {
  const books = [{"title": "Monogenic Obesity, Metabolic Malnourishment, and Cellular Death:: A Comprehensive Review of cellular stress and destress in all forms leading to disease and disorder in all areas", "description": "Rev. Chrissi D. Smith's review presents the author's perspective on obesity and metabolic illness through cellular biology, genetics, immune function, and chronic stress. It challenges calorie-centered models and discusses the author's proposed explanations and approaches. This is the author's perspective, not individual medical guidance.", "tags": ["metabolic health", "cellular biology", "nonfiction"], "matchTerms": ["obesity", "metabolic illness", "genetics", "chronic stress"], "publishedOn": "2026-09-29", "reviewCount": null, "url": "https://www.amazon.com/dp/B0HLFX1YKT"}, {"title": "The Thrum of the Bull Spirit", "description": "After surviving a massacre, Obigdewa travels from the Mississippi River toward British Columbia. There, a bond with B'gihw and the family they build together offers hope as they face grief and a violent past. A short story of survival, love, and resilience.", "tags": ["fiction", "survival", "chosen family"], "matchTerms": [], "publishedOn": "2026-09-28", "reviewCount": null, "url": "https://www.amazon.com/dp/B0HL989S11"}, {"title": "The Great Uric Acid Debacle", "description": "Rev. Chrissi D. Smith draws on lived experience to question common explanations of uric acid and gout, and to discuss connections the author sees among chronic inflammation, metabolic dysfunction, trauma, and healthcare. This is the author's account and perspective, not individual medical guidance.", "tags": ["personal narrative", "health", "nonfiction"], "matchTerms": ["uric acid", "gout", "chronic inflammation", "metabolic dysfunction"], "publishedOn": "2026-08-23", "reviewCount": null, "url": "https://www.amazon.com/dp/B0HG8531WW"}, {"title": "The Neurodivergent Soul: Embracing Faith with AuDHD", "description": "Rev. Chrissi D. Smith writes for readers navigating AuDHD, connecting neurodivergence with faith and lived experience. The book presents the author's view that neurodivergent wiring can be understood as part of a person's identity.", "tags": ["faith", "neurodiversity", "personal reflection"], "matchTerms": [], "publishedOn": "2026-03-09", "reviewCount": 0, "url": "https://www.amazon.com/dp/B0GHVCTWVP"}, {"title": "Theodore", "description": "See the full description on the Amazon listing.", "tags": ["fiction"], "matchTerms": [], "publishedOn": null, "reviewCount": null, "url": "https://www.amazon.com/dp/B0FWPW1CLW"}, {"title": "Forgiving Yourself: 10 Steps To Living in God's Truth", "description": "A faith-based guide to self-forgiveness, with ten scripture-rooted steps focused on releasing guilt and shame, reflecting, praying, and finding spiritual renewal through God's grace.", "tags": ["Christian living", "faith", "self-forgiveness"], "matchTerms": [], "publishedOn": null, "reviewCount": null, "url": "https://www.amazon.com/dp/B0F1DT1M39"}, {"title": "Love", "description": "A faith-centered reflection on love, drawing on biblical insight and personal reflections to explore loving God, giving and receiving love, and putting love into action through service.", "tags": ["Christian living", "faith", "love"], "matchTerms": [], "publishedOn": null, "reviewCount": null, "url": "https://www.amazon.com/dp/B0DNY99FD6"}, {"title": "My Journey To Good Health", "description": "A personal account of the author's journey to good health, covering nutrition, healthcare, exercise, and mental health.", "tags": ["personal narrative", "health", "wellness"], "matchTerms": [], "publishedOn": null, "reviewCount": null, "url": "https://www.amazon.com/dp/B0DHR9GX8V"}, {"title": "On God's Green Earth", "description": "A faith-centered reflection on God's creation, surrender, and finding peace, shaped by the author's memories of growing up on a family farm and watching her grandfathers care for the land.", "tags": ["Christian living", "faith", "creation"], "matchTerms": [], "publishedOn": null, "reviewCount": null, "url": "https://www.amazon.com/dp/B0DJV7G49T"}, {"title": "The Jesus I Know", "description": "See the full description on the Amazon listing.", "tags": ["Christian living", "faith"], "matchTerms": [], "publishedOn": null, "reviewCount": null, "url": "https://www.amazon.com/dp/B0DHV4PPWT"}];
  const slots = document.querySelectorAll('[data-book-discovery]');
  if (!slots.length) return;

  const pageText = [
    document.title,
    document.querySelector('meta[name="description"]')?.content || '',
    document.querySelector('main')?.innerText || document.querySelector('article')?.innerText || ''
  ].join(' ').toLowerCase();

  const matches = books.map((book) => {
    const terms = [...book.tags, ...book.matchTerms];
    const score = terms.filter((term) =>
      term.length > 2 && pageText.includes(term.toLowerCase())
    ).length;
    const ageMs = book.publishedOn ? Date.now() - Date.parse(book.publishedOn) : Infinity;
    const newUnreviewed = book.reviewCount === 0 && ageMs >= 0 && ageMs <= 365 * 24 * 60 * 60 * 1000;
    return { book, score, newUnreviewed };
  }).filter((result) => result.score > 0)
    .sort((left, right) => Number(right.newUnreviewed) - Number(left.newUnreviewed) || right.score - left.score);

  const match = matches[0];
  if (!match) return;

  for (const slot of slots) {
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
  }
})();
