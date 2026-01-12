import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv("TOKEN_TELEGRAM")
ID_CHAT = os.getenv("ID_TELEGRAM")

def enviar_msg(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": ID_CHAT, "text": texto})

def monitorar():
    # --- CHECK FGV (ALEGO) ---
    url_fgv = "https://conhecimento.fgv.br/concursos/alego25" # Conforme sua imagem
    res_fgv = requests.get(url_fgv)
    soup_fgv = BeautifulSoup(res_fgv.text, 'html.parser')
    # Pega o primeiro link da lista de arquivos
    noticia_fgv = soup_fgv.find('a', class_='p-l-0') 
    msg_fgv = f"FGV ALEGO: {noticia_fgv.get_text(strip=True)}" if noticia_fgv else "Sem dados FGV"

    # --- CHECK VERBENA (CÂMARA) ---
    url_verbena = "https://sistemas.institutoverbena.ufg.br/2025/concurso-camara-goiania/"
    res_verbena = requests.get(url_verbena)
    soup_verbena = BeautifulSoup(res_verbena.text, 'html.parser')
    # Pega o primeiro comunicado
    noticia_verbena = soup_verbena.find('div', class_='field-content')
    msg_verbena = f"VERBENA CÂMARA: {noticia_verbena.get_text(strip=True)}" if noticia_verbena else "Sem dados Verbena"

    # Envia o status para o grupo
    enviar_msg(f"✅ Monitoramento Ativo:\n\n1️⃣ {msg_fgv}\n2️⃣ {msg_verbena}")

if __name__ == "__main__":
    monitorar()
