from qr_tool.core.exceptions import QRDecodeError
from qr_tool.core.models import DecodedPayload
from typing import Protocol
from .models import QRCodeImage
from .exceptions import PayloadTooLargeError

class QREncoderAdapter(Protocol):
    """The contract that any infrastructure encoder must fulfill."""
    def encode_qr(self, payload: str | bytes, format: str) -> QRCodeImage:
        ...

def generate_qr_code(payload: str | bytes, format: str, encoder: QREncoderAdapter) -> QRCodeImage:
    """
    The Core Domain orchestration function.
    Notice how it doesn't import segno! It just relies on the Protocol.
    """
    try:
        return encoder.encode_qr(payload, format)
    except ValueError as e:
        if "too large" in str(e).lower():
            raise PayloadTooLargeError("The provided payload exceeds QR capacity.") from e
        raise

class QRDecoderAdapter(Protocol):
    """The contract that any infrastructure decoder must fulfill."""
    def decode_qr(self, image_data: bytes) -> DecodedPayload:
        ...
        
def decode_qr_code(image_data: bytes, decoder: QRDecoderAdapter) -> DecodedPayload:
    """
    The Core Domain orchestration function.
    Notice how it doesn't import pyzbar! It just relies on the Protocol.
    """
    try:
        return decoder.decode_qr(image_data)
    except Exception as e:
        raise QRDecodeError("Failed to find or parse the QR code.") from e