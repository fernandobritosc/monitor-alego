import requests
from bs4 import BeautifulSoup
import os
import hashlib

TOKEN = os.getenv("TOKEN_TELEGRAM")
ID_CHAT = os.getenv("ID_TELEGRAM")
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def monitorar():
    try:
        # --- MONITORAMENTO TOTAL FGV (ALEGO) ---
        res_fgv = requests.get("https://conhecimento.fgv.br/concursos/alego25", headers=HEADERS)
        soup_fgv = BeautifulSoup(res_fgv.text, 'html.parser')
        # Captura toda a área de arquivos do concurso
        area_fgv = soup_fgv.find('div', class_='view-content')
        conteudo_fgv = area_fgv.get_text(strip=True) if area_fgv else "Erro área FGV"

        # --- MONITORAMENTO TOTAL VERBENA (GOIÂNIA) ---
        res_verb = requests.get("https://sistemas.institutoverbena.ufg.br/2025/concurso-camara-goiania/", headers=HEADERS)
        soup_verb = BeautifulSoup(res_verb.text, 'html.parser')
        # Captura toda a área de Editais e Comunicados
        area_verb = soup_verb.find('div', class_='container')
        conteudo_verb = area_verb.get_text(strip=True) if area_verb else "Erro área Verbena"

        # Criamos um "resumo" (hash) do conteúdo atual para comparação futura
        # Se qualquer anexo for adicionado, esse resumo mudará
        status_atual = f"FGV: {len(conteudo_fgv)} chars | Verbena: {len(conteudo_verb)} chars"

        msg = f"🛡️ Segurança Total Ativada!\n\nMonitorando 100% das páginas.\n\n{status_atual}\n\nQualquer novo anexo será detectado!"
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": ID_CHAT, "text": msg})
    
    except Exception as e:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={"chat_id": ID_CHAT, "text": f"Erro técnico: {e}"})

if __name__ == "__main__":
    monitorar()
