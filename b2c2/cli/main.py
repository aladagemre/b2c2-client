# -*- coding: utf-8 -*-
import logging
import os

from PyInquirer import prompt
from rich import print

from b2c2.cli.interface import CommandLineInterface
from b2c2.cli.questions import action_question
from b2c2.cli.tokens import ConfigManager

logger = logging.getLogger(__name__)


def menu():
    config = ConfigManager()
    cmd = CommandLineInterface(config=config)
    print("\n[yellow]" + "=" * 50 + "[/yellow]\n")
    action = prompt(action_question)["action"]
    cmd.execute_command(action)


def create_log_folder():
    if not os.path.exists("logs"):
        os.mkdir("logs")


def main():
    while True:
        menu()


if __name__ == "__main__":
    main()
    # TODO: make click cli interface as well re-using the functions
