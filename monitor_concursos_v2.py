import requests
from bs4 import BeautifulSoup
import os
import json
import logging
from datetime import datetime

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='monitor_concursos.log'
)

TOKEN = os.getenv("TOKEN_TELEGRAM")
ID_CHAT = os.getenv("ID_TELEGRAM")
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

DATA_FILE = "concursos_data.json"

# --- CRONOGRAMA OFICIAL ALEGO 2025 (Extraído do PDF) ---
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
    if not TOKEN or not ID_CHAT:
        logging.error("Configurações do Telegram ausentes.")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        response = requests.post(url, data={
            "chat_id": ID_CHAT, 
            "text": message, 
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        })
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem para o Telegram: {e}")

def verificar_calendario():
    """Verifica se hoje há algum prazo importante no calendário."""
    hoje = datetime.now().strftime("%Y-%m-%d")
    if hoje in CALENDARIO_PRAZOS:
        evento = CALENDARIO_PRAZOS[hoje]
        msg = f"📅 *ALERTA DE PRAZO HOJE!* ({hoje})\n\n"
        msg += f"📍 Evento: *{evento}*\n"
        msg += "\nNão esqueça de conferir os detalhes no site oficial!"
        send_telegram_msg(msg)
        logging.info(f"Alerta de calendário enviado: {evento}")

def get_page_items(url, selector=None):
    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        root = soup.select_one(selector) if selector else soup
        if not root:
            root = soup
        items = []
        for a in root.find_all('a'):
            text = a.get_text(strip=True)
            if text and len(text) > 3:
                items.append(text)
        return sorted(list(set(items)))
    except Exception as e:
        logging.error(f"Erro ao acessar {url}: {e}")
        return None

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def monitorar():
    logging.info("Iniciando monitoramento...")
    verificar_calendario()
    
    sites = {
        "FGV (ALEGO)": {
            "url": "https://conhecimento.fgv.br/concursos/alego25",
            "selector": "#block-system-main"
        },
        "Verbena (Câmara Goiânia)": {
            "url": "https://sistemas.institutoverbena.ufg.br/2025/concurso-camara-goiania/",
            "selector": ".container" 
        }
    }
    
    old_data = load_data()
    new_data = {}
    
    for name, info in sites.items():
        current_items = get_page_items(info['url'], info['selector'])
        if current_items is not None:
            new_data[name] = current_items
            if name in old_data:
                old_items = set(old_data[name])
                diff = set(current_items) - old_items
                if diff:
                    msg = f"🔔 *Nova atualização no site: {name}*\n\n"
                    msg += "Os seguintes itens novos foram encontrados:\n"
                    for item in diff:
                        msg += f"• {item}\n"
                    msg += f"\n🔗 [Acesse o site aqui]({info['url']})"
                    send_telegram_msg(msg)
            else:
                logging.info(f"Primeira execução para {name}.")
        else:
            if name in old_data:
                new_data[name] = old_data[name]
    
    save_data(new_data)

if __name__ == "__main__":
    monitorar()
