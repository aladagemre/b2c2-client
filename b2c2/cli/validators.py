# -*- coding: utf-8 -*-
import decimal
import logging

from prompt_toolkit.validation import ValidationError, Validator


class DecimalValidator(Validator):
    def validate(self, document):
        try:
            decimal.Decimal(document.text)
        except (decimal.ConversionSyntax, decimal.InvalidOperation) as exc:
            raise ValidationError(
                message="Please enter a decimal number",
                cursor_position=len(document.text),
            )


class IntegerValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError as exc:
            raise ValidationError(
                message="Please enter a valid integer",
                cursor_position=len(document.text),
            )


class RangeValidator(Validator):
    """
    Abstract Validator for numeric ranges.
    """

    def __init__(self, type, type_validator, lower_bound, upper_bound):
        self.type = type
        self.type_validator = type_validator
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def validate(self, document):
        self.type_validator.validate(document)
        value = self.type(document.text)
        if not (self.lower_bound <= value <= self.upper_bound):
            raise ValidationError(
                message=f"Value should be between {self.lower_bound} and {self.upper_bound}.",
                cursor_position=len(document.text),
            )


class DecimalRangeValidator(RangeValidator):
    def __init__(self, lower_bound, upper_bound):
        super().__init__(decimal.Decimal, DecimalValidator, lower_bound, upper_bound)


class IntegerRangeValidator(RangeValidator):
    def __init__(self, lower_bound, upper_bound):
        super().__init__(int, IntegerValidator, lower_bound, upper_bound)
