from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request
from osint_modules.ip_lookup import lookup_ip, is_private_ip
from osint_modules.phone_lookup import check_phone
from osint_modules.username_scan import scan_username
from osint_modules.image_metadata import extract_metadata
from osint_modules.email_hunter import hunter_email_lookup  # ✅ NEW import
import os

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    ip = request.form.get("ip")
    phone = request.form.get("phone")
    username = request.form.get("username")
    email = request.form.get("email")
    image = request.files.get("image")

    # -------------------- IP Lookup --------------------
    if ip:
        if is_private_ip(ip):
            ip_result = f"ℹ <b>{ip}</b> is a private/internal IP. No public OSINT data available."
        else:
            ip_result = lookup_ip(ip)
    else:
        ip_result = "No IP provided."

    # ------------------ Phone Lookup -------------------
    phone_data = check_phone(phone) if phone else {}
    phone_result = "<br>".join([f"• {k.capitalize()}: {v}" for k, v in phone_data.items()]) if phone_data else "No phone provided."

    # ---------------- Username Scan --------------------
    user_result = scan_username(username) if username else "No username provided."

    # ---------------- Email Lookup (Hunter.io) ---------------------
    email_result = hunter_email_lookup(email) if email else "No email provided."

    # ---------------- Image Metadata -------------------
    image_result = "No image uploaded."
    if image and image.filename:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)
        metadata = extract_metadata(image_path)
        if metadata:
            image_result = "<br>".join([f"• {k}: {v}" for k, v in metadata.items()])
        else:
            image_result = "Image uploaded, but no EXIF metadata found."

    # -------------- Render Results Page ----------------
    return render_template(
        'result.html',
        ip_result=ip_result,
        phone_result=phone_result,
        user_result=user_result,
        email_result=email_result,
        image_result=image_result
    )

if __name__ == '__main__':
    app.run(debug=True)
