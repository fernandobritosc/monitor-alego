import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv("TOKEN_TELEGRAM")
ID_CHAT = os.getenv("ID_TELEGRAM")
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def monitorar():
    # --- Lógica FGV (ALEGO) ---
    res_fgv = requests.get("https://conhecimento.fgv.br/concursos/alego25", headers=HEADERS)
    soup_fgv = BeautifulSoup(res_fgv.text, 'html.parser')
    noticia_fgv = soup_fgv.find('a', class_='p-l-0')
    txt_fgv = noticia_fgv.get_text(strip=True) if noticia_fgv else "Sem dados"

    # --- Lógica Verbena (Câmara Goiânia) ---
    res_verbena = requests.get("https://sistemas.institutoverbena.ufg.br/2025/concurso-camara-goiania/", headers=HEADERS)
    soup_verbena = BeautifulSoup(res_verbena.text, 'html.parser')
    # Procura o primeiro comunicado da lista que vimos na sua foto
    noticia_verbena = soup_verbena.find('div', class_='field-content')
    txt_verbena = noticia_verbena.get_text(strip=True) if noticia_verbena else "Sem dados"

    # Envia a confirmação para o grupo
    msg = f"✅ Monitoramento Ativo!\n\n🏛 ALEGO (FGV): {txt_fgv[:50]}...\n\n🏢 Goiânia (Verbena): {txt_verbena[:50]}..."
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": ID_CHAT, "text": msg})

if __name__ == "__main__":
    monitorar()
