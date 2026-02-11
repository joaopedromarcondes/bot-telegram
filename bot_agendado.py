import os
import asyncio
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient
from telethon.sessions import StringSession

# Pega as chaves dos Segredos do GitHub
api_id = int(os.environ['TG_API_ID'])
api_hash = os.environ['TG_API_HASH']
session_string = os.environ['TG_SESSION']

# --- CONFIGURAÇÃO ---
TERMOS = ['rtx 4060', 'ryzen 5', 'ssd 1tb', 'monitor'] # Seus termos em minúsculo
CHATS_ALVO = [] # Deixe vazio [] para ler TODOS os grupos, ou coloque IDs: [-100123456, -100987654]

async def main():
    print("Iniciando verificação...")
    async with TelegramClient(StringSession(session_string), api_id, api_hash) as client:
        # Define o tempo limite: Agora (UTC) menos 35 minutos
        limite_tempo = datetime.now(timezone.utc) - timedelta(minutes=35)
        
        # Itera por todos os diálogos (grupos/canais)
        async for dialog in client.iter_dialogs():
            # Se definiu CHATS_ALVO, ignora os que não estão na lista
            if CHATS_ALVO and (dialog.id not in CHATS_ALVO):
                continue

            try:
                # Lê as mensagens desse grupo enviadas após o limite_tempo
                async for message in client.iter_messages(dialog, offset_date=limite_tempo, reverse=True):
                    if not message.text:
                        continue
                        
                    texto = message.text.lower()
                    
                    # Verifica cada termo
                    for termo in TERMOS:
                        if termo in texto:
                            # Monta o Link da mensagem
                            chat_id_str = str(dialog.id).replace('-100', '')
                            link = f"https://t.me/c/{chat_id_str}/{message.id}"
                            if dialog.entity.username: # Se for canal público
                                link = f"https://t.me/{dialog.entity.username}/{message.id}"

                            # Envia o alerta para VOCÊ (Saved Messages)
                            alerta = (
                                f"🚨 **ACHEI OFERTA!**\n\n"
                                f"📦 **Item:** {termo.upper()}\n"
                                f"📢 **Onde:** {dialog.name}\n"
                                f"🔗 **Link:** {link}\n"
                                f"⏰ **Hora:** {message.date.strftime('%H:%M')}"
                            )
                            await client.send_message('me', alerta)
                            print(f"--> Encontrado: {termo} em {dialog.name}")
                            
            except Exception as e:
                # Ignora erros de permissão em grupos específicos
                pass

if __name__ == '__main__':
    asyncio.run(main())