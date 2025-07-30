import asyncio
import telegram

async def enviar_mensagem():
    bot = telegram.Bot(token='8009036600:AAGqvH1-3esgXJsuaq6tK-XNren4CObTv2g')
    await bot.send_message(chat_id='-1002737558462', text="👋 Olá! Bot funcionando com sucesso!")

asyncio.run(enviar_mensagem())


#TOKEN = '8009036600:AAGqvH1-3esgXJsuaq6tK-XNren4CObTv2g'
#CHAT_ID = '-1002737558462'  # Seu grupo

