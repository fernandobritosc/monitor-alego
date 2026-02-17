import requests
from bs4 import BeautifulSoup
import os
import json
import logging
from datetime import datetime
from urllib.parse import urljoin

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
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

DATA_FILE = "concursos_data.json"
CONFIG_FILE = "config.json"

def send_telegram_msg(message):
    if not TOKEN or not ID_CHAT:
        logging.warning("TOKEN ou ID_CHAT do Telegram não configurados.")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        res = requests.post(url, data={
            "chat_id": ID_CHAT, 
            "text": message, 
            "parse_mode": "Markdown", 
            "disable_web_page_preview": True
        })
        res.raise_for_status()
    except Exception as e:
        logging.error(f"Erro ao enviar Telegram: {e}")

def load_json(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Erro ao carregar {filepath}: {e}")
            return {}
    return {}

def save_json(filepath, data):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Erro ao salvar {filepath}: {e}")

def monitorar():
    logging.info("Iniciando monitoramento...")
    config = load_json(CONFIG_FILE)
    if not config:
        logging.error("Arquivo de configuração não encontrado ou vazio!")
        return

    hoje = datetime.now().strftime("%Y-%m-%d")
    old_data = load_json(DATA_FILE)
    new_data = old_data.copy()
    mudanca = False

    # --- PROCESSAMENTO DE CALENDÁRIOS ---
    calendarios = config.get("calendarios", {})
    alertas_enviados = old_data.get("alertas_calendario_enviados", [])
    
    for nome_concurso, prazos in calendarios.items():
        if hoje in prazos:
            identificador_alerta = f"{nome_concurso}_{hoje}"
            if identificador_alerta not in alertas_enviados:
                evento = prazos[hoje]
                msg = f"📅 *ALERTA DE PRAZO: {nome_concurso}*\n\n📍 Data: {hoje}\n🔔 Evento: *{evento}*\n\nConfira no site oficial!"
                send_telegram_msg(msg)
                alertas_enviados.append(identificador_alerta)
                mudanca = True
    
    new_data["alertas_calendario_enviados"] = alertas_enviados

    # --- MONITORAMENTO DE SITES ---
    ignore_list = config.get("ignore_list", [])
    sites = config.get("sites", [])

    for site in sites:
        if not site.get("active", True):
            continue
            
        name = site["name"]
        url = site["url"]
        
        try:
            logging.info(f"Verificando {name}...")
            res = requests.get(url, headers=HEADERS, timeout=30)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Captura texto e link para evitar ignorar atualizações de arquivos com mesmo nome
            items = []
            for a in soup.find_all('a'):
                text = a.get_text(strip=True)
                href = a.get('href')
                
                if not text or not href or len(text) < 5:
                    continue
                
                # Filtro de ruído (Ignore List)
                if any(ignore.lower() in text.lower() for ignore in ignore_list):
                    continue
                
                # Normaliza a URL
                full_url = urljoin(url, href)
                items.append(f"{text} ({full_url})")

            current_items = sorted(list(set(items)))

            if name in old_data and isinstance(old_data[name], list):
                # Compara o que tem de novo
                diff = set(current_items) - set(old_data[name])
                if diff:
                    # Limpa a mensagem para enviar apenas o texto amigável
                    new_docs = []
                    for item in diff:
                        # Extrai o texto antes do parêntese da URL
                        doc_name = item.rsplit(" (", 1)[0]
                        new_docs.append(f"• {doc_name}")
                    
                    msg = f"🔔 *Nova atualização: {name}*\n\n" + "\n".join(new_docs)
                    send_telegram_msg(msg)
                    mudanca = True
            
            new_data[name] = current_items
            
        except Exception as e:
            logging.error(f"Erro ao acessar {name}: {e}")

    if mudanca:
        save_json(DATA_FILE, new_data)
        logging.info("Alterações detectadas e salvas.")
    else:
        logging.info("Nenhuma novidade encontrada.")

if __name__ == "__main__":
    monitorar()
