import json


class ZeroCostAdPipeline:
    def __init__(self, target_urls, asset_payload):
        self.target_urls = target_urls
        self.asset_payload = asset_payload
        self.gateway_endpoints = [
            "https://api.open-syndication-network.org/v1/inject",
            "https://local-rss-bridge-node/publish",
        ]

    def format_programmatic_payload(self, target_url):
        """Format campaign data for a single destination."""
        packet = {
            "title": self.asset_payload.get("title"),
            "hook": self.asset_payload.get("hook"),
            "destination_link": target_url,
            "metadata_tags": self.asset_payload.get("tags", []),
        }
        return json.dumps(packet)

    def execute_routing(self):
        """Print simulated deliveries without making network requests."""
        for endpoint in self.gateway_endpoints:
            for target_url in self.target_urls:
                payload = self.format_programmatic_payload(target_url)
                print(f"[SIMULATION] Would route to {endpoint}: {payload}")


if __name__ == "__main__":
    book_destinations = [
        "https://www.amazon.com/dp/B0HLFX1YKT/ref=sr_1_1?crid=2S2A0GK9BCS4P&dib=eyJ2IjoiMSJ9.tIVzjpHdOh1bCCeFSPwRPg.KUYumjLuJO5Im0qqW-IMJudPMGAiEEWWt63X3wmFB7g&dib_tag=se&keywords=monogenic+obesity+metabolic+malnourishment&qid=1790702984&s=books&sprefix=monogenic+obesity+metabolic+malnourishment+%2Cstripbooks%2C161&sr=1-1",
        "https://www.amazon.com/Thrum-Bull-Spirit-Chrissi-Smith-ebook/dp/B0HL989S11/ref=sr_1_1?crid=3MCJ5Y0C4NMZI&dib=eyJ2IjoiMSJ9.BcFHKKWzlKHq06ugYhcIZg.2MPWeuufx5-YZNXojH4I7VkibdotO7FPenVOlWieiPY&dib_tag=se&keywords=B0HL989S11&nsdOptOutParam=true&qid=1790846918&s=digital-text&sprefix=b0hl989s11%2Cdigital-text%2C177&sr=1-1",
    ]
    campaign_data = {
        "title": "The Thrum of the Bull Spirit",
        "hook": "Uncover the raw mechanics behind modern obscurity and independent creation.",
        "tags": ["indie publishing", "metabolic health", "creative philosophy"],
    }

    pipeline = ZeroCostAdPipeline(
        target_urls=book_destinations,
        asset_payload=campaign_data,
    )
    pipeline.execute_routing()