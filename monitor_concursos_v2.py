import requests
from bs4 import BeautifulSoup
import os
import json
import logging
from datetime import datetime

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

TOKEN = os.getenv("TOKEN_TELEGRAM")
ID_CHAT = os.getenv("ID_TELEGRAM")
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'https://www.google.com/'
}

DATA_FILE = "concursos_data.json"

CALENDARIO_PRAZOS = {
    "2026-01-15": "Publicação da Relação Definitiva de Inscrições e Divulgação da Relação Candidato Vaga",
    "2026-02-02": "Publicação dos locais de prova (CCI)",
    "2026-02-08": "Aplicação da Prova Objetiva e Discursiva",
    "2026-02-10": "Gabarito Preliminar da Prova Objetiva",
    "2026-03-20": "Gabarito Definitivo e Resultado Preliminar da Prova Objetiva",
    "2026-04-06": "Resultado Definitivo da Prova Objetiva e Convocação para Títulos (Analista)",
    "2026-04-24": "Resultado Preliminar da Prova Discursiva",
    "2026-05-18": "Resultado Definitivo da Discursiva e Convocação para Heteroidentificação/Biopsicossocial/Prática/TAF",
    "2026-06-01": "Resultado Definitivo da Adaptação Razoável",
    "2026-06-08": "Resultado Preliminar da Heteroidentificação e Biopsicossocial",
    "2026-06-09": "Resultado Preliminar da Prova Prática",
    "2026-06-11": "Resultado Preliminar da Avaliação Psicológica e TAF",
    "2026-06-26": "Resultado Definitivo da Heteroidentificação e Biopsicossocial",
    "2026-07-01": "Resultado Definitivo de Títulos, Prática, TAF e Avaliação Psicológica",
    "2026-07-01": "RESULTADO FINAL DO CONCURSO"
}

def send_telegram_msg(message):
    if not TOKEN or not ID_CHAT: return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": ID_CHAT, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": True})
    except Exception as e:
        logging.error(f"Erro Telegram: {e}")

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return {}
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def monitorar():
    logging.info("Iniciando...")
    hoje = datetime.now().strftime("%Y-%m-%d")
    old_data = load_data()
    new_data = old_data.copy()
    mudanca = False

    # --- TRAVA ANTI-SPAM PARA O CALENDÁRIO ---
    if hoje in CALENDARIO_PRAZOS:
        # Verifica se o aviso para 'hoje' já consta no JSON como enviado
        if old_data.get("ultimo_alerta_calendario") != hoje:
            evento = CALENDARIO_PRAZOS[hoje]
            msg = f"📅 *ALERTA DE PRAZO HOJE!* ({hoje})\n\n📍 Evento: *{evento}*\n\nConfira no site oficial!"
            send_telegram_msg(msg)
            new_data["ultimo_alerta_calendario"] = hoje
            mudanca = True

    # --- MONITORAMENTO DE SITES ---
    sites = {
        "FGV (ALEGO)": "https://conhecimento.fgv.br/concursos/alego25",
        "Verbena (Câmara Goiânia)": "https://sistemas.institutoverbena.ufg.br/2025/concurso-camara-goiania/",
        "Cebraspe (Câmara dos Deputados)": "https://www.cebraspe.org.br/concursos/cd_25_ns"
    }
    
    for name, url in sites.items():
        try:
            res = requests.get(url, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(res.text, 'html.parser')
            links = [a.get_text(strip=True) for a in soup.find_all('a') if len(a.get_text(strip=True)) > 5]
            current_items = sorted(list(set(links)))

            if name in old_data and isinstance(old_data[name], list):
                diff = set(current_items) - set(old_data[name])
                if diff:
                    msg = f"🔔 *Nova atualização: {name}*\n" + "\n".join([f"• {i}" for i in diff])
                    send_telegram_msg(msg)
                    mudanca = True
            
            new_data[name] = current_items
        except Exception as e:
            logging.error(f"Erro em {name}: {e}")

    if mudanca:
        save_data(new_data)

if __name__ == "__main__":
    monitorar()
