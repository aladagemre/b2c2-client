# -*- coding: utf-8 -*-


class APIError(Exception):
    pass


class Generic(APIError):
    message = "Generic –- Unknown error."
    code = 1000


class InstrumentNotAllowed(APIError):
    message = "Instrument not allowed – Instrument does not exist or you are not authorized to trade it."
    code = 1001


class TheRfqDoesNotBelongToYou(APIError):
    message = "The RFQ does not belong to you."
    code = 1002


class DifferentInstrument(APIError):
    message = "Different instrument – You tried to post a trade with a different instrument than the related RFQ."
    code = 1003


class DifferentSide(APIError):
    message = "Different side – You tried to post a trade with a different side than the related RFQ."
    code = 1004


class DifferentPrice(APIError):
    message = "Different price – You tried to post a trade with a different price than the related RFQ."
    code = 1005


class DifferentQuantity(APIError):
    message = "Different quantity – You tried to post a trade with a different quantity than the related RFQ."
    code = 1006


class QuoteIsNotValid(APIError):
    message = "Quote is not valid – Quote may have expired."
    code = 1007


class PriceNotValid(APIError):
    message = "Price not valid – The price is not valid anymore. This error can occur during big market moves."
    code = 1009


class QuantityTooBig(APIError):
    message = "Quantity too big – Max quantity per trade reached."
    code = 1010


class NotEnoughBalance(APIError):
    message = "Not enough balance – Not enough balance."
    code = 1011


class MaxRiskExposureReached(APIError):
    message = "Max risk exposure reached – Please see our FAQ for more information about the risk exposure."
    code = 1012


class MaxCreditExposureReached(APIError):
    message = "Max credit exposure reached – Please see our FAQ for more information about the credit exposure."
    code = 1013


class NoBtcAddressAssociated(APIError):
    message = "No BTC address associated – You don’t have a BTC address associated to your account."
    code = 1014


class TooManyDecimals(APIError):
    message = "Too many decimals – We only allow four decimals in quantities."
    code = 1015


class TradingIsDisabled(APIError):
    message = "Trading is disabled – May occur after a maintenance or under exceptional circumstances."
    code = 1016


class IllegalParameter(APIError):
    message = "Illegal parameter – Wrong type or parameter."
    code = 1017


class SettlementIsDisabledAtTheMoment(APIError):
    message = "Settlement is disabled at the moment."
    code = 1018


class QuantityIsTooSmall(APIError):
    message = "Quantity is too small."
    code = 1019


class TheFieldValid_UntilIsMalformed(APIError):
    message = "The field valid_until is malformed."
    code = 1020


class YourOrderHasExpired(APIError):
    message = "Your Order has expired."
    code = 1021


class CurrencyNotAllowed(APIError):
    message = "Currency not allowed."
    code = 1022


class WeOnlySupportFokOrderTypeAtTheMoment(APIError):
    message = "We only support “FOK” order_type at the moment."
    code = 1023


class FieldRequired(APIError):
    message = "Field required – Field required."
    code = 1101


class PaginationOffsetTooBig(APIError):
    message = "Pagination offset too big – Narrow down the data space using parameters such as ‘created*gte’, ‘created*lt’, ‘since’."
    code = 1102


class ApiMaintenance(APIError):
    message = "API Maintenance"
    code = 1200


class ThisContractIsAlreadyClosed(APIError):
    message = "This contract is already closed."
    code = 1500


class TheGivenQuantityMustBeSmallerOrEqualToTheContractQuantity(APIError):
    message = "The given quantity must be smaller or equal to the contract quantity."
    code = 1501


class YouDontHaveEnoughMargin(APIError):
    message = "You don’t have enough margin. Please add funds to your account or close some positions."
    code = 1502


class ContractUpdatesAreOnlyForClosingAContract(APIError):
    message = "Contract updates are only for closing a contract."
    code = 1503


class OtherError(APIError):
    message = "Other error."
    code = 1100


api_error_code_map = {
    1000: Generic,
    1001: InstrumentNotAllowed,
    1002: TheRfqDoesNotBelongToYou,
    1003: DifferentInstrument,
    1004: DifferentSide,
    1005: DifferentPrice,
    1006: DifferentQuantity,
    1007: QuoteIsNotValid,
    1009: PriceNotValid,
    1010: QuantityTooBig,
    1011: NotEnoughBalance,
    1012: MaxRiskExposureReached,
    1013: MaxCreditExposureReached,
    1014: NoBtcAddressAssociated,
    1015: TooManyDecimals,
    1016: TradingIsDisabled,
    1017: IllegalParameter,
    1018: SettlementIsDisabledAtTheMoment,
    1019: QuantityIsTooSmall,
    1020: TheFieldValid_UntilIsMalformed,
    1021: YourOrderHasExpired,
    1022: CurrencyNotAllowed,
    1023: WeOnlySupportFokOrderTypeAtTheMoment,
    1101: FieldRequired,
    1102: PaginationOffsetTooBig,
    1200: ApiMaintenance,
    1500: ThisContractIsAlreadyClosed,
    1501: TheGivenQuantityMustBeSmallerOrEqualToTheContractQuantity,
    1502: YouDontHaveEnoughMargin,
    1503: ContractUpdatesAreOnlyForClosingAContract,
    1100: OtherError,
}


def get_api_error_by_code(code: int):
    """
    Returns the API error relevant to the code.
    :param code: integer code between 1000 and 1503
    :return: APIError subclasses if match.
    Otherwise generic HTTPException
    """
    return api_error_code_map.get(code, Generic)
