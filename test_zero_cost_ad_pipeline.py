import unittest
import json
import xml.etree.ElementTree as ET

import zero_cost_ad_pipeline as pipeline


class SiteRenderTests(unittest.TestCase):
    def test_site_uses_accurate_book_details_and_search_metadata(self):
        html = pipeline.render_site(pipeline.BOOKS)

        self.assertIn("Monogenic Obesity, Metabolic Malnourishment, and Cellular Death", html)
        self.assertIn("The Great Uric Acid Debacle", html)
        self.assertIn("IngramSpark", html)
        self.assertEqual(len(pipeline.BOOKS), 10)
        self.assertNotIn("Edit this title", html)
        self.assertIn('property="og:title"', html)
        self.assertIn('property="og:image"', html)
        self.assertIn("summary_large_image", html)
        self.assertIn(pipeline.AMAZON_AUTHOR_URL, html)
        self.assertIn('rel="canonical"', html)
        self.assertIn('type="application/ld+json"', html)

    def test_library_search_and_sharing_are_user_initiated(self):
        html = pipeline.render_site(pipeline.BOOKS)

        self.assertIn('id="book-search"', html)
        self.assertIn('id="topic-filter"', html)
        self.assertIn('id="share-library"', html)
        self.assertIn("navigator.share", html)
        self.assertNotIn("localStorage", html)
        self.assertNotIn("sendBeacon", html)
        self.assertNotIn("/api/personalization", html)
        self.assertIn("data-search=", html)
        self.assertIn("loading=\"lazy\"", html)

    def test_sitemap_contains_public_page_url(self):
        sitemap = ET.fromstring(
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f"<url><loc>{pipeline.SITE_URL}</loc></url></urlset>"
        )

        self.assertEqual(
            sitemap.findtext("{http://www.sitemaps.org/schemas/sitemap/0.9}url/"
                             "{http://www.sitemaps.org/schemas/sitemap/0.9}loc"),
            pipeline.SITE_URL,
        )

    def test_indexnow_notifies_only_owned_site_urls(self):
        payload = json.loads(pipeline.render_indexnow_payload())
        expected_host = "chrissysmith260-droid.github.io"

        self.assertEqual(payload["host"], expected_host)
        self.assertEqual(
            payload["keyLocation"],
            f"{pipeline.SITE_URL}{pipeline.INDEXNOW_KEY}.txt",
        )
        self.assertTrue(payload["urlList"])
        self.assertTrue(
            all(url.startswith(pipeline.SITE_URL) for url in payload["urlList"])
        )

    def test_rss_feed_lists_books_with_stable_ids(self):
        feed = ET.fromstring(pipeline.render_rss(pipeline.BOOKS))
        items = feed.findall("./channel/item")

        self.assertEqual(len(items), 10)
        self.assertEqual(items[2].findtext("guid"), "the-great-uric-acid-debacle")
        self.assertIn("The Great Uric Acid Debacle", items[2].findtext("title"))
        self.assertIn("feed.xml", pipeline.render_site(pipeline.BOOKS))

    def test_book_links_allow_multiple_https_retailers(self):
        book = dict(pipeline.BOOKS[0])
        book["additional_links"] = [
            {"label": "IngramSpark", "url": "https://example.com/book"}
        ]

        pipeline.validate_books([book])
        html = pipeline.render_site([book])

        self.assertIn("View on IngramSpark", html)
        self.assertIn('href="https://example.com/book"', html)

    def test_rejects_non_https_retailer_links(self):
        book = dict(pipeline.BOOKS[0])
        book["additional_links"] = [
            {"label": "IngramSpark", "url": "http://example.com/book"}
        ]

        with self.assertRaises(ValueError):
            pipeline.validate_books([book])

    def test_context_widget_matches_topics_and_links_to_retailer(self):
        widget = pipeline.render_widget(pipeline.BOOKS)

        self.assertIn("data-book-discovery", widget)
        self.assertIn("document.querySelector('article')?.innerText", widget)
        self.assertNotIn("document.body.innerText", widget)
        self.assertIn("https://www.amazon.com/dp/B0HG8531WW", widget)
        self.assertIn("Sponsored book", widget)
        self.assertIn("new release with no reviews yet", widget)
        self.assertIn('"reviewCount": 0', widget)
        self.assertIn("Number(right.newUnreviewed)", widget)
        self.assertNotIn("localStorage", widget)
        self.assertNotIn("sendBeacon", widget)
        self.assertNotIn("fetch(", widget)


if __name__ == "__main__":
    unittest.main()
