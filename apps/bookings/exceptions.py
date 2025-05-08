from rest_framework.exceptions import APIException


class BookingException(APIException):
    status_code = 400
    default_detail = 'Booking error occurred.'
    default_code = 'booking_error'

    def __init__(self, detail=None, code=None):
        if detail is not None:
            self.detail = detail
        if code is not None:
            self.status_code = code
