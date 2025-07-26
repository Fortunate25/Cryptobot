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

# Initialize client
client = TelegramClient(session_name, api_id, api_hash).start(bot_token=bot_token)

# Source & target channels
SOURCE_CHANNELS = ['CoinSauceCrypto', 'cryptothedoggy', 'WatcherGuru', 'onchainalphatrench', 'whaleBuyBotFree', 'memecoinmil']
TARGET_CHANNEL = 'cryptofactsx'

# Lists
KEYWORDS = [
    'crypto', 'btc', 'sol', 'eth', 'pump', 'stablecoin', 'xrp', 'Bitcoin', 'Ethereum', 'Solana', 'XRP',
    'Cryptocurrency', 'buys', '200%', '100%', '300%', '400%', '500%', '600%', '1000%', '2000%', 'Hit', 'Now',
    'buy', 'sell', 'trade', 'trading', 'profit', 'loss', 'alert', 'news', 'analysis', 'prediction', 'forecast',
    'First hit', 'alerted', '$btc', '$sol', '$eth', '$xrp', '$bitcoin', 'Crypto', 'cryptocurrency', 'Breaking'
]

# Promo patterns to block
PROMO_PATTERNS = [r'follow\s+us', r'don[’\'`]t\s+miss', r'turn\s+on\s+notifications']


PROMO_KEYWORDS = [
    'Join our channel', 'Follow us', 'Don’t miss', 'Turn on notifications', '💰 Sol Payment', '💳 Card Payment', '💰 Start from just $49.99', 'Community of Trenchers.', 'Get started from $49.99'
]

# Clean and strip message
def clean_message(message):
    if not message:
        return ""


    # Remove @mentions and blocked domains
    message = re.sub(r'@\w+', '', message)
    message = re.sub(r'(https?:\/\/)?(t\.me|bit\.ly|tinyurl\.com|linktr\.ee|coinmarketcap\.com|axiom\.trade|cointelegraph\.com)\/\S+', '', message)

    # Remove soft promo keywords (but not full message)
    for keyword in PROMO_KEYWORDS:
        message = re.sub(re.escape(keyword), '', message, flags=re.IGNORECASE)

    return message.strip()

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    message_text = event.raw_text

    # 1. Block message if any full-block promo patterns match
    for pattern in PROMO_PATTERNS:
        if re.search(pattern, message_text, re.IGNORECASE):
            return

    # 2. Allow only if it has a keyword or a contract
    has_keyword = any(k.lower() in message_text.lower() for k in KEYWORDS)
    contract_match = re.search(r'\b[1-9A-HJ-NP-Za-km-z]{32,}\b', message_text)

    if not has_keyword and not contract_match:
        return

    # 3. Clean the message
    cleaned_text = clean_message(message_text)

    # 4. Wrap contract address in backticks
    if contract_match:
        address = contract_match.group(0)
        if f'`{address}`' not in cleaned_text:
            cleaned_text = cleaned_text.replace(address, f'`{address}`')

    # 5. Send message with or without media
    if event.media:
        await client.send_file(TARGET_CHANNEL, file=event.media, caption=cleaned_text or None)
    else:
        await client.send_message(TARGET_CHANNEL, cleaned_text)

print("✅ Bot started successfully. Listening for messages...")
client.run_until_disconnected()

