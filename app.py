from flask import Flask, render_template, session, request, redirect, url_for
import requests
import random

app = Flask(__name__)
app.secret_key = "rick_sanchez_secret_portal_key"

BASE_URL = "https://rickandmortyapi.com/api/character/"

@app.route('/', methods=['GET'])
def home():
    if 'favoriler' not in session:
        session['favoriler'] = []

    # 1. URL'de 'char_id' var mı diye bak (Favoriden dönerken burası dolu olacak)
    istenen_id = request.args.get('char_id')

    if istenen_id:
        # Varsa o karakteri göster (Değiştirme!)
        karakter_id = istenen_id
    else:
        # Yoksa (Portalı Aç dendiğinde) Rastgele getir
        karakter_id = random.randint(1, 826)

    try:
        response = requests.get(f"{BASE_URL}{karakter_id}")
        if response.status_code == 200:
            data = response.json()
            
            karakter = {
                'id': data['id'], # ID ÇOK ÖNEMLİ
                'isim': data['name'],
                'resim': data['image'],
                'tur': data['species'],
                'cinsiyet': data['gender'],
                'konum': data['location']['name'],
                'durum': data['status'],
                'renk': "#55efc4" if data['status'] == "Alive" else ("#d63031" if data['status'] == "Dead" else "#636e72")
            }

            return render_template('index.html', karakter=karakter, favoriler=session['favoriler'])
        return "API Hatası"
    except Exception as e:
        return f"Hata: {e}"

@app.route('/favori-ekle', methods=['POST'])
def favori_ekle():
    # Hangi karakterde olduğumuzu formdan alıyoruz
    mevcut_id = request.form.get('id')
    
    yeni_favori = {
        'isim': request.form['isim'],
        'resim': request.form['resim'],
        'tur': request.form['tur'],
        'durum': request.form['durum'],
        'renk': request.form['renk']
    }
    
    mevcut_favoriler = session.get('favoriler', [])
    
    # Aynı isimde varsa ekleme
    if not any(f['isim'] == yeni_favori['isim'] for f in mevcut_favoriler):
        mevcut_favoriler.insert(0, yeni_favori)
        session['favoriler'] = mevcut_favoriler
    
    # ÖNEMLİ: Ana sayfaya dönerken ID'yi de gönderiyoruz ki karakter değişmesin
    return redirect(url_for('home', char_id=mevcut_id))

@app.route('/temizle')
def temizle():
    session['favoriler'] = []
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
