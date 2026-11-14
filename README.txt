ZYVARQO ASSISTANT — STARTER BOT

Included:
- /start welcome and interactive menu
- User registration stored in SQLite
- Marketplace, Services, Account, Orders, Referrals and Support menu buttons
- Support messages forwarded to the admin when ADMIN_ID is configured
- /admin user-count summary for the configured administrator

IMPORTANT SECURITY:
1. Do not put your Telegram bot token in bot.py, README, GitHub, or screenshots.
2. Since the token was visible in your earlier screenshot, revoke it in BotFather first.
3. Save the replacement token only as the TELEGRAM_BOT_TOKEN environment variable on your hosting provider.
4. Set ADMIN_ID to your own numeric Telegram user ID before enabling admin features.
5. This starter does not accept deposits, process withdrawals, hold funds, or promise investment returns.

RUN LOCALLY:
1. Install Python 3.10 or newer.
2. Run: pip install -r requirements.txt
3. Set environment variables TELEGRAM_BOT_TOKEN and optionally ADMIN_ID.
4. Run: python bot.py

DEPLOYMENT:
Run this as a persistent worker/background process on a hosting provider.
The start command is: python bot.py
Add TELEGRAM_BOT_TOKEN and ADMIN_ID as private environment variables in the host dashboard.
Do not commit secrets to GitHub.
