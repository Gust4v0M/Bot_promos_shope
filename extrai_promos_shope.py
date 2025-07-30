import csv
import requests
import random
import time
import threading
import schedule
from datetime import datetime, timedelta

TOKEN = '8009036600:AAGqvH1-3esgXJsuaq6tK-XNren4CObTv2g'
CHAT_ID = '-1002737558462'
EMOJIS = ['🔥', '🤑', '💥', '🎯', '⚡', '💣', '🛍️', '🎁']

# Função que envia a mensagem
def enviar_mensagem_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': mensagem,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    return response.ok

# Agendamento dinâmico com delay
def agendar_envios(caminho_arquivo_csv, intervalo_minutos=60):
    with open(caminho_arquivo_csv, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))

    agora = datetime.now()

    for i, row in enumerate(reader):
        nome = row.get('Item Name', 'Produto sem nome')
        preco = row.get('Price', '0,00').replace('R$', '').strip()
        link = row.get('Offer Link', '')

        if not link:
            continue

        # Horário para envio
        horario_envio = agora + timedelta(minutes=i * intervalo_minutos)

        # Salva os dados como função a ser executada no horário
        schedule_time = horario_envio.strftime('%H:%M')

        def criar_funcao_envio(nome=nome, preco=preco, link=link):
            def enviar():
                emoji_inicio = random.choice(EMOJIS)
                emoji_fim = random.choice(EMOJIS)
                mensagem = (
                    f"{emoji_inicio} <b>{nome}</b>{emoji_fim}\n\n"
                    f"💰 <b>Por apenas:</b> R$ {preco}\n\n"
                    f"🛒 <a href='{link}'>Clique aqui para aproveitar na Shopee</a>"
                )
                sucesso = enviar_mensagem_telegram(mensagem)
                if sucesso:
                    print(f"✅ Enviado: {nome} às {datetime.now().strftime('%H:%M:%S')}")
                else:
                    print(f"❌ Falha: {nome}")
            return enviar

        # Agenda a função no horário definido
        schedule.every().day.at(schedule_time).do(criar_funcao_envio())
        print(f"🕒 Agendado: {nome} às {schedule_time}")

# Loop de execução para manter o script rodando
def run_schedule_loop():
    while True:
        schedule.run_pending()
        time.sleep(10)

# --- Execução ---
agendar_envios("csvs/promos_20250702.csv", intervalo_minutos=35 )

# Roda a programação em outra thread
threading.Thread(target=run_schedule_loop).start()
