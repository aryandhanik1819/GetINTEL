import requests
import os
from dotenv import load_dotenv

load_dotenv()
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

def hunter_email_lookup(email):
    if not HUNTER_API_KEY:
        return "❌ Hunter.io API key not found. Set it in .env file."

    url = "https://api.hunter.io/v2/email-verifier"
    params = {
        'email': email,
        'api_key': HUNTER_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json().get('data', {})
            return "<br>".join([
                f"• Email: {data.get('email')}",
                f"• Status: {data.get('status')}",
                f"• Result: {data.get('result')}",
                f"• Score: {data.get('score')}",
                f"• Disposable: {'Yes' if data.get('disposable') else 'No'}",
                f"• Webmail: {'Yes' if data.get('webmail') else 'No'}",
                f"• MX Records: {'Yes' if data.get('mx_records') else 'No'}",
                f"• SMTP Check: {'Yes' if data.get('smtp_check') else 'No'}",
                f"• Catch All: {'Yes' if data.get('accept_all') else 'No'}",
                f"• Sources: {', '.join([s['uri'] for s in data.get('sources', [])]) or 'None'}"
            ])
        elif response.status_code == 429:
            return "❌ Rate limit exceeded. Try again later."
        else:
            return f"❌ API request failed. Status code: {response.status_code}"
    except Exception as e:
        return f"❌ Error during email lookup: {str(e)}"
