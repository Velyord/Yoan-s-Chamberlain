import requests
import gspread
from datetime import date
from typing import List
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import BadRequest

from domain import (
    WeatherForecaster, WardrobeLedger, MessageSender,
    WeatherForecast, DailyAttire, WardrobeRecommendation,
    WeatherFetchError, LedgerError, MessagingError
)

class OpenMeteoForecaster(WeatherForecaster):
    def __init__(self, latitude: float, longitude: float, timezone: str):
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone.replace("/", "%2F")

    def fetch_tomorrow_forecast(self) -> WeatherForecast:
        url = self._build_api_url()
        response = requests.get(url)
        self._ensure_successful_response(response)
        return self._parse_forecast_data(response.json())

    def _build_api_url(self) -> str:
        return (f"https://api.open-meteo.com/v1/forecast"
                f"?latitude={self.latitude}&longitude={self.longitude}"
                f"&daily=temperature_2m_max,temperature_2m_min&timezone={self.timezone}")

    def _ensure_successful_response(self, response: requests.Response) -> None:
        if response.status_code != 200:
            raise WeatherFetchError("Failed to retrieve weather data from Open-Meteo")

    def _parse_forecast_data(self, data: dict) -> WeatherForecast:
        try:
            return WeatherForecast(
                min_temperature=round(data['daily']['temperature_2m_min'][1]),
                max_temperature=round(data['daily']['temperature_2m_max'][1])
            )
        except KeyError as error:
            raise WeatherFetchError("Malformed weather data received") from error

class GoogleSheetsLedger(WardrobeLedger):
    def __init__(self, spreadsheet_name: str, worksheet_name: str, credentials_dict: dict):
        try:
            client = gspread.service_account_from_dict(credentials_dict)
            spreadsheet = client.open(spreadsheet_name)
            self.worksheet = spreadsheet.worksheet(worksheet_name)
        except Exception as error:
            raise LedgerError("Failed to initialize Google Sheets connection") from error

    def fetch_current_temperatures(self) -> tuple[int, int]:
        return int(self.worksheet.acell('B1').value), int(self.worksheet.acell('C1').value)

    def record_attire(self, attire: DailyAttire, min_temp: int, max_temp: int, today: date) -> None:
        date_formula = f"=DATE({today.year};{today.month};{today.day})"
        new_row =[date_formula, min_temp, max_temp, attire.headwear, attire.torso, attire.legs, attire.jacket]
        self.worksheet.insert_row(new_row, index=3, value_input_option='USER_ENTERED')

    def update_forecast(self, forecast: WeatherForecast) -> None:
        self.worksheet.update_acell('B1', forecast.min_temperature)
        self.worksheet.update_acell('C1', forecast.max_temperature)

    def fetch_recommendation(self) -> WardrobeRecommendation:
        return WardrobeRecommendation(
            headwear=str(self.worksheet.acell('D1').value),
            torso=str(self.worksheet.acell('E1').value),
            legs=str(self.worksheet.acell('F1').value),
            jacket=str(self.worksheet.acell('G1').value)
        )

class TelegramSender(MessageSender):
    def __init__(self, bot_token: str, chat_id: int):
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id

    async def send_message(self, text: str, options: List[str] = None) -> None:
        try:
            reply_markup = self._build_keyboard(options, "q") if options else None
            await self.bot.send_message(chat_id=self.chat_id, text=text, reply_markup=reply_markup, parse_mode="Markdown")
        except Exception as error:
            print(f"Error sending message: {error}") # Log it instead of crashing
            raise MessagingError("Failed to send telegram message") from error

    async def edit_message(self, message_id: int, text: str, options: List[str], current_path: str) -> None:
        try:
            reply_markup = self._build_keyboard(options, current_path)
            await self.bot.edit_message_text(
                chat_id=self.chat_id, message_id=message_id, text=text, reply_markup=reply_markup
            )
        except BadRequest as e:
            if "Message is not modified" in str(e):
                return # Ignore this error, it's harmless
            raise MessagingError("Telegram BadRequest") from e
        except Exception as error:
            print(f"Error editing message: {error}")
            raise MessagingError("Failed to edit telegram message") from error

    async def finalize_message(self, message_id: int, text: str) -> None:
        try:
            await self.bot.edit_message_text(chat_id=self.chat_id, message_id=message_id, text=text)
        except BadRequest as e:
            if "Message is not modified" in str(e):
                return
            raise MessagingError("Telegram BadRequest") from e
        except Exception as error:
            raise MessagingError("Failed to finalize telegram message") from error

    def _build_keyboard(self, options: List[str], base_callback_data: str) -> InlineKeyboardMarkup:
        keyboard = []
        for index, option in enumerate(options):
            callback_data = f"{base_callback_data}_{index}"
            keyboard.append([InlineKeyboardButton(option, callback_data=callback_data)])
        return InlineKeyboardMarkup(keyboard)