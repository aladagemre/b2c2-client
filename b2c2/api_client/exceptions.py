# -*- coding: utf-8 -*-


class HTTPException(Exception):
    message = None

    def __init__(self, *args, **kwargs):
        super(HTTPException, self).__init__(*args, **kwargs)
        exc = kwargs.get("exc")
        if exc and not self.message:
            self.message = exc.args[0]


class BadRequest(HTTPException):
    message = "Bad Request - Incorrect parameters"
    code = 400


class Unauthorized(HTTPException):
    message = "Unauthorized - Wrong Token"
    code = 401


class Forbidden(HTTPException):
    message = "Forbidden - Make sure your IP is whitelisted."
    code = 403


class NotFound(HTTPException):
    message = "Not Found - The specified endpoint could not be found."
    code = 404


class MethodNotAllowed(HTTPException):
    message = (
        "Method Not Allowed – You tried to access an endpoint with an invalid method."
    )
    code = 405


class NotAcceptable(HTTPException):
    message = "Not Acceptable – Incorrect request format."
    code = 406


class UnprocessableEntity(HTTPException):
    message = "Make sure your request data ise matches the entity."
    code = 422


class TooManyRequests(HTTPException):
    message = "Too Many Requests – Rate limited, pause requests."
    code = 429


class InternalServerError(HTTPException):
    message = (
        "Internal Server Error – We had a problem with our server. Try again later."
    )
    code = 500


class ServiceUnavailable(HTTPException):
    message = "Service unavailable"
    code = 503


http_code_map = {
    400: BadRequest,
    401: Unauthorized,
    403: Forbidden,
    404: NotFound,
    405: MethodNotAllowed,
    406: NotAcceptable,
    422: UnprocessableEntity,
    429: TooManyRequests,
    500: InternalServerError,
    503: ServiceUnavailable,
}


def get_http_exception_by_code(code: int):
    """
    Returns the HTTP exception relevant to the code.
    :param code: integer code between 400 and 503.
    :return: HTTPException subclasses if match.
    Otherwise generic HTTPException
    """
    return http_code_map.get(code, HTTPException)


# ==== API Exceptions =====


class APIException(Exception):
    pass


class QuoteNotValidException(APIException):
    message = "Quote is not valid – Quote may have expired."
    code = 1007


class OrderRejectedException(APIException):
    pass


class PriceNotValid(APIException):
    message = "Price not valid – The price is not valid anymore. This error can occur during big market moves."
    code = 1009


class NotEnoughBalance(APIException):
    message = "Not enough balance – Not enough balance."
    code = 1011
