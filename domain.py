from dataclasses import dataclass
from abc import ABC, abstractmethod
from datetime import date
from typing import List

class ConfigurationError(Exception): pass
class WeatherFetchError(Exception): pass
class LedgerError(Exception): pass
class MessagingError(Exception): pass

# Domain Constants
WARDROBE_CHOICES = {
    "head":["none", "winter hat"],
    "torso":["short-sleeved shirt / t-shirt", "light shirt / top", "warm shirt / top", "winter top"],
    "legs":["short pants", "light pants", "warm pants", "warm pants with tights"],
    "jacket":["none", "suit jacket / top shirt", "leather jacket", "winter jacket"]
}

@dataclass(frozen=True)
class WeatherForecast:
    min_temperature: int
    max_temperature: int

@dataclass(frozen=True)
class DailyAttire:
    headwear: str
    torso: str
    legs: str
    jacket: str

@dataclass(frozen=True)
class WardrobeRecommendation:
    headwear: str
    torso: str
    legs: str
    jacket: str

class WeatherForecaster(ABC):
    @abstractmethod
    def fetch_tomorrow_forecast(self) -> WeatherForecast:
        pass

class WardrobeLedger(ABC):
    @abstractmethod
    def fetch_current_temperatures(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def record_attire(self, attire: DailyAttire, min_temp: int, max_temp: int, today: date) -> None:
        pass

    @abstractmethod
    def update_forecast(self, forecast: WeatherForecast) -> None:
        pass

    @abstractmethod
    def fetch_recommendation(self) -> WardrobeRecommendation:
        pass

class MessageSender(ABC):
    @abstractmethod
    async def send_message(self, text: str, options: List[str] = None) -> None:
        pass

    @abstractmethod
    async def edit_message(self, message_id: int, text: str, options: List[str], current_path: str) -> None:
        pass
        
    @abstractmethod
    async def finalize_message(self, message_id: int, text: str) -> None:
        pass