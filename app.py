from flask import Flask, render_template, session, request, redirect, url_for
import requests
import random

app = Flask(__name__)

# Session (Hafıza) anahtarı
app.secret_key = "rick_sanchez_secret_portal_key"

BASE_URL = "https://rickandmortyapi.com/api/character/"

@app.route('/', methods=['GET'])
def home():
    # Hafıza kontrolü
    if 'favoriler' not in session:
        session['favoriler'] = []

    # --- YENİ MANTIK BURADA ---
    # URL'de belirli bir karakter ID'si var mı diye bakıyoruz.
    # Örn: localhost:5000/?char_id=5
    istenen_id = request.args.get('char_id')

    if istenen_id:
        # Eğer favoriden döndüysek AYNI karakteri göster
        karakter_id = istenen_id
    else:
        # Eğer Portalı Aç dediysek RASTGELE karakter göster
        karakter_id = random.randint(1, 826)

    endpoint = f"{BASE_URL}{karakter_id}"
    
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            
            karakter = {
                'id': data['id'], # ID'yi HTML'e göndermek şart oldu
                'isim': data['name'],
                'resim': data['image'],
                'tur': data['species'],
                'cinsiyet': data['gender'],
                'konum': data['location']['name'],
                'durum': data['status'],
                'renk': "#55efc4" if data['status'] == "Alive" else ("#d63031" if data['status'] == "Dead" else "#636e72")
            }

            return render_template('index.html', 
                                   karakter=karakter, 
                                   favoriler=session['favoriler'])
        else:
            return "API Hatası"
    except Exception as e:
        return f"Hata: {e}"

# --- FAVORİ EKLEME ROTASI ---
@app.route('/favori-ekle', methods=['POST'])
def favori_ekle():
    # Formdan verileri al
    mevcut_id = request.form['id'] # Hangi karakterde olduğumuzu öğreniyoruz
    
    yeni_favori = {
        'isim': request.form['isim'],
        'resim': request.form['resim'],
        'tur': request.form['tur'],
        'durum': request.form['durum'],
        'renk': request.form['renk']
    }
    
    mevcut_favoriler = session.get('favoriler', [])
    
    # Aynı karakter kontrolü
    zaten_var = False
    for fav in mevcut_favoriler:
        if fav['isim'] == yeni_favori['isim']:
            zaten_var = True
            break
    
    if not zaten_var:
        mevcut_favoriler.insert(0, yeni_favori)
        session['favoriler'] = mevcut_favoriler
    
    # DİKKAT: Ana sayfaya dönerken "char_id" parametresini de gönderiyoruz.
    # Böylece sayfa yenilendiğinde aynı karakter kalıyor.
    return redirect(url_for('home', char_id=mevcut_id))

@app.route('/temizle')
def temizle():
    session['favoriler'] = []
    # Temizleyince rastgele birine gitmek mantıklı, ya da o anki ID'de kalabiliriz.
    # Şimdilik ana sayfaya (rastgele) atalım.
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
