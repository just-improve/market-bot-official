import time
import urllib.parse
from typing import Optional, Dict, Any, List

# gdzie sprawdzić jaki packa
from requests import Request, Session, Response
import hmac


class FtxClientWJ:
    _ENDPOINT = 'https://ftx.com/api/'
    print("ftx_methods")

    # getCandles
    def get_historical_prices(
            self, market: str, resolution: int = 300, start_time: float = None,
            end_time: float = None
    ) -> List[dict]:
        return self._get(f'markets/{market}/candles', {
            'resolution': resolution,
            'start_time': start_time,
            'end_time': end_time
        })
        # pobiera maksymalnie 500 rekordó - jak Piotrek to zmieniał?

    def get_funding_rates(self, future: str = None, start_time: float = None, end_time: float = None) -> List[dict]:
        return self._get('funding_rates', {
            'future': future,
            'start_time': start_time,
            'end_time': end_time
        })

    def get_all_futures(self) -> List[dict]:
        return self._get('futures')

    def get_future(self, future_name: str = None) -> dict:
        return self._get(f'futures/{future_name}')

    def get_markets(self) -> List[dict]:
        return self._get('markets')

    def get_orderbook(self, market: str, depth: int = None) -> dict:
        return self._get(f'markets/{market}/orderbook', {'depth': depth})

    def get_trades(self, market: str, start_time: float = None, end_time: float = None) -> dict:
        return self._get(f'markets/{market}/trades', {'start_time': start_time, 'end_time': end_time})

    # get_last_candle
    def get_last_historical_prices(self, market: str, resolution: int = 300) -> List[dict]:
        return self._get(f'markets/{market}/candles/last', {'resolution': resolution})

    # pobiera tylko jedną wartość na pewno się może przydać bo pobiera funding rate i openInterests - więc mogę zapisywać do tablicy godzinowej
    # te dane i później porównywać
    def get_fut_vol_fund_oi_last(self, future_name: str) -> dict:
        return self._get(f'futures/{future_name}/stats')

        # get_index_candles
        def get_index_candles(
                self, market: str, resolution: int = 300, start_time: float = None,
                end_time: float = None
        ) -> List[dict]:
            return self._get(f'indexes/{market}/candles', {
                'resolution': resolution,
                'start_time': start_time,
                'end_time': end_time
            })

    # bardzo cenna metoda bo są bidy aski i lastTrade, price
    def get_market_general_info(self, market: str = None) -> Dict:
        return self._get(f'markets/{market}')

    # też pobiera tylko 500 rekordów
    def get_all_funding_rates(self, start_time: float = None, end_time: float = None, future: str = None) -> List[dict]:
        return self._get('funding_rates', {
            'start_time': start_time,
            'end_time': end_time,
            'future': future
        })

    def __init__(self, api_key=None, api_secret=None, subaccount_name=None) -> None:
        self._session = Session()
        self._api_key = api_key
        self._api_secret = api_secret
        self._subaccount_name = subaccount_name

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('GET', path, params=params)

    def _post(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('POST', path, json=params)

    def _delete(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('DELETE', path, json=params)

    def _request(self, method: str, path: str, **kwargs) -> Any:
        request = Request(method, self._ENDPOINT + path, **kwargs)
        response = self._session.send(request.prepare())
        return self._process_response(response)

    def _process_response(self, response: Response) -> Any:
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        else:
            if not data['success']:
                raise Exception(data['error'])
            return data['result']
