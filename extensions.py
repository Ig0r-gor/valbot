import requests
import json
from config import money

class APIException(Exception):
    pass

class MoneyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Перевод одинаковых валют не выполняется: {base} в {quote}')

        try:
            quote_ticker = money[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать значение: {quote}')

        try:
            base_ticker = money[base]
        except KeyError:
            raise APIException(f'Не удалось обработать значение: {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество:  {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = (json.loads(r.content)[money[base]])*amount

        return total_base