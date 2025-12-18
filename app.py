from flask import Flask, render_template, session
import requests
import random

app = Flask(__name__)

# Session (Hafıza) kullanmak için gizli bir anahtar şarttır
app.secret_key = "rick_sanchez_wubba_lubba_dub_dub"

BASE_URL = "https://rickandmortyapi.com/api/character/"

@app.route('/')
def home():
    # 1. Rastgele Karakter Çek
    karakter_id = random.randint(1, 826)
    endpoint = f"{BASE_URL}{karakter_id}"
    
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            
            # Karakter Verileri
            karakter = {
                'isim': data['name'],
                'resim': data['image'],
                'tur': data['species'],
                'cinsiyet': data['gender'],
                'konum': data['location']['name'],
                'durum': data['status'],
                # Duruma göre renk seçimi
                'renk': "#55efc4" if data['status'] == "Alive" else ("#d63031" if data['status'] == "Dead" else "#636e72")
            }

            # --- STATEFUL KISMI (HAFIZA) ---
            
            # Eğer hafızada 'gecmis' diye bir liste yoksa oluştur
            if 'gecmis' not in session:
                session['gecmis'] = []

            # Mevcut karakteri hafızaya ekle (Listenin en başına)
            # Aynı karakter üst üste gelmesin diye kontrol edebiliriz ama şimdilik gerek yok
            session['gecmis'].insert(0, karakter)

            # Hafıza çok şişmesin, sadece son 5 karakteri tutalım
            if len(session['gecmis']) > 5:
                session['gecmis'].pop()
            
            # Session'ın güncellendiğini belirt
            session.modified = True

            return render_template('index.html', 
                                   karakter=karakter, 
                                   gecmis=session['gecmis']) # Geçmişi de sayfaya gönderiyoruz
        else:
            return "API Hatası"
    except Exception as e:
        return f"Hata: {e}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
