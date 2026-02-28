class QRToolError(Exception):
    """
    Base Exception for all domain errors.
    """
    pass

class PayloadTooLargeError(QRToolError):
    """
    Exception raised when the payload is too large.
    """
    pass

class QRDecodeError(QRToolError):
    """
    Exception raised when the QR code cannot be decoded.
    """
    pass