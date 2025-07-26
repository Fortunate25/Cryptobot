from keep_alive import keep_alive
keep_alive()

import os
import re
from dotenv import load_dotenv
from telethon import TelegramClient, events

# Load credentials
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
session_name = "cryptobot"

# Initialize the Telegram client using bot token
client = TelegramClient(session_name, api_id, api_hash).start(bot_token=bot_token)

# Channels to monitor
SOURCE_CHANNELS = ['CoinSauceCrypto', 'cryptothedoggy', 'WatcherGuru', 'onchainalphatrench', 'whaleBuyBotFree', 'memecoinmil']
# Your own channel to post to
TARGET_CHANNEL = 'cryptofactsx'

# Keywords to filter
KEYWORDS = ['crypto', 'btc', 'sol', 'eth', 'pump', 'stablecoin', 'xrp', 'Bitcoin', 'Ethereum', 'Solana', 'XRP', 'Cryptocurrency', 'buys', '200%', '100%', '300%', '400%', '500%', '600%', '1000%', '2000%', 'Hit', 'Now', 'buy', 'sell', 'trade', 'trading', 'profit', 'loss', 'alert', 'news', 'analysis', 'prediction', 'forecast', 'First hit', 'alerted', '$btc', '$sol', '$eth', '$xrp', '$bitcoin', 'Crypto', 'cryptocurrency', 'Breaking'
]

ALLOWED_DOMAINS = ['x.com', 't.me/phanes_bot']

def clean_message(message):
    if not message:
        return ""

    message = re.sub(
        r'https?://[^\s)]+',
        lambda m: m.group(0) if any(domain in m.group(0) for domain in ALLOWED_DOMAINS) else '',
        message
    )

    message = re.sub(r'@\w+', '', message)
    message = re.sub(r'(https?:\/\/)?(t\.me|bit\.ly|tinyurl\.com|linktr\.ee|coinmarketcap\.com|axiom\.trade|cointelegraph\.com)\/\S+', '', message)

    promo_keywords = [
        'Join our channel', 'Follow us', 'Don’t miss', 'Turn on notifications', '💰 Sol Payment', '💳 Card Payment', '💰 Start from just $49.99', 'Community of Trenchers.', 'Get started from $49.99'
    ]
    for phrase in promo_keywords:
        message = message.replace(phrase, '')

    return message.strip()

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    message_text = event.raw_text

    has_keyword = any(keyword.lower() in message_text.lower() for keyword in KEYWORDS)
    has_contract = re.search(r'`[1-9A-HJ-NP-Za-km-z]{32,}`', message_text)

    if (has_keyword or has_contract) and len(message_text.split()) > 1:
        cleaned_text = clean_message(message_text)

        if has_contract:
            cleaned_text = message_text

        if event.media:
            await client.send_file(TARGET_CHANNEL, file=event.media, caption=cleaned_text or None)
        else:
            await client.send_message(TARGET_CHANNEL, cleaned_text)

print("🤖 Bot is running...")
client.run_until_disconnected()
