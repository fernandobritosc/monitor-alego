import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv("TOKEN_TELEGRAM")
ID_CHAT = os.getenv("ID_TELEGRAM")
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def monitorar():
    try:
        # --- FGV ALEGO ---
        res_fgv = requests.get("https://conhecimento.fgv.br/concursos/alego25", headers=HEADERS)
        soup_fgv = BeautifulSoup(res_fgv.text, 'html.parser')
        # Pega a primeira notícia da lista de arquivos que vimos na sua foto
        item_fgv = soup_fgv.find('a', href=True, text=True) 
        txt_fgv = item_fgv.get_text(strip=True)[:60] if item_fgv else "Link da página de arquivos"

        # --- VERBENA GOIÂNIA ---
        res_verb = requests.get("https://sistemas.institutoverbena.ufg.br/2025/concurso-camara-goiania/", headers=HEADERS)
        soup_verb = BeautifulSoup(res_verb.text, 'html.parser')
        # Procura pelo texto 'Realizar Inscrição' que está na sua foto
        item_verb = soup_verb.find(text=lambda t: "Inscrição" in t)
        txt_verb = item_verb.strip() if item_verb else "Seção de comunicados ativa"

        msg = f"✅ Monitoramento Ativo!\n\n🏛 ALEGO (FGV): {txt_fgv}\n\n🏢 Goiânia (Verbena): {txt_verb}"
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": ID_CHAT, "text": msg})
    
    except Exception as e:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": ID_CHAT, "text": f"Erro: {e}"})

if __name__ == "__main__":
    monitorar()
