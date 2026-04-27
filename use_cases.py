from datetime import date
from domain import (
    WeatherForecaster, WardrobeLedger, MessageSender, 
    DailyAttire, WARDROBE_CHOICES
)

class InitiateQuestionnaireUseCase:
    def __init__(self, message_sender: MessageSender):
        self.message_sender = message_sender

    async def execute(self) -> None:
        prompt = (
            "Forgive my intrusion, my Lord. I hope I do not disturb your rest. "
            "Might your excellence be so kind as to share: what was the proper attire for your noble brow this day?"
        )
        await self.message_sender.send_message(prompt, WARDROBE_CHOICES["head"])

class AdvanceQuestionnaireUseCase:
    def __init__(self, message_sender: MessageSender):
        self.message_sender = message_sender

    async def execute(self, message_id: int, callback_data: str) -> None:
        parts_count = len(callback_data.split("_"))
        
        if parts_count == 2:
            await self._ask_torso(message_id, callback_data)
        elif parts_count == 3:
            await self._ask_legs(message_id, callback_data)
        elif parts_count == 4:
            await self._ask_jacket(message_id, callback_data)

    async def _ask_torso(self, message_id: int, path: str) -> None:
        text = "A wise choice, Sire. And pray tell, what garment proved most suitable for your majestic torso?"
        await self.message_sender.edit_message(message_id, text, WARDROBE_CHOICES["torso"], path)

    async def _ask_legs(self, message_id: int, path: str) -> None:
        text = "Splendid, my King. Might I also inquire: what was the correct choice for your stately limbs today?"
        await self.message_sender.edit_message(message_id, text, WARDROBE_CHOICES["legs"], path)

    async def _ask_jacket(self, message_id: int, path: str) -> None:
        text = "Almost finished, Your Majesty. One final detail: which outer regalia was most fitting for the day's climate?"
        await self.message_sender.edit_message(message_id, text, WARDROBE_CHOICES["jacket"], path)

class FinalizeRecordUseCase:
    def __init__(self, ledger: WardrobeLedger, forecaster: WeatherForecaster, sender: MessageSender, city: str):
        self.ledger = ledger
        self.forecaster = forecaster
        self.sender = sender
        self.city = city

    async def execute(self, message_id: int, callback_data: str, today: date) -> None:
        await self._acknowledge_completion(message_id)
        
        try:
            attire = self._parse_attire_from_callback(callback_data)
            await self._process_ledger_and_forecast(attire, today)
        except Exception as error:
            await self.sender.send_message(f"Alas! An error occurred: {str(error)}")

    async def _acknowledge_completion(self, message_id: int) -> None:
        text = "Your wisdom is noted! I shall update the Royal Ledger and consult the heavens for tomorrow's omens..."
        await self.sender.finalize_message(message_id, text)

    def _parse_attire_from_callback(self, callback_data: str) -> DailyAttire:
        parts = callback_data.split("_")
        head_idx, torso_idx, legs_idx, jacket_idx = map(int, parts[1:])
        
        return DailyAttire(
            headwear=WARDROBE_CHOICES["head"][head_idx],
            torso=WARDROBE_CHOICES["torso"][torso_idx],
            legs=WARDROBE_CHOICES["legs"][legs_idx],
            jacket=WARDROBE_CHOICES["jacket"][jacket_idx]
        )

    async def _process_ledger_and_forecast(self, attire: DailyAttire, today: date) -> None:
        min_temp, max_temp = self.ledger.fetch_current_temperatures()
        self.ledger.record_attire(attire, min_temp, max_temp, today)
        
        forecast = self.forecaster.fetch_tomorrow_forecast()
        self.ledger.update_forecast(forecast)
        
        recommendation = self.ledger.fetch_recommendation()
        report = self._format_report(forecast, recommendation)
        
        await self.sender.send_message(report)

    def _format_report(self, forecast, recommendation) -> str:
        return (
            f"✨ **The Royal Ledger has been updated, my Lord!**\n\n"
            f"I have peered into the horizon for tomorrow's omens in {self.city}:\n"
            f"❄️ **Min Temp:** {forecast.min_temperature}°C\n"
            f"🔥 **Max Temp:** {forecast.max_temperature}°C\n\n"
            f"📜 **According to the ancient scrolls, your ensemble shall be:**\n"
            f"👑 **Brow:** \t{recommendation.headwear}\n"
            f"🛡️ **Torso:** \t{recommendation.torso}\n"
            f"👖 **Limbs:** \t{recommendation.legs}\n"
            f"🧥 **Mantle:** \t{recommendation.jacket}\n\n"
        )