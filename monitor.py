import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv("TOKEN_TELEGRAM")
ID_CHAT = os.getenv("ID_TELEGRAM")
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Aqui você deve colocar os números que o robô acabou de ler
ULTIMO_FGV = 5401 
ULTIMO_VERBENA = 482

def monitorar():
    try:
        # Consulta FGV
        res_fgv = requests.get("https://conhecimento.fgv.br/concursos/alego25", headers=HEADERS)
        soup_fgv = BeautifulSoup(res_fgv.text, 'html.parser')
        atual_fgv = len(soup_fgv.get_text(strip=True))

        # Consulta Verbena
        res_verb = requests.get("https://sistemas.institutoverbena.ufg.br/2025/concurso-camara-goiania/", headers=HEADERS)
        soup_verb = BeautifulSoup(res_verb.text, 'html.parser')
        area_verb = soup_verb.find('div', class_='container')
        atual_verb = len(area_verb.get_text(strip=True)) if area_verb else 0

        # Verifica se algo mudou
        mudou = False
        msg = ""

        if atual_fgv != ULTIMO_FGV:
            msg += "🔔 Veja a nova publicação na FGV (ALEGO)!\n"
            mudou = True
        
        if atual_verb != ULTIMO_VERBENA:
            msg += "🔔 Veja a nova publicação na Verbena (Goiânia)!\n"
            mudou = True

        if mudou:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": ID_CHAT, "text": msg})
        else:
            # Apenas para você saber que o teste rodou e está tudo igual
            status = f"✅ Tudo igual por aqui.\nFGV: {atual_fgv} | Verbena: {atual_verb}"
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": ID_CHAT, "text": status})
    
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    monitorar()
