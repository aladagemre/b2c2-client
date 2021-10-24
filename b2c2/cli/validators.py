# -*- coding: utf-8 -*-
import decimal

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
