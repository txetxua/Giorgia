import discord
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

# Inicializar el cliente de Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Función para traducir texto usando DeepL
def translate_text(text, target_lang):
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": target_lang
    }
    response = requests.post(DEEPL_API_URL, data=params)
    if response.status_code == 200:
        return response.json()["translations"][0]["text"]
    else:
        print(f"Error en la traducción: {response.status_code}")
        return None

# Evento cuando el bot está listo
@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')

# Evento cuando se recibe un mensaje
@client.event
async def on_message(message):
    # Ignorar mensajes del propio bot
    if message.author == client.user:
        return

    # Traducir automáticamente
    if message.content:
        # Primero, intentar traducir de español a italiano
        translated_text = translate_text(message.content, "IT")
        if translated_text and translated_text.lower() != message.content.lower():
            await message.channel.send(f"🇮🇹 **Traducción al italiano:** {translated_text}")
        else:
            # Si no se tradujo a italiano, intentar traducir de italiano a español
            translated_text = translate_text(message.content, "ES")
            if translated_text and translated_text.lower() != message.content.lower():
                await message.channel.send(f"🇪🇸 **Traducción al español:** {translated_text}")
            else:
                print("No se pudo detectar el idioma o el mensaje no requiere traducción.")

# Iniciar el bot
client.run(DISCORD_TOKEN)