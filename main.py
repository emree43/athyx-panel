from flask import Flask, request, render_template_string, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "athyx_gizli_anahtar_123456"

SIFRE = "amca"

API_LIST = [
    {"name": "TC Sorgu", "endpoint": "http://arastir.vip/api/tc.php", "params": ["tc"]},
    {"name": "Ad Soyad Sorgu", "endpoint": "http://arastir.vip/api/adsoyad.php", "params": ["ad", "soyad"]},
    {"name": "Aile Sorgu", "endpoint": "http://arastir.vip/api/aile.php", "params": ["tc"]},
    {"name": "Sülale Sorgu", "endpoint": "http://arastir.vip/api/sulale.php", "params": ["tc"]},
    {"name": "Çocuk Sorgu", "endpoint": "http://arastir.vip/api/cocuk.php", "params": ["tc"]},
    {"name": "Adres Sorgu", "endpoint": "http://arastir.vip/api/adres.php", "params": ["tc"]},
    {"name": "GSM'den TC", "endpoint": "http://arastir.vip/api/gsmtc.php", "params": ["gsm"]},
    {"name": "TC'den GSM", "endpoint": "http://arastir.vip/api/tcgsm.php", "params": ["tc"]},
    {"name": "İş Yeri Sorgu", "endpoint": "http://arastir.vip/api/isyeri.php", "params": ["tc"]}
]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>athyx Paneli</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #0b0e14;
            color: #e0e0e0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            max-width: 1100px;
            width: 100%;
            margin: auto;
            background: #151e28;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 0 40px #00ffcc22;
            border: 1px solid #00ffcc33;
        }
        h1 {
            color: #00ffcc;
            text-shadow: 0 0 20px #00ffcc66;
            text-align: center;
            font-size: 2.2rem;
            margin-bottom: 5px;
        }
        .hosgeldin {
            text-align: center;
            font-size: 1.3rem;
            color: #f0e68c;
            margin-bottom: 30px;
            border-bottom: 1px solid #2a3a4a;
            padding-bottom: 15px;
            font-style: italic;
        }
        .hosgeldin span {
            color: #00ffcc;
            font-weight: bold;
        }
        .cikis-btn {
            float: right;
            background: #ff4444;
            color: #fff;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            text-decoration: none;
        }
        .cikis-btn:hover {
            background: #cc0000;
        }
        .api-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .api-card {
            background: #1e2a36;
            padding: 18px;
            border-radius: 16px;
            border: 1px solid #2a3a4a;
            transition: 0.3s;
        }
        .api-card:hover {
            border-color: #00ffcc;
            box-shadow: 0 0 20px #00ffcc22;
        }
        .api-card h3 {
            color: #00ffcc;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }
        .api-card input {
            width: 100%;
            padding: 10px;
            margin: 5px 0;
            background: #0b0e14;
            border: 1px solid #2a3a4a;
            color: #fff;
            border-radius: 8px;
            font-size: 0.95rem;
        }
        .api-card button {
            width: 100%;
            padding: 10px;
            background: #00ffcc;
            color: #000;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 1rem;
            cursor: pointer;
            margin-top: 8px;
            transition: 0.2s;
        }
        .api-card button:hover {
            background: #00ddbb;
        }
        .sonuc {
            margin-top: 30px;
            background: #0b0e14;
            padding: 20px;
            border-radius: 16px;
            border: 1px solid #00ffcc44;
            white-space: pre-wrap;
            word-break: break-word;
            max-height: 400px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 0.9rem;
            color: #aaddff;
        }
        .sonuc h2 {
            color: #00ffcc;
            font-family: 'Segoe UI', sans-serif;
            margin-bottom: 10px;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #555;
            font-size: 0.8rem;
        }
        @media (max-width: 600px) {
            .container { padding: 15px; }
            h1 { font-size: 1.5rem; }
            .api-grid { grid-template-columns: 1fr; }
        }
        .login-box {
            max-width: 400px;
            width: 100%;
            margin: 0 auto;
            background: #151e28;
            padding: 40px;
            border-radius: 20px;
            border: 1px solid #00ffcc33;
            box-shadow: 0 0 40px #00ffcc22;
            text-align: center;
        }
        .login-box input {
            width: 100%;
            padding: 14px;
            margin: 10px 0;
            background: #0b0e14;
            border: 1px solid #2a3a4a;
            color: #fff;
            border-radius: 10px;
            font-size: 1rem;
        }
        .login-box button {
            width: 100%;
            padding: 14px;
            background: #00ffcc;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            font-size: 1.1rem;
            cursor: pointer;
        }
        .login-box h2 {
            color: #00ffcc;
            margin-bottom: 20px;
        }
        .login-box .hata {
            color: #ff6666;
            margin-top: 10px;
        }
    </style>
</head>
<body>
{% if not oturum %}
<div class="login-box">
    <h2>🔐 athyx Paneli</h2>
    <form method="POST" action="/giris">
        <input type="password" name="sifre" placeholder="Şifreyi Gir" required>
        <button type="submit">Giriş Yap</button>
        {% if hata %}
        <div class="hata">❌ Şifre yanlış!</div>
        {% endif %}
    </form>
</div>
{% else %}
<div class="container">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <h1>⚡ athyx Paneli</h1>
        <a href="/cikis"><button class="cikis-btn">Çıkış</button></a>
    </div>
    <div class="hosgeldin">
        👋 <span>athyx paneline hoş geldin iyi sorgularrr</span> 🚀
    </div>
    <div class="api-grid">
        {% for api in api_list %}
        <div class="api-card">
            <h3>{{ api.name }}</h3>
            <form method="POST" action="/sorgula">
                <input type="hidden" name="endpoint" value="{{ api.endpoint }}">
                {% for p in api.params %}
                <input type="text" name="{{ p }}" placeholder="{{ p|upper }}" required>
                {% endfor %}
                <button type="submit">Sorgula</button>
            </form>
        </div>
        {% endfor %}
    </div>
    {% if sonuc %}
    <div class="sonuc">
        <h2>📋 Sonuç</h2>
        <pre>{{ sonuc }}</pre>
    </div>
    {% endif %}
    <div class="footer">🔒 Güvenli Bağlantı • athyx Panel v1.0</div>
</div>
{% endif %}
</body>
</html>
"""

@app.route("/")
def ana():
    if "giris" in session:
        return render_template_string(HTML, oturum=True, api_list=API_LIST, sonuc=session.get("sonuc", ""), hata=False)
    return render_template_string(HTML, oturum=False, hata=False)

@app.route("/giris", methods=["POST"])
def giris():
    sifre = request.form.get("sifre")
    if sifre == SIFRE:
        session["giris"] = True
        session["sonuc"] = ""
        return redirect(url_for("ana"))
    return render_template_string(HTML, oturum=False, hata=True)

@app.route("/cikis")
def cikis():
    session.clear()
    return redirect(url_for("ana"))

@app.route("/sorgula", methods=["POST"])
def sorgula():
    if "giris" not in session:
        return redirect(url_for("ana"))
    endpoint = request.form.get("endpoint")
    params = {}
    for key in request.form:
        if key not in ["endpoint"]:
            params[key] = request.form.get(key)
    try:
        response = requests.get(endpoint, params=params, timeout=15)
        session["sonuc"] = response.text if response.status_code == 200 else f"❌ Hata: {response.status_code}"
    except Exception as e:
        session["sonuc"] = f"❌ Bağlantı hatası: {str(e)}"
    return redirect(url_for("ana"))