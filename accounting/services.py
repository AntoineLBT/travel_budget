from decimal import Decimal
from typing import Any, Dict

from requests import get


class CurrencyRatesGetter:
    """
    API DOC : https://frankfurter.dev/
    """

    @staticmethod
    def get_exchange_rate(from_currency: str, to_currency: str) -> Dict[str, Any]:
        return get(
            f"https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}"
        )

    @staticmethod
    def convert_amount(
        from_currency: str, to_currency: str, amount: Decimal
    ) -> Decimal:
        rate_response = get(
            f"https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}"
        )
        current_rate = rate_response.json()["rates"][to_currency]
        return amount * Decimal(current_rate)
