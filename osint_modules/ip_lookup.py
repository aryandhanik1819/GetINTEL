# osint_modules/ip_lookup.py
import requests
import ipaddress

def is_private_ip(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return False

def lookup_ip(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        data = response.json()

        if data["status"] == "success":
            result = (
                f"🌍 IP Info for <b>{ip}</b>:<br>"
                f"• Country: {data['country']}<br>"
                f"• Region: {data['regionName']}<br>"
                f"• City: {data['city']}<br>"
                f"• ISP: {data['isp']}<br>"
                f"• Org: {data['org']}<br>"
                f"• Timezone: {data['timezone']}<br>"
                f"• Lat/Lon: {data['lat']}, {data['lon']}<br>"
                f"• ZIP: {data['zip']}"
            )
            return result
        else:
            return f"❌ IP lookup failed for {ip}."
    except Exception as e:
        return f"❌ Exception during IP lookup: {str(e)}"
