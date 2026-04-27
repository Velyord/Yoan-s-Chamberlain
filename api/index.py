import asyncio
import datetime
import pytz
from flask import Flask, request
from telegram import Update, Bot

from config import EnvironmentConfig
from infrastructure import OpenMeteoForecaster, GoogleSheetsLedger, TelegramSender
from use_cases import InitiateQuestionnaireUseCase, AdvanceQuestionnaireUseCase, FinalizeRecordUseCase

app = Flask(__name__)
config = EnvironmentConfig()

forecaster = OpenMeteoForecaster(config.latitude, config.longitude, config.timezone)
ledger = GoogleSheetsLedger(config.spreadsheet_name, "👕", config.google_credentials)
message_sender = TelegramSender(config.bot_token, config.chat_id)

initiate_use_case = InitiateQuestionnaireUseCase(message_sender)
advance_use_case = AdvanceQuestionnaireUseCase(message_sender)
finalize_use_case = FinalizeRecordUseCase(ledger, forecaster, message_sender, config.city_name)


@app.route('/api/cron', methods=['GET'])
def run_daily_cron():
    local_tz = pytz.timezone(config.timezone)
    now_local = datetime.datetime.now(local_tz)
    
    if now_local.hour == 20:
        asyncio.run(initiate_use_case.execute())
        return "Message sent!", 200
        
    return "Not the right time.", 200

@app.route('/api/webhook', methods=['POST'])
def telegram_webhook():
    update_data = request.get_json(force=True)
    asyncio.run(_handle_webhook_payload(update_data))
    return "OK", 200

async def _handle_webhook_payload(update_data: dict):
    dummy_bot = Bot(token=config.bot_token)
    update = Update.de_json(update_data, dummy_bot)
    
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        
        parts_count = len(query.data.split("_"))
        if parts_count <= 4:
            await advance_use_case.execute(query.message.message_id, query.data)
        else:
            today = datetime.datetime.now(pytz.timezone(config.timezone)).date()
            await finalize_use_case.execute(query.message.message_id, query.data, today)