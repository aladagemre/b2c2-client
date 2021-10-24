# -*- coding: utf-8 -*-
from decimal import Decimal, getcontext

getcontext().prec = 6

BALANCE = {
    "USD": Decimal(400000),
    "BTC": Decimal(0),
    "JPY": Decimal(0),
    "GBP": Decimal(0),
    "ETH": Decimal(0),
    "EUR": Decimal(0),
    "CAD": Decimal(0),
    "LTC": Decimal(0),
    "XRP": Decimal(0),
    "BCH": Decimal(0),
}


INSTRUMENT_PRICES = {
    "BTCUSD.CFD": Decimal("57497.30"),
    "BTCUSD.SPOT": Decimal("57497.30"),
    "BTCEUR.SPOT": Decimal("49575.32"),
    "BTCGBP.SPOT": Decimal("42045.56"),
    "ETHBTC.SPOT": Decimal("0.065388"),
    "ETHUSD.SPOT": Decimal("3758.64"),
    "LTCUSD.SPOT": Decimal("179.60"),
    "XRPUSD.SPOT": Decimal("1.12906"),
    "BCHUSD.SPOT": Decimal("595.72"),
}


INSTRUMENTS = [
    {"name": "BTCUSD.CFD", "price": Decimal("57497.30")},
    {
        "name": "BTCUSD.SPOT",
        "price": Decimal("57497.30"),
    },
    {
        "name": "BTCEUR.SPOT",
        "price": Decimal("49575.32"),
    },
    {
        "name": "BTCGBP.SPOT",
        "price": Decimal("42045.56"),
    },
    {
        "name": "ETHBTC.SPOT",
        "price": Decimal("0.065388"),
    },
    {
        "name": "ETHUSD.SPOT",
        "price": Decimal("3758.64"),
    },
    {
        "name": "LTCUSD.SPOT",
        "price": Decimal("179.60"),
    },
    {
        "name": "XRPUSD.SPOT",
        "price": Decimal("1.12906"),
    },
    {
        "name": "BCHUSD.SPOT",
        "price": Decimal("595.72"),
    },
]
