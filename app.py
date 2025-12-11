
from flask import Flask, render_template
import requests
import random

app = Flask(__name__)

# Rick and Morty API URL'si
BASE_URL = "https://rickandmortyapi.com/api/character/"

@app.route('/')
def home():
    # 1 ile 826 arasında rastgele karakter seç
    karakter_id = random.randint(1, 826)
    endpoint = f"{BASE_URL}{karakter_id}"
    
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            
            k_isim = data.get('name')
            k_durum = data.get('status')
            k_tur = data.get('species')
            k_cinsiyet = data.get('gender')
            k_resim = data.get('image')
            k_konum = data['location']['name']
            
            # Renk ayarı
            durum_renk = "gray"
            if k_durum == "Alive":
                durum_renk = "#55cc44" # Yeşil
            elif k_durum == "Dead":
                durum_renk = "#d63d2e" # Kırmızı

            return render_template('index.html',
                                   isim=k_isim,
                                   durum=k_durum,
                                   tur=k_tur,
                                   cinsiyet=k_cinsiyet,
                                   resim=k_resim,
                                   konum=k_konum,
                                   renk=durum_renk)
        else:
            return "API Hatası"
    except:
        return "Bağlantı Hatası"

if __name__ == '__main__':
    # Docker için host 0.0.0.0 olmak ZORUNDA
    app.run(debug=True, host='0.0.0.0', port=5000)
