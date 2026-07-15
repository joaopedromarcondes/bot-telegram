import os
import asyncio
import requests
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient
from telethon.sessions import StringSession

# --- CREDENCIAIS ---
api_id = int(os.environ['TG_API_ID'])
api_hash = os.environ['TG_API_HASH']
session_string = os.environ['TG_SESSION']

# Credenciais do Bot Notificador
bot_token = os.environ['BOT_TOKEN']
chat_id_destino = os.environ['MEU_CHAT_ID']

# --- CONFIGURAÇÃO ---
TERMOS = ['fonte corsair', 'vdh', 'nvme'] 
CHATS_ALVO = [] 

# Função para enviar via BOT (Isso gera notificação!)
def enviar_notificacao(mensagem):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    dados = {
        "chat_id": chat_id_destino,
        "text": mensagem,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        resposta = requests.post(url, data=dados)
        # Agora o bot vai nos contar a verdade:
        if resposta.status_code == 200:
            print("Notificação entregue de verdade no seu Telegram!")
        else:
            print(f"O Telegram recusou a mensagem! Erro: {resposta.text}")
    except Exception as e:
        print(f"Erro de conexão com a internet: {e}")

async def main():
    print("Iniciando verificação...")
    async with TelegramClient(StringSession(session_string), api_id, api_hash) as client:
        # Verifica últimas 2 horas
        limite_tempo = datetime.now(timezone.utc) - timedelta(hours=2)
        
        async for dialog in client.iter_dialogs():
            # 🛑 TRAVA 1: Ignora conversas privadas (incluindo o seu Bot Carteiro)
            # Foca apenas em Grupos e Canais de ofertas
            if dialog.is_user:
                continue
            
            if CHATS_ALVO and (dialog.id not in CHATS_ALVO):
                continue

            try:
                # Lê mensagens recentes
                async for message in client.iter_messages(dialog, offset_date=limite_tempo, reverse=True):
                    if not message.text: continue
                        
                    texto = message.text.lower()

                    # 🛑 TRAVA 2: Se a mensagem for um alerta do próprio bot, ignora!
                    if "achei oferta!" in texto:
                        continue
                    
                    for termo in TERMOS:
                        if termo in texto:
                            # Monta Link
                            chat_id_str = str(dialog.id).replace('-100', '')
                            link = f"https://t.me/c/{chat_id_str}/{message.id}"
                            if dialog.entity.username:
                                link = f"https://t.me/{dialog.entity.username}/{message.id}"

                            # Mensagem Bonita
                            alerta = (
                                f"🚨 **ACHEI OFERTA!**\n\n"
                                f"📦 **Item:** `{termo.upper()}`\n"
                                f"📢 **Onde:** {dialog.name}\n"
                                f"🔗 [Ver Mensagem]({link})\n"
                            )
                            
                            # AQUI ESTÁ A MÁGICA:
                            # Em vez de mandar para 'me', chamamos a função do Bot
                            print(f"--> Encontrado: {termo}. Enviando notificação...")
                            enviar_notificacao(alerta)
                            
            except Exception as e:
                pass

if __name__ == '__main__':
    asyncio.run(main())
