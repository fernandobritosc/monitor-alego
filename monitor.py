import requests
from bs4 import BeautifulSoup
import os

# Configurações vindas dos seus Secrets
TOKEN = os.getenv("TOKEN_TELEGRAM")
ID_CHAT = os.getenv("ID_TELEGRAM")

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": ID_CHAT, "text": mensagem})

def monitorar():
    # --- MONITOR FGV (ALEGO) ---
    url_fgv = "https://conhecimento.fgv.br/concursos/alego24"
    res_fgv = requests.get(url_fgv)
    soup_fgv = BeautifulSoup(res_fgv.text, 'html.parser')
    # Pega o primeiro item da lista de notícias da FGV
    noticia_fgv = soup_fgv.find('div', class_='views-row')
    txt_fgv = noticia_fgv.get_text(strip=True) if noticia_fgv else "Erro FGV"

    # --- MONITOR VERBENA (CÂMARA GOIÂNIA) ---
    url_verbena = "https://sistemas.institutoverbena.ufg.br/2025/concurso-camara-goiania/"
    res_verbena = requests.get(url_verbena)
    soup_verbena = BeautifulSoup(res_verbena.text, 'html.parser')
    # Tenta pegar a primeira linha de comunicados
    noticia_verbena = soup_verbena.find('div', class_='field-content')
    txt_verbena = noticia_verbena.get_text(strip=True) if noticia_verbena else "Erro Verbena"

    # Lógica simples de comparação (exemplo simplificado)
    # Aqui você salvaria num arquivo txt para comparar se mudou
    # Por enquanto, ele apenas avisa que o monitoramento está ativo
    print(f"FGV: {txt_fgv}")
    print(f"Verbena: {txt_verbena}")

if __name__ == "__main__":
    monitorar()
