# -*- coding: utf-8 -*-
from decimal import Decimal
from typing import Optional, Tuple

from PyInquirer import prompt
from rich import print

from b2c2.cli.validators import (
    DecimalRangeValidator,
    DecimalValidator,
    IntegerRangeValidator,
    IntegerValidator,
)


def print_color(text, color):
    print(f"[bold {color}]{text}[/bold {color}]")


def print_red(text):
    print_color(text, "red")


def print_green(text):
    print_color(text, "green")


def prompt_string(message, default=""):
    questions = [
        {"type": "input", "name": "string", "message": message, "default": default}
    ]
    answers = prompt(questions)
    return answers and answers.get("string")


def prompt_integer(
    message, default: Optional[int] = None, boundaries: Optional[Tuple[int, int]] = None
) -> Optional[int]:
    default = str(default) if isinstance(default, int) else ""
    validator = IntegerRangeValidator(*boundaries) if boundaries else IntegerValidator

    questions = [
        {
            "type": "input",
            "name": "value",
            "message": message,
            "validate": validator,
            "default": default,
        },
    ]
    answers = prompt(questions)
    return answers and int(answers.get("value"))


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


def prompt_decimal(
    message: str,
    default: Optional[Decimal] = None,
    boundaries: Optional[Tuple[Decimal, Decimal]] = None,
) -> Optional[Decimal]:
    default = str(default) if isinstance(default, Decimal) else ""
    validator = DecimalRangeValidator(*boundaries) if boundaries else DecimalValidator
    questions = [
        {
            "type": "input",
            "name": "value",
            "message": message,
            "validate": validator,
            "default": default,
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
