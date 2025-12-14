from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- Veritabanı Ayarları ---
# Verileri 'market.db' adında bir dosyada tutacağız
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Veritabanı Tablosu (Model) ---
class Iletisim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_soyad = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mesaj = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Mesaj {self.ad_soyad}>'

# Uygulama başlarken veritabanını oluştur
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    # Eğer formu doldurup "Gönder"e bastılarsa (POST isteği)
    if request.method == "POST":
        gelen_ad = request.form.get("name")      # HTML'deki name="name"
        gelen_email = request.form.get("email")  # HTML'deki name="email"
        gelen_mesaj = request.form.get("message")# HTML'deki name="message"

        # Veritabanına yeni kayıt oluştur
        yeni_mesaj = Iletisim(ad_soyad=gelen_ad, email=gelen_email, mesaj=gelen_mesaj)
        db.session.add(yeni_mesaj)
        db.session.commit()
        
        # İşlem bitince sayfayı yenile (veya teşekkür sayfasına git)
        return redirect(url_for('home'))

    return render_template("index.html")

# --- (GİZLİ) Mesajları Görme Paneli ---
# Tarayıcıya /mesajlari-oku yazarak gelenleri görebilirsin
# --- (GİZLİ) Mesajları Görme Paneli ---
@app.route("/mesajlari-oku")
def mesajlari_oku():
    # Veritabanındaki tüm mesajları al
    tum_mesajlar = Iletisim.query.all()
    # admin.html sayfasına gönder
    return render_template("admin.html", mesajlar=tum_mesajlar)
# --- Mesaj Silme İşlemi ---
@app.route('/mesaj-sil/<int:id>')
def mesaj_sil(id):
    # 1. Silinecek mesajı ID numarasına göre bul
    silinecek_mesaj = Iletisim.query.get_or_404(id)
    
    # 2. Veritabanından sil
    db.session.delete(silinecek_mesaj)
    
    # 3. Değişiklikleri kaydet (Commit)
    db.session.commit()
    
    # 4. İşlem bitince tekrar mesaj listesine dön
    return redirect(url_for('mesajlari_oku'))

if __name__ == "__main__":
    app.run(debug=True)