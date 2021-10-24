# -*- coding: utf-8 -*-
import datetime
import uuid
from collections import OrderedDict
from decimal import Decimal

from fastapi import FastAPI, HTTPException

from b2c2.common.models import (
    OrderRequest,
    OrderResponse,
    RFQRequest,
    RFQResponse,
    Trade,
)
from b2c2.mockserver.defaults import BALANCE, INSTRUMENT_PRICES
from b2c2.mockserver.settings import VALIDITY_WINDOW
from b2c2.mockserver.utils import (
    get_base_balance,
    get_pair,
    get_price,
    get_quote_balance,
)

app = FastAPI()

balance = BALANCE
orders_by_id = OrderedDict()  # type: OrderedDict[str, OrderResponse]
orders_by_client_order_id = OrderedDict()  # type: OrderedDict[str, OrderResponse]
trades_by_id = OrderedDict()  # type: OrderedDict[str, Trade]


@app.get("/balance/")
def get_balance():
    return dict([(base, str(value)) for base, value in balance.items()])


@app.get("/instruments/")
def get_instruments():
    return [dict(name=instrument_name) for instrument_name in INSTRUMENT_PRICES.keys()]


@app.post("/request_for_quote/")
def get_request_for_quote(rfq: RFQRequest):
    # Check average price for the instrument
    price = get_price(rfq.instrument)
    # Set the dates for creation and validity.
    created = datetime.datetime.now()
    valid_until = created + datetime.timedelta(seconds=VALIDITY_WINDOW)

    return RFQResponse(
        valid_until=valid_until,
        rfq_id=str(uuid.uuid4()),
        client_rfq_id=rfq.client_rfq_id,
        quantity=rfq.quantity,
        side=rfq.side,
        instrument=rfq.instrument,
        price=price,
        created=created,
    )


@app.get("/order/{order_id}/")
def get_order(order_id: str):
    order = orders_by_id.get(order_id)
    if not order:
        order = orders_by_client_order_id.get(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.get("/trade/{trade_id}/")
def get_trade(trade_id: str):
    trade = trades_by_id.get(trade_id)
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    return trade


@app.get("/order/")
def get_orders():
    return list(orders_by_id.values())


@app.get("/trade/")
def get_trades():
    return list(trades_by_id.values())


@app.get("/ledger/")
def get_ledgers():
    # TODO: Implement
    pass


@app.post("/order/")
def post_order(order_request: OrderRequest):
    if order_request.client_order_id in orders_by_client_order_id.keys():
        raise HTTPException(
            status_code=400, detail="An order with this id already exists"
        )
    order_id = str(uuid.uuid4())
    price = get_price(order_request.instrument)
    total_amount = price * order_request.quantity
    order_created = datetime.datetime.now()
    base_balance = get_base_balance(balance, order_request.instrument)
    quote_balance = get_quote_balance(balance, order_request.instrument)

    if (
        order_request.side == "buy"
        and price / Decimal(order_request.price) > 1.11
        or quote_balance < total_amount
    ) or (order_request.side == "sell" and base_balance < order_request.quantity):
        # reject it. price is way too low or not sufficient balance.
        executed_price = None
        trades = []
    else:
        base, quote = get_pair(order_request.instrument)
        if order_request.side == "buy":
            balance[quote] -= total_amount
            balance[base] += order_request.quantity
        elif order_request.side == "sell":
            balance[quote] += total_amount
            balance[base] -= order_request.quantity

        executed_price = price

        trades = [
            Trade(
                instrument=order_request.instrument,
                trade_id=str(uuid.uuid4()),
                origin="rest",
                rfq_id=None,
                created=order_created,  # use multiple created if multiple trades
                price=executed_price,
                quantity=order_request.quantity,
                order=order_id,
                side=order_request.side,
                executing_unit=order_request.executing_unit,
            )
        ]

    response = OrderResponse(
        order_id=order_id,
        client_order_id=order_request.client_order_id,
        quantity=order_request.quantity,
        side=order_request.side,
        instrument=order_request.instrument,
        price=order_request.price,
        executed_price=executed_price,  # TODO: add some deviation
        executing_unit=order_request.executing_unit,
        trades=trades,
        created=order_created,
    )

    orders_by_id[response.order_id] = response
    orders_by_client_order_id[response.client_order_id] = response
    for trade in trades:
        trades_by_id[trade.trade_id] = trade
    return response
