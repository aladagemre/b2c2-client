# -*- coding: utf-8 -*-
import logging

from PyInquirer import prompt
from rich.console import Console
from rich.table import Table

import b2c2.cli.questions as q
from b2c2.api_client.api import B2C2Client
from b2c2.cli.tokens import ConfigManager
from b2c2.cli.utils import (
    print_green,
    print_red,
    prompt_decimal,
    prompt_list,
    prompt_string,
    prompt_yes_no,
)


class CommandLineInterface:
    def __init__(self, config: ConfigManager):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.token = self.config.get_token()
        self.api_url = self.config.get_api_url()

        if not self.token:
            # If no token provided, ask for one.
            self.token_settings()

        self.action_map = {
            "List Instruments": self.list_instruments,
            "Request for Quote (RFQRequest)": self.request_for_quote,
            "Create Order": self.create_order,
            "Display Balance": self.display_balance,
            "Display Order History": self.display_order_history,
            "Display Trade History": self.display_trade_history,
            "Display Order Details": self.display_order_details,
            "Display Trade Details": self.display_trade_details,
            "Token Settings": self.token_settings,
            "Check connection": self.check_api_connection,
            "Quit": quit,
        }
        self.api_client = B2C2Client(token=self.token, api_url=self.api_url)

    def execute_command(self, action):
        self.action_map[action]()

    def list_instruments(self):
        if not self.check_api_connection():
            return
        instruments = self.api_client.list_instruments()
        if not instruments:
            self.logger.error(
                "Could not connect to the server. Please try again later."
            )
            return
        question = q.get_list_instruments_question(
            [instrument.name for instrument in instruments]
        )
        answer = prompt(question).get("instrument_action")
        if answer == "No Thanks":
            return
        self.request_for_quote(instrument_name=answer)

    def request_for_quote(self, instrument_name=None):
        if not self.check_api_connection():
            return
        if not instrument_name:
            instrument_name = prompt_string("Instrument:")
        side = prompt_list("Side:", ["buy", "sell"])
        quantity = prompt_decimal("Quantity")

        # Make RFQ Request
        rfq_response = self.api_client.get_rfq(instrument_name, side, quantity)
        if not rfq_response:
            print_red(
                "Could not get response from the server. Please check your connection."
            )
            return

        rfq_response.display()

        # Ask for execution permission
        execute_order = prompt_yes_no(
            "Do you want to execute an order with these details?"
        )
        if execute_order:
            order_type = prompt_list("Order Type:", ["FOK", "MKT"])
            executing_unit = prompt_string("Executing Unit:")
            order_response = self.api_client.create_order_from_rfq(
                rfq_response, order_type, executing_unit=executing_unit or ""
            )
            if order_response.is_rejected:
                print_red("\nYour order was rejected.\n")
            else:
                print_green(f"\nYour order was successfully placed.\n")

            order_response.display()
            self.display_balance()

    def create_order(self):
        self.api_client.list_instruments()

    def display_balance(self):
        if not self.check_api_connection():
            return
        balance = self.api_client.get_balance()
        balance.display()

    def display_order_history(self):
        if not self.check_api_connection():
            return
        orders = self.api_client.get_order_history()
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

    def display_trade_history(self):
        if not self.check_api_connection():
            return

    def display_order_details(self):
        if not self.check_api_connection():
            return
        order_id = prompt_string("Enter order_id / client_order_id:")
        order = self.api_client.get_order_detail(order_id)
        order.display()

    def display_trade_details(self):
        if not self.check_api_connection():
            return
        # TODO: add

    def _save_token(self, token):
        self.config.set_token(token)
        self.config.save_config()
        self.logger.info("Your token has been saved.")

    def token_settings(self):
        while not self.token:
            token = prompt_string("Please provide your token:")
            print(token)
            if token:
                self.token = token
                self._save_token(token)
            elif token == dict():
                quit()

    def check_api_connection(self):
        return self.api_client.check_connection()
