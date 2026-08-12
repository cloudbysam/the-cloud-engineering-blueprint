import random
import string
from locust import HttpUser, task, between

class URLShortenerUser(HttpUser):
    # Pause between 0.1s and 0.5s between requests per user to simulate fast traffic
    wait_time = between(0.1, 0.5)

    def on_start(self):
        """Called when a virtual user is spawned. We create one short URL to use for read tasks."""
        self.short_code = None
        response = self.client.post(
            "/shorten",
            json={"url": "https://aws.amazon.com/ecs/"},
            name="/shorten (initialization)"
        )
        if response.status_code == 201:
            data = response.json()
            # Extract short code from the full URL string returned
            self.short_code = data.get("short_url", "").split("/")[-1]

    @task(8)
    def test_redirect(self):
        """Simulate high-volume read traffic (80% of workload)."""
        if self.short_code:
            # Catch redirects (302) as successful responses
            self.client.get(f"/{self.short_code}", name="/<short_code>", allow_redirects=False)

    @task(2)
    def test_shorten(self):
        """Simulate concurrent URL creation traffic (20% of workload)."""
        random_suffix = "".join(random.choices(string.ascii_lowercase, k=6))
        sample_url = f"https://example.com/page-{random_suffix}"
        
        self.client.post(
            "/shorten",
            json={"url": sample_url},
            name="/shorten"
        )