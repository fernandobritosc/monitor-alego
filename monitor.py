import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv("TOKEN_TELEGRAM")
ID_CHAT = os.getenv("ID_TELEGRAM")
# Cabeçalho para o site não bloquear o robô
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def enviar_msg(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": ID_CHAT, "text": texto}
    r = requests.post(url, data=payload)
    print(f"Status Telegram: {r.status_code}") # Mostra no log do GitHub se enviou

def monitorar():
    try:
        # --- TESTE FGV (ALEGO) ---
        url_fgv = "https://conhecimento.fgv.br/concursos/alego25"
        res_fgv = requests.get(url_fgv, headers=HEADERS, timeout=10)
        soup_fgv = BeautifulSoup(res_fgv.text, 'html.parser')
        noticia_fgv = soup_fgv.find('a') # Pega o primeiro link que achar
        txt_fgv = noticia_fgv.get_text(strip=True)[:50] if noticia_fgv else "Não lido"
        
        # Envia a mensagem IMEDIATAMENTE após ler a FGV
        enviar_msg(f"🤖 Monitor On!\n\nFGV: {txt_fgv}\nLink: {url_fgv}")
        
    except Exception as e:
        enviar_msg(f"Erro no robô: {e}")

if __name__ == "__main__":
    monitorar()
