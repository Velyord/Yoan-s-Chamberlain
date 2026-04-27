import os
import json
from domain import ConfigurationError

class EnvironmentConfig:
    def __init__(self):
        self.bot_token = self._get_required_var("BOT_TOKEN")
        self.chat_id = int(self._get_required_var("CHAT_ID"))
        self.spreadsheet_name = self._get_required_var("SPREADSHEET_NAME")
        self.city_name = self._get_required_var("CITY_NAME")
        self.latitude = float(self._get_required_var("LATITUDE"))
        self.longitude = float(self._get_required_var("LONGITUDE"))
        self.timezone = self._get_required_var("TIMEZONE")
        self.google_credentials = self._parse_json_var("GOOGLE_CREDENTIALS_JSON")

    def _get_required_var(self, key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ConfigurationError(f"Missing required environment variable: {key}")
        return value

    def _parse_json_var(self, key: str) -> dict:
        raw_value = self._get_required_var(key)
        try:
            return json.loads(raw_value)
        except json.JSONDecodeError as error:
            raise ConfigurationError(f"Environment variable {key} contains invalid JSON.") from error