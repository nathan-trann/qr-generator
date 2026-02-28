from typing import Union
from typing import Optional
from dataclasses import dataclass
from enum import Enum

class OutputFormat(Enum):
    PNG = "png"
    TXT = "txt"

class DecodedPayloadEnum(Enum):
    TEXT = "text"
    URL = "url"
    BINARY = "binary"

@dataclass
class QRCodeImage:
    data: bytes
    format: str # e.g., "png", "svg", "eps"
    

@dataclass
class DecodedPayload:
    """
    The Domain representation of what was inside the QR code.
    """
    raw_bytes: bytes
    text: Optional[str] = None # Populated ONLY if the bytes are valid UTF-8
    type: DecodedPayloadEnum = DecodedPayloadEnum.TEXT # e.g., "text", "url", "binary"