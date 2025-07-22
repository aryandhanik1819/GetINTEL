import subprocess
import os

def scan_username(username):
    try:
        output_dir = os.path.join("static", "reports")
        os.makedirs(output_dir, exist_ok=True)

        # Run Maigret with correct output folder and HTML format
        cmd = [
            "python3",
            "-m", "maigret",
            username,
            "--folderoutput", output_dir,
            "--html"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return f"❌ Error occurred while scanning username:<br><pre>{result.stderr}</pre>"

        # Maigret saves HTML in: static/reports/report_<username>_plain.html
        output_file = os.path.join(output_dir, f"report_{username}_plain.html")
        if os.path.exists(output_file):
            return f"✅ Scan complete: <a href='/{output_file}' target='_blank'>Open {username}'s Report</a>"
        else:
            return "⚠️ Scan ran, but HTML report was not found."

    except Exception as e:
        return f"❌ Exception occurred:<br><pre>{str(e)}</pre>"
