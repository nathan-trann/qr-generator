
from pyzbar.pyzbar import decode
from qr_tool.core.models import DecodedPayloadEnum
from qr_tool.core.exceptions import QRDecodeError
from qr_tool.core.models import DecodedPayload
import io
import string
from PIL import Image

class PyZbarDecoderAdapter:
    def decode_qr(self, image_data: bytes) -> DecodedPayload:
        # Convert raw files bytes into a Pixel Matrix
        buffer = io.BytesIO(image_data)
        
        try:
            img = Image.open(buffer)
        except Exception as e:
            raise QRDecodeError("The provided image is not valid.") from e
        
        decoded_objects = decode(img)
        if not decoded_objects:
            raise QRDecodeError("No QR code found in the image.")
        
        raw_bytes = decoded_objects[0].data
        
        try:
            text = raw_bytes.decode('utf-8')
            printable_chars = set(string.printable)
            
            # If the decoded string contains NULL bytes, it almost certainty isn't standard text.
            if '\x00' in text:
                text = None
                payload_type = DecodedPayloadEnum.BINARY
            else:
                # Count characters that are not standard printable text
                none_printable = sum(1 for c in text if c not in printable_chars)
                # If more than 5% of characters are weird unicode/control characters, 
                # assume it's actually a binary file that happened to luckily decode.
                if len(text) > 0 and (none_printable / len(text)) > 0.05:
                    text = None
                    payload_type = DecodedPayloadEnum.BINARY
                else:
                    payload_type = DecodedPayloadEnum.TEXT
            
        except UnicodeDecodeError:
            text = None
            payload_type = DecodedPayloadEnum.BINARY
            
        return DecodedPayload(raw_bytes=raw_bytes, text=text, type=payload_type)