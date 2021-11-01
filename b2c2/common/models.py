# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Tuple

from pydantic import BaseModel
from rich import print

from b2c2.common.constants import CURRENCIES, FIAT_CURRENCIES


class Side(str, Enum):
    buy = "buy"
    sell = "sell"


class Instrument(BaseModel):
    name: str

    def _get_currencies(self):
        return CURRENCIES

    def _is_currency(self, currency):
        return currency in self._get_currencies()

    def pair(self) -> Tuple[str, str]:
        """
        Extracts (base, quote) from the instrument name (Ex: "BTCUSDT")
        If can not validate the instrument, raises Exception.
        :return: (base, quote) - Ex: ("BTC", "USDT")
        """
        instrument = self.name.split(".")[0]
        if len(instrument) == 6:
            return instrument[:3], instrument[3:]
        elif len(instrument) == 7:
            if self._is_currency(instrument[:3]) and self._is_currency(instrument[3:]):
                # BTCUSDT
                return instrument[:3], instrument[3:]
            elif self._is_currency(instrument[:4]) and self._is_currency(
                instrument[4:]
            ):
                # USDTUSD
                return instrument[:4], instrument[4:]

        raise Exception("Unexpected instrument: {}".format(instrument))

    @property
    def base(self):
        return self.pair()[0]

    @property
    def quote(self):
        return self.pair()[1]

    @property
    def type(self):
        return self.name.split(".")[-1]


class Balance(dict):
    def __setitem__(self, key, value):
        super(Balance, self).__setitem__(key, Decimal(value))

    def display(self):
        print("=" * 20 + " Balances " + "=" * 20)
        for key, value in self.items():
            value = Decimal(value)
            if key in FIAT_CURRENCIES:
                print(f"[bold green]{key:3s}[/bold green]: {value:>16.2f}")
            else:
                print(f"[bold green]{key:3s}[/bold green]: {value:>22.8f}")


class RFQRequest(BaseModel):
    instrument: str  # Instrument as given by the /instruments/ endpoint.
    side: Side  # Either ‘buy’ or ‘sell’.
    quantity: Decimal  # Quantity in base currency (maximum 4 decimals).
    client_rfq_id: str  # A universally unique identifier that will be returned to you if the request succeeds.


class RFQResponse(BaseModel):
    valid_until: datetime.datetime
    rfq_id: str
    client_rfq_id: str  # A universally unique identifier that will be returned to you if the request succeeds.
    quantity: Decimal  # Quantity in base currency (maximum 4 decimals).
    side: Side  # Either ‘buy’ or ‘sell’.
    instrument: str  # Instrument as given by the /instruments/ endpoint.
    price: Decimal
    created: datetime.datetime

    def display(self):
        print("=" * 20 + " RFQ Response " + "=" * 20)
        for key, value in self.__dict__.items():
            key = key.replace("_", " ").capitalize()
            print(f"[bold green]{key:25s}[/bold green]: {value}")

    def has_expired(self):
        return self.valid_until <= datetime.datetime.now()

    @staticmethod
    def sample_value():
        return {
            "valid_until": "2017-01-01T19:45:22.025464Z",
            "rfq_id": "d4e41399-e7a1-4576-9b46-349420040e1a",
            "client_rfq_id": "149dc3e7-4e30-4e1a-bb9c-9c30bd8f5ec7",
            "quantity": "1.0000000000",
            "side": "buy",
            "instrument": "BTCUSD.SPOT",
            "price": "700.00000000",
            "created": "2018-02-06T16:07:50.122206Z",
        }


class OrderRequest(BaseModel):
    instrument: str
    side: Side
    quantity: Decimal
    client_order_id: str
    price: Decimal
    order_type: str
    valid_until: datetime.datetime
    executing_unit: Optional[str]
    force_open: Optional[bool]
    acceptable_slippage_in_basis_points: Optional[str]

    def dict(self, *args, **kwargs):
        d = super(OrderRequest, self).dict()
        d["price"] = str(d["price"])
        d["quantity"] = str(d["quantity"])
        d["valid_until"] = d["valid_until"].strftime("%Y-%m-%dT%H:%M:%S")
        return d


class Trade(BaseModel):
    instrument: str
    trade_id: str
    origin: str
    rfq_id: Optional[str]
    created: datetime.datetime
    price: Decimal
    quantity: Decimal
    order: str
    side: Side
    executing_unit: str

    def display(self):
        color = "yellow"
        dashes = f"[bold {color}]" + "=" * 10 + f"[/bold {color}]"
        print(dashes + f" [bold {color}]Trade {self.trade_id}[/bold {color}] " + dashes)
        for key, value in self.__dict__.items():
            key = key.replace("_", " ").capitalize()
            print(f"[bold green]{key:25s}[/bold green]: {value}")


class OrderResponse(BaseModel):
    order_id: str
    client_order_id: str
    quantity: Decimal
    side: Side
    instrument: str
    price: Decimal
    executed_price: Optional[Decimal]
    executing_unit: str
    trades: List[Trade]
    created: datetime.datetime

    @property
    def is_rejected(self):
        return self.executed_price is None

    def display(self):
        color = "red" if self.is_rejected else "green"
        dashes = f"[bold {color}]" + "=" * 20 + f"[/bold {color}]"
        print(dashes + f" [bold {color}]Order Details[/bold {color}] " + dashes)
        order_dict = self.__dict__.copy()
        trades = order_dict.pop("trades")
        for key, value in order_dict.items():
            key = key.replace("_", " ").capitalize()
            print(f"[bold {color}]{key:25s}[/bold {color}]: {value}")
        if trades:
            for trade in trades:
                trade.display()


class Ledger(BaseModel):
    transaction_id: str
    created: datetime.datetime
    reference: str
    currency: str
    amount: Decimal
    type: str
    group: str
