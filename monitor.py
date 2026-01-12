import os
import requests
from bs4 import BeautifulSoup

# O GitHub Actions pegará estes valores dos segredos que vamos configurar
TOKEN = os.getenv("TOKEN_TELEGRAM")
ID = os.getenv("ID_TELEGRAM")
URL = "https://conhecimento.fgv.br/concursos/alego25"

def verificar():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(URL, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        item = soup.find('div', class_='views-row')
        
        if item:
            texto_atual = item.get_text().strip()
            
            # Tenta ler o que foi visto na última vez
            if os.path.exists("ultimo_visto.txt"):
                with open("ultimo_visto.txt", "r", encoding='utf-8') as f:
                    ultimo_visto = f.read()
            else:
                ultimo_visto = ""

            # Se mudou, manda o Telegram
            if texto_atual != ultimo_visto:
                msg = f"🔔 NOVIDADE FGV ALEGO:\n\n{texto_atual}\n\nLink: {URL}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                              data={"chat_id": ID, "text": msg})
                
                # Salva o novo texto para a próxima comparação
                with open("ultimo_visto.txt", "w", encoding='utf-8') as f:
                    f.write(texto_atual)
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    verificar()
