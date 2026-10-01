# AdGenerator

## Free promotion pipeline

This script does not send ads or make network requests. It creates copy you can
review and share manually, plus a static book page that can be hosted for free
with GitHub Pages.

Run it with Python 3:

```sh
python3 zero_cost_ad_pipeline.py
```

It generates:

- `campaign_pack.md`: short social posts, community-post drafts, and an opt-in
	email draft for each book. Share only where promotion is allowed, and send
	emails only to people who opted in.
- `docs/index.html`: a mobile-friendly public page linking to the book listings.

### Before publishing

Edit the `BOOKS` entries in `zero_cost_ad_pipeline.py`. The title and description
for `B0HLFX1YKT` are placeholders because they were not included in the original
script. Check that every title and description accurately describes its book,
then rerun the generator.

To publish the page with GitHub Pages, push the repository to GitHub, open the
repository's **Settings > Pages**, choose **Deploy from a branch**, select the
`main` branch and `/docs` folder, and save. GitHub will provide the public page
URL when deployment completes. Publishing the page makes it accessible; it does
not automatically place ads in other people's browsing or send promotional
messages.