import asyncio
import datetime
import pytz
from flask import Flask, request
from telegram import Update, Bot
from telegram.error import BadRequest

from config import EnvironmentConfig
from infrastructure import OpenMeteoForecaster, GoogleSheetsLedger, TelegramSender
from use_cases import InitiateQuestionnaireUseCase, AdvanceQuestionnaireUseCase, FinalizeRecordUseCase

app = Flask(__name__)

def get_use_cases():
    config = EnvironmentConfig()
    forecaster = OpenMeteoForecaster(config.latitude, config.longitude, config.timezone)
    ledger = GoogleSheetsLedger(config.spreadsheet_name, "👕", config.google_credentials)
    message_sender = TelegramSender(config.bot_token, config.chat_id)

    return (
        InitiateQuestionnaireUseCase(message_sender),
        AdvanceQuestionnaireUseCase(message_sender),
        FinalizeRecordUseCase(ledger, forecaster, message_sender, config.city_name),
        config
    )

@app.route('/api/cron', methods=['GET'])
def run_daily_cron():
    initiate_uc, _, _, _ = get_use_cases()
    asyncio.run(initiate_uc.execute())
    return "Message sent!", 200

@app.route('/api/webhook', methods=['POST'])
def telegram_webhook():
    update_data = request.get_json(force=True)
    asyncio.run(_handle_webhook_payload(update_data))
    return "OK", 200

async def _handle_webhook_payload(update_data: dict):
    initiate_uc, advance_uc, finalize_uc, config = get_use_cases()
    dummy_bot = Bot(token=config.bot_token)
    update = Update.de_json(update_data, dummy_bot)
    
    if update.callback_query:
        query = update.callback_query
        try:
            await query.answer()
        except BadRequest:
            pass # Ignore "Query is too old" errors
        
        parts_count = len(query.data.split("_"))
        if parts_count <= 4:
            await advance_uc.execute(query.message.message_id, query.data)
        else:
            today = datetime.datetime.now(pytz.timezone(config.timezone)).date()
            await finalize_uc.execute(query.message.message_id, query.data, today)