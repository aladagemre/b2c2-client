# -*- coding: utf-8 -*-
import random
from decimal import Decimal

from fastapi import HTTPException

from b2c2.mockserver.defaults import INSTRUMENT_PRICES


def get_instrument_type(instrument):
    pair, instrument_type = instrument.split(".")
    return instrument_type


def get_pair(instrument):
    pair, instrument_type = instrument.split(".")
    base, quote = pair[:3], pair[3:]
    return base, quote


def get_base(instrument):
    base, quote = get_pair(instrument)
    return base


def get_quote(instrument):
    base, quote = get_pair(instrument)
    return quote


def get_quote_balance(balance, instrument):
    quote = get_quote(instrument)
    return balance.get(quote)


def get_base_balance(balance, instrument):
    base = get_base(instrument)
    return balance.get(base)


def get_price(instrument, fluctuation=(-1, 1)) -> Decimal:
    """Returns the price of the given instrument"""
    price = INSTRUMENT_PRICES.get(instrument)
    if not price:
        raise HTTPException(status_code=400, detail="No such instrument found")

    if fluctuation:
        # Add some fluctuation to the average price
        fluctuation_lower, fluctuation_higher = fluctuation
        fluctuation_percent = (
            random.randrange(fluctuation_lower * 100, fluctuation_higher * 100) / 10000
        )
        price *= Decimal(1 + fluctuation_percent)
    return price
