import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv("TOKEN_TELEGRAM")
ID_CHAT = os.getenv("ID_TELEGRAM")
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def monitorar():
    try:
        # --- FGV ALEGO (Captura Ampla) ---
        res_fgv = requests.get("https://conhecimento.fgv.br/concursos/alego25", headers=HEADERS)
        soup_fgv = BeautifulSoup(res_fgv.text, 'html.parser')
        # Pega todo o texto visível da página para não ter erro
        conteudo_fgv = soup_fgv.get_text(strip=True)

        # --- VERBENA GOIÂNIA (Mantido pois funciona) ---
        res_verb = requests.get("https://sistemas.institutoverbena.ufg.br/2025/concurso-camara-goiania/", headers=HEADERS)
        soup_verb = BeautifulSoup(res_verb.text, 'html.parser')
        area_verb = soup_verb.find('div', class_='container')
        conteudo_verb = area_verb.get_text(strip=True) if area_verb else "Erro Verbena"

        status = f"🛡️ Monitoramento Blindado!\n\n🏛️ FGV (ALEGO): {len(conteudo_fgv)} chars\n🏢 Verbena (Goiânia): {len(conteudo_verb)} chars"
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": ID_CHAT, "text": status})
    
    except Exception as e:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": ID_CHAT, "text": f"Erro: {e}"})

if __name__ == "__main__":
    monitorar()
