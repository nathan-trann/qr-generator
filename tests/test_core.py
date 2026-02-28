from qr_tool.core.engine import decode_qr_code
from qr_tool.core.exceptions import QRDecodeError
from qr_tool.core.models import OutputFormat
from qr_tool.core.engine import generate_qr_code
from qr_tool.core.exceptions import PayloadTooLargeError
import pytest

class FakeEncoderAdapter:
    def encode_qr(self, payload: str | bytes, format: str):
        raise ValueError("Data is too large for the requested QR version")
    
def test_encoder_engine_with_payload_too_large_error():
    fake_adapter = FakeEncoderAdapter()
    payload = "A super long string that will definitely be too large for the QR code version that the encoder will try to use."
    with pytest.raises(PayloadTooLargeError, match="exceeds QR capacity"):
        generate_qr_code(payload, OutputFormat.PNG.value, encoder=fake_adapter)
        

class FakeDecoderAdapter:
    def decode_qr(self, image_data: bytes):
        raise ValueError("Corrupt Image Data")
    
def test_decoder_engine_with_qr_decode_error():
    fake_adapter = FakeDecoderAdapter()
    image_data = b"Invalid QR code data"
    with pytest.raises(QRDecodeError, match="Failed to find or parse the QR code."):
        decode_qr_code(image_data, decoder=fake_adapter)