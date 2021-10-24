# -*- coding: utf-8 -*-
import logging

from PyInquirer import prompt
from rich.console import Console
from rich.table import Table

import b2c2.cli.questions as q
from b2c2.cli.apiclient import B2C2Client
from b2c2.cli.utils import (
    print_red,
    prompt_decimal,
    prompt_list,
    prompt_string,
    prompt_yes_no,
)
from b2c2.settings import API_URL, TOKEN

logger = logging.getLogger(__name__)
api_client = B2C2Client(token=TOKEN, api_url=API_URL)


def list_instruments():
    if not check_api_connection():
        return
    instruments = api_client.list_instruments()
    if not instruments:
        logger.error("Could not connect to the server. Please try again later.")
        return
    question = q.get_list_instruments_question(
        [instrument.name for instrument in instruments]
    )
    answer = prompt(question).get("instrument_action")
    if answer == "No Thanks":
        return
    request_for_quote(instrument_name=answer)


def request_for_quote(instrument_name=None):
    if not check_api_connection():
        return
    if not instrument_name:
        instrument_name = prompt_string("Instrument:")
    side = prompt_list("Side:", ["buy", "sell"])
    quantity = prompt_decimal("Quantity")

    # Make RFQ Request
    rfq_response = api_client.get_rfq(instrument_name, side, quantity)
    if not rfq_response:
        return

    rfq_response.display()

    # Ask for execution permission
    execute_order = prompt_yes_no("Do you want to execute an order with these details?")
    if execute_order:
        order_type = prompt_list("Order Type:", ["FOK", "MKT"])
        executing_unit = prompt_string("Executing Unit:")
        order_response = api_client.create_order_from_rfq(
            rfq_response, order_type, executing_unit=executing_unit or ""
        )
        display_balance()


def create_order():
    api_client.list_instruments()


def display_balance():
    if not check_api_connection():
        return
    balance = api_client.get_balance()
    balance.display()


def display_order_history():
    if not check_api_connection():
        return
    orders = api_client.get_order_history()
    if not orders:
        print_red("No orders yet.")
        return

    # TODO: Add precisions and justify=right
    columns = [
        "created",
        "order_id",
        "client_order_id",
        "quantity",
        "side",
        "instrument",
        "price",
        "executed_price",
        "executing_unit",
    ]
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    for column in columns:
        table.add_column(column)
    for order in orders:
        data = [str(order.__dict__.get(col)) for col in columns]
        table.add_row(*data)
    console.print(table)


def display_trade_history():
    if not check_api_connection():
        return


def display_order_details():
    if not check_api_connection():
        return
    order_id = prompt_string("Enter order_id / client_order_id:")
    order = api_client.get_order_detail(order_id)
    order.display()


def display_trade_details():
    if not check_api_connection():
        return
    # TODO: add


def check_api_connection():
    return api_client.check_connection()


action_map = {
    "List Instruments": list_instruments,
    "Request for Quote (RFQRequest)": request_for_quote,
    "Create Order": create_order,
    "Display Balance": display_balance,
    "Display Order History": display_order_history,
    "Display Trade History": display_trade_history,
    "Display Order Details": display_order_details,
    "Display Trade Details": display_trade_details,
    "Check connection": check_api_connection,
    "Quit": quit,
}
