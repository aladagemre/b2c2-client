# -*- coding: utf-8 -*-
import logging

from PyInquirer import prompt
from rich import print

from b2c2.cli.actions import action_map
from b2c2.cli.questions import action_question
from b2c2.settings import TOKEN

logger = logging.getLogger(__name__)

token = TOKEN


def menu():
    print("\n[yellow]" + "=" * 50 + "[/yellow]\n")
    action = prompt(action_question)["action"]
    action_map[action]()


if __name__ == "__main__":
    while True:
        menu()
    # TODO: make click cli interface as well re-using the functions
