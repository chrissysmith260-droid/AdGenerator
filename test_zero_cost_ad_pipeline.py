import unittest

import zero_cost_ad_pipeline as pipeline


class SiteRenderTests(unittest.TestCase):
    def test_site_tracks_personalization_locally_and_over_network(self):
        html = pipeline.render_site(pipeline.BOOKS)

        self.assertIn("localStorage", html)
        self.assertIn("navigator.sendBeacon", html)
        self.assertIn("data-book-slug", html)
        self.assertIn("Personalized picks", html)


if __name__ == "__main__":
    unittest.main()
