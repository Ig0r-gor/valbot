import requests
import json
from config import money

class APIException(Exception):
    pass

class MoneyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f'Перевод одинаковых валют не выполняется: {base} в {quote}')

        try:
            base_ticker = money[base]
        except KeyError:
            raise APIException(f'Не удалось обработать значение: {base}')

        try:
            quote_ticker = money[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать значение: {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество:  {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = (json.loads(r.content)[money[quote]])*amount

        return total_base
