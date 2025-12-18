from flask import Flask, render_template, session, request, redirect, url_for
import requests
import random

app = Flask(__name__)

# Session (Hafıza) için gizli anahtar (Bunu değiştirme)
app.secret_key = "rick_sanchez_secret_portal_key"

BASE_URL = "https://rickandmortyapi.com/api/character/"

@app.route('/', methods=['GET', 'POST'])
def home():
    # Sayfa ilk açıldığında veya 'Portalı Aç' dendiğinde
    
    # Eğer hafızada favoriler listesi yoksa oluştur
    if 'favoriler' not in session:
        session['favoriler'] = []

    # Rastgele Karakter Çek
    karakter_id = random.randint(1, 826)
    endpoint = f"{BASE_URL}{karakter_id}"
    
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            
            karakter = {
                'id': data['id'], # ID önemli (tekrar eklemeyi önlemek için)
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
    # Formdan gelen verileri al
    yeni_favori = {
        'isim': request.form['isim'],
        'resim': request.form['resim'],
        'tur': request.form['tur'],
        'durum': request.form['durum'],
        'renk': request.form['renk']
    }
    
    # Hafıza listesini al
    mevcut_favoriler = session.get('favoriler', [])
    
    # AYNI KARAKTERİ İKİ KERE EKLEMEMEK İÇİN KONTROL:
    # Listede bu isimde biri var mı diye bakıyoruz
    zaten_var = False
    for fav in mevcut_favoriler:
        if fav['isim'] == yeni_favori['isim']:
            zaten_var = True
            break
    
    if not zaten_var:
        mevcut_favoriler.insert(0, yeni_favori) # En başa ekle
        session['favoriler'] = mevcut_favoriler # Listeyi güncelle
    
    # Ana sayfaya geri dön (Karakter değişmesin diye redirect yerine render yapabilirdik ama basit olsun diye redirect)
    return redirect(url_for('home'))

# --- FAVORİLERİ TEMİZLEME ROTASI (Opsiyonel ama şık durur) ---
@app.route('/temizle')
def temizle():
    session['favoriler'] = []
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
