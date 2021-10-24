# -*- coding: utf-8 -*-
import logging
import os

from PyInquirer import prompt
from rich import print

from b2c2.cli.actions import action_map
from b2c2.cli.questions import action_question

logger = logging.getLogger(__name__)


def menu():
    print("\n[yellow]" + "=" * 50 + "[/yellow]\n")
    action = prompt(action_question)["action"]
    action_map[action]()


def create_log_folder():
    if not os.path.exists("logs"):
        os.mkdir("logs")


def main():
    while True:
        menu()


if __name__ == "__main__":
    main()
    # TODO: make click cli interface as well re-using the functions
