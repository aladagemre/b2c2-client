# -*- coding: utf-8 -*-
from decimal import Decimal

from PyInquirer import prompt
from rich import print

from b2c2.cli.validators import DecimalValidator


def print_color(text, color):
    print(f"[bold {color}]{text}[/bold {color}]")


def print_red(text):
    print_color(text, "red")


def print_green(text):
    print_color(text, "green")


def prompt_string(message):
    questions = [{"type": "input", "name": "string", "message": message}]
    answers = prompt(questions)
    return answers and answers.get("string")


def prompt_list(message, choices):
    questions = [
        {
            "type": "list",
            "name": "choice",
            "message": message,
            "choices": choices,
        }
    ]
    answers = prompt(questions)
    return answers and answers.get("choice")


def prompt_decimal(message):
    questions = [
        {
            "type": "input",
            "name": "value",
            "message": message,
            "validate": DecimalValidator,
        },
    ]
    answers = prompt(questions)
    return answers and Decimal(answers.get("value"))


def prompt_yes_no(message):
    questions = [
        {
            "type": "confirm",
            "name": "choice",
            "message": message,
            "default": False,
        }
    ]
    answers = prompt(questions)
    return answers and answers.get("choice")
