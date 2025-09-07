from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    report = ""
    if request.method == "POST":
        domain = request.form.get("domain")
        if domain:
            report = f"🔒 Scanning {domain}...\n\n"
            try:
                resp = requests.get("https://" + domain, timeout=5)
                headers = resp.headers
                checks = {
                    "Content-Security-Policy": "Protects against XSS",
                    "Strict-Transport-Security": "Forces HTTPS",
                    "X-Frame-Options": "Prevents clickjacking",
                    "X-Content-Type-Options": "Stops MIME-sniffing",
                    "Referrer-Policy": "Controls referrer info"
                }
                for h, desc in checks.items():
                    if h in headers:
                        report += f"✅ {h} present ({headers[h]}) — {desc}\n"
                    else:
                        report += f"❌ {h} missing — {desc}\n"
            except Exception as e:
                report += f"Error: {e}"
    return render_template_string("""
        <h2>Simple Security Scanner</h2>
        <form method="post">
          <input type="text" name="domain" placeholder="example.com" required>
          <button type="submit">Scan</button>
        </form>
        <pre>{{report}}</pre>
    """, report=report)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)